import argparse
import getpass
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


# main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--sendfrom",
                        required=True, help="Sender email address (Gmail)")
    parser.add_argument("-t", "--sendto",
                        required=True,
                        help="name of the text file with a list of emails that \
                              the email should send to")
    parser.add_argument("-b", "--body",
                        default="This is a test to validate your email address. Please \
                                  disregard this message.",
                        help="email body plain text")
    parser.add_argument("-s", "--smtp-server",
                        default='smtp.gmail.com',
                        help="SMTP server")
    parser.add_argument("-p", "--smtp-port",
                        default=587,
                        help="SMTP server port")
    args = parser.parse_args()

    sender = args.sendfrom
    mail_list = read_mail_list(args.sendto)
    email = read_message(args.email)

    send_email(sender, mail_list, email)


# reads a text file and returns a list of email addresses
def read_mail_list(file):
    mail_list = []
    with open(os.path.join(file)) as f:
        for line in f.readlines():
            line = line.rstrip()
            mail_list.append(line)
    return mail_list


# reads a text file and returns a list with the subject and the message
def read_message(file):
    message = []
    with open(os.path.join(file)) as f:
        for line in f:
            parts = line.split(': ')
            message.extend([parts[0], parts[1]])
    return message


# sends the email
def send_email(sender, receiver, email):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(receiver)
    msg['Subject'] = email[0]

    msg.attach(MIMEText(email[1], 'plain'))

    pswd = getpass.getpass('Password: ')

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, pswd)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        print "Email sent successfully"
    except smtplib.SMTPRecipientsRefused, e:
        print e.recipients
    finally:
        server.quit()

if __name__ == "__main__":
    main()
