import mongoengine

class Mails(mongoengine.Document):
    id_ = mongoengine.FloatField(required=True)
    subject_ = mongoengine.StringField(required=True)
    from_ = mongoengine.StringField(required=True)
    to_ = mongoengine.StringField(required=True)
    date_ = mongoengine.DateTimeField(required=True)
    text_ = mongoengine.StringField(required=True)
    interest_ = mongoengine.BooleanField()
    mailing_list_ = mongoengine.StringField()
    mail_account_ = mongoengine.StringField()

    meta = {'db_alias': 'core',
            'collection': 'mail_learner'}