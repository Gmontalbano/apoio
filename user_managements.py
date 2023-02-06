import sqlite3
import time

import pandas as pd
import streamlit as st
from hashes import make_hashes, check_hashes


def add_userdata(username, password, email, permission):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username,password,email,permission) VALUES (?,?,?,?)',
              (username, password, email, permission))
    conn.commit()


def view_all_users():
    conn = sqlite3.connect('data.db')
    df = pd.read_sql('select username, email, permission from userstable', conn)
    return df


def user_lis():
    conn = sqlite3.connect('data.db')
    query = 'SELECT username FROM userstable'
    df = pd.read_sql(query, conn)
    users = df['username'].to_list()
    return users


def delete_user(user_name):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM userstable WHERE username = '{user_name}'")
    conn.commit()


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
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
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
            query = f"SELECT email FROM userstable WHERE username = '{user_update}'"
            df = pd.read_sql(query, conn)
            email = df['email'][0]
            att_email = st.text_input("Email",email)
        if st.checkbox("Permição"):
            change_permission = True
            query = f"SELECT permission FROM userstable WHERE username = '{user_update}'"
            df = pd.read_sql(query, conn)
            permission = df['permission'][0]
            type_permission = ['admin', 'user', 'apoio', 'secretaria']
            index = type_permission.index(permission)
            type_permission.insert(0, type_permission.pop(index))
            perm = st.selectbox("Permissão", type_permission)
        if st.button("Atualizar usuario"):
            changes = ""
            if change_pass:
                changes += f"password = '{make_hashes(att_password)}'"
            if change_email:
                if len(changes) > 0:
                    changes += ", "
                changes += f"email = '{att_email}'"
            if change_permission:
                if len(changes) > 0:
                    changes += ", "
                changes += f"permission = '{perm}'"
            st.write(changes)
            c.execute(f'UPDATE userstable SET {changes} WHERE username = "{user_update}"')
            conn.commit()
            st.success("Updated user")

    # All
    with all_user:
        st.subheader("Users Profiles")
        user_result = view_all_users()
        clean_db = pd.DataFrame(user_result)
        st.dataframe(clean_db)

