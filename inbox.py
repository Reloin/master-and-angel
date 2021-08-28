import imaplib
import email
import json
from send_email import send_email

host = "imap.gmail.com"
user = None
pswd = None

with open("pwd.json") as p:
    credentials = json.load(p)
    user = credentials["email"]
    pswd = credentials["password"]

def check_mail():
    #connect to email server
    mail = imaplib.IMAP4_SSL(host)
    mail.login(user, pswd)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')

    #read all unseen email
    for num in search_data[0].split():
        receiver = None
        my_message = None
        _, data = mail.fetch(num, "(RFC822)")
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        
        #message is in 
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                my_message = body.decode()
                my_message = my_message.splitlines()
        #determine if email is to angel or master
        type = my_message[0].lower()
        #restore message
        my_message = '\n'.join(my_message)
        
        #determine to send to master or angle
        if "angel" in type:
            with open('angel.json') as f:
                data = json.load(f)
                master = email.utils.parseaddr(email_message["from"])
                receiver = data[master[1]]
        if 'master' in type:
            with open('master.json') as f:
                data = json.load(f)
                angel = email.utils.parseaddr(email_message["from"])
                receiver = data[angel[1]]

        #check exception
        if receiver == None: pass
        
        #function to send email
        send_email(my_message, email_message["subject"], receiver)

check_mail()