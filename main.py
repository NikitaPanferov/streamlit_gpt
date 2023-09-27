import os
from datetime import datetime

import openai
import streamlit as st
from openai import InvalidRequestError
from pymongo import MongoClient
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

st.set_page_config(page_title='Open GPT', page_icon='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAYFBMVEV0qpz///+Ds6ZppJVvp5lopJV/sKRxqZp5raDX5eHA19GRu6/x9/Vtppfk7uv0+Pety8PV5OCjxbyZv7W71M3K3difw7ne6ufq8vCyzsfy9/aLt6u/1tCUvLLH29avzcX7cXLbAAARjklEQVR4nN1d6briKBCNASTqJWrc9/d/y0miV1mqoCDYV+d8Mz9mOh05AWqnKEYxqCfTW3M5leX4L1CWp1lzmC73UWMuqA/uN03JmeKcy6Io5F+g/d2Cc6UYHzebn7wMd4tKqP4XPgRciaqZ5GJYLwrG/5oSAM5ks8vA8DoWn0ivh5Si3AxkOC3UX9MIgBXTAQyvH8+vg/Jz9DCcVOyvB0+EqjxCB2U4v4i/HngExGoey3DDPkk5hCHZNY7h9lsW6AtsG8FwX32DhLGhKtCcgxhuvm8C72BLGsPDN4kYE+JAYdh86wx2YIsww68m2FJsQgy/nCBA0WJ4+3aC7kI1Ga6/V8i8wNY4w83/gWArUZcYw/33L9E72B5h+NcDy4cKZrj6WF8+GmoLMfxaWw0C2wAMPyqWNhhs7jD8H63RDvJiM5y8V1HI4l+vEDaxGFbv+R3ZhagZ6+LVXAmm1L9bKZXJ8PoGMdOyY8XlsNnt73tiPq+Xh23F/lF8hE0Nhvl/QDK5ApML82VTMP4vWOoMz7mjFlxtfVmF3YK/P06iphrD3O8u1mhw7xfXfxCNfTHMquylqrDAnoll+WaOd7XfMywz7gouA3kEDZv3Zg3k6ZdhnVEXYlFLBO8NKYj9g+Eim5LinJa1fGFXvFFD8sWDYbY3slNQwLhYvXMa7wx3uX4CilYScH6fwch2PcNMi1SyYDoWwfJts9gt0yKbScrgnHo9bU7dL1TjU7NewhUU2VaRg6pj+JNnkagaGPrmopjqLDTZ/6uUKMAKilr1dSTsAZXNVxXHluEmi04S7gzuFxyo4Wjt1YM7k7WqLrfpsq73+7rebdZNKRnPsHvUpmXY5PhewtmD+xVaw6HEllDWVE9Xw90Q3rQMxwNf0sEKwrYOROOtUZFiS9Iru0YOXGFlyzDDWuAXa2Sb4MA4J0rezXhQuRIfFTnCwJU1qq0grC5Bte92M8rrELB9MRnO0JIy8zFpZXFBc0E6jmXyhmST4jp4lSoz2bMnyUAumhgL75oaFODX4jB8H5oESRPITnFFoqP5JW2t8UMxWFmY5QFHyutUBZUUBDBNoiibYmgkmJ+McVTh13Fu6xYa6hRHi6+KWQIrHaY5egmuUaoqBDAvE5TjrDil0NIGbExheCWxE2S/9thv1ovmctk2h+sO+QizeIqnokwi9hqxvqOOIYKqQPT8fj2TXRG5bP+RXZi8XIDRglU0xXIoQ0PZz/wbRSrYRZ6vK+GE+zkTDTDd4W1gYShDpQsNf3ZHIhWS8wZLZnB2cifyFCn7BzLkQneEvK9iJewhL3wmOhelM4+RDvsQhq1zOzOm0LMLObIBryETXTp1XJGGdDJDKcY3a1LwXcjZDeS3o0S91dgyf+JqYtIYSq5cKYBHQ9gFDM8ciXFEJ8S1jdH8SQy5hBIva2S9sTG8AQ90f0FYRtCbGSpE5sMvUhz2keJSFlYkNib8GM8Q83p+oF/lwq337FCfIs1oaxYDildHLENeYUYXFLITF9BHmjfxTrsZ6trThU0kQ2RKOriRc+ycxzopTCiMT9uQXxHHUHjcOtvWkArOIy5TzwEY9iG4J0DEMOSFzy+3PqqCTbT9LDkspIzI1Za6ziMYyrHXrzN3hnLKrXt4TDQerLUxAl419UvRGfLSx8/R99AzV7wAQ/LVer0NcBzrL6OOm8xQQgS1zW9ai5DK3I1RFf/r9wci5YZtMyVuZypDOXaHPC00//5ozKFyRNLRcxSOvRyIvV9Rai+cE5cplaE62kM+SyVnr/80Vymz9YTHROPSUHVLj7FjBBSIjiKRobBHvOtkPqcy3Eh08UnmLGhcXxpxvTNNJdIYOqNY9HyIDGuPjyRWzuJoFyCa99AdbqI0JTHUmXQ4PhITJIb4cHG3A7VbuW5FkAjSGApTEda/Qp3CcI9LR8zt6LEBw7/Gt6aZ3xSGzDS/XsEKCkN0LWFuxxM3SDgp/YFsDE1NuHstuiEMGex26PgBkjFMU8G0AgQCQzM7qGv2dIbe4+Xa1xzbf1tpC5tWoxJmaIqZOfZHMQwV4HbMabE4ri1tWtAtzJAZftlM3xtpDMHc6JQLUjyVr7SPkmeVmpmXtTHeJIZQbnRSdVJFXADdaDlcxnDyMDQMpblpWyYwVIXrRD8likTCqhPNadbt4zwMDc/6YsrvaIZcAbnRm7YMeQGryJchp4+HZJiGGBpukF1LHMkQzI3aUUUkvfG0jHSGWfShcVbxZL0yjiGUG4XC+mIFRsgfhlz2Vaq/0CkHj2EI5UaRsD7gbvTopju7pDEWqRP8oTOUUPnwDTXJsUzVQShdW+TQh7oydNUPmSG88HxxN+bmDTscL7k1vm7oumYgkSHqI3VqIBS6saH9T1q9mp+hseovjugiMRSIArjjjMe/uZ1xsjHNIEt1KxCQzSSGcOD0CV94LVA6Ravm8jPULXnAhCbHabzwhdc81TfUiKmfoV7vdHVlcwrDGjC7PakMzvASxhxxGqaJQOBURjzD1jRRkOW2xuuAOZLhIQqa0CrVvp8raOIZrvsID7S95ls8oIq4y8SDMAGG2guB5yIZvhajmLkelDfmCIU8SPyCslR7IVCoE8XQ0O+gFwyH1x7Pu2Er20pOYmi0BXFXUQxDO6+moIOYBzy0qtza/iqDtjCcsSEMgbyaZJVr6vysPOHj0goBHIdb3lKfwwGrFCt9gsxVz3bkyprGJaVegS5pgKM1NIbtvGDvB10OTxrHfrwhzCKdIZDMIjH0lz6BftIN1Y52Iy/CTgxofE3gAaUBRMvbD+YyHP2g6VTdPxyRiqMCDDU1BJStDcpbPAEwhKLdD1glEOHsTIChZnwAn+uNDLs8PbzJTJ8qXBwV2Ifa24Aq9bcybP0qeDua+ehgXU3AptFXvasudIbH7AxRv0rq5lAwlBGwaXSV71q6RtLG0AlJDIFDFqBfJY3TjoBHEMNQaGaEm8wy01K6cEhieBZndx7XgLIx1mnIiQpFonRt5S5Tq4rolQpLYtjKFsivAoKqRqohULsfYCj1arm1sx6Eva4WD+GQxrD9u2zmGnJr5xVGcdTBb9iEYt66/zR3JDN3wkz7mRjEEPST3ON1+iQGZE0wb6Evm4XztYAm2n0qLJ1h51fZL3XfYQzLv0yDc6jrCyDpCsVtp4oPYQjkn1wZp4tTfzgjmD80thpkuTlH8fsY6CCGXdjC2I7uLOnD8hunQYZmZAxaEJAArJ9hzjSGVjrY/VldyLvyIYqh1GUNMl4osDSQYftSL0O+9f5xDMNCGWrYldz97wFttN/L0DD2vGZNmKE5idiZI6hE5q0M9WC1VyMSaqKUWSCBBfGQHNrbGGqWG5BweIFUuWfushINMUBH1OrA8Rj5YhLFUK/D9JqmFIbWifsRemYcPGY49XZI1CP2cQy1n/KuE1J9qVV+6ek/BtUjeDKE3HhzFEPdYvbabbQqaGFpA1ii9oC2I5KwtzNncXOoWTXeQ/LESna7AU3taVwJHdmGPFkn+xnHUPNNvUUZRIZOE6HO+MQeBuO8a+t5wBL6U4bAzRjeBHxoO0LWbCRDzSXwHmQjn5lZOQPyHgSFEvDP5yV8DjVO0miuaQZJY4UznvCcbwET8PcyPaz8IIqhXq01XFsUQLziAShQ9MsRTtgzrPlHJEPtLcuhNk3/HDIqMFD0HAXgVx2BeFoKQ/3QrPd8EJGh9NT9+Boj+PyqYQz1tJj3UDCRofI2HvNcIhg8N3J8Sf0YhkY9mvcUG5Eh0rnzCc/pVzBh/8RBpVneRqspr21PZajFvkGZg2f8POe3uuoL+VpuMQx1O9LvoFFXqfZzM3hPohm/Aus8cNePaQx1yec/iJhgl44xfx4/yIzYOP3qSmJoyAV/lpTIUP9kHF93CzDjByvGXzs1jaH+qYZF9R9j1JNM/YZDz7c42xEs9tV8jRSGRmAlcISNyFB3Le4csPMttp8EmWiGv5jAUHL9mwVS+ckM8YL6s+Yngf3ZTNWSwJDr3lmo0XPqKu2BFNQ/E/Bgf7arVYGQMof6+wLJtRRJo+lXrKC+1wMSKupyGyvEMzRLFYJDT9AW+h+Aruyo245ApzXQLohmaDaEDd6ukqLxg+GIO0f3fwXOLtMYWg06gnVfVKtNW4xOus5bUP8CUpEXyVAWxr4Id9ClMvQeofYV1P8CraqMnUNjb8/DdcLUVaoJfSgqwhXu2HY44o0VXpV7BIacm8JrFS5OpEYTdfUODxR1IEb+WMdL9IcZKqvNEaWElurj6w4nchqHQU08+nH4HGTt0wUZMjvgRxk6OdamvRdL9UgBGXLemKNh3QYYuh3OZ5RSdnJEWF+D6FPuQWWswLB/p1XK7mfonnI/ZOo48Bi7rmaxHpCFsx3PvuiG/TU8DCUrHf1KqmOP6fWlT4zv42k9dSaeE1tAhMr8cDpDdQLKPTL3iTKXqVscpeE3MQP4iq/hQ1HGLTqHwMN7altBejczvbxjDhwv0cCL5rye4RsQPqpl+upSAo8kEIxYpbrhNjr7l0jXktvTWggO81j2rrcBXk3vvRjRc89wIpLvosMsvB+r3ToHkl1PxNz1F9MZ0lgliVcoCeTWh4O9ppFGtz0WMT8ewdCMISZdUo55WoDbAafzOvzE3R8Q0/tSGT+0iG7TiR0/B90OhqV0POl1EDGr1LptJbKJP5L4xfq52bURD+yj772M6kFrNlSKa+KPuclruKuCW1/d4Yd0CZGJKIZ2A8wt+Xtitz6gbgd0kPgnocFybB9hW8AdaOJGIuEqj9vh6vvlJe1mq8he0HYecUJo6yzFFmyp4y1XMT/lfLlVqTd3RXcst4cZ7I2PhI2dEiIDeiOA0a0ccltgLEN5skd670SGDhXbgN6e14acIXpJGKLnULm3pS1PCEfOkLuPA710TRt44HVN8X31oZLu3Uo420QqMUOar3j8/h7GLqT2C8aQcDcCnFZbLkrF1P22H6WYqJolEkOdBmWGoe1DmZcQyoT7nuwD1U/U3YVNTbM4TCdohHjiSfc/YDbbHHrPfJlyZ5cT1SPD5/c/324oT2rbbhRl0r1rqky7WAzO81vvNj9fAicTZdrdeZwnXH7naTqvvdlUR7fBF92WqfcfikCHKwe+epsXLNOXfskDirKg9QRzEXeH4RFvjmG81IrORNy2gqEccA8pMW/YwdN4xnijJcKuw6ewZTjgLlkuVkSOc9LNOXYMIMc1ty3DQfcBc9RuseHp5vWAci7pyXIlestw2OV5re25CJRm3vHjv9WXu4mr+LsOIbQM6dfuYINjcnt1A0eOytxhFnrfGctJPt5yrNGeYY671aVixWkxXe7qel/vltd1cyqUS3rXQI6sZHzh+sjTPJfadwxDZVNESPm84F61HmuX2YBywsutFL8hf9laDqqz0YHnchHsGObZ0CDA6MVovzlcqqoqeFHNbhs4LnrORbBnSGzPlwDpVSYe2/aWjWDPMMPd4xgE8Yp4C+nXXrnoGA6333GEDiNA2BPuhaajZzhYX3jg3LEZRDYZc0fPMNhxbAgkVOXtmcDYmxFD6BkONGtCiPBCApd2peDOMCanmgLo5mKI34HiI0fizvCdsqaHZGVQqu4blp/fk2Gw0nYwJCtuHu0435xSExMBPBgOcqGo4GK8AMOM9XTGIjO7dPwyHBy0o4EzVm3Xy93P/TLAeT25Lk6cJV1MSsQvwzcapzZkFxLvkkmcidZKHxrxDeHJMOYS4Sx4M7EnngztO2T+N3gx9Hdb+l68GGYJ3X0gNIZDU5EfCp3h2y2bP4HBkHyL8DfBYPh2C/wvYDJMKMf7eFgMSV3Ovws2w7hyvG+AwzBTtuBz4DKMqDj8CgAM48qoPx4Qw9H1/0QRZDja/TPf5v2AGeaNq/8tMIajafbA5R8BZTg65g4+/xFwht7TrV8EH8OuUvn7OfoZjuaLr+cYYNhyPHvruD8fQYYtdulHAT4AFIZdVqEj+Z0saQw71OdLJZhS+I1anwk6ww7H3Wa9WJ3Kf5cCGI7yP5WM0CefOInHAAAAAElFTkSuQmCC')

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


def get_history(new_mes, count=4):
    messages = [{'role': i['role'], 'content': i['content']} for i in st.session_state.messages[-count:]]
    messages.append({"role": "user", "content": new_mes})
    return messages


def set_chat(name):
    def inner_func():
        st.session_state['chat'] = name
        st.session_state['collection'] = db[name]
        st.session_state["messages"] = list(st.session_state["collection"].find())
    return inner_func


def ask_gpt(model):
    for i in range(4):
        try:
            return openai.ChatCompletion.create(model=model, messages=get_history(prompt, 4-i))
        except InvalidRequestError:
            pass


with st.sidebar:
    st.write(f'Welcome *{st.session_state["username"]}*')
    authenticator.logout('Logout', 'main', key='unique_key')
    if st.button('New Chat'):
        st.session_state['chat'] = None
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

if prompt := st.chat_input():

    st.chat_message("user").write(prompt)

    field = st.chat_message("assistant")
    mess = field.empty()
    mess.write('<div class="loading">💬</>', unsafe_allow_html=True)
    response = ask_gpt(model=st.session_state['model'])
    if not response:
        mess.error('Please reduce the length of the messages' + '' if st.session_state['model'] == 'gpt-4' else ' or change model to gpt-4')
        st.stop()

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
            "datetime": datetime.now(),
        },
        {
            "role": "assistant",
            "content": msg,
            'tokens': response['usage']['completion_tokens'],
            'total_tokens': response['usage']['total_tokens'],
            'model': st.session_state.model,
            "datetime": datetime.now(),
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

    mess.write(msg)
