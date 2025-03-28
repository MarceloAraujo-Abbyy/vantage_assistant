
## comment the above lines if you are running locally and have pysqlite3 installed
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

## uncomment the above lines if you are running locally and have pysqlite3 installed
import sqlite3
import streamlit as st
import random
import time
import os
from query_data import get_answer


###  streamlit run C:\Users\marceloraraujo\Documents\GitHub\vantage_assistant\vantage_assistant.py

# Function to get the content from a BaseMessage object
def get_message_content(message) -> str:
    try:
        return message.content
    except:
        return "Unable to find matching results."


# Function to get the content from a BaseMessage object
def get_message_source(message) -> str:
    try:
        return message.sources[0]
    except:
        return "not found"
    

# Streamed response emulator
def response_generator(prompt):
    response, source = get_answer(prompt)
    print("returned: ", response, source)
    resp = get_message_content(response)
    sour = "Source: " + source[0]
    for word in str(resp).split():
        yield word + " "
        time.sleep(0.05)
    for word in str(sour).split():
        yield word + " "
        time.sleep(0.05)


# Streamed response emulator
def login_vantage():
    print("Login Vantage")
    if username != "" and password != "":
        import requests
        import json
        tenantId = st.secrets["VANTAGE_TENANT_ID"]
        url = base_url+"/auth2/"+tenantId+"/connect/token"
        payload = 'grant_type=password&scope=openid permissions global.wildcard&username='+username+'&password='+password+'&client_id='+client_id+'&client_secret='+secret_id
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)
        obj = json.loads(response.text)
        print(obj)
        if "access_token" in obj:
            accessToken = "Bearer " + str(obj["access_token"])
            st.session_state['token'] = accessToken
            st.markdown("Logged with Success!")
        else:
            st.session_state['token'] = ''
            st.markdown("Error to login! ")

if 'token' not in st.session_state:
    st.session_state['token'] = ''

with st.sidebar:
    tenant = st.secrets["VANTAGE_TENANT_ID"]
    tenant_name = st.secrets["VANTAGE_TENANT_NAME"]
    client_id = st.secrets["VANTAGE_CLIENT_ID"]
    secret_id = st.secrets["VANTAGE_CLIENT_SECRET"]
    base_url = st.secrets["VANTAGE_BASE_URL"]
    st.image("abbyy.png")
    st.title("Vantage Login")
    tenant = st.text_input("Tenant", tenant_name ,disabled=True)
    username = st.text_input("Email")
    password = st.text_input("Password",type="password")
    st.button("Login", on_click=login_vantage())

if  st.session_state["token"] != "":

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("ABBYY Vantage Assistant")
    st.write("Author: marcelo.araujo@abbyy.com")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Hi! How can I help you today?"):

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})



