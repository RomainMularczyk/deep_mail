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

        # Setting mail metadata format
        self.mail_id = []
        self.raw_mails = []

    @staticmethod
    def update_mails(last_mail):
        """Gets datetime of the last time mail_constructor was called and pickles it."""

        # Checking if update_file exists
        try:
            with open('filters/update', 'rb') as update_file:
                read_update = pickle.Unpickler(update_file, encoding="utf-8").load()
        except FileNotFoundError:
            pass

        with open('filters/update', 'wb') as update_file:
            update_data = pickle.Pickler(update_file)
            update_data.dump(last_mail)

        return read_update

    @staticmethod
    def check_encoding(part, content):
        """Checks MIME Content-Type charset encoding and returns mail payload decoded."""

        if part.get_content_charset() == "utf-8":
            clean_content = content.decode("utf-8")
        elif part.get_content_charset() == "us-ascii":
            clean_content = content.decode("us-ascii")
        elif part.get_content_charset() == "iso-8859-1":
            clean_content = content.decode("iso-8859-1")
        else:
            try:
                clean_content = content.decode("utf-8")
            except UnicodeDecodeError:
                clean_content = content.decode("iso-8859-1")

        return clean_content

    def search_mails(self, last_mail):
        """Looks for all the mails since last mail and returns a dict with mail
        and all its metadata."""

        result, data = self.mail.uid('search', None, last_mail)
        # list full of mail ids
        self.mail_id = data[0].decode("utf-8").split(" ")

        for _ in self.mail_id:
            result, email_data = self.mail.uid('fetch', _, '(RFC822)')
            # email_data is a tuple (mail_id, mail_content)
            raw_mail = email_data[0][1]

            raw_mail = email.message_from_bytes(raw_mail, policy=self.policy)

            self.raw_mails.append(raw_mail)

    def get_mail_plain_text(self, part):
        """Gets a mail dict and returns its body plain text."""

        plain_content = part.get_payload(decode=True)
        clean_content = self.check_encoding(part, plain_content)

        return clean_content

    def get_mail_html_text(self, part):
        """Gets a mail dict and return its body in HTML."""

        html_content = part.get_payload(decode=True)
        clean_content = self.check_encoding(part, html_content)
        # Soupifying the payload
        soup = BeautifulSoup(clean_content, "html.parser")

        return soup.get_text(strip=True)

    def get_mail_metadata(self):
        """Gets all mail data and pack them into a dict."""

        mail_metadata = []

        for id_, mail in zip(self.mail_id, self.raw_mails):

            # Data structure
            metadata = {'id': id_,
                        'from': mail['From'],
                        'to': mail['To'],
                        'subject': mail['Subject'],
                        'date': mail['Date'],
                        'text': ''}

            # Resetting mail parts list
            part_list = []

            for part in mail.walk():
                if part.is_multipart():
                    continue
                # if "html" in part.get_content_type():
                #     content = self.get_mail_html_text(part)
                #     part_list.append(content)
                elif "plain" in part.get_content_type():
                    content = self.get_mail_plain_text(part)
                    part_list.append(content)

            clean_content = "\n".join(part_list)
            metadata['text'] = clean_content
            mail_metadata.append(metadata)

        return mail_metadata
