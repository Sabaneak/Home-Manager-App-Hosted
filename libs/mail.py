from decouple import config
import sendgrid
from sendgrid.helpers.mail import *

class Send_Email:
    """
    Library to send emails via Sendgrid API.
    Env variables: API_key, From_email
    """
    SENDGRID_API_KEY = config('SENDGRID_API_KEY')
    FROM_EMAIL = config('FROM_EMAIL')

    @classmethod
    def send_email(cls, receiver, html):
        """
        Method to send email for user confirmation.
        Params: -
            receiver: The email user signs up with
            html: Text to be sent with email
        Output: Email sent
        """
        sg = sendgrid.SendGridAPIClient(cls.SENDGRID_API_KEY)
        message = Mail(
            from_email= cls.FROM_EMAIL,
            to_emails= receiver,
            subject='Confirm Email Address',
            html_content= html)
        try:
            response = sg.send(message)
        except Exception as e:
            print(e.message)

    @classmethod
    def send_reminder(cls, receiver, html, unix):
        """
        Method to send email for meetings/reminders at a particular time.
        Params: -
            receiver: The email user signs up with
            html: Text to be sent with email
            unix: Unix timestamp of time of email delivery
        Output: Email sent
        """
        sg = sendgrid.SendGridAPIClient(cls.SENDGRID_API_KEY)
        from_email = Email(cls.FROM_EMAIL)
        to_email = To(receiver)
        subject = "Meeting Reminder"
        content = Content("text/html", html)
        message = Mail(from_email, to_email, subject, content)
        message.send_at = SendAt(unix)
        
        try:
            response = sg.send(message.get())
        except Exception as e:
            print(e.message)
