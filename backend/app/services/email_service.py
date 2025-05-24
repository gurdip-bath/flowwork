import requests
import os

def send_email():
    print("FLOWWORK EMAIL SERVICE CALLED!")
    print(f"Sending email with title: Test Email")
    
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
        "title": "Sign Documents for FlowHR",
        "body": "Hello from FlowWork HR! You've been invited to sign documents for FlowHR. Please click the link below to proceed.",
    }
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sendmail-ultimate-email-sender.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    # Send email
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"API Status Code: {response.status_code}")
        print(f"API Response Body: {response.text}")
        return {'status_code': response.status_code, 'body': response.text}
    except:
        return {'status_code': 500, 'body': 'Request failed'}