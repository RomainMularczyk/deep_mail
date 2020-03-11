import smtplib

smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
smtp_obj.ehlo()
smtp_obj.starttls()

with open('mail.txt', 'r') as log:
    log = log.read()

smtp_obj.login('romain.mularczyk@gmail.com', log)

for i in range(1, 1):
    smtp_obj.sendmail('romain.mularczyk@gmail.com',
                      'laurie.floucat@gmail.com',
                      'Subject: BOUM ! RoroBot greeting you for the {}rd time ! :)\n\
                      Hey, This is RoroBot just walking by, stopped to say hi :) Bisous ! <3.'.format(i))

smtp_obj.quit()