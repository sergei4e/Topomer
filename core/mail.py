# coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from settings import gmail_login, gmail_pass


env = Environment(loader=FileSystemLoader('templates'))


def sendmail(mailto, template='firstmail.html', subj='', data=None):
    msg = MIMEMultipart()
    msg['From'] = gmail_login
    msg['To'] = mailto
    msg['Subject'] = subj

    template = env.get_template(template)
    code = template.render(data=data)

    msg.attach(MIMEText(code, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_login, gmail_pass)

    server.sendmail(gmail_login, mailto, msg.as_string())
    server.quit()


def smail(data, mailto):
    sendmail(
        mailto=mailto,
        subj="Анализ страницы {} по запросу {}".format(data['url'], data['query']),
        data=data,
        template='mail.html'
    )
