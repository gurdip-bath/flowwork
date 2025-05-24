import requests
import os

def send_email():

    # Check API key
    api_key = os.environ.get('RAPIDAPI_KEY')
    if not api_key:
        return {'status_code': 500, 'body': 'No API key'}
    
    # Email data
    url = "https://sendmail-ultimate-email-sender.p.rapidapi.com/send-email"
    payload = {
        "sendTo": "gurdip-singh@outlook.com",
        "replyTo": "bathgurdip1@gmail.com", 
        "isHtml": False,
        "title": "Test Email",
        "body": "Hello from FlowWork HR!"
    }
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sendmail-ultimate-email-sender.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    # Send email
    try:
        response = requests.post(url, json=payload, headers=headers)
        return {'status_code': response.status_code, 'body': response.text}
    except:
        return {'status_code': 500, 'body': 'Request failed'}