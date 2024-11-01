import logging
import os
import sys
import smtplib
import pickle
import base64
from . import gpt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

# Define app directory
app_dir = os.path.dirname(__file__)

# Logging setup
log_path = os.path.join(app_dir, "smtp_oauth_python_gmail.log")
fh = logging.FileHandler(filename=log_path)
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
handlers = [fh, sh]
logging.basicConfig(format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    handlers=handlers)
logger = logging.getLogger('email_setup')
logger.setLevel(logging.INFO)
logger.info('start ' + __file__)

# SMTP configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_EMAIL = "snehasingh0515@gmail.com"
RECIPIENT = "adityasingha.4321@gmail.com"
SCOPES = ['https://mail.google.com/']

def gmail_authenticate():
    logging.info("In gmail_authenticate, refreshing token.pickle as needed")
    creds = None
    token_file = os.path.join(app_dir, "token.pickle")

    # Check if token.pickle exists
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            logger.info("Reading creds from pickle")
            creds = pickle.load(token)

    # If no valid credentials available, log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as e:
                logger.error(f"Error refreshing token: {e}")
        else:
            logger.info("Creating flow, creating server")
            logger.info("GOOGLE REQUIRES REAUTHENTICATION - run this step on a machine with GUI Browser")
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(app_dir, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_file, "wb") as token:
                logger.info("Saving the credentials for the next run")
                pickle.dump(creds, token)
    
    logger.info(creds)
    return creds.token

def send_smtp_oauth(recipient, subject, content):
    """
    Sends an email using the latest OAUTH bearer token information
    """
    logger.info("In send_smtp_oauth, attempting gmail authenticate")
    token = gmail_authenticate()
    logger.info("gmail_authenticate completed")

    # Create MIMEText Email
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html'))  # 'html' ensures the content is treated as HTML

    # Connect to Gmail Server
    logger.info("Creating smtp session")
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    auth_string = b'user=' + bytes(f"{SMTP_EMAIL}", 'ascii') + b'\1auth=Bearer ' + token.encode() + b'\1\1'
    logger.info("Sending auth string")
    code, msg_response = session.docmd('AUTH', 'XOAUTH2 ' + (base64.b64encode(auth_string)).decode('ascii'))

    # Check if authentication was successful
    if code != 235:
        logger.error(f"SMTP Authentication failed: {msg_response}")
        return

    # Send Email & Exit
    logger.info("Sending email")
    session.sendmail(SMTP_EMAIL, recipient, msg.as_string())
    session.quit()

def create_mail_content():
    subject = "This is header"
    print(subject)
    response = gpt.gpt_response()
    print(response)
    body = f"<pre>{response}</per>"
    # body = """<pre>hello
    # i am trying to properly format this string
    # lets see if its working this way
    # date:                          monday 
    # sign                           aditya singh
    # </pre>
    # """  # Using <pre> tag to preserve whitespace and formatting
    return subject, body

if __name__ == '__main__':
    subject, e_body = create_mail_content()
    print(subject,e_body)
    send_smtp_oauth(RECIPIENT, subject, e_body)
