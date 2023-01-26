import streamlit as st
import pandas as pd


def solicitar_item():
    # Carrega o arquivo xlsx com os dados do estoque
    stock = pd.read_excel("stock.xlsx")
    # Cria um menu dropdown com os nomes dos itens no estoque
    item_name = st.selectbox("Selecione o item para solicitar", stock["name"])
    # Pega a quantidade disponível do item selecionado
    item_quantity = stock.loc[stock["name"] == item_name, "quantity"].values[0]
    al_sol = stock.loc[stock["name"] == item_name, "solicitado"].values[0]
    # Pede ao usuário para inserir a quantidade desejada
    requested_quantity = st.number_input("Insira a quantidade desejada (máximo {})".format(item_quantity+al_sol), min_value=1, max_value=item_quantity)
    if st.button("Solicitar item"):
        # Atualiza a quantidade do item no estoque
        stock.loc[stock["name"] == item_name, "solicitado"] -= requested_quantity
        stock.to_excel("stock.xlsx", index=False)
        st.success("Item solicitado com sucesso!")


def devolver_item():
    # Carrega o arquivo xlsx com os dados do estoque
    stock = pd.read_excel("stock.xlsx")
    # Cria um menu dropdown com os nomes dos itens no estoque
    item_name = st.selectbox("Selecione o item para devolver", stock["name"])
    al_sol = stock.loc[stock["name"] == item_name, "solicitado"].values[0]
    # Pede ao usuário para inserir a quantidade a ser devolvida
    returned_quantity = st.number_input("Insira a quantidade a ser devolvida", min_value=1, max_value=al_sol*-1)
    if st.button("Devolver item"):
        # Atualiza a quantidade do item no estoque
        stock.loc[stock["name"] == item_name, "solicitado"] += returned_quantity
        stock.to_excel("stock.xlsx", index=False)
        st.success("Item devolvido com sucesso!")

