
# AWS SES (developer analysis)
- ## Understanding SES
- ## Understanding Sandbox Mode
- ## Steps to follow
  - ### Verifying Domain
  - ### Verifying Email
- ## Understanding Notification for an Identity
- ## Setting up Notification for an Identity
- ## Understanding ConfigurationSets
- ## Steps to follow to configure the webhook events
- ## Understanding Supression List
<br >

# Understanding SES
Simple Email Service is an email service provided by AWS where we've provision for both send and recieve emails.

- Sending emails<br>
There 3 different ways to send an email to given list of recipients.

    1. Using SES Console
    2. Using SES Api
    3. Using SMTP Credentials
- Recieving emails<br>

    To recieve emails you need to do following things

    1. Add proper MX records
    2. Verify your domain
    3. Verify your identity
    4. Create Rule Set with recipient
    5. Add Action

# Understanding Sandbox Mode
By default, SES comes in sandbox mode. And there are certain restrictions will be applied if ses in sandbox mode.

- You can only send mail to verified email addresses and domains, or to the Amazon SES mailbox simulator.

- You can only send mail from verified email addresses and domains.

    Note

    This restriction applies even when your account isn't in the sandbox.

- You can send a maximum of 200 messages per 24-hour period.

- You can send a maximum of 1 message per second.

# Steps to follow

- ## Verifying domain
    In order to send emails, we need to have a from email address and that should be verified by SES. 
    
    But in case you've dynamically added email address then it will be always a challenge to verify the email address. In this case, instead of verifying individual email address you can verify a domain.

- ## Verifying email
    As mentioned above, you need to verify your email address before sending any emails to outside. Once you add an entry of email then SES will send the confirmation email to the specified email address, and recipient need to confirm the subscription.

# Understanding Notification for and Identity
There are 3 different notifications that are required to be addressed.

- Bounce Notification

  There are 2 types of Bounce events avaialble, one is soft bounce and another one hard bounce.
  
  Soft Bounce -  A soft bounce is an e-mail message that gets as far as the recipient's mail server but is bounced back undelivered before it gets to the intended recipient. A soft bounce might occur because the recipient's inbox is full.
  
  Hard Bounce - A hard bounce is an e-mail message that has been returned to the sender because the recipient's address is invalid. A hard bounce might occur because the domain name doesn't exist or because the recipient is unknown.
  
  It is very important to not send the emails to bounced emails. If you send emails to soft/hard bounced emails then your reputation will gp down and your ISP's will not send your emails.

  So, in order to prepare a blocked emails list SES provinding a way through notifying the emails such are bouced. AWS providing SNS interface to publish these messages. You can provide a SNS topic to get notified whenever there is a Bounce event occured.

- Complaint Notification

    A complaint occurs when a recipient reports that they don't want to receive an email. They might have clicked the "Report spam" button in their email client, complained to their email provider, notified Amazon SES directly, or through some other method. 

    The emails who got `marked as spam` or recieved as complaint then we should immediately stop sending emails to them. If you do send even after the complaint then your reputation will go down.

- Delivery Notification

    When SES successfully delivers your email then it will publish a record with the details. This is used to track the activity

# Setting up Notification for an Identity or Domain
You can setup Bounce, Complaint and Delivery Notification for both Domain and an individual identity. The provision aws is providing is in the form of SNS topic.

You can point to different SNS topics for different events(Bounce, Complaint and Delivery)

# Understanding ConfigurationSets

- What are Configuration Sets?

    A group of rules that you can apply while sending the emails.

- When to use them?
    Just include the name of the configuration set while sending the email.

- What are these rules about?

    These rules are describing about 2 things
    - Event Publishing
    - IP Pool Management

    
    - Event Publishing

        We've discussed about Email Notifications such as `bounce`, `complaint` and `delivery` for an identity. However, there are different events that we can recieve from the server about email activity such as following

        - Bounce
        - Complaint
        - Delivery
        - Send
        - Reject
        - Open
        - Click
        - Rendering Failure

        In order to recieve this email activity, you must create a configuration sets with this rule.
    
    - IP Pooling

        If you lease dedicated IP addresses to use with Amazon SES, you can create groups of these addresses, called dedicated IP pools. You can then associate these dedicated IP pools with configuration sets. A common use case is to create one pool of dedicated IP addresses for sending marketing communications, and another for sending transactional emails. Your sender reputation for transactional emails is then isolated from that of your marketing emails.

# Steps to follow to configure the webhook events

As mentioned above, if you want to recieve an email activity you should configure the Configuration Sets, you can specify different destinations for the configuration sets. There are following destinations available.

- CloudWatch
- Firehose
- SNS

So that, you can publish your email activity messages to the above destinations. However, if you want these messages to be recieved by your webserver as webhook then you can configure a SNS topic. And should create a subscription of webhook.

# Understanding Supression List
Amazon SES maintains a suppression list of recipient email addresses that have recently caused a hard bounce for any Amazon SES customer. If you try to send an email through Amazon SES to an address that is on the suppression list, the call to Amazon SES succeeds, but Amazon SES treats the email as a hard bounce instead of attempting to send it. Like any hard bounce, suppression list bounces count towards your sending quota and your bounce rate. An email address can remain on the suppression list for up to 14 days.