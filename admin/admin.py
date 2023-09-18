import streamlit as st

from utils import auth, get_stats, setup

client = setup()
# auth----------------------------------------------------------------
auth, _ = auth()


with st.sidebar:
    select = st.selectbox("Выбери пользователя для статистики", ('Все пользователи', *[item for item in client.list_database_names() if item not in ["admin", "config", "local"]]))
    if select == 'Все пользователи':
        st.session_state['stat_user'] = None
    else:
        st.session_state['stat_user'] = select

get_stats(client, st.session_state['stat_user'])
