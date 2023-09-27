import streamlit as st

from utils import auth, get_stats, setup, get_excel

client = setup()
# auth----------------------------------------------------------------
auth, _ = auth()


users = [item for item in client.list_database_names() if item not in ["admin", "config", "local"]]
with st.sidebar:
    select = st.selectbox("Выбери пользователя для статистики", ('Все пользователи', *users))
    if select == 'Все пользователи':
        st.session_state['stat_user'] = None
    else:
        st.session_state['stat_user'] = select

    if st.button('Prepare excel'):
        data = {i if i else 'All': get_stats(client, i) for i in [None, *users]}
        st.download_button(label='Download excel file',
                           data=get_excel(data),
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                           file_name='OpenGPT stats.xlsx')

dz, dt, cz, ct = get_stats(client, st.session_state['stat_user'])

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

# with st.sidebar:
#     b = st.button('click', on_click=download_excel(dz, dt, cz, ct, 'test.xlsx'))
    #application/vnd.openxmlformats-officedocument.spreadsheetml.sheet


