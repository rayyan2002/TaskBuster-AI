import streamlit as st
from agent import run_concluder_agent
from datasets import load_dataset
import streamlit as st


st.title("AI Agent Streamlit")
query = st.text_input("Ask a Question:")
if st.button("Run Agent"):
    if query.strip():
        answer = run_concluder_agent(query)
        st.write(f"Output: {answer}")
    else:
        st.write("Please enter a question.")
