import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_send_email():
    sender_email = 'aditya.bhardwaj@datatheta.com'
    sender_password = 'wpjzgjgfjtxyfcdh'

    receiver_email = 'aditya.bhardwaj@datatheta.com'

    subject = 'Test Email - Notification System'
    body = 'This is a test email to confirm the email notification system is working correctly.'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Test email sent successfully to aditya.bhardwaj@datatheta.com.")
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")

if __name__ == '__main__':
    test_send_email()
