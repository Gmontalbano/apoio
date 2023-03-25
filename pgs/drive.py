from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import streamlit as st
import os


def auth():
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    return drive

def teste():
    nome = st.text_input("Digite seu nome")
    # mais campos de inscrição e talvez uma chave de segurança
    # talvez criar tudo no final
    if st.button("Próximo") or st.session_state.load_file:
        st.session_state.load_file = True
        drive = auth()
        if not st.session_state.folder:
            folder_name = nome
            folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
            folder.Upload()
            st.session_state.folder_id = folder['id']
            st.session_state.folder = True
        file = st.file_uploader("Update a file")
        f2 = st.file_uploader("a",key="2")
        x = [file,f2]
        if st.button("Up"):
            os.mkdir(f"temp")
            for f in x:
                with open(os.path.join('temp', f.name), 'wb') as file:
                    file.write(f.getbuffer())
                folder_id = st.session_state.folder_id
                file_drive = drive.CreateFile({'title': os.path.basename(f"{file.name}"), 'parents': [{'id': folder_id}]})
                #file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
                file_drive.SetContentFile(f"{file.name}")
                file_drive.Upload()
            st.success("File has been uploaded")
            for arquivo in os.listdir("temp"):
                caminho_arquivo = os.path.join("temp", arquivo)
                os.remove(caminho_arquivo)

            os.rmdir("temp")





