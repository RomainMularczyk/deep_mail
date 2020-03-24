from constructor.mail_constructor import MailConstructor

with open('mail.txt', 'r') as log:
    log = log.read()

test = MailConstructor(server="imap.gmail.com",
                       email_address="romain.mularczyk@gmail.com",
                       log=log)

shit_id, shitmail, shitprint = test.search_mails('SINCE 23-Mar-2020')
shittext = test.get_mail_html_text(shit_id, shitmail)