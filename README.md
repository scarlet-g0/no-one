# NO.ONE Project

Developing NO.ONE components using different LLMs (Gemini, GPT-5, Mistral...), LangFuse for LLM-as-a-Judge, agno for the agentic workflow and streamlit for development and collecting Philipp's feedback. 
---

## 🚀 How to Run

1.  **Create and activate the virtual environment using `uv`**:
    ```bash
    uv venv no-one-env
    source no-one-env/bin/activate
    ```

2.  **Install dependencies**:
    This project will eventually have a `requirements.txt` file. For now, install the main packages:
    ```bash
    uv pip install streamlit langfuse agno
    ```

3.  **Set API keys**:
    # OpenAI API Key
    echo "OPENAI_API_KEY=your-openai-api-key-here" >> .env

    # Langfuse Configuration, get from 1password
    echo "LANGFUSE_PUBLIC_KEY=your-langfuse-public-key" >> .env
    echo "LANGFUSE_SECRET_KEY=your-langfuse-secret-key" >> .env
    echo "LANGFUSE_HOST=https://langfuse.gradient0.com" >> .env
    echo "LANGFUSE_TRACING_ENVIRONMENT=development" >> .env

4.  **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

---

## Dependencies

* Streamlit
* LangFuse
* Python 3.9+
