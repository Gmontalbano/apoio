import streamlit as st
from PIL import Image
from controle import main_controle
from classes import make_class
from sol import solicitar_item, sol_externa, externa_manage

from user_managements import users_manage
from hashes import make_hashes, check_hashes
from cal import show_cal, cal_m
from sqlalchemy import create_engine
from sqlalchemy import and_
import sqlalchemy as db
from configparser import ConfigParser

st.set_page_config(page_title='Pioneiros da colina')

if "load_state" not in st.session_state:
    st.session_state.load_state = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = 0
if "sub_data" not in st.session_state:
    st.session_state.sub_data = False
if "pedido_data" not in st.session_state:
    st.session_state.pedido_data = {}
if "has_pedido_data" not in st.session_state:
    st.session_state.has_pedido_data = False
if "pedido_user" not in st.session_state:
    st.session_state.pedido_user = {}
if "has_pedido_user" not in st.session_state:
    st.session_state.has_pedido_user = False
if "pedido_c" not in st.session_state:
    st.session_state.pedido_c = {}
if "loggin" not in st.session_state:
    st.session_state.loggin = False

key = ".env"
parser = ConfigParser()
_ = parser.read(key)
db_url = parser.get('postgres', 'db_url')
engine = create_engine(db_url)
metadata = db.MetaData()
conn = engine.connect()
users = db.Table('users_table', metadata, autoload_with=engine)


def login_user(username, password):
    data = db.select(users).where(and_(users.columns.username == username, users.columns.password == password))
    conn = engine.connect()
    ResultProxy = conn.execute(data)
    q_result = ResultProxy.fetchall()
    query = db.select(users.columns.permission).where(
        and_(users.columns.username == username, users.columns.password == password))
    ResultProxy = conn.execute(query)
    permission = ResultProxy.fetchall()
    query = db.select(users.columns.user_id).where(
        and_(users.columns.username == username, users.columns.password == password))
    ResultProxy = conn.execute(query)
    user_id = ResultProxy.fetchall()
    if q_result:
        st.session_state.user_id = user_id[0][0]
        r = True
        return r, permission[0][0]
    else:
        r = False
        return r, 0


def main():
    img, title_text = st.columns([1, 2])
    image = Image.open('imgs/pc_logo.jpg')
    img.image(image, caption='Mais que um clube, uma familia')
    title_text.title("Pioneiros da colina")

    st.sidebar.title("Login section")

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.button("Login") or st.session_state.loggin:
        st.session_state.loggin = True
        hashed_pswd = make_hashes(password)
        result, permission = login_user(username, check_hashes(password, hashed_pswd))

        if result:
            st.session_state.username = username
            st.session_state.load_state = True

            type_permission = {
                'admin': ["Solicitação de material", "Estoque", "Usuarios", "Classes", "Calendário", "Externa"],
                'user': ["Solicitação de material"],
                'apoio': ["Solicitação de material", "Estoque"],
                'secretaria': ['Classes']}
            menu = type_permission[permission]

            choice = st.sidebar.selectbox("Selecione uma opção", menu)

            if choice == "Solicitação de material":
                solicitar_item()
            elif choice == "Estoque":
                main_controle()
            elif choice == "Usuarios":
                users_manage()
            elif choice == 'Classes':
                make_class()
            elif choice == "Calendário":
                cal_m()
            elif choice == "Externa":
                externa_manage()
        else:
            st.sidebar.error("Incorrect Username/Password")
    else:
        tab1, tab2, tab3 = st.tabs(["Nosso clube", "Calendário", "Solicitação externa"])
        with tab2:
            show_cal()
        with tab3:
            sol_externa()


if __name__ == '__main__':
    main()
