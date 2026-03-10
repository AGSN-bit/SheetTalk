import streamlit as st
import pandas as pd
from groq import Groq

# Get Groq API key from user
api_key = st.text_input("Enter your Groq API key", type="password")

if api_key:
    client = Groq(api_key=api_key)

    st.title("📊 Chat With Your Data (AI Powered)")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.subheader("Dataset Preview")
        st.write(df.head())

        question = st.text_input("Ask a question about the data")

        if question:

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

                st.subheader("Generated Code")
                st.code(code)

                try:

                    # Execute generated code safely
                    result = eval(code, {"df": df, "pd": pd})

                    st.subheader("Result")
                    st.write(result)

                    # Auto chart if result is dataframe/series
                    if isinstance(result, (pd.Series, pd.DataFrame)):
                        st.subheader("Visualization")
                        st.bar_chart(result)

                except Exception as e:
                    st.error(f"Error executing code: {e}")

            except Exception as e:
                st.error(f"API Error: {e}")
else:
    st.info("Please enter your Groq API key to use the app.")

