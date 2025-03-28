# Vantage Assistant

This application uses RAG (Retrieval Augmented Generation) and LLM (ChatGPT OpenAI) to access all Vantage documentation, and let you interact with the Vantage manuals using natural language. 


## Usage

You'll need to set up your ABBYY Vantage tenant and OpenAI account. 

When create your streamlit app, set the secrets with the according information: 

```python
OPENAI_API_KEY = ""
VANTAGE_CLIENT_ID = "" 
VANTAGE_CLIENT_SECRET = ""
VANTAGE_TENANT_NAME = ""
VANTAGE_TENANT_ID = "" 
VANTAGE_BASE_URL = "https://vantage-us.abbyy.com"

