import streamlit as st
from langfuse import Langfuse
import os

# --- Configuration ---
# It's best practice to use environment variables for keys.
# You can set these in your terminal before running the app:
# export LANGFUSE_SECRET_KEY="your_secret_key"
# export LANGFUSE_PUBLIC_KEY="your_public_key"

try:
    # Initialize Langfuse
    langfuse = Langfuse()
    langfuse_status = "Langfuse SDK initialized successfully. Ready to trace. ✅"
except Exception as e:
    langfuse_status = f"Could not initialize Langfuse. Please check your keys. ❌\nError: {e}"

# --- Streamlit App ---
st.set_page_config(
    page_title="Setup Test",
    layout="centered"
)

st.title("Agno, Streamlit & LangFuse Setup Test")
st.markdown("---")

st.header("Component Status")
st.info(f"**Streamlit:** Running successfully. ✅")
st.info(f"**Langfuse:** {langfuse_status}")

st.markdown("---")
st.success("Your environment is set up and ready to go!")