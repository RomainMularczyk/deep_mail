from database_modules.data_structure import Mails

from mongoengine import *

def data_last_mail():
    """Returns the latest mail saved in DB."""

    connect('mail_learner_db', alias='core')
    date_list = Mails.objects().order_by('-date_')

    return date_list[0].date_