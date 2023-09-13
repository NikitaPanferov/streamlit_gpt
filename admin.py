import os

import openai
import streamlit as st
from pymongo import MongoClient
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv

load_dotenv()

# styles ----------------------------------------------------------------
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# styles ----------------------------------------------------------------

# auth----------------------------------------------------------------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
authenticator.login('Login', 'main')
# auth----------------------------------------------------------------

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    st.stop()
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    st.stop()
# auth----------------------------------------------------------------


if os.getenv('MONGO_USER') and os.getenv('MONGO_PASS'):
    client = MongoClient(f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST', 'localhost')}:27017/")
else:
    client = MongoClient(f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:27017/")

db = client[st.session_state["username"]]
chats = db.list_collection_names()


with st.sidebar:
    st.write(f'Welcome *{st.session_state["username"]}*')
    authenticator.logout('Logout', 'main', key='unique_key')

users = [item for item in client.list_database_names() if item not in ["admin", "config", "local"]]

for user in users:
    db = client[user]
    st.write(user)
    for chat in db.list_collection_names():
        pass
