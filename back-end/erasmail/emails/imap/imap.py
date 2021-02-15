import re

from imapclient import IMAPClient, imapclient
from email.parser import BytesHeaderParser
from utils import *


# FROM header might contain a name and an email or only an email
# this functions extracts the email and the name (if possible)
def get_sender_from_header(from_header):
    redeable_from_header = make_readable_header(from_header)
    
    idx = redeable_from_header.find('<')
    if idx == -1:
        return ('', redeable_from_header)

    sender_name = redeable_from_header[0:idx].lower().strip('" ')
    sender_email = redeable_from_header[idx+1:-1].lower()

    return (sender_name, sender_email)

# BODYSTRUCTURE is a complex header containing multiple parts of informations
# This function extracts the attachment part of the bodystructure
def get_attachments(bodystructure_header):
    attachments = list()
    if type(bodystructure_header[0]) == list:
        for part in bodystructure_header[0]:
            attachments += get_attachments(part)
    else:
        for part in bodystructure_header:
            if type(part) == tuple and len(part) > 0 and (part[0] == b'attachment' or part[0] == b'ATTACHMENT'):
                attachments += [ tuple((make_readable_header(bodystructure_header[2][1]), bodystructure_header[6])) ]
    return attachments

def get_message_id(message_id_header):
    message_id_re = re.compile('<([^>]+)>')
    message_id = message_id_re.search(make_readable_header(message_id_header))
    if message_id:
        message_id = message_id.group(1)
    return message_id

def get_references(references_header):
    refences_re = re.compile('<([^>]+)>')
    references = refences_re.findall(make_readable_header(references_header))
    references = uniq(references)
    return references

def get_in_reply_to(in_reply_to_header):
    in_reply_to_re = re.compile('<([^>]+)>')
    in_reply_tos = in_reply_to_re.findall(make_readable_header(in_reply_to_header))
    in_reply_tos = uniq(in_reply_tos)
    return in_reply_tos

def get_seen_flag(flags):
    return b'\\Seen' in flags

def get_list_unsubscribe(list_unsubscribe):
    if list_unsubscribe:
        unsubscribe_splited = str(list_unsubscribe).split(',')
        list_unsubscribe =  [(re.search('<(.*)>', item).group(1)) for item in  unsubscribe_splited]
    return list_unsubscribe

def is_undesirable_folders(folder):
    return b'\\Noselect' in folder[0] or imapclient.TRASH in folder[0] or imapclient.DRAFTS in folder[0] or imapclient.JUNK in folder[0]

def get_all_emails(host, username, password):

    # all_to_fetch =  ['BODYSTRUCTURE', 'RFC822.SIZE', 'BODY.PEEK[HEADER.FIELDS (From)]' ,'BODY.PEEK[HEADER.FIELDS (Subject)]','BODY.PEEK[HEADER.FIELDS (References)]', 'BODY.PEEK[HEADER.FIELDS (In-Reply-To)]', 'BODY.PEEK[HEADER.FIELDS (Message-ID)]', 'BODY.PEEK[HEADER.FIELDS (List-Unsubscribe)]', 'BODY.PEEK[HEADER.FIELDS (List-Unsubscribe-Post)]' ]
    all_to_fetch = ['BODYSTRUCTURE', 'RFC822.SIZE', 'BODY.PEEK[HEADER]', 'FLAGS']
    

    server = IMAPClient(host)
    server.login(username, password)

    parser = BytesHeaderParser() # Creates a header parser
    

    folders = server.list_folders()

    fetched_emails = []
    
    for folder in folders:
        if is_undesirable_folders(folder):
            continue

        selected_folder = folder[2] # (b'\\HasNoChildren',), b'/', 'INBOX')
        server.select_folder(selected_folder)
        messages = server.search(['All'])
        fetched = server.fetch(messages, all_to_fetch)

        
        for msg_id, data in fetched.items():
            parsed_header = parser.parsebytes(data[b'BODY[HEADER]']) # Parse a byte structure as a dictionary structure
            
            sender_name, sender_email = get_sender_from_header(parsed_header['From'])

            email_headers = {
                'folder' : selected_folder,
                'uid' : msg_id,
                'subject' : make_readable_header(parsed_header['Subject']),
                'sender_name' : sender_name,
                'sender_email' : sender_email,
                'receiver' : username,
                'size' : data[b'RFC822.SIZE'], 
                'received_at' : parsed_header['Date'],
                'message_id' : get_message_id(parsed_header.get('Message-ID', '')),
                
                'attachments' : get_attachments(data[b'BODYSTRUCTURE']),
                'references' : get_references(parsed_header.get('References', '')),
                'in_reply_to' : get_in_reply_to(parsed_header.get('In-Reply-To', '')),

                'list_unsubscribe' : get_list_unsubscribe(parsed_header.get('List-Unsubscribe', [])), # List-Unsubscribe
                'list_unsubscribe_post' : parsed_header.get('List-Unsubscribe-Post', False), # List-Unsubscribe-Post

                'seen': get_seen_flag(data[b'FLAGS']),
            }

            fetched_emails.append(email_headers)
        server.unselect_folder()
    
    server.logout()

    return fetched_emails


HOST = 'outlook.office365.com'
USERNAME = 'test.memory.20.21@outlook.be'
PASSWORD = 'ighymaubdccnvjxv'

HOST = 'imap.gmail.com'
USERNAME = 'test.memory.20.21@gmail.com'
PASSWORD = 'awdlfovxkfxcbbdb'

ans = get_all_emails(HOST, USERNAME, PASSWORD)

for e in ans:
    print('-------------------------------------------------------')
    print('-------------------------------------------------------')
    print()
    print(e)
    print()



