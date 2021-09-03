import imaplib
import email
import json
from bs4 import BeautifulSoup
import html2text
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
        #read email and separate email body
        _, data = mail.fetch(num, "(RFC822)")
        _, body = data[0]
        email_message = email.message_from_bytes(body)
        subject = email_message["subject"]
        sender_email = email.utils.parseaddr(email_message["from"])[1]
        receiver = None
        
        #read email content
        my_message = get_decoded_email_body(body)
        my_message = my_message.decode()
        
        #test if message is html
        if bool(BeautifulSoup(my_message, "html.parser").find()):
            my_message = html2text.html2text(my_message)
        
        #determine if email is to angel or master
        my_message = list(filter(None, my_message.splitlines()))
        type = my_message[0].lower()
        #restore message
        my_message = '\n'.join(my_message)
        
        #determine to send to master or angle
        if "angel" in type or "天使" in type:
            with open('angel.json') as f:
                data = json.load(f)
                receiver = data[sender_email]
        elif 'master' in type or "主人" in type:
            with open('master.json') as f:
                data = json.load(f)
                receiver = data[sender_email]
        else:
            receiver = sender_email
            subject = "指令错误, command error"
            my_message = '''读取为"{}"。
输入有误，请第一行必须以英文写angel或master，大小写无所谓。抱歉为了保证没有误传才有如此措施。若您已照着指示书写，那可能是解读问题，非常抱歉我会尽快修复的。
Keyword error, please include the keyword "angel" or "Master" in the first line, keyword is not case sensitive. I beg your pardon as it was to ensure the email was sent to the right person. 
If you had followed the instructions written, then it probably has to do with decoding, I will fix it ASAP, sorry.
先此致谢 Regards
            '''.format(type)

        #check exception
        if receiver == None: 
            print("error with: {}".format(sender_email))
            with open("error_log.txt", "a") as f:
                f.write(email.utils.parseaddr(email_message["from"]))
                print("\n")
            continue
        
        #function to send email
        send_email(my_message, subject, receiver)

#universal decoder to decode emails
def get_decoded_email_body(message_body):
    """ Decode email body.
    Detect character set if the header is not set.
    We try to get text/plain, but if there is not one then fallback to text/html.
    :param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
    :return: Message body as unicode string
    """

    msg = email.message_from_bytes(message_body)

    text = ""
    if msg.is_multipart():
        html = None
        for part in msg.get_payload():

            if part.get_content_charset() is None:
                # We cannot know the character set, so return decoded "something"
                text = part.get_payload(decode=True)
                continue

            charset = part.get_content_charset()

            if part.get_content_type() == 'text/plain':
                text = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

            if part.get_content_type() == 'text/html':
                html = str(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')

        if text is not None:
            return text.strip()
        else:
            return html.strip()
    else:
        text = str(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        return text.strip()

check_mail()