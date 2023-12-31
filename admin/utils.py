import os
import uuid

import pandas
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
    st.set_page_config(page_title='Open GPT Admin',
                       page_icon='data:image/png;base64,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')
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

    return dz, dt, cz, ct


def get_excel(data: dict):
    file_name = f"{uuid.uuid4().hex}.xlsx"
    with pandas.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        for name, df in data.items():
            pandas.DataFrame(df[0]['gpt-3.5-turbo']).to_excel(writer, sheet_name=name, startrow=2)
            pandas.DataFrame(df[0]['gpt-4']).to_excel(writer, sheet_name=name, startcol=3, startrow=2)
            pandas.DataFrame(df[1]['gpt-3.5-turbo']).to_excel(writer, sheet_name=name, startcol=7, startrow=2)
            pandas.DataFrame(df[1]['gpt-4']).to_excel(writer, sheet_name=name, startcol=10, startrow=2)
            pandas.DataFrame(df[2]['gpt-3.5-turbo']).to_excel(writer, sheet_name=name, startcol=14, startrow=2)
            pandas.DataFrame(df[2]['gpt-4']).to_excel(writer, sheet_name=name, startcol=17, startrow=2)
            pandas.DataFrame(df[3]['gpt-3.5-turbo']).to_excel(writer, sheet_name=name, startcol=21, startrow=2)
            pandas.DataFrame(df[3]['gpt-4']).to_excel(writer, sheet_name=name, startcol=24, startrow=2)
            sheet = writer.sheets[name]
            sheet.merge_range('A1:F1', 'Кол-во запрос/за день')
            sheet.merge_range('A2:C2', 'gpt-3.5-turbo')
            sheet.merge_range('D2:F2', 'gpt-4')

            sheet.merge_range('H1:M1', 'Кол-во токенов за день')
            sheet.merge_range('H2:J2', 'gpt-3.5-turbo')
            sheet.merge_range('K2:M2', 'gpt-4')

            sheet.merge_range('O1:T1', 'Кол-во запросов и ответов по часам')
            sheet.merge_range('O2:Q2', 'gpt-3.5-turbo')
            sheet.merge_range('R2:T2', 'gpt-4')

            sheet.merge_range('V1:AA1', 'Кол-во токенов по часам')
            sheet.merge_range('V2:X2', 'gpt-3.5-turbo')
            sheet.merge_range('Y2:AA2', 'gpt-4')

    with open(file_name, 'rb') as file:
        out = file.read()

    os.remove(file_name)
    return out
