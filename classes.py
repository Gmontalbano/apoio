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
        for name, birt in zip(df['NOME COMPLETO'], df['DATA DE NASCIMENTO']):
            if birt.month >= 7:
                if birt.year == 2012:
                    dbv.append({'nome': name, 'classe':'amigo', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2011:
                    dbv.append({'nome': name, 'classe':'companheiro', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2010:
                    dbv.append({'nome': name, 'classe':'pesquisador', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2009:
                    dbv.append({'nome': name, 'classe':'pioneiro', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2008:
                    dbv.append({'nome': name, 'classe':'excursionista', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2007:
                    dbv.append({'nome': name, 'classe':'guia', 'mes': birt.month, 'ano': birt.year})

            elif birt.month < 7:
                if birt.year == 2013:
                    dbv.append({'nome': name, 'classe':'amigo', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2012:
                    dbv.append({'nome': name, 'classe':'companheiro', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2011:
                    dbv.append({'nome': name, 'classe':'pesquisador', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2010:
                    dbv.append({'nome': name, 'classe':'pioeniro', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2009:
                    dbv.append({'nome': name, 'classe':'excursionista', 'mes': birt.month, 'ano': birt.year})
                if birt.year == 2008:
                    dbv.append({'nome': name, 'classe':'guia', 'mes': birt.month, 'ano': birt.year})
        new_df = pd.DataFrame(dbv)
        dff = to_excel(new_df)
        st.download_button("Download", dff, file_name='classes.xlsx')
