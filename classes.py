import pandas as pd
import streamlit as st
from io import BytesIO


def to_excel(exportacao):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    exportacao.to_excel(writer, sheet_name='sheet1',index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def make_class():
    uploaded_file = st.file_uploader("Upload do arquivo com as datas de nascimento")

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        dbv = []
        df['CATEGORIA'] = 'AMIGO'
        df.loc[(df['DATA DE NASCIMENTO'] >= '2011-06-30') & (
                    df['DATA DE NASCIMENTO'] <= '2012-06-30'), 'CATEGORIA'] = 'COMPANHEIRO'
        df.loc[(df['DATA DE NASCIMENTO'] >= '2010-06-30') & (
                    df['DATA DE NASCIMENTO'] <= '2011-06-30'), 'CATEGORIA'] = 'PESQUISADOR'
        df.loc[(df['DATA DE NASCIMENTO'] >= '2009-06-30') & (
                    df['DATA DE NASCIMENTO'] <= '2010-06-30'), 'CATEGORIA'] = 'PIONEIRO'
        df.loc[(df['DATA DE NASCIMENTO'] >= '2008-06-30') & (
                    df['DATA DE NASCIMENTO'] <= '2009-06-30'), 'CATEGORIA'] = 'EXCURSIONISTA'
        df.loc[(df['DATA DE NASCIMENTO'] >= '2007-06-30') & (
                    df['DATA DE NASCIMENTO'] <= '2008-06-30'), 'CATEGORIA'] = 'GUIA'
        #new_df = pd.DataFrame(dbv)
        dff = to_excel(df)
        st.download_button("Download", dff, file_name='classes.xlsx')
