import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import getpass
import argparse

# main function
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--sendfrom", required=True, help="Sender email address (Gmail)")
  parser.add_argument("-t", "--sendto", required=True, help="name of the text file with a list of emails that the email should send to")
  parser.add_argument("-e", "--email", required=True, help="name of the text file that includes the subject and the message")
  args = parser.parse_args()

  sender = args.sendfrom
  mailList = readMailList(args.sendto)
  email = readMessage(args.email)

  sendEmail(sender, mailList, email)

# reads a text file and returns a list of email addresses
def readMailList(file):
  mailList = []
  with open(os.path.join(file)) as f:
    for line in f.readlines():
        line = line.rstrip()
        mailList.append(line)
  return mailList

# reads a text file and returns a list with the subject and the message
def readMessage(file):
  message = []
  with open(os.path.join(file)) as f:
    for line in f:
        parts = line.split(': ')
        message.extend([parts[0], parts[1]])
  return message

# sends the email
def sendEmail(sender, receiver, email):
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
