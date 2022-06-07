import smtplib
from email.message import EmailMessage
import random

def get_6_digit_code():
    return str(random.randrange(1_000_000)).zfill(6)


def send_code(to: str):
    port = 587  # For starttls
    smtp_server = "smtp.office365.com"

    email_address = "cyberous@outlook.co.il"
    email_password = "videochat2022"

    msg = EmailMessage()
    auth = get_6_digit_code()
    message = f'Your authentication code is {auth}.\n' \
              f'DO NOT SHARE THIS CODE WITH ANYBODY.'
    msg.set_content(message)

    msg['Subject'] = "cyberous - authentication code"
    msg['From'] = email_address
    msg['To'] = to


    # manages a connection to an SMTP server
    server = smtplib.SMTP(host=smtp_server, port=port)

    # connect to the SMTP server as TLS mode ( for security )
    server.starttls()

    # login to the email account
    server.login(email_address, email_password)

    # send the actual message
    server.send_message(msg)

    # terminates the session
    server.quit()

    return auth


if __name__ == '__main__':
    code = send_code('leeorgold123@gmail.com')
    print(code)
