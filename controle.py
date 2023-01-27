import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


def add_item():
    # Recebe o nome do item a ser adicionado
    item_name = st.text_input("Insira o nome do item a ser adicionado")
    # Recebe a quantidade do item a ser adicionado
    item_quantity = st.number_input("Insira a quantidade do item a ser adicionado", min_value=1, value=1)
    if st.button("Adicionar item"):
        # Salva as alterações
        c.execute(f"INSERT INTO items (item, quantidade, ocupado) VALUES ('{item_name}', '{item_quantity}', 0)")
        conn.commit()
        st.success("Item adicionado com sucesso!")


def delete_item():
    # Carrega do banco a coluna item
    df = pd.read_sql('select item from items', conn)
    lista = df['item'].tolist()
    # Cria um menu dropdown com os nomes dos itens no estoque
    item_name = st.selectbox("Selecione o item para deletar", lista)
    if st.button("Deletar item"):
        # Deleta o item selecionado do estoque
        c.execute(f"DELETE FROM items WHERE item = '{item_name}'")
        conn.commit()
        st.success("Item deletado com sucesso!")


def view_items():
    df = pd.read_sql('select * from items', conn)
    st.dataframe(df)


def main_controle():

    st.sidebar.title("Menu")
    menu = ["Adicionar item", "Ver estoque", "Deletar item"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)

    if choice == "Adicionar item":
        add_item()
    elif choice == "Ver estoque":
        view_items()
    elif choice == "Deletar item":
        delete_item()


if __name__ == "__main__":
    main_controle()


