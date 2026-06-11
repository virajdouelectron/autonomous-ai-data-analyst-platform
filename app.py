import streamlit as st
import requests
import os
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        background: linear-gradient(135deg, #0a0e27 0%, #0f1035 100%);
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .header-section {
        text-align: center;
        padding: 40px 20px 30px;
        background: linear-gradient(180deg, rgba(102,126,234,0.1) 0%, transparent 100%);
        border-radius: 16px;
        margin-bottom: 30px;
        border: 1px solid rgba(102,126,234,0.2);
    }
    
    .header-title {
        font-size: 3em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .header-subtitle {
        font-size: 1.1em;
        color: #a0a0a0;
        font-weight: 400;
    }
    
    .stButton button {
        width: 100%;
        border-radius: 10px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 14px;
        font-weight: 600;
        font-size: 1em;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stFileUploader {
        border: 2px dashed rgba(102,126,234,0.3) !important;
        border-radius: 16px !important;
        padding: 30px !important;
        background: rgba(255,255,255,0.02) !important;
    }
    
    .chat-section {
        margin-top: 40px;
        padding: 20px;
        border-radius: 16px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: 600;
        margin: 10px 0;
    }
    
    .status-success {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #a0a0a0;
    }
</style>
""", unsafe_allow_html=True)

if "dataset" not in st.session_state:
    st.session_state.dataset = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
<div class="header-section">
    <div class="header-title">📊 AI Data Analyst</div>
    <div class="header-subtitle">Upload a CSV and have an intelligent conversation with your data</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### Upload Your Dataset")
uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    key="main_uploader",
    label_visibility="collapsed"
)

if uploaded_file:
    try:
        with st.spinner("📤 Processing your file..."):
            logger.info(f"Uploading file: {uploaded_file.name}")
            
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")
            }
            response = requests.post(
                f"{BACKEND_URL}/api/upload",
                files=files,
                timeout=15
            )
            
            if response.status_code == 200:
                st.session_state.dataset = response.json()
                logger.info(f"Upload successful: {st.session_state.dataset['rows']} rows")
                
                st.markdown(f"""
                <div class="status-badge status-success">
                    ✅ Successfully loaded {st.session_state.dataset['rows']} rows × {st.session_state.dataset['columns']} columns
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("📋 Data Preview & Statistics", expanded=True):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Rows", st.session_state.dataset['rows'])
                    with col2:
                        st.metric("Columns", st.session_state.dataset['columns'])
                    with col3:
                        st.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
                    with col4:
                        st.metric("Timestamp", datetime.now().strftime("%H:%M:%S"))
                    
                    st.markdown("**Column Information:**")
                    col_df = pd.DataFrame({
                        "Column": st.session_state.dataset['column_names'],
                        "Type": [
                            st.session_state.dataset['dtypes'].get(col, 'Unknown')
                            for col in st.session_state.dataset['column_names']
                        ]
                    })
                    st.dataframe(col_df, use_container_width=True)
                    
                    st.markdown("**Data Preview:**")
                    preview_df = pd.DataFrame(st.session_state.dataset['data'])
                    st.dataframe(preview_df, use_container_width=True)
            else:
                st.error(f"Upload failed: {response.text}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

if st.session_state.dataset:
    st.markdown("""
    <div class="chat-section">
        <h3 style="margin: 0 0 20px 0;">💬 Chat with Your Data</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.code(msg["content"], language="python")
    
    user_input = st.chat_input("Ask a question about your data...")
    
    if user_input and st.session_state.dataset:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        logger.info(f"Query: {user_input[:50]}")
        
        with st.spinner("🤔 Analyzing your data..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/query",
                    json={
                        "question": user_input,
                        "column_names": st.session_state.dataset["column_names"]
                    },
                    timeout=15
                )
                
                if response.status_code == 200:
                    ai_response = response.json().get("code", "No response")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                    logger.info("Response generated successfully")
                    st.rerun()
                else:
                    st.error("Failed to generate response")
            except Exception as e:
                logger.error(f"Query error: {str(e)}")
                st.error(f"Error: {str(e)}")
else:
    st.markdown("""
    <div class="empty-state">
        <div style="font-size: 4em; margin-bottom: 20px;">📊</div>
        <div style="font-size: 1.2em; margin-bottom: 10px;"><strong>Ready to analyze your data?</strong></div>
        <p>Upload a CSV file to get started</p>
    </div>
    """, unsafe_allow_html=True)
