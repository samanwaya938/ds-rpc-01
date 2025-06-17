# frontend/app.py

import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

# Session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "login_time" not in st.session_state:
    st.session_state.login_time = ""
if "chat_history" not in st.session_state:          
    st.session_state.chat_history = []
if "current_input" not in st.session_state:         
    st.session_state.current_input = ""

def login_ui():
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Select Role", ["engineering", "finance", "hr", "marketing", "general"])

    if st.button("Login"):
        response = requests.post(f"{API_URL}/login", json={
            "username": username,
            "password": password,
            "role": role
        })

        if response.status_code == 200:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials or role mismatch.")

def chat_ui():
    st.title(f"💬 Chatbot - Role: {st.session_state.role}")

    # Sidebar info
    st.sidebar.success(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
    st.sidebar.info(f"Login time: {st.session_state.login_time}")
    
    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.login_time = ""
        st.session_state.chat_history = []
        st.session_state.current_input = ""
        st.rerun()

    # Display history
    for message in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(message["query"])
        with st.chat_message("assistant"):
            st.markdown(message["response"])

    # Controlled input box
    if "current_input" not in st.session_state:
        st.session_state.current_input = ""

    query = st.chat_input("Ask a question:", key="chat_input")

    if query:
        res = requests.post(f"{API_URL}/chat", json={
            "query": query,
            "role": st.session_state.role,
            "username": st.session_state.username
        })

        if res.status_code == 200:
            response = res.json()["response"]

            # Append to chat history
            st.session_state.chat_history.append({
                "query": query,
                "response": response
            })

            # Clear input and rerun for updated layout
            st.session_state.current_input = ""
            st.rerun()
        else:
            st.error(f"Error: {res.text}")


if not st.session_state.authenticated:
    login_ui()
else:
    chat_ui()
