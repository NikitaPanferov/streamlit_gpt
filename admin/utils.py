import os

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from dotenv import load_dotenv
from pymongo import MongoClient
from yaml import SafeLoader

load_dotenv()
admins = os.getenv('ADMINS').split(',')


@st.cache_data
def load_slyles():
    with open('styles.css') as f:
        return f.read()


def setup():
    st.markdown(f'<style>{load_slyles()}</style>', unsafe_allow_html=True)

    if os.getenv('MONGO_USER') and os.getenv('MONGO_PASS'):
        client = MongoClient(
            f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST', 'localhost')}:27017/")
    else:
        client = MongoClient(f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:27017/")

    return client


def auth():
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
    elif st.session_state["username"] not in admins:
        st.error('you don\'t have access')
        st.stop()
    # auth----------------------------------------------------------------
    with st.sidebar:
        st.write(f'Welcome *{st.session_state["username"]}*')
        authenticator.logout('Logout', 'main', key='unique_key')

    def save_creds():
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

    return authenticator, save_creds


def get_stats(client, username=None):

    users = [username] if username else [item for item in client.list_database_names() if item not in ["admin", "config", "local"]]

    dz = {
        'gpt-4': {
            'user': {},
            'assistant': {},
        },
        'gpt-3.5-turbo': {
            'user': {},
            'assistant': {},
        },
    }
    dt = {
        'gpt-4': {
            'user': {},
            'assistant': {},
        },
        'gpt-3.5-turbo': {
            'user': {},
            'assistant': {},
        },
    }
    cz = {
        'gpt-4': {
            'user': {},
            'assistant': {},
        },
        'gpt-3.5-turbo': {
            'user': {},
            'assistant': {},
        },
    }
    ct = {
        'gpt-4': {
            'user': {},
            'assistant': {},
        },
        'gpt-3.5-turbo': {
            'user': {},
            'assistant': {},
        },
    }

    for user in users:
        db = client[user]
        for chat in db.list_collection_names():
            for message in db[chat].find():
                # st.write(message['datetime'].date())
                date = message['datetime'].date()
                tokens = message['total_tokens'] if message['role'] == 'user' else message['tokens']
                hour = message['datetime'].hour

                dz[message['model']][message['role']][date] = dz[message['model']][message['role']].get(date, 0) + 1

                dt[message['model']][message['role']][date] = dt[message['model']][message['role']].get(date,
                                                                                                        0) + tokens

                cz[message['model']][message['role']][hour] = cz[message['model']][message['role']].get(hour, 0) + 1

                ct[message['model']][message['role']][hour] = ct[message['model']][message['role']].get(hour,
                                                                                                        0) + tokens

    st.markdown("<h3 style='text-align: center;'>Кол-во запрос/за день</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write('gpt-4')
        st.dataframe(dz['gpt-4'])

    with col2:
        st.write('gpt-3.5-turbo')
        st.dataframe(dz['gpt-3.5-turbo'])

    st.markdown("<h3 style='text-align: center;'>Кол-во токенов за день</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write('gpt-4')
        st.dataframe(dt['gpt-4'])

    with col2:
        st.write('gpt-3.5-turbo')
        st.dataframe(dt['gpt-3.5-turbo'])

    st.markdown("<h3 style='text-align: center;'>Кол-во запросов и ответов по часам</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write('gpt-4')
        st.dataframe(cz['gpt-4'])

    with col2:
        st.write('gpt-3.5-turbo')
        st.dataframe(cz['gpt-3.5-turbo'])

    st.markdown("<h3 style='text-align: center;'>Кол-во токенов по часам</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write('gpt-4')
        st.dataframe(ct['gpt-4'])

    with col2:
        st.write('gpt-3.5-turbo')
        st.dataframe(ct['gpt-3.5-turbo'])