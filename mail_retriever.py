import imaplib
import email
from email import policy
from email.contentmanager import raw_data_manager
from email.header import decode_header
import re


# ---------------- Loggy things ----------------

def logger(file):
    """Takes a filepath in input and outputs log to connect to mailserver."""

    with open(file, 'r') as log:
        log = log.read()

    return log

# ---------------- Maily things ----------------

def mail_connector(server, email_address, log):
    """Connects to imap client."""

    # Loggy things
    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_address, log)

    # Select inbox folder in Gmail
    mail.select("inbox")

    # Searching latest mails ids
    result, data = mail.uid('search', None, "SINCE 16-Mar-2020")

    # data is a one item list from which we split each mail id
    mail_id = data[0].decode("utf-8").split(" ")

    # ---------------- Fetching mails one by one ----------------

    # Here is where we pick up the emails
    for id in mail_id:
        # New search and fetching mails
        result, email_data = mail.uid('fetch', id, '(RFC822)')
        # email_data is a tuple (mail_id, mail_content)
        raw_mail = email_data[0][1]

        policy = email.policy.SMTP

        # Using MIME format to get mail infos
        mail_message = email.message_from_bytes(raw_mail, policy=policy)

        # Building mail metadata
        email_obj = {'from': mail_message['From'],
                     'to': mail_message['To'],
                     'subject': mail_message['Subject'],
                     'date': mail_message['Date']}

        print("****************")

        regex_encoding = re.compile(r"(?<=\=\?)([\w]+)")
        didmatch = re.match(regex_encoding, mail_message.get('subject'))

        print(mail_message.get('subject'))

        try:
            print(didmatch)
        except AttributeError:
            print("None")


        # ---------------- Fetching each mail part one by one ----------------

        counter = 1

        # emails have several parts, so let's iterate over those parts
        for part in mail_message.walk():

            try:
                content = part.get_content()
                print(content)
            except KeyError:
                print("multipart")

            # MIME format is "Content-Type: main_type/sub_type
            if part.get_content_maintype() == "multipart":
                continue
            filename = part.get_filename()
            if not filename:
                ext = '.html'
                filename = 'msg-part-%08d%s' % (counter, ext)
            counter += 1

            content_type = part.get_content_type()
            if "plain" in content_type:
                payload = part.get_payload(decode=True)
                print(payload)
            elif "html" in content_type:
                continue
            else:
                print("PJ : " + str(content_type))

# ------------- Launching -------------

log_data = logger('mail.txt')

email = mail_connector("imap.gmail.com", "romain.mularczyk@gmail.com", log_data)