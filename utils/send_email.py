import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(text):
    host = "smtp.office365.com"
    port = "587"
    login = "apoiodacolina.pc@gmail.com"
    senha = "Jaguncomotorizado2000"

    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()
    server.login(login, senha)

    corpo = text

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = login
    email_msg['Subject'] = "Solicitação de material externa"
    email_msg.attach(MIMEText(corpo, 'plain'))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()


def send_client(text, adress):
    host = "smtp.office365.com"
    port = "587"
    login = "apoiodacolina.pc@gmail.com"
    senha = "Jaguncomotorizado2000"

    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()
    server.login(login, senha)

    corpo = text

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = adress
    email_msg['Subject'] = "Solicitação de material pioneiros da colina"
    email_msg.attach(MIMEText(corpo, 'plain'))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()
