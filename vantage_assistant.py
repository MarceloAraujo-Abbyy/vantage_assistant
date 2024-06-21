__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sqlite3
import streamlit as st
import random
import time
import os
from query_data import get_answer

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
    resp = get_message_content(response)
    sour = "Source: " + source[0]
    for word in str(resp).split():
        yield word + " "
        time.sleep(0.05)
    for word in str(sour).split():
        yield word + " "
        time.sleep(0.05)


# Streamed response emulator
def login_vantage(username,password):
    tenant_id = st.secrets["VANTAGE_TENANT_ID"]
    client_id = st.secrets["VANTAGE_CLIENT_ID"]
    client_secret = st.secrets["VANTAGE_CLIENT_SECRET"]
    if username != "" and password != "":
        import requests
        import json
        url = "https://vantage-us.abbyy.com/auth2/"+tenant_id+"/connect/token"
        payload = 'grant_type=password&scope=openid permissions global.wildcard&username='+username+'&password='+password+'&client_id='+client_id+'&client_secret='+client_secret
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", url, headers=headers, data=payload)
        obj = json.loads(response.text)
        if "access_token" in obj:
            accessToken = "Bearer " + str(obj["access_token"])
            st.session_state['token'] = accessToken
            st.session_state['status'] = "🟢 Logged in " + tenant_name
        else:
            st.session_state['token'] = ''
            st.session_state['status'] = "🔴 Error to logging in " + tenant_name

if 'token' not in st.session_state:
    st.session_state['token'] = ''
if 'status' not in st.session_state:
    st.session_state['status'] = "🟠 Disconnected "

st.title("ABBYY Vantage Assistant")
st.write("Author: marcelo.araujo@abbyy.com")

with st.sidebar:
    tenant_name = st.secrets["VANTAGE_TENANT_NAME"]
    st.image("abbyy.png")
    st.title("Vantage Login")
    tenant_name = st.text_input("Tenant", tenant_name ,disabled=True)
    username = st.text_input("Email")
    password = st.text_input("Password",type="password")
    st.button("Login", on_click=login_vantage,args=[username,password])
    status = st.text_input("Status", value=st.session_state['status'], disabled=True)

if  st.session_state["token"] != "":

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

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



