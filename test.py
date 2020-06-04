from constructor.mail_constructor import MailConstructor
from filters.mailinglist_filter import filter_subject
from database_modules.data_structure import Mails
from database_modules.data_last_mail import data_last_mail

from mongoengine import *
from DateTime import DateTime

# Getting logs
with open('mail.txt', 'r') as log:
    log = log.read()

# Building IMAP object
test = MailConstructor(server="imap.gmail.com",
                       email_address="romain.mularczyk@gmail.com",
                       log=log)

# Getting the last mail date
last_mail = data_last_mail()
# Updating pickler to store the latest mail date value
test.update_mails(last_mail)
# Converting datetime to RFC822 format
dt = DateTime(last_mail)
rfc822_date = f"{dt.day()}-{dt.aMonth()}-{dt.year()}"
print(rfc822_date)

# Building query to request IMAP object
query = f"SINCE {rfc822_date}"

test.search_mails(query)
mail = test.get_mail_metadata()

db = connect('mail_learner_db', alias='core')

for m in mail:
    didfilter = filter_subject("filters/mailing_lists.txt",
                               "filters/english_mailing_lists.txt",
                               m['subject'])

    print(m['date'])

    if didfilter[0] is True:
        id_ = m['id']
        from_ = m['from']
        to_ = m['to']
        subject_ = m['subject']
        date_ = m['date']
        text_ = m['text']
        interest_ = ''
        mailing_list_ = didfilter[1]
        mail_account_ = "romain.mularczyk@gmail.com"

        print(subject_)

        try:
            cont_db = Mails(id_=id_,
                            from_=from_,
                            to_=to_,
                            subject_=subject_,
                            date_=date_,
                            text_=text_,
                            interest_=interest_,
                            mailing_list_=mailing_list_,
                            mail_account_=mail_account_)
            cont_db.save()
        except ValidationError:
            print(f"Field missing for email with following subject : {subject_}")

    else:
        pass
