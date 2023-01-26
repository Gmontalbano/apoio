import streamlit as st
import pandas as pd


def add_item():
    name = st.text_input("Nome do item")
    quantity = st.number_input("Quantidade", step=1, min_value=0)
    if st.button('Adicionar item'):
        # Carrega o arquivo xlsx com os dados do estoque
        stock = pd.read_excel("stock.xlsx")

        # Adiciona o novo item ao estoque
        new_item = {"name": name, "quantity": quantity, "solicitado": 0}
        stock = stock.append(new_item, ignore_index=True)

        # Salva as alterações no arquivo xlsx
        stock.to_excel("stock.xlsx", index=False)
        st.success("Item adicionado com sucesso!")


def delete_item():
    # Carrega o arquivo xlsx com os dados do estoque
    stock = pd.read_excel("stock.xlsx")
    # Cria um menu dropdown com os nomes dos itens no estoque
    item_name = st.selectbox("Selecione o item para deletar", stock["name"])
    if st.button("Deletar item"):
        # Encontra a linha correspondente ao item selecionado
        item_to_delete = stock[stock['name'] == item_name]
        # Deleta a linha do DataFrame
        stock = stock.drop(item_to_delete.index)
        # Salva as alterações no arquivo xlsx
        stock.to_excel("stock.xlsx", index=False)
        st.success("Item deletado com sucesso!")


def view_stock():
    # Carrega o arquivo xlsx com os dados do estoque
    stock = pd.read_excel('stock.xlsx')
    # Cria uma tabela para exibir os itens do estoque
    st.write("Itens do estoque:")
    st.table(stock)


def main_controle():

    st.sidebar.title("Menu")
    menu = ["Adicionar item", "Ver estoque", "Deletar item"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)

    if choice == "Adicionar item":
        add_item()
    elif choice == "Ver estoque":
        view_stock()
    elif choice == "Deletar item":
        delete_item()


if __name__ == "__main__":
    main_controle()


