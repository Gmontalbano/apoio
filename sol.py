import streamlit as st
from datetime import timedelta, date
import pandas as pd
import sqlite3


def check_itens():
    conn = sqlite3.connect('./data.db')
    df = pd.read_sql('select item from items', conn)
    lista = df['item'].tolist()
    return lista


def check_qtd(item_name):
    conn = sqlite3.connect('./data.db')
    df = pd.read_sql(f"SELECT quantidade  FROM items WHERE item = '{item_name}'", conn)
    conn.close()
    qtd = df['quantidade'][0]
    return qtd


def check_data(data):
    conn = sqlite3.connect('./data.db')
    df = pd.read_sql(f"SELECT itens FROM solicitacao_historico WHERE data = '{data}'", conn)
    if len(df['itens']) != 0:
        st.session_state.has_pedido_data = True
        st.session_state.pedido_data[data] = eval(df['itens'][0])
    else:
        st.session_state.has_pedido_data = False
        st.session_state.pedido_data[data] = {}


def check_pedido(data):
    conn = sqlite3.connect('./data.db')
    df = pd.read_sql(f"SELECT pedido  FROM solicitacao_interna WHERE username = '{st.session_state.username}' AND reuniao = '{data}'", conn)
    if len(df) != 0:
        st.session_state.has_pedido_user = True
        st.session_state.pedido_user[data] = eval(df['pedido'][0])
    else:
        st.session_state.pedido_user[data] = {}
        st.session_state.has_pedido_user = False



def check_pedido_c(data):
    conn = sqlite3.connect('./data.db')
    df = pd.read_sql(f"SELECT pedido  FROM solicitacao_interna WHERE username = '{st.session_state.username}' AND reuniao = '{data}'", conn)
    if len(df) != 0:
        st.session_state.pedido_c = eval(df['pedido'][0])
    else:
        st.session_state.pedido_c = {}

def difference(novo, antigo):
    result = {}
    print(f"Novo: {novo}")
    print("\n")
    print(f"ANtigo: {antigo}")
    for key in novo:
        if key in antigo:
            result[key] = {'item': key, 'qtd': novo[key]['qtd'] - antigo[key]['qtd']}
        else:
            result[key] = {'item': key, 'qtd': novo[key]['qtd']}
    for key in antigo:
        if key not in novo:
            result[key] = {'item': key, 'qtd': -antigo[key]['qtd']}
    return result

def solicitar_item():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    end_date = date.today() + timedelta(days=8)
    data = st.date_input("Data da reunião")
    if st.button("data") or st.session_state.sub_data:
        st.session_state.sub_data = True
        check_pedido_c(data)
        if data in st.session_state.pedido_data and data in st.session_state.pedido_user:
            if data >= end_date:
                name, value = st.columns(2)
                lista = check_itens()
                item_name = name.selectbox("Selecione o item para solicitar", lista)
                max_value = check_qtd(item_name)
                if item_name in st.session_state.pedido_data[data]:
                    max_value -= st.session_state.pedido_data[data][item_name]['qtd']
                if item_name in st.session_state.pedido_c:
                    sub = st.session_state.pedido_c[item_name]['qtd'] - st.session_state.pedido_user[data][item_name]['qtd']
                    if sub > 0:
                        max_value += sub
                value.metric("Disponivel", max_value)
                item_quantity = name.number_input("Insira a quantidade do item solicitado", step=1)
                b1, b2 = st.columns(2)
                if max_value <= 0:
                    b1.error("Item indisponivel para o dia")
                else:
                    if b1.button("Adicionar item item") and item_quantity > 0:
                        if item_quantity <= max_value:
                            if item_name not in st.session_state.pedido_user[data]:
                                st.session_state.pedido_user[data][item_name] = {'item': item_name, 'qtd': item_quantity}
                            else:
                                st.session_state.pedido_user[data][item_name]['qtd'] += item_quantity
                        else:
                            b1.error("Quantidade solicitada maior que a disponivel")
                        st.experimental_rerun()

                if b2.button("Remover item") and item_quantity > 0:
                    if item_name in st.session_state.pedido_user[data]:
                        if item_quantity <= st.session_state.pedido_user[data][item_name]['qtd']:
                            st.session_state.pedido_user[data][item_name]['qtd'] -= item_quantity
                        else:
                            st.error("Não é possível remover mais que o solicitado")
                    st.experimental_rerun()
                with st.container():
                    st.subheader("Materiais solicitados")
                    for i in st.session_state.pedido_user[data]:
                        st.write(f"{i}: {st.session_state.pedido_user[data][i]['qtd']}")
                e, bt, e2 = st.columns(3)
                if bt.button("Finalizar solicitação"):
                    X = str(st.session_state.pedido_user[data])
                    X = X.replace("'", '"')
                    if st.session_state.has_pedido_user:
                        query = f"UPDATE solicitacao_interna SET pedido = '{X}' WHERE username = '{st.session_state.username}' AND reuniao = '{data}'"
                    else:
                        query = f"INSERT INTO solicitacao_interna(username, pedido, reuniao) VALUES ('{st.session_state.username}', '{X}', '{data}')"
                    print(query)
                    c.execute(query)

                    if st.session_state.has_pedido_data:
                        dif = difference(st.session_state.pedido_user[data], st.session_state.pedido_c)
                        for i in dif:
                            if i in st.session_state.pedido_data[data]:
                                st.session_state.pedido_data[data][i]['qtd'] += dif[i]['qtd']
                            else:
                                st.session_state.pedido_data[data][i] = dif[i]
                        X = str(st.session_state.pedido_data[data])
                        X = X.replace("'", '"')
                        c.execute(f"UPDATE solicitacao_historico SET itens = '{X}' WHERE data = '{data}'")
                    else:
                        c.execute(f"INSERT INTO solicitacao_historico(data, itens) VALUES ('{data}', '{X}')")
                    conn.commit()
                    st.session_state.pedido_c = {}
                    st.session_state.pedido_data = {}
                    st.session_state.pedido_user = {}
                    check_data(data)
                    check_pedido(data)
                    st.experimental_rerun()
            else:
                st.error("Solicitação de materiais encerrada para a data")
        else:
            check_data(data)
            check_pedido(data)
            st.experimental_rerun()
