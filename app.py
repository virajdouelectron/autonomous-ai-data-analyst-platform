import streamlit as st

# MUST BE FIRST - before any other st commands
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# NOW start backend
import subprocess
import time
import sys
import os
import requests
import pandas as pd
from datetime import datetime
import threading

@st.cache_resource
def start_backend():
    """Start FastAPI backend as subprocess (only once)."""
    try:
        requests.get("http://localhost:8000/health", timeout=1)
        return True
    except:
        pass
    
    # Start silently without st.write() messages
    env = os.environ.copy()
    backend_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "app:app", 
         "--host", "0.0.0.0", 
         "--port", "8000", 
         "--log-level", "info"],
        cwd="/app/backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    
    # Wait quietly
    for i in range(60):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                return True
        except:
            time.sleep(1)
    
    return False

# Start backend
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
backend_ready = start_backend()

# ADD ALL THE REST OF YOUR CODE HERE
# CSS, session state, landing page, app page, etc.

# ... rest stays the same

# Professional Blue/Teal/White Landing Page CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: #f8fafc;
        color: #0f172a;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* HEADER styles */
    .header-logo {
        font-family: 'Outfit', sans-serif;
        font-size: 1.6em;
        font-weight: 800;
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }
    
    /* HERO SECTION */
    .hero {
        background: radial-gradient(circle at top right, rgba(2, 132, 199, 0.08), transparent 45%),
                    radial-gradient(circle at bottom left, rgba(13, 148, 136, 0.05), transparent 45%),
                    #ffffff;
        padding: 100px 40px 80px;
        text-align: center;
        border-radius: 24px;
        border: 1px solid rgba(2, 132, 199, 0.08);
        box-shadow: 0 10px 30px -10px rgba(2, 132, 199, 0.05);
        margin-bottom: 40px;
    }
    
    .hero-title {
        font-size: 3.8em;
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 24px;
        line-height: 1.15;
        letter-spacing: -1.5px;
    }
    
    .hero-title span {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.25em;
        color: #475569;
        margin-bottom: 40px;
        max-width: 680px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    /* FEATURES SECTION */
    .features-title {
        font-size: 2.5em;
        font-weight: 800;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 48px;
        color: #0f172a;
        letter-spacing: -0.8px;
    }
    
    .feature-card {
        background: #ffffff;
        padding: 40px 32px;
        border-radius: 20px;
        border: 1px solid rgba(2, 132, 199, 0.06);
        box-shadow: 0 4px 20px -2px rgba(2, 132, 199, 0.03);
        transition: all 0.3s ease;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 30px -10px rgba(2, 132, 199, 0.08);
        border-color: rgba(2, 132, 199, 0.3);
    }
    
    .feature-icon-wrapper {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, rgba(2, 132, 199, 0.1) 0%, rgba(13, 148, 136, 0.05) 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 24px;
        font-size: 2em;
    }
    
    .feature-title {
        font-size: 1.35em;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 14px;
        letter-spacing: -0.3px;
    }
    
    .feature-desc {
        color: #64748b;
        font-size: 0.95em;
        line-height: 1.6;
    }
    
    /* STATS SECTION */
    .stats {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        padding: 50px 40px;
        border-radius: 24px;
        margin: 60px 0;
        display: flex;
        justify-content: space-around;
        align-items: center;
        color: white;
        box-shadow: 0 20px 40px -15px rgba(2, 132, 199, 0.25);
    }
    
    .stat-item {
        text-align: center;
        flex: 1;
    }
    
    .stat-number {
        font-family: 'Outfit', sans-serif;
        font-size: 3.5em;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }
    
    .stat-label {
        font-size: 0.95em;
        opacity: 0.95;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* HOW IT WORKS */
    .how-title {
        font-size: 2.5em;
        font-weight: 800;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 48px;
        color: #0f172a;
        letter-spacing: -0.8px;
    }
    
    .step {
        background: #ffffff;
        padding: 32px 24px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(2, 132, 199, 0.05);
        box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
        position: relative;
        margin-bottom: 20px;
    }
    
    .step:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -8px rgba(2, 132, 199, 0.06);
        border-color: rgba(2, 132, 199, 0.2);
    }
    
    .step-number {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.4em;
        margin: 0 auto 20px;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.2);
        font-family: 'Outfit', sans-serif;
    }
    
    .step-title {
        font-size: 1.15em;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }
    
    .step-desc {
        color: #64748b;
        font-size: 0.9em;
        line-height: 1.5;
    }
    
    /* CTA SECTION */
    .cta-section {
        background: linear-gradient(135deg, #0f172a 0%, #0f2942 100%);
        padding: 80px 40px;
        border-radius: 24px;
        text-align: center;
        color: white;
        margin: 60px 0 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        position: relative;
    }
    
    .cta-title {
        font-size: 2.8em;
        font-weight: 900;
        margin-bottom: 16px;
        letter-spacing: -1px;
    }
    
    .cta-desc {
        font-size: 1.25em;
        opacity: 0.85;
        margin-bottom: 40px;
        max-width: 550px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* STREAMLIT COMPONENT RESETS & OVERRIDES */
    .stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 24px !important;
        font-weight: 600 !important;
        font-size: 0.95em !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.18) !important;
        height: auto !important;
        width: auto !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(2, 132, 199, 0.3) !important;
        color: white !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* UPLOADER WRAPPER */
    .stFileUploader {
        border: 2px dashed rgba(2, 132, 199, 0.2) !important;
        border-radius: 20px !important;
        padding: 30px 20px !important;
        background: #ffffff !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.01) !important;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #0284c7 !important;
        background: rgba(2, 132, 199, 0.01) !important;
    }

    .stExpander {
        border: 1px solid rgba(2, 132, 199, 0.08) !important;
        border-radius: 16px !important;
        background: #ffffff !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.01) !important;
        margin-bottom: 20px !important;
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    @media (max-width: 768px) {
        .stats {
            flex-direction: column;
            gap: 30px;
        }
        .hero-title {
            font-size: 2.5em;
        }
        .cta-title {
            font-size: 2em;
        }
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"
if "dataset" not in st.session_state:
    st.session_state.dataset = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# HEADER
col_logo, col_spacer, col_btn = st.columns([2, 3, 1.2])
with col_logo:
    st.markdown("<div class='header-logo'>📊 AI Data Analyst</div>", unsafe_allow_html=True)

with col_btn:
    if st.session_state.current_page == "landing":
        if st.button("🚀 Get Started", key="header_cta"):
            st.session_state.current_page = "app"
            st.rerun()
    else:
        if st.button("← Back to Landing", key="header_back"):
            st.session_state.current_page = "landing"
            st.rerun()

# LANDING PAGE
if st.session_state.current_page == "landing":
    
    # HERO SECTION
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Your AI partner for <span>Data Analysis</span></div>
        <div class="hero-subtitle">Upload CSV files and ask natural language questions. Get instant insights, ready-to-run Pandas code, and data visualizations dynamically.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_h1, col_h2, col_h3 = st.columns([1.5, 2, 1.5])
    with col_h2:
        if st.button("🚀 Get Started Now", key="hero_cta_btn", use_container_width=True):
            st.session_state.current_page = "app"
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # FEATURES SECTION
    st.markdown('<div class="features-title">Powerful Capabilities</div>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-wrapper">📤</div>
            <div class="feature-title">Instant Upload</div>
            <div class="feature-desc">Load CSV datasets seamlessly. Instantly preview schema, row/column dimensions, and field statistics.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-wrapper">💬</div>
            <div class="feature-title">Natural Language Queries</div>
            <div class="feature-desc">Type queries in plain conversational English. The assistant automatically generates precise Pandas queries.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-wrapper">🤖</div>
            <div class="feature-title">AI-Powered Insights</div>
            <div class="feature-desc">Uncover hidden correlations and get automated, actionable recommendations tailored to your dataset.</div>
        </div>
        """, unsafe_allow_html=True)
    
    # STATS SECTION
    st.markdown("""
    <div class="stats">
        <div class="stat-item">
            <div class="stat-number">1,200+</div>
            <div class="stat-label">Analyses Completed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">98.2%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">&lt; 5s</div>
            <div class="stat-label">Response Time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # HOW IT WORKS
    st.markdown('<div class="how-title">How It Works</div>', unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    
    with col_s1:
        st.markdown("""
        <div class="step">
            <div class="step-number">1</div>
            <div class="step-title">Upload File</div>
            <div class="step-desc">Select and upload your tabular CSV document.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_s2:
        st.markdown("""
        <div class="step">
            <div class="step-number">2</div>
            <div class="step-title">Preview Schema</div>
            <div class="step-desc">Inspect structural metrics and fields.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_s3:
        st.markdown("""
        <div class="step">
            <div class="step-number">3</div>
            <div class="step-title">Ask Question</div>
            <div class="step-desc">Ask your query in plain English.</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_s4:
        st.markdown("""
        <div class="step">
            <div class="step-number">4</div>
            <div class="step-title">Get Insights</div>
            <div class="step-desc">Receive optimized code and answers.</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # FINAL CTA
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Ready to analyze your data?</div>
        <div class="cta-desc">Accelerate your data science workflow with immediate AI synthesis.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1.5, 2, 1.5])
    with col_c2:
        if st.button("Launch App Now →", key="final_cta_btn", use_container_width=True):
            st.session_state.current_page = "app"
            st.rerun()

# APP PAGE
else:
    if not backend_ready:
        st.error("Backend is not ready. Please refresh the page.")
        st.stop()

    st.markdown("### 📤 Upload Your Dataset")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        key="main_uploader",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        try:
            with st.spinner("📤 Processing and parsing your file..."):
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
                    st.success(f"✅ Successfully loaded {st.session_state.dataset['rows']} rows!")
                    
                    with st.expander("📋 Data Preview & Columns", expanded=True):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Rows", st.session_state.dataset['rows'])
                        with col2:
                            st.metric("Columns", st.session_state.dataset['columns'])
                        with col3:
                            st.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
                        with col4:
                            st.metric("Loaded At", datetime.now().strftime("%H:%M:%S"))
                        
                        st.markdown("**Column Schema:**")
                        col_df = pd.DataFrame({
                            "Column Name": st.session_state.dataset['column_names'],
                            "Inferred Type": [
                                st.session_state.dataset['dtypes'].get(col, 'Unknown')
                                for col in st.session_state.dataset['column_names']
                            ]
                        })
                        st.dataframe(col_df, use_container_width=True)
                        
                        st.markdown("**Data Sample (First 10 rows):**")
                        preview_df = pd.DataFrame(st.session_state.dataset['data'])
                        st.dataframe(preview_df, use_container_width=True)
                else:
                    st.error(f"Upload failed: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    if st.session_state.dataset:
        st.markdown("### 📊 Data Visualization")
        preview_df = pd.DataFrame(st.session_state.dataset['data'])
        numeric_cols = preview_df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_cols:
            col1, col2 = st.columns(2)
            
            with col1:
                selected_col = st.selectbox("Column:", numeric_cols, key="viz_col")
                st.bar_chart(preview_df[selected_col], use_container_width=True)
            
            with col2:
                st.markdown("**Statistics**")
                stats = preview_df[numeric_cols].describe()
                st.dataframe(stats, use_container_width=True)
        
        st.divider()
        st.markdown("### 💬 Chat with Your Data")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.code(msg["content"], language="python")
        
        user_input = st.chat_input("Ask a question about the uploaded columns...")
        
        if user_input and st.session_state.dataset:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.spinner("🤔 Analyzing and generating code..."):
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
                        st.rerun()
                    else:
                        st.error("Failed to generate response from query engine.")
                except Exception as e:
                    st.error(f"Query Error: {str(e)}")
