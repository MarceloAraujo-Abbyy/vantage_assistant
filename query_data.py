import argparse
from dataclasses import dataclass
import os 
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st

CHROMA_PATH = "chroma"
st.secrets["OPENAI_API_KEY"]

PROMPT_TEMPLATE = """
Its function is to help users of the ABBYY Vantage product. 
Please answer the question in details, quoting step by step according to the context provided. 
Consider only the context provided. If you can't find the information, say that you were unable to locate the information. 
Answer the question based only on the following context:

{context}

---

Question: {question}
"""

def get_answer(question):
    # Create CLI.
    query_text = question

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        response_text = "content='Unable to find matching results.'"
        sources = ["Unable to find matching results."]
        print(">>>>" + response_text, sources)
        return response_text, sources

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    model = ChatOpenAI()
    response_text = model.invoke(prompt)
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    print(response_text, sources)
    return response_text, sources

