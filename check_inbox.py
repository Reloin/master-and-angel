import imaplib
import email
import json

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
        receiver = None
        my_message = get_decoded_email_body(body)
        my_message = my_message.decode().splitlines()
        
        #determine if email is to angel or master
        type = my_message[0].lower()
        #restore message
        my_message = '\n'.join(my_message)
        
        #determine to send to master or angle
        if "angel" in type or "天使" in type:
            print("angel\n")
            with open('angel.json') as f:
                data = json.load(f)
                master = email.utils.parseaddr(email_message["from"])
                receiver = data[master[1]]
        elif 'master' in type or "主人" in type:
            print("master\n")
            with open('master.json') as f:
                data = json.load(f)
                angel = email.utils.parseaddr(email_message["from"])
                receiver = data[angel[1]]
        else:
            receiver = email.utils.parseaddr(email_message["from"])[1]
            subject = "指令错误, command error"
            my_message = '''输入有误，请第一行必须以英文写angel或master，或不使用reply而是发新的邮件，大小写无所谓但必须是英文。抱歉为了保证没有误传才有如此措施。
            Keyword error, please include the keyword "angel" or "Master" in the first line, and try to compose a new email rather than reply, keyword is not case sensitive but must be in english. I beg my pardon as it was to ensure the email was sent to the right person.
            先此致谢 Regards
            '''

        print("subject:\t" + subject + "\n")
        print(my_message)
        
        
        break

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