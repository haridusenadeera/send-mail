# send-mail
Send emails with Gmail as provider using python SMTP module
# Usage

**list.txt** - contains a list of email addresses that you want to send your email to.

**email.txt** - contains the email you want to send. 

### Email (email.txt) format

````
Subject: Body
````

#### example

````
Test Email: This is a test. 
````

run the following command from the command line.

`python send-mail.py -f your-email@gmail.com -t list.txt -e email.txt`
