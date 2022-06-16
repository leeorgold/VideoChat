import os
import smtplib
from email.message import EmailMessage
import random



def get_6_digit_code():
    return str(random.randrange(1_000_000)).zfill(6)


def send_code(email: str):
    """The function gets an email address and sends it an authentication code.
    The function does not check the emails' validity.
    :param email - str. email address to send the code.
    :return auth - the authentication code sent
    """
    port = 587  # For starttls
    smtp_server = "smtp.office365.com"

    cyberous_address = "cyberous@outlook.co.il"
    cyberous_password = os.getenv('EMAIL_PASSWORD')

    msg = EmailMessage()
    auth = get_6_digit_code()
    message = f'Your authentication code is {auth}.\n' \
              f'DO NOT SHARE THIS CODE WITH ANYBODY.'
    msg.set_content(message)

    msg['Subject'] = "cyberous - authentication code"
    msg['From'] = cyberous_address
    msg['To'] = email


    # manages a connection to an SMTP server
    server = smtplib.SMTP(host=smtp_server, port=port)

    # connect to the SMTP server as TLS mode (for security)
    server.starttls()

    # login to the email account
    server.login(cyberous_address, cyberous_password)

    # send the actual message
    server.send_message(msg)

    # terminates the session
    server.quit()

    return auth


