import streamlit as st
import pandas as pd
import json


def qtd_item(item_name, stock):
    for item in stock["items"]:
        if item["name"] == item_name:
            qtd = item["quantity"]-item["ocupado"]
            break
    return qtd


def solicitar_item():
    # Carrega o arquivo JSON com os dados do estoque
    with open("stock.json", "r") as file:
        stock = json.load(file)
    # Cria um menu dropdown com os nomes dos itens no estoque
    item_name = st.selectbox("Selecione o item para solicitar", [item["name"] for item in stock["items"]])
    # ver quantidade de itens disponiveis
    max_value = qtd_item(item_name, stock)
    st.write(max_value)
    # Recebe a quantidade do item solicitado
    item_quantity = st.number_input("Insira a quantidade do item solicitado", step=1, min_value=0, max_value=max_value)
    if st.button("Solicitar item"):
        # Atualiza a quantidade do item solicitado
        if item_quantity <= max_value:
            print(item_quantity)
            for item in stock["items"]:
                if item["name"] == item_name:
                    item["ocupado"] += item_quantity
                    break
            # Salva as alterações no arquivo JSON
            with open("stock.json", "w") as file:
                json.dump(stock, file)
            st.success("Item solicitado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Quantidade solcitada maior que disponivel", icon="🚨")


def devolver_item():
    # Carrega o arquivo JSON com os dados do estoque
    with open("stock.json", "r") as file:
        stock = json.load(file)
    # Cria um menu dropdown com os nomes dos itens no estoque
    item_name = st.selectbox("Selecione o item para devolver", [item["name"] for item in stock["items"]])
    # Recebe a quantidade do item a ser devolvido
    item_quantity = st.number_input("Insira a quantidade do item a ser devolvido", min_value=1, value=1)
    if st.button("Devolver item"):
        # Atualiza a quantidade do item devolvido
        for item in stock["items"]:
            if item["name"] == item_name:
                item["ocupado"] -= item_quantity
                break
        # Salva as alterações no arquivo JSON
        with open("stock.json", "w") as file:
            json.dump(stock, file)
        st.success("Item devolvido com sucesso!")

