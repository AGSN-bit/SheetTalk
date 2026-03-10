# SheetTalk - Chat With Your CSV Data

SheetTalk is an AI-powered Streamlit app that allows you to chat with your CSV data using natural language. It uses Groq API to convert your questions into pandas code and executes it to give you instant insights from your data.

## Features

- 📊 Upload CSV files
- 💬 Ask questions in natural language
- 🤖 AI-powered code generation using Groq API
- 📈 Automatic data visualization
- 🔒 Your API key stays secure (entered locally)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AGSN-bit/SheetTalk.git
cd SheetTalk
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Get your Groq API key from https://console.groq.com/

2. Run the app:
```bash
streamlit run app.py
```

3. Open your browser to http://localhost:8501

4. Enter your Groq API key when prompted

5. Upload a CSV file and start asking questions!

## Example Questions

- "Show me the first 5 rows"
- "What is the average of column 'Sales'?"
- "Give me the summary statistics"
- "Show only rows where column 'Age' > 30"

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI**: Groq API (Llama 3.3 70B)
- **Data Processing**: Pandas

## License

MIT License

