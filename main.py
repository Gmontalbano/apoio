import streamlit as st
import sqlite3
from PIL import Image

from controle import main_controle
from classes import make_class
from sol import solicitar_item
from send_email import send, send_client
from user_managements import users_manage
from hashes import make_hashes, check_hashes
from cal import tt_cal, calendario


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
if "loggin" not in st.session_state:
    st.session_state.loggin = False

conn = sqlite3.connect('data.db')
c = conn.cursor()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    c.execute('SELECT permission FROM userstable WHERE username =? AND password = ?', (username, password))
    permission = c.fetchall()
    if data:
        return data, permission[0][0]
    else:
        return data, 0


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

            type_permission = {'admin': ["Solicita????o de material", "Estoque", "Usuarios", "Classes", "Calend??rio"],
                               'user': ["Solicita????o de material"],
                               'apoio': ["Solicita????o de material", "Estoque"],
                               'secretaria': ['Classes']}
            menu = type_permission[permission]

            choice = st.sidebar.selectbox("Selecione uma op????o", menu)

            if choice == "Solicita????o de material":
                solicitar_item()
            elif choice == "Estoque":
                main_controle()
            elif choice == "Usuarios":
                users_manage()
            elif choice == 'Classes':
                make_class()
            elif choice == "Calend??rio":
                calendario()



        else:
            st.sidebar.error("Incorrect Username/Password")
    else:
        tab1, tab2, tab3 = st.tabs(["Nosso clube", "Calend??rio", "Solicita????o externa"])
        with tab2:
            calendario()
        with tab3:
            tab3.subheader("Solicita????o de empr??stimo de material")
            tab3.markdown("O empr??stimo ?? feito exclusivamente para departamentos interndo do UNASP-SP")
            nome = tab3.text_input("Nome", key="requester_name")
            email = tab3.text_input("Email", key="requester_email")
            telefone = tab3.text_input("Telefone", key="requester_tel")
            # tab3.text_input("CPF", key="requester_cpf")
            dep = tab3.text_input("Departamento", key="requester_departament")
            meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
            coleta, devo = tab3.columns(2)
            coleta.subheader("Dia para coletar o material")
            dia = coleta.selectbox("Dia", range(1, 32), key='cd')
            mes = coleta.selectbox("Mes", meses, key='cm')
            devo.subheader("Devolu????o o material")
            diad = devo.selectbox("Dia", range(1, 32), key='dd')
            mesd = devo.selectbox("Mes", meses, key='dm')
            me, bc = st.columns(2)
            me.metric("Mesas", 40)
            bc.metric("Bancos", 300)
            mesas = me.number_input("Insira a quantidade de mesas", step=1)
            bancos = bc.number_input("Insira a quantidade de bancos", step=1)
            if tab3.button("Solcitar material"):
                with st.spinner(text="Fazendo solicita????o..."):
                    text = f"{nome} do departamento {dep} solicitou material \n Coleta: {dia}/{mes} \n Devolu????o: {diad}/{mesd} \n Mesas: {mesas} \n Bancos: {bancos}\n{email} |  {telefone}"
                    send(text)
                    text = f"Ol??, {nome}.\n" \
                           f"Obrigado por utilizar nosso sistema de solicita????o de materiais, em breve entraremos em contato para confirmarmos a disponibilidade e entrega\n" \
                           f"Grato, Clube de desbravadores pioneiros da colina" \
                           f"Solicita????o \nMesas: {mesas} \n Bancos: {bancos}\n" \
                           f"Este email ?? uma confirma????o da solicita????o, entraremos em contato para aprovar o empr??stimo"
                    send_client(text, email)
                tab3.success("Solcita????o enviada")


if __name__ == '__main__':
    main()
