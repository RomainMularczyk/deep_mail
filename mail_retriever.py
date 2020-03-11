import imaplib
import email


def logger(file):
    """Takes a filepath in input and outputs log to connect to mailserver."""

    with open(file, 'r') as log:
        log = log.read()

    return log


def mail_connector(server, email_address, log):
    """Connects to imap client."""

    # Loggy things
    mail = imaplib.IMAP4_SSL(server)
    mail.login(email_address, log)

    # Select inbox folder in Gmail
    mail.select("inbox")

    # Searching latest mails
    result, data = mail.uid('search', None, "SINCE 11-Mar-2020")
    # Let's take just the first mail out of the list
    mail_id = data[0].decode("utf-8").split(" ")
    mail_id = mail_id[0]

    print(mail_id)

    # New search and fetching mails
    result, email_data = mail.uid('fetch', mail_id, '(RFC822)')
    # email_data is a tuple (mail_id, mail_content)
    raw_mail = email_data[0][1]

    # Using MIME format to get mail infos
    mail_message = email.message_from_bytes(raw_mail)

    # Building mail metadata
    email_obj = {'from': mail_message['From'],
                 'to': mail_message['To'],
                 'subject': mail_message['Subject'],
                 'date': mail_message['Date']}

    counter = 1

    # emails have several parts, so let's iterate over those parts
    for part in mail_message.walk():
        # MIME format is "Content-Type: main_type/sub_type
        if part.get_content_maintype() == "multipart":
            continue
        filename = part.get_filename()
        if not filename:
            ext = '.html'
            filename = 'msg-part-%08d%s' % (counter, ext)
        counter += 1
        print(filename)

    content_type = part.get_content_type()
    if "plain" in content_type:
        print(part.get_payload())
    elif "html" in content_type:
        print("do some BS4")
    else:
        print(content_type)

    print(email_obj)

# ------------- Launching -------------

log_data = logger('mail.txt')

email = mail_connector("imap.gmail.com", "romain.mularczyk@gmail.com", log_data)
