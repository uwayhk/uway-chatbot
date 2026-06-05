import streamlit as st
from openai import OpenAI
import os
import json
from datetime import datetime
from pathlib import Path

# ============================================================================
# UWAY Compliance Assistant - Chatbot with Multi-Provider Failover
# ============================================================================
# Primary:    NVIDIA NIM (Free Tier)
# Fallbacks:  Gemini 2.5, DeepSeek via OpenRouter
# Knowledge:  Sumsub KYC Best Practices + Uway Company Profile
# ============================================================================

st.set_page_config(
    page_title="UWAY Compliance Assistant",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for branding
st.markdown("""
<style>
    .main-header { font-size: 28px; font-weight: bold; color: #1a2332; margin-bottom: 10px; }
    .sub-header { font-size: 14px; color: #64748b; margin-bottom: 30px; }
    .stChatMessage { border-radius: 8px; }
    .stChatInput { border-radius: 8px; }
    .knowledge-badge { background-color: #00d4ff; color: #1a2332; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛡️ UWAY Financial Compliance Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask about AML/KYC compliance, HKMA/SFC regulations, and cross-border payment rules</div>', unsafe_allow_html=True)

# ============================================================================
# Knowledge Base Loader (Multi-Source with Citations)
# ============================================================================
KNOWLEDGE_DIR = "/app/knowledge_base"

def load_knowledge_base():
    """Load all markdown files from knowledge base directory recursively"""
    knowledge = {}
    doc_sources = {}
    try:
        kb_path = Path(KNOWLEDGE_DIR)
        if kb_path.exists():
            # Recursively find all .md and .mdx files
            for md_file in kb_path.rglob("*.md"):
                if "index.json" in str(md_file):
                    continue
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Create title from file path
                    rel_path = md_file.relative_to(kb_path)
                    title = f"{rel_path.parent}/{md_file.stem}".replace("/", " > ").replace("_", " ").title()
                    knowledge[title] = content
                    # Store source path for citations
                    doc_sources[title] = str(rel_path)
            # Also load .mdx files
            for mdx_file in kb_path.rglob("*.mdx"):
                with open(mdx_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    rel_path = mdx_file.relative_to(kb_path)
                    title = f"{rel_path.parent}/{mdx_file.stem}".replace("/", " > ").replace("_", " ").title()
                    knowledge[title] = content
                    doc_sources[title] = str(rel_path)
    except Exception as e:
        st.warning(f"Failed to load knowledge base: {e}")
    return knowledge, doc_sources

def format_knowledge_for_prompt(knowledge: dict, doc_sources: dict) -> str:
    """Format knowledge base content for system prompt with source tracking"""
    if not knowledge:
        return ""
    
    formatted = "\n\n=== KNOWLEDGE BASE ===\n"
    formatted += "You have access to the following proprietary knowledge base. Use this information to answer accurately.\n"
    formatted += "IMPORTANT: When citing information, mention the source document name.\n\n"
    
    for title, content in knowledge.items():
        source = doc_sources.get(title, "Unknown")
        formatted += f"--- DOCUMENT: {title} (Source: {source}) ---\n"
        formatted += f"{content}\n\n"
    
    formatted += "=== END KNOWLEDGE BASE ===\n"
    formatted += "When answering questions:\n"
    formatted += "1. If the question relates to information in the knowledge base, use that information as your primary source\n"
    formatted += "2. Cite your sources by mentioning the document name (e.g., 'According to [Document Name]...')\n"
    formatted += "3. For Uway docs, reference: docs.hkuway.com/docs/[path]\n"
    formatted += "4. For Sumsub docs, reference: docs.sumsub.com/[path]\n"
    formatted += "5. Always be transparent and accurate - if information is not in your knowledge base, acknowledge this\n"
    
    return formatted

# Load knowledge base at startup
knowledge_base, doc_sources = load_knowledge_base()

# ============================================================================
# Session History File Storage
# ============================================================================
HISTORY_FILE = "/tmp/uway_chat_history.json"

def load_chat_history():
    """Load chat history from file"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Failed to load history: {e}")
    return []

def save_chat_history(messages):
    """Save chat history to file"""
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.warning(f"Failed to save history: {e}")

def clear_chat_history():
    """Clear chat history file"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
    except Exception as e:
        st.warning(f"Failed to clear history: {e}")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

if "provider_used" not in st.session_state:
    st.session_state.provider_used = None

if "api_errors" not in st.session_state:
    st.session_state.api_errors = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "provider" in msg:
            st.caption(f"Model: {msg['provider']}")

# ============================================================================
# Provider Manager Classes
# ============================================================================

class NVIDIAProvider:
    """Primary: NVIDIA NIM Free Tier"""
    def __init__(self):
        self.api_key = os.environ.get("NVIDIA_API_KEY")
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = "minimaxai/minimax-m2.7"
    
    def chat(self, messages: list, system_prompt: str, stream: bool = True):
        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        full_messages = [{"role": "system", "content": system_prompt}]
        full_messages.extend(messages)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=0.7,
            top_p=0.95,
            max_tokens=8192,
            stream=stream
        )
        
        if stream:
            for chunk in response:
                if not getattr(chunk, "choices", None):
                    continue
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        else:
            yield response.choices[0].message.content


class GeminiProvider:
    """Fallback: Google Gemini 2.5 (requires ADC or API key)"""
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model = "gemini-2.5-pro"
    
    def chat(self, messages: list, system_prompt: str, stream: bool = True):
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        
        model = genai.GenerativeModel(self.model)
        full_messages = system_prompt + "\n\n" + "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        response = model.generate_content(full_messages, stream=stream)
        
        if stream:
            for chunk in response:
                yield chunk.text
        else:
            yield response.text


class NVIDIA_Backup:
    """Fallback: NVIDIA NIM with Llama 3.3 70B"""
    def __init__(self):
        self.api_key = os.environ.get("NVIDIA_API_KEY")
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.model = "meta/llama-3.3-70b-instruct"
    
    def chat(self, messages: list, system_prompt: str, stream: bool = True):
        client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        
        full_messages = [{"role": "system", "content": system_prompt}]
        full_messages.extend(messages)
        
        response = client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=0.7,
            top_p=0.95,
            max_tokens=8192,
            stream=stream
        )
        
        if stream:
            for chunk in response:
                if not getattr(chunk, "choices", None):
                    continue
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        else:
            yield response.choices[0].message.content


class ProviderRouter:
    """Route to available provider with automatic failover"""
    def __init__(self):
        self.providers = {
            "nvidia": NVIDIAProvider(),
            "nvidia-backup": NVIDIA_Backup(),
            "gemini": GeminiProvider()
        }
    
    def chat(self, messages: list, system_prompt: str, stream: bool = True):
        error_log = []
        
        # Try providers in order of priority
        for provider_name, provider in self.providers.items():
            try:
                yield from provider.chat(messages, system_prompt, stream)
                return  # Success, exit function
            except Exception as e:
                error_log.append(f"{provider_name}: {str(e)}")
                st.warning(f"⚠️ {provider_name} failed: {str(e)[:100]}... Trying next provider...")
        
        # All providers failed
        raise RuntimeError(f"All providers unavailable. Errors: {'; '.join(error_log)}")


def get_system_prompt():
    """Financial compliance assistant system prompt with knowledge base"""
    base_prompt = """You are a professional financial compliance assistant specializing in Hong Kong and Singapore regulatory frameworks.

Your expertise includes:
- Anti-Money Laundering (AML) & Know Your Customer (KYC) requirements
- Hong Kong Monetary Authority (HKMA) guidelines
- Securities and Futures Commission (SFC) regulations  
- Financial Action Task Force (FATF) recommendations
- Cross-border payment compliance (SWIFT, correspondent banking)
- Sumsub KYC/AML best practices
- Uway Innovation Limited company information

When answering compliance questions:
1. Reference specific regulatory bodies and guidelines when applicable
2. Highlight key compliance obligations and reporting requirements
3. Note any jurisdiction-specific considerations (HK vs SG vs international)
4. Be precise and actionable, avoiding vague statements
5. If uncertain about a regulation, acknowledge limitations and suggest verification

When asked about Uway Innovation Limited:
- Be transparent that this is the company operating this chatbot
- Provide verifiable facts (incorporation date: May 30, 2025, jurisdiction: Hong Kong)
- Direct users to official sources (Hong Kong Companies Registry) for verification
- Emphasize compliance commitment
- Do NOT make unverifiable claims about financial status

When asked about KYC best practices:
- Reference Sumsub framework and industry standards
- Cover CIP, risk-based approach, documentation requirements
- Mention jurisdiction-specific requirements (HKMA, MAS, etc.)
- Include technology integration recommendations

CITATION REQUIREMENT:
- When using information from the knowledge base, cite the source document
- For Uway docs: mention "According to [doc name] at docs.hkuway.com"
- For Sumsub docs: mention "According to Sumsub documentation at docs.sumsub.com"
- Include relevant URLs when possible

IMPORTANT: This is for informational purposes only. Always recommend consulting licensed compliance professionals for critical business decisions."""

    # Append knowledge base content
    kb_content = format_knowledge_for_prompt(knowledge_base, doc_sources)
    return base_prompt + kb_content


# ============================================================================
# Sidebar Configuration
# ============================================================================
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Knowledge base status with detailed breakdown
    if knowledge_base:
        st.success(f"✅ Knowledge Base Loaded ({len(knowledge_base)} documents)")
        
        # Count docs by category
        uway_count = sum(1 for k in knowledge_base.keys() if "uway-docs" in str(doc_sources.get(k, "")))
        sumsub_count = sum(1 for k in knowledge_base.keys() if "sumsub/" in str(doc_sources.get(k, "")))
        root_count = len(knowledge_base) - uway_count - sumsub_count
        
        with st.expander("📚 View Knowledge Base"):
            if root_count > 0:
                st.markdown(f"**📁 Root** ({root_count} docs)")
                for title in knowledge_base.keys():
                    if doc_sources.get(title, "").count("/") <= 1 and "sumsub/" not in doc_sources.get(title, "") and "uway-docs" not in doc_sources.get(title, ""):
                        st.markdown(f"  - {title}")
            if sumsub_count > 0:
                st.markdown(f"**🤖 Sumsub** ({sumsub_count} docs)")
                for title in knowledge_base.keys():
                    if "sumsub/" in str(doc_sources.get(title, "")):
                        st.markdown(f"  - {title}")
            if uway_count > 0:
                st.markdown(f"**🏢 Uway Docs** ({uway_count} docs)")
                for title in knowledge_base.keys():
                    if "uway-docs" in str(doc_sources.get(title, "")):
                        st.markdown(f"  - {title}")
    else:
        st.warning("⚠️ Knowledge Base Not Found")
    
    st.divider()
    
    system_prompt = st.text_area(
        "System Prompt",
        value=get_system_prompt(),
        height=300,
        help="Customize the AI assistant's behavior"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values = more creative responses"
    )
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=256,
        max_value=8192,
        value=4096,
        step=256
    )
    
    st.divider()
    st.caption("Provider Priority:")
    st.markdown("1️⃣ NVIDIA NIM (Primary)")
    st.markdown("2️⃣ NVIDIA NIM Llama 70B (Backup)")
    st.markdown("3️⃣ Gemini 2.5 (Requires API key)")
    
    st.divider()
    
    # Show history file info
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
            st.caption(f"💾 History saved: {len(history)} messages")
        except:
            st.caption("💾 History saved")
    else:
        st.caption("💾 No history yet")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.provider_used = None
        clear_chat_history()
        st.rerun()
    
    st.divider()
    st.info(f"💡 Powered by NVIDIA NIM\n\n📚 Knowledge: {len(knowledge_base)} docs (Uway + Sumsub)")


# ============================================================================
# Chat Input & Processing
# ============================================================================
if prompt := st.chat_input("Ask about AML/KYC compliance..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate assistant response with failover
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        router = ProviderRouter()
        provider_chosen = None
        
        try:
            # Track which provider succeeded
            for i, chunk in enumerate(router.chat(st.session_state.messages, system_prompt)):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                
                # Guess provider on first successful chunk
                if i == 0 and provider_chosen is None:
                    provider_chosen = "nvidia"
            
            message_placeholder.markdown(full_response)
            
            # Add to history with provider info
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response,
                "provider": provider_chosen or "nvidia"
            })
            
            # Save to file
            save_chat_history(st.session_state.messages)
            
        except Exception as e:
            st.error(f"❌ All providers failed: {str(e)}")
            full_response = "I'm currently unable to respond due to API issues. Please try again later."
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": full_response
            })
            
            # Save to file
            save_chat_history(st.session_state.messages)

# Footer
st.divider()
st.caption(f"© 2026 UWAY Innovation Limited | For informational purposes only | Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
