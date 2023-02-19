import streamlit as st
from datetime import timedelta, date
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
sol_historico = db.Table('solicitacao_historico', metadata, autoload_with=engine)


def check_itens():
    query = db.select(patrimonio.columns.item_name)
    df = pd.read_sql(con=conn, sql=query)
    lista = df['item_name'].tolist()
    return lista


def check_qtd(item_name):
    query = db.select(patrimonio.columns.quantidade).where(patrimonio.columns.item_name == item_name)
    df = pd.read_sql(con=conn, sql=query)
    qtd = df['quantidade'][0]
    return qtd


def check_data(data):
    query = db.select(sol_historico.columns.pedido).where(sol_historico.columns.data == data)
    df = pd.read_sql(con=conn, sql=query)
    if len(df['pedido']) != 0:
        st.session_state.has_pedido_data = True
        st.session_state.pedido_data[data] = df['pedido'][0]
    else:
        st.session_state.has_pedido_data = False
        st.session_state.pedido_data[data] = {}


def check_pedido(data):
    query = db.select(sol_interna.columns.pedido).where(and_(sol_interna.columns.user_id == st.session_state.user_id, sol_interna.columns.reuniao == data))
    df = pd.read_sql(con=conn, sql=query)
    if st.session_state.username not in st.session_state.pedido_user:
        st.session_state.pedido_user[st.session_state.username] = {}
    if len(df) != 0:
        st.session_state.has_pedido_user = True
        st.session_state.pedido_user[st.session_state.username][data] = df['pedido'][0]
    else:
        st.session_state.pedido_user[st.session_state.username] = {data: {}}
        st.session_state.has_pedido_user = False


def check_pedido_c(data):
    query = db.select(sol_interna.columns.pedido).where(
        and_(sol_interna.columns.user_id == st.session_state.user_id, sol_interna.columns.reuniao == data))
    df = pd.read_sql(con=conn, sql=query)
    if len(df) != 0:
        st.session_state.pedido_c = df['pedido'][0]
    else:
        st.session_state.pedido_c = {}


def difference(novo, antigo):
    result = {}
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
    end_date = date.today() + timedelta(days=8)
    data = st.date_input("Data da reunião")
    if st.button("data") or st.session_state.sub_data:
        st.session_state.sub_data = True
        st.write(data)
        check_pedido_c(data)
        if st.session_state.username not in st.session_state.pedido_user:
            st.session_state.pedido_user[st.session_state.username] = {}
        if data in st.session_state.pedido_user[st.session_state.username]:
            if data >= end_date:
                check_data(data)
                name, value = st.columns(2)
                lista = check_itens()
                item_name = name.selectbox("Selecione o item para solicitar", lista)
                max_value = check_qtd(item_name)
                if item_name in st.session_state.pedido_data[data]:
                    max_value -= st.session_state.pedido_data[data][item_name]['qtd']
                if item_name in st.session_state.pedido_c:
                    sub = st.session_state.pedido_c[item_name]['qtd'] - st.session_state.pedido_user[st.session_state.username][data][item_name]['qtd']
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
                            if item_name not in st.session_state.pedido_user[st.session_state.username][data]:
                                st.session_state.pedido_user[st.session_state.username][data][item_name] = {'item': item_name, 'qtd': item_quantity}
                            else:
                                st.session_state.pedido_user[st.session_state.username][data][item_name]['qtd'] += item_quantity
                        else:
                            b1.error("Quantidade solicitada maior que a disponivel")
                        st.experimental_rerun()

                if b2.button("Remover item") and item_quantity > 0:
                    if item_name in st.session_state.pedido_user[st.session_state.username][data]:
                        if item_quantity <= st.session_state.pedido_user[st.session_state.username][data][item_name]['qtd']:
                            st.session_state.pedido_user[st.session_state.username][data][item_name]['qtd'] -= item_quantity
                        else:
                            st.error("Não é possível remover mais que o solicitado")
                    st.experimental_rerun()
                with st.container():
                    st.subheader("Materiais solicitados")
                    for i in st.session_state.pedido_user[st.session_state.username][data]:
                        st.write(f"{i}: {st.session_state.pedido_user[st.session_state.username][data][i]['qtd']}")
                e, bt, e2 = st.columns(3)
                if bt.button("Finalizar solicitação"):
                    X = st.session_state.pedido_user[st.session_state.username][data]
                    st.write(X)
                    if st.session_state.has_pedido_user:
                        query = db.update(sol_interna).where(and_(sol_interna.columns.user_id == st.session_state.user_id,sol_interna.columns.reuniao == data)).values(X)
                    else:
                        query = db.insert(sol_interna).values(pedido=X, user_id=st.session_state.user_id, reuniao=data)
                    conn.execute(query)
                    conn.commit()
                    if st.session_state.has_pedido_data:
                        dif = difference(st.session_state.pedido_user[st.session_state.username][data], st.session_state.pedido_c)
                        for i in dif:
                            if i in st.session_state.pedido_data[data]:
                                st.session_state.pedido_data[data][i]['qtd'] += dif[i]['qtd']
                            else:
                                st.session_state.pedido_data[data][i] = dif[i]
                        X = st.session_state.pedido_data[data]
                        query = db.update(sol_historico).where(sol_historico.columns.data == data).values(X)
                    else:
                        query = db.insert(sol_historico).values(data=data, pedido=X)
                    conn.execute(query)
                    conn.commit()
                    st.session_state.pedido_c = {}
                    st.session_state.pedido_data = {}
                    st.session_state.pedido_user = {}
                    check_pedido(data)
                    st.experimental_rerun()
            else:
                st.error("Solicitação de materiais encerrada para a data")
        else:
            check_data(data)
            check_pedido(data)
            st.experimental_rerun()
