import streamlit as st
import pandas as pd
import json
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


def qtd_item(item_name):
    df = pd.read_sql(f"SELECT quantidade, ocupado FROM items WHERE item = '{item_name}'", conn)
    qtd = df['quantidade'][0]-df['ocupado'][0]
    return qtd


def solicitar_item():
    df = pd.read_sql('select item from items', conn)
    lista = df['item'].tolist()
    # Cria um menu dropdown com os nomes dos itens no estoque
    name, value = st.columns(2)
    item_name = name.selectbox("Selecione o item para solicitar", lista)
    # ver quantidade de itens disponiveis
    max_value = qtd_item(item_name)
    print("Max", max_value)
    value.metric('Disponivel', max_value)
    # Recebe a quantidade do item solicitado
    item_quantity = st.number_input("Insira a quantidade do item solicitado", step=1)
    print("qtd", item_quantity)
    if st.button("Solicitar item"):
        # Atualiza a quantidade do item solicitado
        if item_quantity <= max_value:
            df = pd.read_sql(f"select ocupado from items where item = '{item_name}'", conn)
            ocupado = df['ocupado'][0] + item_quantity
            print("ocupado", ocupado)
            c.execute(f'UPDATE items SET ocupado = {ocupado} WHERE item = "{item_name}"')
            conn.commit()
            st.experimental_rerun()
        else:
            st.error("Quantidade solcitada maior que disponivel", icon="🚨")


def devolver_item():
    df = pd.read_sql('select item, ocupado from items', conn)
    lista = df['item'].tolist()
    max_value = df['ocupado'][0]
    name, value = st.columns(2)
    # Cria um menu dropdown com  os nomes dos itens no estoque
    item_name = name.selectbox("Selecione o item para devolver", lista)
    value.metric('Ocupado', max_value)
    # Recebe a quantidade do item a ser devolvido
    item_quantity = st.number_input("Insira a quantidade do item a ser devolvido", min_value=1, value=1)
    if st.button("Devolver item"):
        if item_quantity <= max_value:
            df = pd.read_sql(f"select ocupado from items where item = '{item_name}'", conn)
            devolucao = df['ocupado'][0] - item_quantity
            print("ocupado", devolucao)
            c.execute(f'UPDATE items SET ocupado = {devolucao} WHERE item = "{item_name}"')
            conn.commit()
            st.experimental_rerun()
            st.success("Item devolvido com sucesso!")
        else:
            st.error(f"Quantidade devolvida maior que emprestada", icon="🚨")

