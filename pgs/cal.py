import pandas as pd
import streamlit as st
import datetime as dt
from datetime import date, timedelta, datetime
import time
import calendar
import streamlit.components.v1 as stc
from sqlalchemy import create_engine, text
from sqlalchemy import and_
import sqlalchemy as db
from configparser import ConfigParser


def mix_colors(color1, color2):
    """Mix two colors in HTML format (e.g., #FFFFFF)"""
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r = int((r1 + r2) / 2)
    g = int((g1 + g2) / 2)
    b = int((b1 + b2) / 2)
    return f"#{r:02x}{g:02x}{b:02x}"


key = ".env"
parser = ConfigParser()
_ = parser.read(key)
db_url = parser.get('postgres', 'db_url')
engine = create_engine(db_url)
metadata = db.MetaData()
conn = engine.connect()
cal = db.Table('calendario', metadata, autoload_with=engine)


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


def calendario(year, month, resto=None):
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
    M_ING = calendar.month_name[month]
    x = text_cal.formatmonth(year, month).replace(F"{M_ING}", meses[f'{M_ING}']).replace("Mon", "Seg").replace("Tue", "Ter").replace("Wed", "Qua") \
        .replace("Thu", "Qui").replace("Fri", "Sex").replace("Sat", "Sab").replace("Sun", "Dom") \
        .replace('border="0"', 'border="2"').replace('cellpadding="0"', 'cellpadding="2"')
    num_days = calendar.monthrange(year, month)[1]
    start_date = dt.date(year, month, 1)
    end_date = dt.date(year, month, num_days)
    query = db.select(cal).filter(and_(cal.columns.data_inicio >= start_date, cal.columns.data_inicio <= end_date))
    df = pd.read_sql(query, conn)
    df = df.reset_index()
    co, ev = st.columns(2)
    itable = f'<body><table border="2" cellpadding="2" cellspacing="0" class="month">' \
             f'<tr><th class="dia">Dia</th><th class="ev">Evento</th>'
    padrao = '<tr><td class="dia">{data}</td><td class="ev">{texto}</td></tr>'
    fim = '</table></body>'
    if resto is not None:
        for e in resto:
            df = df.append(e, ignore_index=True)
    df = df.sort_values(by=['data_inicio'])
    resto = []
    t = {}
    for index, row in df.iterrows():
        a = {}
        d = row['data_inicio'].day
        dia = None
        if row['data_inicio'].month == row['data_fim'].month:
            if row["data_inicio"].day == row["data_fim"].day:
                n = padrao.replace('>{data}', f'style="background-color:{row["cor"]}">{d}').replace('{texto}', f"{row['evento']}")
                t[d] = row['cor']
                #x = x.replace(f">{d}<", f'style="background-color:{row["cor"]};">{d}<')
            else:
                while d <= row['data_fim'].day:
                    t[d] = row['cor']
                    #x = x.replace(f">{d}<", f'style="background-color:{row["cor"]}">{d}<')
                    d += 1
                n = padrao.replace('>{data}', f'style="background-color:{row["cor"]}">{row["data_inicio"].day} - {row["data_fim"].day}').replace('{texto}', f"{row['evento']}")
            itable += n


        else:
            from calendar import monthrange
            last_date = row['data_inicio'].replace(day=monthrange(row['data_inicio'].year, row['data_inicio'].month)[1])
            str_date = f"01/0{row['data_fim'].month}/{row['data_fim'].year}"
            date = datetime.strptime(str_date, '%d/%m/%Y').date()
            # date = datetime.strptime(str_date, '%d/%m/%Y').date()
            a['data_inicio'] = date
            a['data_fim'] = row['data_fim']
            a['evento'] = row['evento']
            a['cor'] = row['cor']
            resto.append(a)

            while d <= last_date.day:
                t[d] = row['cor']
                #x = x.replace(f">{d}<", f'style="background-color:{row["cor"]}">{d}<')
                d += 1
            n = padrao.replace('>{data}',
                               f'style="background-color:{row["cor"]}">{row["data_inicio"].day} - {last_date.day}').replace(
                '{texto}', f"{row['evento']}")
            itable += n
    for dia in t:
        x = x.replace(f">{dia}<", f'style="background-color:{t[dia]}">{dia}<')
    x = x.split("<body>")
    x = x[0]

    with co:
        stc.html(x, height=250, width=250)
    with ev:
        stc.html(itable, height=250, width=250)
    return resto


def show_cal():
    year = date.today().year
    resto = None
    for month in range(1, 13):
        if resto is not None:
            if len(resto)>0:
                resto = calendario(year, month, resto)
            else:
                resto = calendario(year, month)
        else:
            resto = calendario(year, month)


def add_event():
    st.subheader("Criar")
    event_name = st.text_input("Nome do evento")
    data_inicio = st.date_input("Data do inicio do evento")
    data_fim = st.date_input("Data do final do evento")
    cor = st.color_picker("Escolha uma cor")
    if st.button("Criar"):
        query = db.insert(cal).values(evento=event_name, data_inicio=data_inicio, data_fim=data_fim, cor=cor)
        conn.execute(query)
        conn.commit()
        st.experimental_rerun()
    year = 2023
    month = 2
    num_days = calendar.monthrange(year, month)[1]
    start_date = dt.date(year, month, 1)
    end_date = dt.date(year, month, num_days)
    query = db.select(cal).filter(and_(cal.columns.data_inicio >= start_date, cal.columns.data_inicio <= end_date))
    df = pd.read_sql(con=conn, sql=query)
    st.dataframe(df)


def event_lis():
    query = db.select(cal.columns.evento)
    df = pd.read_sql(con=conn, sql=query)
    user = df['evento'].to_list()
    return user


def delete_event(evento):
    query = db.delete(cal).where(cal.columns.evento == evento)
    conn.execute(query)
    conn.commit()


def del_event():
    st.subheader("Deletar")
    events = event_lis()
    e_del = st.selectbox("Evento", events, key="delete_event")
    if st.button("Deletar evento"):
        delete_event(e_del)
        st.success("You have successfully deleted a event")
        time.sleep(1)
        st.experimental_rerun()


def update_event():
    st.subheader("Atualizar")
    events = event_lis()
    event_update = st.selectbox("Evento", events, key="event_update")
    nome = st.checkbox("Nome")
    data = st.checkbox("Data")
    cor = st.checkbox("Cor")
    if nome:
        att_name = st.text_input("Evento", event_update)
    if data:
        query = db.select(cal.columns.data_inicio, cal.columns.data_fim).where(cal.columns.evento == event_update)
        df = pd.read_sql(con=conn, sql=query)
        data_inicio = df['data_inicio'][0]
        data_fim = df['data_fim'][0]
        n_inicio = st.date_input("Inicio", data_inicio)
        st.write(n_inicio)
        n_fim = st.date_input("Fim", data_fim)
    if cor:
        query = db.select(cal.columns.cor).where(cal.columns.evento == event_update)
        df = pd.read_sql(con=conn, sql=query)
        cor = df['cor'][0]
        n_cor = st.color_picker("Cor", cor)

    if st.button("Atualizar evento"):
        if nome:
            query = db.update(cal).where(cal.columns.evento == event_update).values(evento=att_name)
            conn.execute(query)
            conn.commit()
        if data:
            query = db.update(cal).where(cal.columns.evento == event_update).values(data_inicio=n_inicio, data_fim=n_fim)
            conn.execute(query)
            conn.commit()
        if cor:
            query = db.update(cal).where(cal.columns.evento == event_update).values(cor=n_cor)
            conn.execute(query)
            conn.commit()
        time.sleep(0.5)
        st.success("Updated event")
        st.experimental_rerun()


def cal_m():
    tabs = ['create', 'delete', 'updade', 'Calendário']
    create, delete, update, calend = st.tabs(tabs)
    with create:
        add_event()
    with delete:
        del_event()
    with update:
        update_event()
    with calend:
        show_cal()



