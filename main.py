import time
from datetime import date
import streamlit as st
import sqlite3
import hashlib
from controle import main_controle
from sol import solicitar_item, devolver_item
import pandas as pd
from PIL import Image
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


st.set_page_config(page_title='Pioneiros da colina')

if "load_state" not in st.session_state:
    st.session_state.load_state = False


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


conn = sqlite3.connect('data.db')
c = conn.cursor()


# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password,email,permission):
    c.execute('INSERT INTO userstable(username,password,email,permission) VALUES (?,?,?,?)', (username, password, email, permission))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    c.execute('SELECT permission FROM userstable WHERE username =? AND password = ?', (username, password))
    permission = c.fetchall()
    return data, permission[0][0]


def view_all_users():
    df = pd.read_sql('select username, email, permission from userstable', conn)
    return df


def main():
    """Simple Login App"""
    img, title_text = st.columns([1,2])
    image = Image.open('imgs/pc_logo.jpg')
    img.image(image, caption='Mais que um clube, uma familia')
    title_text.title("Pioneiros da colina")

    st.sidebar.title("Login section")

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.checkbox("Login"):  # trocar para button e redirect
        hashed_pswd = make_hashes(password)
        result, permission = login_user(username, check_hashes(password, hashed_pswd))

        if result:
            st.session_state.load_state = True
            st.success("Logged In as {}".format(username))

            if permission == 'admin':
                menu = ["Solicitação de material", "Estoque", "Create user"]
            elif permission == 'user':
                menu = ["Solicitação de material"]
            elif permission == 'apoio':
                menu = ["Solicitação de material", "Estoque"]

            choice = st.sidebar.selectbox("Selecione uma opção", menu)
            if choice == "Solicitação de material":
                menu2 = ["Solicitar", "Devolver"]
                choice2 = st.sidebar.selectbox("Selecione", menu2)
                if choice2 == "Solicitar":
                    solicitar_item()
                elif choice2 == "Devolver":
                    devolver_item()

            elif choice == "Estoque":
                main_controle()
            elif choice == "Create user":
                st.subheader("Create New Account")
                new_user = st.text_input("Username", key="new_user")
                new_email = st.text_input("Email", key="new_email")
                new_password = st.text_input("Password", type='password', key="new_pass")
                type_permission = ['admin', 'user', 'apoio']
                perm = st.selectbox("Permissão", type_permission)
                if st.button("Adicionar user"):
                    add_userdata(new_user, make_hashes(new_password),new_email, perm)
                    st.success("You have successfully created a valid Account")
                st.subheader("User Profiles")
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result)
                st.dataframe(clean_db)
        else:
            st.warning("Incorrect Username/Password")
    else:
        tab1, tab2, tab3 = st.tabs(["Nosso clube", "Inscrição de membros", "Solicitação externa"])
        tab3.subheader("Solicitação de empréstimo de material")
        tab3.markdown("O empréstimo é feito exclusivamente para departamentos interndo do UNASP-SP")
        tab3.text_input("Nome", key="requester_name")
        tab3.text_input("Email", key="requester_email")
        tab3.text_input("Telefone", key="requester_tel")
        tab3.text_input("CPF", key="requester_cpf")
        tab3.text_input("Departamento", key="requester_departament")
        meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
        coleta, devo = tab3.columns(2)
        coleta.subheader("Dia para coletar o material")
        dia = coleta.selectbox("Dia", range(1,32), key='cd')
        mes = coleta.selectbox("Mes", meses, key='cm')
        devo.subheader("Devolução o material")
        diad = devo.selectbox("Dia", range(1, 32), key='dd')
        mesd = devo.selectbox("Mes", meses, key='dm')


if __name__ == '__main__':
    main()
