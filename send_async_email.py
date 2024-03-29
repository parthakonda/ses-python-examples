import boto3

client = boto3.client('ses')

import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time

import asyncio

from email_data import EMAILS

class EmailEngine:

    def __init__(self, emails):
        self.emails = emails

    
    async def send_raw_email(self, sender, recipient, subject, body, tags, configuration_set):
        region_name = 'us-east-1'
        SENDER = sender
        RECIPIENT = recipient
        CONFIGURATION_SET = configuration_set
        SUBJECT = subject
        BODY_TEXT = body
        BODY_HTML =body
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
                Tags=tags
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print(subject)
    
    async def run(self):
        tasks = []
        for _email in self.emails:
            tasks.append(self.send_raw_email(**_email))
        data = await asyncio.gather(*tasks)
        return data

if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    runner = EmailEngine(emails=EMAILS)    
    loop.run_until_complete(runner.run())
    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))