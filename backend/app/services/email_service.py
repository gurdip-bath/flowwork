import sendgrid
import os
from sendgrid.helpers.mail import *

def send_email():
    """
    Send a basic email using SendGrid.
    """
    # Set up SendGrid client
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('ac03d73574msh8a39254c86dcb9dp174941jsne7d9accb70ba'))
    from_email = Email("bathgurdip1@gmail.com")
    to_email = To("gurdip-singh@outlook.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)

    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)
    print(response.body)
    print(response.headers)

    return {
        'status_code': response.status_code,
        'body': response.body,
        'headers': response.headers
    }

    #TODO - integrate SendMail instead as SendGrid has an issue with it's API on RapidAPI.