import time
import pandas as pd
import streamlit as st
from utils.hashes import make_hashes
from sqlalchemy import create_engine
import sqlalchemy as db
from configparser import ConfigParser
key = ".env"
parser = ConfigParser()
_ = parser.read(key)
db_url = parser.get('postgres', 'db_url')
engine = create_engine(db_url)
metadata = db.MetaData()
conn = engine.connect()
users_table = db.Table('users_table', metadata, autoload_with=engine)


def add_userdata(username, password, email, permission):
    query = db.insert(users_table).values(username=username, password=password, email=email, permission=permission)
    conn.execute(query)
    conn.commit()



def view_all_users():
    query = db.select(users_table.columns.username, users_table.columns.email, users_table.columns.permission)
    df = pd.read_sql(con=conn, sql=query)
    return df


def user_lis():
    query = db.select(users_table.columns.username)
    df = pd.read_sql(con=conn, sql=query)
    user = df['username'].to_list()
    return user


def delete_user(user_name):
    query = db.delete(users_table).where(users_table.columns.username == user_name)
    conn.execute(query)
    conn.commit()


def update_user():
    users = user_lis()
    user_update = st.selectbox("Usuario", users, key="update_user")
    change_pass = False
    change_email = False
    change_permission = False
    if st.checkbox("Senha"):
        change_pass = True
        att_password = st.text_input("Nova senha")
    if st.checkbox("email"):
        change_email = True
        # query = f"SELECT email FROM userstable WHERE username = '{user_update}'"
        query = db.select(users_table.columns.email).where(users_table.columns.username == user_update)
        df = pd.read_sql(con=conn, sql=query)
        email = df['email'][0]
        att_email = st.text_input("Email", email)
    if st.checkbox("Permição"):
        change_permission = True
        query = db.select(users_table.columns.permission).where(users_table.columns.username == user_update)
        df = pd.read_sql(con=conn, sql=query)
        permission = df['permission'][0]
        type_permission = ['admin', 'user', 'apoio', 'secretaria']
        index = type_permission.index(permission)
        type_permission.insert(0, type_permission.pop(index))
        perm = st.selectbox("Permissão", type_permission)
    if st.button("Atualizar usuario"):
        if change_pass:
            query = db.update(users_table).where(users_table.columns.username == user_update).values(
                password=make_hashes(att_password))
            conn.execute(query)
            conn.commit()
        if change_email:
            query = db.update(users_table).where(users_table.columns.username == user_update).values(email=att_email)
            conn.execute(query)
            conn.commit()
        if change_permission:
            query = db.update(users_table).where(users_table.columns.username == user_update).values(permission=perm)
            conn.execute(query)
            conn.commit()
        time.sleep(0.5)
        st.success("Updated user")
        st.experimental_rerun()


def users_manage():
    tabs = ['create', 'delete', 'updade', 'all']
    create, delete, update, all_user = st.tabs(tabs)

    # Create
    with create:
        st.subheader("Create New Account")
        new_user = st.text_input("Username", key="new_user")
        new_email = st.text_input("Email", key="new_email")
        new_password = st.text_input("Password", type='password', key="new_pass")
        type_permission = ['admin', 'user', 'apoio', 'secretaria']
        perm = st.selectbox("Permissão", type_permission)
        if st.button("Adicionar user"):
            add_userdata(new_user, make_hashes(new_password), new_email, perm)
            st.success("You have successfully created a valid Account")

    # Delete
    with delete:
        users = user_lis()
        user_del = st.selectbox("Usuario", users, key="delete_user")
        if st.button("Deletar user"):
            delete_user(user_del)
            delete.success("You have successfully deleted a Account")
            time.sleep(1)
            st.experimental_rerun()

    #Update
    with update:
        update_user()


    # All
    with all_user:
        st.subheader("Users Profiles")
        user_result = view_all_users()
        clean_db = pd.DataFrame(user_result)
        st.dataframe(clean_db)

