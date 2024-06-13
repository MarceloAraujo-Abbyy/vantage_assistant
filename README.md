# Vantage Assistant

This application uses RAG (Retrieval Augmented Generation) and LLM (ChatGPT OpenAI) to access all Vantage documentation, and let you interact with the manuals using natural language. 


Install dependencies.

```python
pip install -r requirements.txt
```

## Usage

You'll need to set up your ABBYY Vantage tenant abd OpenAI account. 

When create your streamlit app, set the secrets with the according information: 

```python
OPENAI_API_KEY = ""
VANTAGE_CLIENT_ID = "" 
VANTAGE_SECRET_ID = ""
VANTAGE_TENANT_ID = "" 

