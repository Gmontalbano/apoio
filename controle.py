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
        c.execute(f"INSERT INTO items (item, quantidade) VALUES ('{item_name}', '{item_quantity}')")
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


def devolver_item():
    # alterar para tabela historico e tirar coluna ocupado
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    df = pd.read_sql('select item from items', conn)

    lista = df['item'].tolist()
    name, value = st.columns(2)
    # Cria um menu dropdown com  os nomes dos itens no estoque
    item_name = name.selectbox("Selecione o item para devolver", lista)
    # Recebe a quantidade do item a ser devolvido
    item_quantity = st.number_input("Insira a quantidade do item a ser devolvido", min_value=1, value=1)
    if st.button("Devolver item"):
        df = pd.read_sql(f"select ocupado from items where item = '{item_name}'", conn)
        devolucao = df['ocupado'][0] - item_quantity
        c.execute(f'UPDATE items SET ocupado = {devolucao} WHERE item = "{item_name}"')
        conn.commit()
        st.experimental_rerun()
        st.success("Item devolvido com sucesso!")

    conn.close()


def mat_reu():
    df = pd.read_sql('SELECT * FROM solicitacao_interna', conn)
    st.write("Apenas para teste")
    st.dataframe(df)


def sol_dia():
    df = pd.read_sql('SELECT DISTINCT reuniao FROM solicitacao_interna', conn)
    datas = df['reuniao'].tolist()
    choice = st.selectbox("Selecione a reunião", datas)
    dff = pd.read_sql(f"SELECT * FROM solicitacao_interna WHERE reuniao = '{choice}'", conn)
    st.dataframe(dff)
    for index, row in dff.iterrows():
        st.write(f"Solicitante: {row['username']}")
        pedido = eval(row['pedido'])
        for x in pedido:
            st.write(f"{x}: {pedido[x]['qtd']}")
    mat_reu()


def main_controle():
    menu = ["Devolução", "Adicionar item", "Deletar item", "Ver estoque", "Reuniões"]
    # choice = st.sidebar.selectbox("Selecione uma opção", menu)
    dev, add, delete, see, reu = st.tabs(menu)
    with dev:
        devolver_item()
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
