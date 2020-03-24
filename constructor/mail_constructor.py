import imaplib
import pickle
import email
from email import policy
from bs4 import BeautifulSoup


class MailConstructor:
    """Builds mail connexion through IMAP, updates datetime and fetch mails based
    on last update."""

    def __init__(self, server, email_address, log):
        """Building connexion and getting datetime."""

        self.mail = imaplib.IMAP4_SSL(server)
        self.mail.login(email_address, log)
        self.mail.select('inbox')

        # Mail format things
        self.policy = policy.SMTP

    def search_mails(self, last_mail):
        """Looks for all the mails since last mail and returns a dict with mail
        and all its metadata."""

        result, data = self.mail.uid('search', None, last_mail)
        # list full of mail ids
        mail_id = data[0].decode("utf-8").split(" ")
        # list that gathers mail metadata
        metadata_list = []
        # list that gathers email obj
        raw_list = []

        for _ in mail_id:
            result, email_data = self.mail.uid('fetch', _, '(RFC822)')
            # email_data is a tuple (mail_id, mail_content)
            raw_mail = email_data[0][1]

            raw_mail = email.message_from_bytes(raw_mail, policy=self.policy)

            # Mail data structure

            mail_metadata = {'from': raw_mail['From'],
                             'to': raw_mail['To'],
                             'subject': raw_mail['Subject'],
                             'date': raw_mail['Date']}

            metadata_list.append(mail_metadata)
            raw_list.append(raw_mail)

        return mail_id, raw_list, metadata_list

    @staticmethod
    def update_mails(last_mail):
        """Gets datetime of the last time mail_constructor was called and pickles it."""

        # Checking if update_file exists
        try:
            with open('update', 'rb') as update_file:
                read_update = pickle.Unpickler(update_file)
        except FileNotFoundError:
            pass

        with open('update', 'wb') as update_file:
            update_data = pickle.Pickler(update_file)
            update_data.dump(last_mail)

        return read_update

    def check_encoding(self, part, content):
        """Checks MIME Content-Type charset encoding and returns mail payload decoded."""

        if part.get_content_charset() == "utf-8":
            clean_content = content.decode("utf-8")
        elif part.get_content_charset() == "us-ascii":
            clean_content = content.decode("us-ascii")
        elif part.get_content_charset() == "iso-8859-1":
            clean_content = content.decode("iso-8859-1")

        return clean_content

    def get_mail_plain_text(self, mail_id, raw_list):
        """Gets a mail dict and returns its body plain text."""

        mail_list = []
        part_list = []

        for i, mail in zip(mail_id, raw_list):

            _ = {'id': i,
                 'text': ''}

            for part in mail.walk():

                if part.is_multipart():
                    continue
                if "plain" in part.get_content_type():
                    plain_content = part.get_payload(decode=True)

                    clean_content = self.check_encoding(part, plain_content)

                    part_list.append(clean_content)
                    content = "\n".join(part_list)
                    _['text'] = content

            mail_list.append(_)

            from pprint import pprint ; pprint(mail_list)

        return mail_list

    def get_mail_html_text(self, mail_id, raw_list):
        """Gets a mail dict and return its body in HTML."""

        mail_list = []
        part_list = []

        for i, mail in zip(mail_id, raw_list):

            _ = {'id': i,
                 'text': ''}

            for part in mail.walk():

                if part.is_multipart():
                    continue
                if "html" in part.get_content_type():
                    html_content = part.get_payload(decode=True)

                    html_content = self.check_encoding(part, html_content)

            soup = BeautifulSoup(html_content, "html.parser")

            return soup.get_text()
