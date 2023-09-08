import os

import openai
import streamlit as st
from pymongo import MongoClient
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

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

# if st.session_state["authentication_status"]:
    # st.write(f'Welcome *{st.session_state["name"]}*')
    # st.title('Some content')
if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    st.stop()
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    st.stop()
if os.getenv('MONGO_USER') and os.getenv('MONGO_PASS'):
    client = MongoClient(f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST', 'localhost')}:27017/")
else:
    client = MongoClient(f"mongodb://{os.getenv('MONGO_HOST', 'localhost')}:27017/")
db = client[st.session_state["username"]]
chats = db.list_collection_names()
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

stats_string = """
        <div class='stats'> 
            <p> Tokens {}</p>
            <p> Total Tokens {}</p>
        </div>
        """


def get_history(new_mes):
    messages = [{'role': i['role'], 'content': i['content']} for i in st.session_state.messages[-4:]]
    messages.append({"role": "user", "content": new_mes})
    return messages


def set_chat(name):
    def inner_func():
        print('ok')
        st.session_state['chat'] = name
        st.session_state['collection'] = db[name]
        st.session_state["messages"] = list(st.session_state["collection"].find())
    return inner_func


with st.sidebar:
    st.write(f'Welcome *{st.session_state["username"]}*')
    authenticator.logout('Logout', 'main', key='unique_key')
    version = st.selectbox("Choose ChatGPT version", ("3.5", "4.0"))

    if version == "3.5":
        # Use GPT-3.5 model
        st.session_state['model'] = "gpt-3.5-turbo"
    else:
        # USe GPT-4.0 model
        st.session_state['model'] = "gpt-4"

    for chat in chats:
        button_type = 'primary' if st.session_state.get('chat') == chat else 'secondary'
        st.button(chat, use_container_width=True, on_click=set_chat(chat), type=button_type)


st.title("💬 Chatbot")
if not st.session_state.get('chat'):
    st.write('Create new chat or choose one')
    name = st.text_input('Chat name')
    submit_button = st.button('Create chat')
    if submit_button:
        if name == '':
            st.warning('Please enter chat name')
        elif name in chats:
            st.warning('This name already exists')
        else:
            db.create_collection(name)
            st.session_state['chat'] = name
            st.session_state['collection'] = db[name]
    else:
        st.stop()


st.chat_message('assistant').write('How can I help you?')
if "messages" not in st.session_state:
    st.session_state["messages"] = list(st.session_state["collection"].find())

for msg in st.session_state.messages:
    field = st.chat_message(msg["role"])
    field.write(msg["content"], unsafe_allow_html=True)
    field.write(stats_string.format(msg["tokens"], msg["total_tokens"]), unsafe_allow_html=True)

if prompt := st.chat_input():

    st.chat_message("user").write(prompt)

    field = st.chat_message("assistant")
    mess = field.empty()
    mess.write('<div class="loading">💬</>', unsafe_allow_html=True)

    response = openai.ChatCompletion.create(model=st.session_state['model'], messages=get_history(prompt))
    msg = response.choices[0].message.content
    if st.session_state.get('messages'):
        max_history = min(4, len(st.session_state.messages))
    m = [
        {
            "role": "user",
            "content": prompt,
            'tokens':  response['usage']['prompt_tokens'] if st.session_state.get('messages') == [] else response['usage']['prompt_tokens'] - sum([st.session_state.messages[-i]['tokens'] for i in range(1, max_history+1)]),
            'total_tokens': response['usage']['prompt_tokens'],
            "model": st.session_state.model,
        },
        {
            "role": "assistant",
            "content": msg,
            'tokens': response['usage']['completion_tokens'],
            'total_tokens': response['usage']['total_tokens'],
            'model': st.session_state.model,
        }
    ]
    usage = f"""
        <div class='stats'> 
            <p> Prompt: {response['usage']['prompt_tokens']}</p>
            <p>Response: {response['usage']['completion_tokens']}</p>
        </div>
        """
    st.session_state.messages.extend(m)
    st.session_state.collection.insert_many(m)

    print(st.session_state.messages)

    mess.write(msg)
    field.write(usage, unsafe_allow_html=True)
