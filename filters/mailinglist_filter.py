import re

def filter_subject(mailing_lists, english_mailing_lists, subject):

    # Checking if subject contains "[]"
    if re.search(r"^Re: \[", subject) or re.search(r"\[", subject):
        with open(mailing_lists, "r") as file:
            mailing_lists = file.read()
            mailing_lists = mailing_lists.split(",")

        for mailing_list in mailing_lists:
            regex = re.compile("\[" + mailing_list + "\]")

            if re.search(regex, subject):
                return True, mailing_list
            else:
                continue
    else:
        with open(english_mailing_lists, "r") as file:
            mailing_lists = file.read()
            mailing_lists = mailing_lists.split(",")

        for mailing_list in mailing_lists:
            print(mailing_list)
            regex = re.compile(mailing_list)

            if re.search(regex, subject):
                return True, mailing_list
            else:
                continue

    return False, "None"
