# UWAY Chatbot - Streamlit Frontend
# 调用 EC2 后端 API (16.163.147.170:8000)

import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="UWAY Compliance Assistant",
    page_icon="🛡️",
    layout="wide"
)

# Brand colors CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fa;
    }
    .main-header {
        color: #1a2332;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("<div style='font-size:3rem'>🛡️</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<p class='main-header'>UWAY Financial Compliance Assistant</p>", unsafe_allow_html=True)

# Backend API configuration
API_BASE_URL = "http://16.163.147.170"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Health Check
    st.subheader("Backend Status")
    try:
        health_response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ Backend Connected")
            st.caption(f"IP: 16.163.147.170:8000")
        else:
            st.error("❌ Backend Unavailable")
    except Exception as e:
        st.error(f"❌ Connection Failed: {str(e)[:50]}")
    
    st.divider()
    
    # Stats
    st.subheader("💬 Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    if st.button("🗑️ Clear History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("© 2026 UWAY Innovation Limited")

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "timestamp" in msg:
            st.caption(f"🕐 {msg['timestamp']}")

# Chat input
if prompt := st.chat_input("Ask about AML/KYC compliance in Hong Kong..."):
    # Add user message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })
    
    with st.chat_message("user"):
        st.write(prompt)
        st.caption(f"🕐 {timestamp}")
    
    # Call backend API
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_BASE_URL}/api/chat",
                    headers={"Content-Type": "application/json"},
                    json={"message": prompt},
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()
                
                answer = data.get("answer", "No response received")
                sources = data.get("sources", [])
                confidence = data.get("confidence_score", 0)
            
            # Display response
            st.write(answer)
            
            # Show metadata
            meta_cols = st.columns(3)
            with meta_cols[0]:
                st.caption(f"📚 Sources: {', '.join(sources) if sources else 'N/A'}")
            with meta_cols[1]:
                st.caption(f"🎯 Confidence: {confidence:.0%}")
            with meta_cols[2]:
                st.caption(f"🕐 {timestamp}")
            
            # Save assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "timestamp": timestamp
            })
            
        except requests.exceptions.Timeout:
            st.error("⚠️ Request timeout. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend server.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

# Footer
st.divider()
st.markdown("<p class='footer'>For informational purposes only | Not legal advice</p>", unsafe_allow_html=True)
