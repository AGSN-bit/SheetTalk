import streamlit as st
import pandas as pd
from groq import Groq
import time

# Page configuration
st.set_page_config(
    page_title="SheetTalk - Chat With Your Data",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern chatbot UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }
    
    /* Chat Container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Message Bubbles - User */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 16px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 70%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        animation: slideInRight 0.3s ease-out;
    }
    
    /* Message Bubbles - Bot */
    .bot-message {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        color: #e0e0e0;
        padding: 16px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 70%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: slideInLeft 0.3s ease-out;
    }
    
    /* Title Styling */
    .main-title {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 50%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0 0 30px rgba(0, 210, 255, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    
    /* Input Container */
    .input-container {
        background: rgba(30, 30, 46, 0.9);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* API Key Input */
    .stTextInput > div > div > input {
        background: rgba(40, 40, 60, 0.8) !important;
        color: #e0e0e0 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(40, 40, 60, 0.6);
        border-radius: 16px;
        padding: 20px;
        border: 2px dashed rgba(255, 255, 255, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Data Preview Card */
    .data-card {
        background: rgba(30, 30, 46, 0.9);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Result Display */
    .result-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        margin-top: 20px;
    }
    
    /* Code Display */
    .stCodeBlock {
        background: #1e1e2e !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Charts */
    .stBarChart {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(20, 20, 35, 0.95) !important;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    .typing-indicator {
        display: flex;
        gap: 5px;
        padding: 10px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        animation: pulse 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    /* Status Messages */
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    .info-message {
        background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.85rem;
        margin-top: 40px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer span {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
    }
    
    /* Logo/Brand */
    .brand-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Section Headers */
    .section-header {
        color: #00d2ff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* DataFrame Styling */
    .dataframe {
        border: none !important;
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    .dataframe tbody tr {
        background: rgba(40, 40, 60, 0.6) !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(60, 60, 80, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'df_uploaded' not in st.session_state:
    st.session_state.df_uploaded = False

if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

# Sidebar for API key and settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")
    
    api_key = st.text_input("🔑 Groq API Key", type="password", help="Get your API key from https://console.groq.com/")
    
    if api_key:
        st.session_state.api_key_set = True
        client = Groq(api_key=api_key)
        st.markdown('<div class="success-message">✅ API Key Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-message">ℹ️ Enter your Groq API key to get started</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Your Data")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.df_uploaded = True
        st.success(f"✅ Loaded: {uploaded_file.name}")
        st.info(f"📈 {len(df)} rows × {len(df.columns)} columns")

# Main content area
st.markdown('<div class="brand-icon">💬</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">SheetTalk</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ AI-Powered Chat with Your CSV Data ✨</p>', unsafe_allow_html=True)

# Main chat interface
if st.session_state.api_key_set and st.session_state.df_uploaded:
    st.markdown("---")
    st.markdown('<div class="section-header">💬 Ask Questions</div>', unsafe_allow_html=True)
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message['role'] == 'user':
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Question input
    question = st.chat_input("💭 Ask anything about your data...")
    
    if question:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Create prompt for Groq
        df = st.session_state.df
        prompt = f"""
You are an expert Python data analyst.

A pandas dataframe named df already exists.

Columns in df:
{list(df.columns)}

Your task:
Convert the user's question into a SINGLE executable pandas command.

STRICT RULES:
- Use ONLY the dataframe df
- Use pandas operations only
- Do NOT create variables
- Do NOT use print()
- Return ONE line of valid Python code
- The code must directly return the result

Examples:

Question: total revenue by city
Answer:
df.groupby('city')['revenue'].sum()

Question: city with highest revenue
Answer:
df.groupby('city')['revenue'].sum().idxmax()

Now answer:

Question: {question}
"""
        
        with st.spinner("🤔 Thinking..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                
                code = completion.choices[0].message.content
                
                # Clean markdown formatting
                code = code.replace("```python", "").replace("```", "").strip()
                
                # Extract the line containing df operation
                lines = code.split("\n")
                code = [line for line in lines if "df" in line][0]
                
                # Execute generated code
                result = eval(code, {"df": df, "pd": pd})
                
                # Create result message
                result_msg = f"**Generated Code:**\n```python\n{code}\n```\n\n**Result:**\n{result}"
                
                if isinstance(result, (pd.Series, pd.DataFrame)):
                    result_msg += "\n\n📊 **Visualization:**"
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.session_state.messages.append({"role": "assistant", "content": result_msg, "result": result})
                else:
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.session_state.messages.append({"role": "assistant", "content": result_msg})
                    
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        # Rerun to display new messages
        st.rerun()
    
    # Display results with visualization
    for i, msg in enumerate(st.session_state.messages):
        if msg['role'] == 'assistant' and 'result' in msg:
            st.markdown(f'<div class="result-box">{msg["content"]}</div>', unsafe_allow_html=True)
            if 'Visualization' in msg['content']:
                st.bar_chart(msg['result'])
    
    # Data preview section
    st.markdown("---")
    st.markdown('<div class="section-header">📊 Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)

elif not st.session_state.api_key_set:
    st.markdown("""
    <div class="chat-container">
        <div class="bot-message">
            👋 Welcome to <b>SheetTalk</b>!<br><br>
            I'm your AI-powered data analyst. To get started:<br>
            1. Enter your Groq API key in the sidebar<br>
            2. Upload a CSV file<br>
            3. Start asking questions about your data!<br><br>
            💡 Get your free API key at <a href="https://console.groq.com/" target="_blank">console.groq.com</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show features
    st.markdown("---")
    st.markdown("""
    <div style="display: flex; justify-content: space-around; text-align: center; color: #a0a0a0;">
        <div>
            <div style="font-size: 2rem;">📊</div>
            <div>Upload CSV</div>
        </div>
        <div>
            <div style="font-size: 2rem;">💬</div>
            <div>Ask Questions</div>
        </div>
        <div>
            <div style="font-size: 2rem;">🤖</div>
            <div>AI Analysis</div>
        </div>
        <div>
            <div style="font-size: 2rem;">📈</div>
            <div>Visualize</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif not st.session_state.df_uploaded:
    st.markdown("""
    <div class="chat-container">
        <div class="bot-message">
            👋 API Key connected! Now please upload a CSV file to continue.<br><br>
            💡 You can use the file uploader in the sidebar to upload your data.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer with copyright
st.markdown("---")
st.markdown(f"""
<div class="footer">
    © {pd.Timestamp.now().year} SheetTalk. All rights reserved.<br>
    Made with ❤️ for data enthusiasts | Powered by <span>Dhokla</span>
</div>
""", unsafe_allow_html=True)

