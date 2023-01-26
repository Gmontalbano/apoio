import streamlit as st

# Variável global que armazena o estado de login
logged_in = False

def login():
    global logged_in
    # Cria um título
    st.title("Login")
    # Cria uma área vazia para a interface de login
    with st.spacer():
        # Adiciona um campo de texto para o nome de usuário
        username = st.text_input("Username")
        # Adiciona um campo de senha
        password = st.text_input("Password", type='password')
        # Adiciona um botão de login
        if st.button("Login"):
            # Adiciona lógica de autenticação aqui
            if username == "admin" and password == "password":
                st.success("Login realizado com sucesso!")
                logged_in = True
            else:
                st.error("Usuário ou senha incorretos.")

def acess_page():
    # Verifica se o usuário está logado
    if logged_in:
        st.success("Bem-vindo à página restrita!")
    else:
        st.warning("Você precisa fazer login para acessar essa página.")

def main():
    st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")
    st.sidebar.title("Menu")
    menu = ["Homepage", "Acess Page"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Chama a função de página apropriada de acordo com a escolha do usuário
    if choice == "Homepage":
        st.write(login)
    elif choice == "Acess Page":
        st.write(acess_page)

if __name__== "__main__":
    main()
