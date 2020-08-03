import smtplib
import ssl
import random
import interface as inter


def send_code(user_email, userid):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "pointshippingtest@gmail.com"
    receiver_email = user_email
    password = "Pointshipping12"
    # not good practice to save pw in code

    code = random.randint(100000, 999999)
    message = f"""\
    Subject: Point Shipping Password Recovery

    Your password recovery code is {code}"""
    try:
        resp = inter.update_code(code, userid)
        if resp:
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message)
                    return code
            except smtplib.SMTPRecipientsRefused:
                return False
            except SMTPSenderRefused:
                return False
            except SMTPDataError:
                return False
        else:
            return False