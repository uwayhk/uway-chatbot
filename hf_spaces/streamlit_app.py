import streamlit as st
import requests
import json
from datetime import datetime

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

if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = st.secrets.get("AWS_API_URL", "https://your-ec2-ip.uway.hk/api/chat")

# Sidebar config
with st.sidebar:
    st.header("⚙️ Settings")
    api_url = st.text_input(
        "Backend API URL",
        value=st.session_state.api_base_url,
        help="Your AWS EC2 FastAPI endpoint"
    )
    
    st.divider()
    st.subheader("💬 Conversation Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

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
    
    # Call backend API
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                f"{api_url}/chat",
                json={"message": prompt, "session_id": "hf_session"},
                timeout=60,
                stream=False
            )
            response.raise_for_status()
            
            result = response.json()
            answer = result.get("answer", "Sorry, no response received.")
            
            # Display streaming-style animation
            placeholder = st.empty()
            displayed = ""
            for char in answer:
                displayed += char
                placeholder.markdown(displayed + "▌")
            
            placeholder.markdown(answer)
            
            # Save assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to backend. Please check your AWS EC2 status.")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer
st.divider()
st.caption("Powered by UWAY AI • Gemini 2.5 • Financial Compliance Assistant")