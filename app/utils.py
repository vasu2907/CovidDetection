import os
import sys
import json
import urllib3
import time
import smtplib, ssl, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_covid_email(reciever_name, reciever_email, covidResult):
    success = False
    sender_email = 'service.socialcode@gmail.com'
    sender_password = 'qpmz2907'
    curr = str(datetime.datetime.now())
    try:
        message = MIMEMultipart("alternative")
        message['Subject'] = "Account verification from SocialCode!"
        message['From'] = sender_email
        message['To'] = reciever_email

        html = f"""\
        <html>
        <body>
            <p>Hi {reciever_name},<br>
            Your Covid report detected on {datetime.datetime.now().strftime("%A")} {curr.split(' ')[0]} at {curr.split(' ')[1].split('.')[0][:-3]} is {covidResult}.
            </p>
        </body>
        </html>
        """
        part1 = MIMEText(html, "html")
        message.attach(part1)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email, reciever_email, message.as_string()
            )
    except Exception as e:
        print(f"Some error ocurred {e}")
    else:
        success = True
    return success