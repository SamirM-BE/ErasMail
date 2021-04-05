from imapclient import IMAPClient, imapclient

from email.mime.multipart import MIMEMultipart
import smtplib

def send_email(sender, smtp_host, password, to, subject):
    msg = MIMEMultipart()
    msg['From'] = sender

    # create server
    server = smtplib.SMTP(host=smtp_host, port=587) #TODO: port not good, only good for gmail and outlook
    server.ehlo()
    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    

    msg['To'] = to
    msg['Subject'] = subject
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    
    print("successfully sent email to %s" % (msg['To']))

def delete_unsub_email(host, sender, password, to):
    server = IMAPClient(host)
    server.login(sender, password)
    sent_folder = server.find_special_folder(imapclient.SENT)    
    server.select_folder(sent_folder)
    messages = server.search(['TO', to])
    server.delete_messages(messages)
    server.logout