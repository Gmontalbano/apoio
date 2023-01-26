import streamlit as st
import sqlite3
import hashlib
from controle import main_controle
from sol import solicitar_item, devolver_item
import pandas as pd

st.set_page_config(page_title='Pioneiros da colina', page_icon='🐆')

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


def add_userdata(username, password,permission):
    c.execute('INSERT INTO userstable(username,password,permission) VALUES (?,?,?)', (username, password,permission))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    c.execute('SELECT permission FROM userstable WHERE username =? AND password = ?', (username, password))
    permission = c.fetchall()
    return data, permission[0][0]



def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    """Simple Login App"""

    st.title("Solicitação de materiais Pioneiros da colina")

    st.subheader("Login Section")
    st.subheader("Create New Account")

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.checkbox("Login"):  # trocar para button e redirect
        # if password == '12345':
        create_usertable()
        hashed_pswd = make_hashes(password)

        result, permission = login_user(username, check_hashes(password, hashed_pswd))
        if result:
            st.session_state.load_state = True
            st.success("Logged In as {}".format(username))

            if permission == 'admin':
                menu = ["Solicitação de material", "Estoque", "Create"]
            elif permission == 'user':
                menu = ["Solicitação de material"]
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
            elif choice == "Create":
                st.subheader("Create New Account")
                new_user = st.text_input("Username", key="new_user")
                new_password = st.text_input("Password", type='password', key="new_pass")
                type_permission = ['admin', 'user']
                perm = st.selectbox("Permissão", type_permission)
                if st.button("Adicionar user"):
                    add_userdata(new_user, make_hashes(new_password), perm)
                    st.success("You have successfully created a valid Account")
                    st.info("Go to Login Menu to login")
                st.subheader("User Profiles")
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result)
                st.dataframe(clean_db)
        else:
            st.warning("Incorrect Username/Password")


if __name__ == '__main__':
    main()
