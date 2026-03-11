import streamlit as st
import pandas as pd
from groq import Groq

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
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1rem;
        margin-bottom: 30px;
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
    
    /* Result Container */
    .result-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        margin: 10px 0;
    }
    
    /* Code Display */
    .stCodeBlock {
        background: #1e1e2e !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(20, 20, 35, 0.95) !important;
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
    
    /* Section Headers */
    .section-header {
        color: #00d2ff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    /* Data Preview Header */
    .data-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(30, 30, 46, 0.9);
        padding: 15px 20px;
        border-radius: 12px 12px 0 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: none;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(40, 40, 60, 0.6);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Dataframe Container */
    .dataframe-container {
        background: rgba(30, 30, 46, 0.9);
        border-radius: 0 0 12px 12px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: none;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d2ff;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #a0a0a0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'df_uploaded' not in st.session_state:
    st.session_state.df_uploaded = False

if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

if 'current_code' not in st.session_state:
    st.session_state.current_code = None

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
        
        # Show dataset info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">Rows</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(df.columns)}</div>
                <div class="metric-label">Columns</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show column names
        st.markdown("**Columns:**")
        st.code(", ".join(df.columns.tolist()), language=None)

# Main content area
st.markdown('<h1 class="main-title">💬 SheetTalk</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">✨ AI-Powered Chat with Your CSV Data ✨</p>', unsafe_allow_html=True)

# Main chat interface
if st.session_state.api_key_set and st.session_state.df_uploaded:
    st.markdown("---")
    
    # Use tabs for different views
    tab1, tab2 = st.tabs(["💬 Chat", "📊 Data"])
    
    with tab1:
        # Display chat messages
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(message["content"])
                else:
                    # Display bot response
                    if "code" in message:
                        st.markdown("**Generated Code:**")
                        st.code(message["code"], language="python")
                    if "result" in message:
                        st.markdown("**Result:**")
                        result = message["result"]
                        if isinstance(result, (pd.Series, pd.DataFrame)):
                            st.dataframe(result, width='stretch')
                        else:
                            st.markdown(f"### {result}")
        
        # Chat input
        if question := st.chat_input("💭 Ask anything about your data..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": question})
            
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
            
            with st.spinner("🤔 Analyzing your data..."):
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
                    
                    # Store current result
                    st.session_state.current_result = result
                    st.session_state.current_code = code
                    
                    # Add assistant response to history
                    response = {"role": "assistant", "code": code, "result": result}
                    st.session_state.chat_history.append(response)
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            
            # Rerun to display new messages
            st.rerun()
        
        # Show current result with visualization if available
        if st.session_state.current_result is not None:
            st.markdown("---")
            st.markdown('<div class="section-header">📈 Analysis Result</div>', unsafe_allow_html=True)
            
            result = st.session_state.current_result
            code = st.session_state.current_code
            
            with st.container():
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("**Generated Code:**")
                    st.code(code, language="python")
                with col2:
                    st.markdown("**Output:**")
                    if isinstance(result, (pd.Series, pd.DataFrame)):
                        st.dataframe(result, width='stretch')
                    else:
                        st.markdown(f"## {result}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Show chart for DataFrame/Series results
            if isinstance(result, (pd.Series, pd.DataFrame)):
                st.markdown('<div class="section-header">📊 Visualization</div>', unsafe_allow_html=True)
                st.bar_chart(result)
    
    with tab2:
        df = st.session_state.df
        st.markdown('<div class="section-header">📋 Dataset Preview</div>', unsafe_allow_html=True)
        
        # Data overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Numeric Columns", len(df.select_dtypes(include='number').columns))
        with col4:
            st.metric("Text Columns", len(df.select_dtypes(include='object').columns))
        
        # Data preview
        st.markdown("### First 10 Rows")
        st.dataframe(df.head(10), width='stretch')
        
        # Column info
        st.markdown("### Column Information")
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.values,
            'Non-Null': df.notna().sum().values,
            'Null': df.isna().sum().values
        })
        st.dataframe(col_info, width='stretch')

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

