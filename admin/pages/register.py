import streamlit as st

from utils import auth, setup

client = setup()
# auth----------------------------------------------------------------
auth, save_creds = auth()

try:
    if auth.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
        save_creds()
except Exception as e:
    st.error(e)