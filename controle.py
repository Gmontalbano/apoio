import streamlit as st
import pandas as pd
import json

from pandas.io.json import json_normalize


def add_item():
    # Carrega o arquivo JSON com os dados do estoque
    with open("stock.json", "r") as file:
        stock = json.load(file)
    # Recebe o nome do item a ser adicionado
    item_name = st.text_input("Insira o nome do item a ser adicionado")
    # Recebe a quantidade do item a ser adicionado
    item_quantity = st.number_input("Insira a quantidade do item a ser adicionado", min_value=1, value=1)
    if st.button("Adicionar item"):
        # Adiciona o novo item ao dicionário
        #  stock.append = {"name": item_name, 'quantity': item_quantity}
        # Salva as alterações no arquivo JSON
        with open("stock.json", "r+") as file:
            stock = json.load(file)
            stock["items"].append({"name": item_name, 'quantity': item_quantity})
            file.seek(0)
            json.dump(stock, file)
        st.success("Item adicionado com sucesso!")


def delete_item():
    # Carrega o arquivo JSON com os dados do estoque
    with open("stock.json", "r") as file:
        stock = json.load(file)
    # Cria um menu dropdown com os nomes dos itens no estoque
    item_name = st.selectbox("Selecione o item para deletar", [item["name"] for item in stock["items"]])
    if st.button("Deletar item"):
        # Deleta o item selecionado do estoque
        for i, item in enumerate(stock["items"]):
            if item["name"] == item_name:
                del stock["items"][i]
                break
        # Salva as alterações no arquivo JSON
        with open("stock.json", "w") as file:
            json.dump(stock, file)
        st.success("Item deletado com sucesso!")


def view_stock():
    # Carrega o arquivo JSON com os dados do estoque
    with open("stock.json", "r") as file:
        stock = json.load(file)

    # Converte o dicionário para um dataframe
    # df = pd.DataFrame(stock["items"])
    df = json_normalize(stock["items"])

    # Exibe a tabela do estoque
    st.dataframe(df)


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


