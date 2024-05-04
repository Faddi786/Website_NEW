import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email, password, receiver_email, subject, message, attachment_paths=None):
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(message, 'plain'))

    # Add attachments, if any
    if attachment_paths:
        for attachment_path in attachment_paths:
            part = MIMEBase('application', 'octet-stream')
            with open(attachment_path, 'rb') as attachment_file:
                part.set_payload(attachment_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
            msg.attach(part)

    # Connect to SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
    
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python send_email.py sender_email password receiver_email subject message [attachment_path1 attachment_path2 ...]")
        sys.exit(1)

    sender_email = sys.argv[1]
    password = sys.argv[2]
    receiver_email = sys.argv[3]
    subject = sys.argv[4]
    message = sys.argv[5]
    attachment_paths = sys.argv[6:]

    send_email(sender_email, password, receiver_email, subject, message, attachment_paths)
