import os

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send_email(smtp_server, smtp_port, sender_email, receiver_email, password, subject, msg_body, attachments=None, tls=False):
    # attachments = [{'file_path': receipt_path, 'maintype': 'application', 'subtype': 'pdf'}]
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(msg_body, "html"))
    if attachments is not None:
        for a in attachments:
            # Initializing video object
            file_part = MIMEBase(a['maintype'], a['subtype'])

            # Importing video file
            file_part.set_payload(open(a['file_path'], "rb").read())

            encoders.encode_base64(file_part)
            file_name = os.path.basename(a['file_path'])
            file_part.add_header('Content-Disposition', "attachment; filename= " + file_name)

            msg.attach(file_part)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS) if tls else ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
    server.login(sender_email, password)
    result = server.sendmail(sender_email.strip(), receiver_email.strip(), msg.as_string())
    if result != {}:
        print("Error sending email:", result)
    server.quit()
