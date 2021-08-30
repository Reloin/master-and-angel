import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

mail = None
pswd = None

with open("pwd.json") as p:
    credentials = json.load(p)
    mail = credentials["email"]
    pswd = credentials["password"]
    
def send_email(content="Hello there", subject="Good day", receiver=None):
    if receiver == None:
        pass
    
    #process message
    msg = MIMEMultipart("alternative")
    msg["From"] = mail
    msg["To"] = receiver
    msg["Subject"] = subject
    
    #processing content
    txt_part = MIMEText(content, "plain")
    msg.attach(txt_part)
    msg_str = msg.as_string()
    
    #login to smtp server"
    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    server.ehlo()
    server.starttls()
    server.login(mail, pswd)
    server.sendmail(mail, receiver, msg_str)
    server.quit()

