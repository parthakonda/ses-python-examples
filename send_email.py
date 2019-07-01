import boto3

client = boto3.client('ses')

import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_raw_email():
    region_name = 'us-east-1'
    SENDER = "Name <email>"
    RECIPIENT = "email"
    CONFIGURATION_SET = "ses-events"
    SUBJECT = "Test Email - 1"
    BODY_TEXT = "Hello,\r\nThis content is from an automated script"
    BODY_HTML = """\
        <html>
        <head></head>
        <body>
        <h1>Hello - 1!</h1>
        <p>This content is from an automated script.</p>
        </body>
        </html>
    """
    CHARSET = "utf-8"
    client = boto3.client('ses',region_name=region_name)
    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg['Reply-To'] = SENDER
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    msg.attach(msg_body)
    msg.add_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
    msg.add_header('Cache - Control', 'post - check = 0, pre - check = 0')
    msg.add_header('Pragma', 'no-cache')
    try:
        #Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data':msg.as_string(),
            },
            ConfigurationSetName=CONFIGURATION_SET,
            Tags=[{
                'Name': "Customer",
                "Value": "my_cusstomer"
            }]
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:")
        print(response['MessageId'])

send_raw_email()