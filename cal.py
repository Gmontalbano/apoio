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


def cal_2():

    year = date.today().year
    month = date.today().month
    # Criar tabela para eventos
    # Chamar a tabela e pegar os eventos do mes atual
    dates = [{'Dia': 7, 'Evento': 'niver'}, {'Dia': 11, 'Evento': 'teste'}]
    text_cal = calendar.HTMLCalendar(firstweekday=0)

    x = text_cal.formatmonth(year, month).replace("Mon", "Seg").replace("Tue", "Ter").replace("Wed", "Qua")\
        .replace("Thu", "Qui").replace("Fri", "Sex").replace("Sat", "Sab").replace("Sun", "Dom")\
        .replace('border="0"', 'border="2"').replace('cellpadding="0"', 'cellpadding="2"')
    for event in dates:
        x = x.replace(f">{event['Dia']}<", f'style="background-color:#464e5f">{event["Dia"]}<')

    x = x.split("<body>")
    x = x[0]

    co, ev = st.columns(2)
    with co:
        stc.html(x, height=250, width=250)
    df = pd.DataFrame.from_dict(dates)
    ev.dataframe(df)