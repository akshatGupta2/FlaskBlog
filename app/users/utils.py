import base64
import secrets
from flask import url_for, current_app
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
from os import environ
from PIL import Image

from email.message import EmailMessage


SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def save_picture(form_picture):
    random_hx = secrets.token_hex(8)
    _, fext = os.path.splitext(form_picture.filename)
    final_name = random_hx + fext
    img_path = os.path.join(current_app.root_path, 'static/profile_pic', final_name)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.save(img_path)
    i.thumbnail(output_size)
    return final_name


def get_creds():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=5000, access_type="offline", prompt="consent")
        # Save the credentials for future use
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())
    return creds


def send_reset_email(user):
    token=user.get_reset_token()
    msg:str = f'''
    To reset ur password visit the following link {url_for('users.reset_password', token=token, _external=True)}
    
    If u did not intend to then ignore
    '''
    creds=get_creds()
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        
        message=EmailMessage()
        message.set_content(msg)
        message['To']=user.email
        message['From']="noreply@demo.com"
        message['Subject']="Password Reset Request"
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message
    