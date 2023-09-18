import streamlit as st

from utils import auth, setup

client = setup()
# auth----------------------------------------------------------------
auth()

def set_chat(name):
    def inner_func():
        st.session_state['chat'] = name
        st.session_state['collection'] = db[name]
        st.session_state["messages"] = list(st.session_state["collection"].find())
    return inner_func

with st.sidebar:
    select = st.selectbox('Выберите пользователя', [item for item in client.list_database_names() if item not in ["admin", "config", "local"]])

    st.session_state['user_mes'] = select

    db = client[select]
    chats = db.list_collection_names()
    for chat in chats:
        button_type = 'primary' if st.session_state.get('chat') == chat else 'secondary'
        st.button(chat, use_container_width=True, on_click=set_chat(chat), type=button_type)

stats_string = """
        <div class='stats'> 
            <p> Tokens {}</p>
            <p> Total Tokens {}</p>
            <p> GPT version {}</p>
        </div>
        """
if not st.session_state.get('chat'):
    st.header("Выберите чат")
    st.stop()
for msg in st.session_state.messages:
    field = st.chat_message(msg["role"])
    field.write(msg["content"], unsafe_allow_html=True)
    field.write(stats_string.format(msg["tokens"], msg["total_tokens"], msg["model"]), unsafe_allow_html=True)
