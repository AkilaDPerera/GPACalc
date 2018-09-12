'''
Created on Apr 28, 2017

@author: Akila
'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(subject, message): #arg 'to' removed
    support_email = 'ezreportz@gmail.com'
    support_password = 'ezreportz12'
    
    msg = MIMEMultipart()
    msg['From'] = support_email
    msg['To'] = "akilamatrix@gmail.com" #to
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(support_email, support_password)

    mailserver.sendmail(support_email, msg['To'], msg.as_string())

    mailserver.quit()
