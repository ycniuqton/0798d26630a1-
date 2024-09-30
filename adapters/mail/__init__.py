import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, smtp_server, port, login, password):
        self.smtp_server = smtp_server
        self.port = port
        self.login = login
        self.password = password

    def send(self, sender_email, receiver_email, subject, body, is_html=False):
        """
        Sends an email based on the content type (plain text or HTML).
        :param sender_email: Sender's email address.
        :param receiver_email: Receiver's email address.
        :param subject: Subject of the email.
        :param body: Body of the email (plain text or HTML).
        :param is_html: Boolean to indicate if the body is HTML. Defaults to False (plain text).
        """
        if is_html:
            self._send_html_email(sender_email, receiver_email, subject, body)
        else:
            self._send_text_email(sender_email, receiver_email, subject, body)

    def _send_text_email(self, sender_email, receiver_email, subject, body):
        """Private method to send a plain text email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                server.login(self.login, self.password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print(f"Text email sent successfully to {receiver_email}")

        except Exception as e:
            print(f"Failed to send text email. Error: {e}")

    def _send_html_email(self, sender_email, receiver_email, subject, body):
        """Private method to send an HTML email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP_SSL(self.smtp_server, self.port) as server:
                server.login(self.login, self.password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print(f"HTML email sent successfully to {receiver_email}")

        except Exception as e:
            print(f"Failed to send HTML email. Error: {e}")
