import streamlit as st
import sqlite3
import hashlib
from controle import main_controle
from classes import make_class
from sol import solicitar_item
import pandas as pd
from PIL import Image
from send_email import send, send_client

st.set_page_config(page_title='Pioneiros da colina')

if "load_state" not in st.session_state:
    st.session_state.load_state = False
if "username" not in st.session_state:
    st.session_state.username = ""
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
            st.session_state.username = username
            st.session_state.load_state = True
            # st.success("Logged In as {}".format(username))

            if permission == 'admin':
                menu = ["Solicitação de material", "Estoque", "Usuarios", "Classes"]
            elif permission == 'user':
                menu = ["Solicitação de material"]
            elif permission == 'apoio':
                menu = ["Solicitação de material", "Estoque"]
            elif permission == 'secretaria':
                menu = ['Classes']

            choice = st.sidebar.selectbox("Selecione uma opção", menu)
            if choice == "Solicitação de material":
                solicitar_item()


            elif choice == "Estoque":
                main_controle()
            elif choice == "Usuarios":
                st.subheader("Create New Account")
                new_user = st.text_input("Username", key="new_user")
                new_email = st.text_input("Email", key="new_email")
                new_password = st.text_input("Password", type='password', key="new_pass")
                type_permission = ['admin', 'user', 'apoio', 'secretaria']
                perm = st.selectbox("Permissão", type_permission)
                if st.button("Adicionar user"):
                    add_userdata(new_user, make_hashes(new_password),new_email, perm)
                    st.success("You have successfully created a valid Account")
                st.subheader("Users Profiles")
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result)
                st.dataframe(clean_db)
            elif choice == 'Classes':
                make_class()

        else:
            st.warning("Incorrect Username/Password")
    else:
        tab1, tab2, tab3 = st.tabs(["Nosso clube", "Inscrição de membros", "Solicitação externa"])
        tab3.subheader("Solicitação de empréstimo de material")
        tab3.markdown("O empréstimo é feito exclusivamente para departamentos interndo do UNASP-SP")
        nome = tab3.text_input("Nome", key="requester_name")
        email = tab3.text_input("Email", key="requester_email")
        telefone = tab3.text_input("Telefone", key="requester_tel")
        # tab3.text_input("CPF", key="requester_cpf")
        dep = tab3.text_input("Departamento", key="requester_departament")
        meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
        coleta, devo = tab3.columns(2)
        coleta.subheader("Dia para coletar o material")
        dia = coleta.selectbox("Dia", range(1,32), key='cd')
        mes = coleta.selectbox("Mes", meses, key='cm')
        devo.subheader("Devolução o material")
        diad = devo.selectbox("Dia", range(1, 32), key='dd')
        mesd = devo.selectbox("Mes", meses, key='dm')
        if tab3.button("Solcitar material"):
            with st.spinner(text="Fazendo solicitação..."):
                text = f"{nome} do departamento {dep} solcitou material \n Coleta: {dia}/{mes} \n Devolução: {diad}/{mesd} \n {email} |  {telefone}"
                send(text)
                text = f"Olá, {nome}.\n" \
                       f"Obrigado por utilizar nosso sistema de solicitação de materiais, em breve entraremos em contato para confirmarmos a disponibilidade e entrega\n" \
                       f"Grato, Clube de desbravadores pioneiros da colina"
                send_client(text, email)
            tab3.success("Solcitação enviada")


if __name__ == '__main__':
    main()
