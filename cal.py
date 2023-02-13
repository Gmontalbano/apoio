import pandas as pd
import streamlit as st
from datetime import date, timedelta
import calendar
import streamlit.components.v1 as stc


# Função para retornar todas as datas entre uma data inicial e final
def get_dates(start_date, end_date):
    return [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]


def tt_cal():
    # Inicialização do calendário
    today = date.today()
    start_date = today - timedelta(days=(today.weekday()))
    end_date = start_date + timedelta(days=6)
    # dates = get_dates(start_date, end_date)

    # Adiciona o calendário na tela
    st.title("Agenda")
    st.write("Semana de", start_date, "até", end_date)

    # Adiciona uma lista de eventos na tela
    events = {}
    event_name = st.text_input("Nome do evento")
    event_date = st.date_input("Data do evento")

    if st.checkbox("Adicionar evento"):
        events[event_name] = {'name': event_name, 'date': event_date}

    st.write("Eventos:", events)


def calendario():
    year = date.today().year
    month = date.today().month
    # Criar tabela para eventos
    # Chamar a tabela e pegar os eventos do mes atual
    text_cal = calendar.HTMLCalendar(firstweekday=6)
    meses = {'January': 'Janeiro',
             'February': 'Fevereiro',
             'March': 'Março',
             'April': 'Abril',
             'May': 'Maio',
             'June': 'Junho',
             'July': 'Julho',
             'August': 'Agosto',
             'September': 'Setembro',
             'October': 'Outubro',
             'November': 'Novembro',
             'December': 'Dezembro'}
    M_ING = date.today().strftime("%B")
    x = text_cal.formatmonth(year, month).replace(F"{M_ING}", meses[f'{M_ING}']).replace("Mon", "Seg").replace("Tue", "Ter").replace("Wed", "Qua") \
        .replace("Thu", "Qui").replace("Fri", "Sex").replace("Sat", "Sab").replace("Sun", "Dom") \
        .replace('border="0"', 'border="2"').replace('cellpadding="0"', 'cellpadding="2"')
    import sqlite3
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    query = f"SELECT * FROM calendario WHERE mes = {month} AND ano = {year}"
    df = pd.read_sql(query, conn)
    df = df.reset_index()
    co, ev = st.columns(2)
    f = len(df) / 2
    i = 1
    itable = f'<body><table border="2" cellpadding="2" cellspacing="0" class="month">' \
             f'<tr><th class="dia">Dia</th><th class="ev">Evento</th>'
    padrao = '<tr><td class="dia">{data}</td><td class="ev">{texto}</td></tr>'
    fim = '</table></body>'
    for index, row in df.iterrows():
        x = x.replace(f">{row['dia']}<", f'style="background-color:{row["color"]}">{row["dia"]}<')
        n = padrao.replace('{data}', f"{row['dia']}").replace('{texto}', f"{row['evento']}")
        itable += n
    itable += fim

    x = x.split("<body>")
    x = x[0]

    with co:
        stc.html(x, height=250, width=250)
    with ev:
        stc.html(itable, height=250, width=250)
