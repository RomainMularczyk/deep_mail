import imaplib
import base64
import os
import email

# -------------- Secret things --------------
email_user = input('Email : ')
email_password = input('Password : ')

# -------------- Loggy things --------------
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(email_user, email_password)
mail.select('inbox')

# -------------- Searching mails --------------
is_ok, data = mail.search(None, 'SINCE 11-Mar-2020')
mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    # data comes back as a list with one item, so we have to take data[0]
    # data[0] is then a tuple with (mail_id, mail_content)
    raw_email = data[0][1]
    string_email = raw_email.decode('utf-8')
    email_message = email.message_from_string(string_email)

    email_obj = {'from': email_message['From'],
                 'to': email_message['To'],
                 'subject': email_message['Subject'],
                 'date': email_message['Date']}

    print(email_obj)