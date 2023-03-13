from time import sleep

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import and_
import sqlalchemy as db
from configparser import ConfigParser
key = ".env"
parser = ConfigParser()
_ = parser.read(key)
db_url = parser.get('postgres', 'db_url')


engine = create_engine(db_url)
metadata = db.MetaData()
conn = engine.connect()
patrimonio = db.Table('patrimonio', metadata, autoload_with=engine)
sol_interna = db.Table('solicitacao_interna', metadata, autoload_with=engine)


def add_item():
    # Recebe o nome do item a ser adicionado
    item_name = st.text_input("Insira o nome do item a ser adicionado")
    # Recebe a quantidade do item a ser adicionado
    item_quantity = st.number_input("Insira a quantidade do item a ser adicionado", min_value=1, value=1)
    if st.button("Adicionar item"):
        # Salva as alterações
        query = db.insert(patrimonio).values(item_name=item_name, quantidade=item_quantity)
        conn.execute(query)
        conn.commit()
        st.success("Item adicionado com sucesso!")
        sleep(0.5)
        st.experimental_rerun()


def delete_item():
    # Carrega do banco a coluna item
    query = db.select(patrimonio.columns.item_name)
    df = pd.read_sql(con=conn, sql=query)
    lista = df['item_name'].tolist()
    # Cria um menu dropdown com os nomes dos itens no estoque
    item_name = st.selectbox("Selecione o item para deletar", lista)
    if st.button("Deletar item"):
        # Deleta o item selecionado do estoque
        query = db.delete(patrimonio).where(patrimonio.columns.item_name == item_name)
        conn.execute(query)
        conn.commit()
        st.success("Item deletado com sucesso!")
        sleep(0.5)
        st.experimental_rerun()


def view_items():
    query = db.select(patrimonio)
    df = pd.read_sql(con=conn, sql=query)
    st.dataframe(df)


def card(title, content, color='white'):
    """Exibe um card no estilo Trello.

    Arguments:
        title {str} -- Título do card
        content {str} -- Conteúdo do card
        color {str} -- Cor de fundo do card (default: {'white'})

    Returns:
        None
    """
    card_style = f"background-color: {color}; padding: 10px; border-radius: 10px; margin: 10px 0"
    title_style = "font-weight: bold; font-size: 20px; margin-bottom: 10px"
    content_style = "font-size: 16px"

    st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
    st.markdown(f"<p style='{title_style}'>{title}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='{content_style}'>{content}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def sol_dia():
    query = db.select(sol_interna.columns.reuniao).distinct()
    df = pd.read_sql(con=conn, sql=query)
    datas = df['reuniao'].tolist()
    choice = st.selectbox("Selecione a reunião", datas)
    query = db.select(sol_interna).where(sol_interna.columns.reuniao == choice)
    dff = pd.read_sql(con=conn, sql=query)
    st.dataframe(dff)
    for index, row in dff.iterrows():
        p = ""
        pedido = row['pedido']
        for x in pedido:
            p += f"{x}: {pedido[x]['qtd']} <br>"
        card(f"{row['user_id']}", f"{p}", color='lightblue')


def main_controle():
    menu = ["Adicionar item", "Deletar item", "Ver estoque", "Reuniões"]
    # choice = st.sidebar.selectbox("Selecione uma opção", menu)
    add, delete, see, reu = st.tabs(menu)
    with see:
        view_items()
    with add:
        add_item()
    with delete:
        delete_item()
    with reu:
        sol_dia()


if __name__ == "__main__":
    main_controle()
