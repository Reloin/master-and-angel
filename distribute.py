import easyimap
import imaplib
import email
import smtplib
import json

host = "imap.gmail.com"
user = None
pswd = None


with open("pwd.json") as p:
    credentials = json.load(p)
    user = credentials["email"]
    pswd = credentials["password"]

def check_mail():
    #using imaplib to read unseen emails
    imap_server = imaplib.IMAP4_SSL(host)
    imap_server.login(user, pswd)
    imap_server.select("inbox")
    _, search_data = imap_server.search(None, 'UNSEEN')
    
    #using easyimap to parse email
    imapper = easyimap.connect(host, user, pswd)

    #read all unseen email
    for num in search_data[0].split():
        #read email and separate email body
        _, data = imap_server.fetch(num, "(RFC822)")
        _, body = data[0]
        
        mail = imapper.mail(num)
        receiver = mail.body.splitlines()[0].lower()
        sender_email = email.utils.parseaddr(mail.from_addr)
        
        #determine to send to master or angle
        if "angel" in receiver or "天使" in receiver:
            with open('angel.json') as f:
                data = json.load(f)
                receiver = data[sender_email[1]]
        elif 'master' in receiver or "主人" in receiver:
            with open('master.json') as f:
                data = json.load(f)
                receiver = data[sender_email[1]]
            
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.ehlo()
        server.starttls()
        server.login(user, pswd)
        server.sendmail(user, receiver, body)
        server.quit()

check_mail()