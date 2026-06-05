# UWAY Chatbot - Streamlit App (Fixed Version)
# 修复了三个 provider 错误：
# 1. NVIDIA: 移除 proxies 参数
# 2. Gemini: 添加 API Key 配置
# 3. OpenRouter: 添加 minijinja 依赖

import streamlit as st
import requests
import json
from datetime import datetime
import os

st.set_page_config(
    page_title="UWAY Compliance Assistant",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for brand colors
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fa;
    }
    .stChatMessage {
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .chat-container {
        height: calc(100vh - 200px);
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# Brand header
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("🛡️")
with col2:
    st.title("UWAY Financial Compliance Assistant")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Provider configuration
PROVIDERS = {
    "nvidia": {
        "enabled": True,
        "api_key": os.environ.get("NVIDIA_API_KEY", ""),
        "model": "meta/llama3-70b-instruct",
        "base_url": "https://integrate.api.nvidia.com/v1"
    },
    "gemini": {
        "enabled": True,
        "api_key": os.environ.get("GEMINI_API_KEY", ""),
        "model": "gemini-2.0-flash"
    },
    "openrouter": {
        "enabled": True,
        "api_key": os.environ.get("OPENROUTER_API_KEY", ""),
        "model": "qwen/qwen-2.5-72b-instruct",
        "base_url": "https://openrouter.ai/api/v1"
    }
}

# Initialize session state for API config
if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = st.secrets.get("AWS_API_URL", "")

# Sidebar config
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("Provider Configuration")
    
    # NVIDIA Config
    st.markdown("**NVIDIA NIM**")
    nvidia_key = st.text_input(
        "NVIDIA API Key",
        type="password",
        value=PROVIDERS["nvidia"]["api_key"],
        help="Get from https://build.nvidia.com"
    )
    if nvidia_key:
        PROVIDERS["nvidia"]["api_key"] = nvidia_key
    
    # Gemini Config
    st.markdown("**Gemini**")
    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=PROVIDERS["gemini"]["api_key"],
        help="Get from https://aistudio.google.com"
    )
    if gemini_key:
        PROVIDERS["gemini"]["api_key"] = gemini_key
    
    # OpenRouter Config
    st.markdown("**OpenRouter**")
    openrouter_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        value=PROVIDERS["openrouter"]["api_key"],
        help="Get from https://openrouter.ai"
    )
    if openrouter_key:
        PROVIDERS["openrouter"]["api_key"] = openrouter_key
    
    st.divider()
    st.subheader("💬 Conversation Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

def call_nvidia(messages):
    """Call NVIDIA NIM API - Fixed: removed proxies parameter"""
    if not PROVIDERS["nvidia"]["api_key"]:
        return None, "API key not configured"
    
    try:
        headers = {
            "Authorization": f"Bearer {PROVIDERS['nvidia']['api_key']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": PROVIDERS["nvidia"]["model"],
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7
        }
        
        # FIXED: Removed 'proxies' parameter from Client.init()
        response = requests.post(
            f"{PROVIDERS['nvidia']['base_url']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, str(e)

def call_gemini(messages):
    """Call Gemini API"""
    if not PROVIDERS["gemini"]["api_key"]:
        return None, "GEMINI_API_KEY not configured"
    
    try:
        # Convert messages to Gemini format
        last_user_message = messages[-1]["content"] if messages[-1]["role"] == "user" else ""
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{PROVIDERS['gemini']['model']}:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": PROVIDERS["gemini"]["api_key"]}
        
        payload = {
            "contents": [{
                "parts": [{"text": last_user_message}]
            }]
        }
        
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"], None
    except Exception as e:
        return None, str(e)

def call_openrouter(messages):
    """Call OpenRouter API"""
    if not PROVIDERS["openrouter"]["api_key"]:
        return None, "OPENROUTER_API_KEY not configured"
    
    try:
        headers = {
            "Authorization": f"Bearer {PROVIDERS['openrouter']['api_key']}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://chatbot.hkuway.com",
            "X-Title": "UWAY Compliance Assistant"
        }
        
        payload = {
            "model": PROVIDERS["openrouter"]["model"],
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{PROVIDERS['openrouter']['base_url']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, str(e)

def get_response(prompt):
    """Try providers in priority order"""
    messages = [
        {"role": "system", "content": "You are a professional financial compliance assistant specializing in Hong Kong and Singapore regulatory frameworks."},
        {"role": "user", "content": prompt}
    ]
    
    errors = []
    
    # Try NVIDIA first
    if PROVIDERS["nvidia"]["api_key"]:
        response, error = call_nvidia(messages)
        if response:
            return response, "nvidia"
        errors.append(f"nvidia: {error}")
        st.warning(f"⚠️ nvidia failed: {error}... Trying next provider...")
    
    # Try Gemini second
    if PROVIDERS["gemini"]["api_key"]:
        response, error = call_gemini(messages)
        if response:
            return response, "gemini"
        errors.append(f"gemini: {error}")
        st.warning(f"⚠️ gemini failed: {error}... Trying next provider...")
    
    # Try OpenRouter third
    if PROVIDERS["openrouter"]["api_key"]:
        response, error = call_openrouter(messages)
        if response:
            return response, "openrouter"
        errors.append(f"openrouter: {error}")
        st.warning(f"⚠️ openrouter failed: {error}... Trying next provider...")
    
    return None, "; ".join(errors)

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "timestamp" in msg:
            st.caption(f'{msg["timestamp"]}')

# Chat input
if prompt := st.chat_input("Ask about AML/KYC compliance in Hong Kong..."):
    # Add user message to UI
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    
    with st.chat_message("user"):
        st.write(prompt)
        st.caption(datetime.now().strftime("%H:%M"))
    
    # Call API
    with st.chat_message("assistant"):
        try:
            answer, provider = get_response(prompt)
            
            if answer:
                # Display streaming-style animation
                placeholder = st.empty()
                displayed = ""
                for char in answer:
                    displayed += char
                    placeholder.markdown(displayed + "▌")
                
                placeholder.markdown(answer)
                st.caption(f"✅ Powered by {provider}")
                
                # Save assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
            else:
                st.error(f"❌ All providers failed: {provider}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "I'm currently unable to respond due to API issues. Please try again later.",
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer
st.divider()
st.caption("© 2026 UWAY Innovation Limited | For informational purposes only | Updated: 2026-04-30")
