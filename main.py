import streamlit as st
import sqlite3
import hashlib
from controle import main_controle
from sol import solicitar_item, devolver_item

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


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


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

        result = login_user(username, check_hashes(password, hashed_pswd))
        if result:
            st.session_state.load_state = True
            st.success("Logged In as {}".format(username))
            menu = ["Solicitação de material", "Estoque"]
            choice = st.sidebar.selectbox("Selecione uma opção", menu)
            if choice == "Solicitação de material":
                menu2 = ["Solicitar", "Devolver"]
                choice2 = st.sidebar.selectbox("Selecione", menu2)
                if choice2 == "Solicitar":
                    solicitar_item()
                elif choice2 == "Devolver":
                    devolver_item()

            elif choice =="Estoque":
                main_controle()
        else:
            st.warning("Incorrect Username/Password")


if __name__ == '__main__':
    main()
