from collections import defaultdict
import re

from imapclient import IMAPClient, imapclient
from email.parser import BytesHeaderParser
from .utils import *

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
                if type(bodystructure_header[2]) == tuple and bodystructure_header[2][1]:  # bodystructure_header[2][1] possible position du ficher 
                    # bodystructure_header[6] position de la taille
                    attachments += [ tuple((make_readable_header(bodystructure_header[2][1]), bodystructure_header[6]))] 
                elif type(part[1]) == tuple and part[1][1]: # part[1][1] possible position du ficher
                    attachments += [ tuple((make_readable_header(part[1][1]), bodystructure_header[6]))] # faire des stats
    return attachments

def get_message_id(message_id_header):
    message_id_re = re.compile('<([^>]+)>')
    message_id = message_id_re.search(make_readable_header(message_id_header))
    if message_id:
        return message_id.group(1)
    return ''

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

def get_list_unsubscribe(list_unsubscribe, list_unsubscribe_post):
    if list_unsubscribe:
        list_unsubscribe_url = re.search("<(http.*?)>", list_unsubscribe)
        list_unsubscribe_mailto = re.search("<(mailto.*?)>", list_unsubscribe)
        if list_unsubscribe_post and list_unsubscribe_url:
            return list_unsubscribe_url.group(1)
        elif list_unsubscribe_mailto:
            return list_unsubscribe_mailto.group(1)
        elif list_unsubscribe_url:
            return list_unsubscribe_url.group(1)
        elif list_unsubscribe[:6] == 'mailto' or list_unsubscribe[:4] == 'http': # in this case the header has only one field without <>
            return list_unsubscribe
    return ''

def is_undesirable_folder(folder):
    return b'\\Noselect' in folder[0] or imapclient.JUNK in folder[0] or imapclient.TRASH in folder[0] or imapclient.DRAFTS in folder[0] or imapclient.ALL in folder[0]

def fetch_messages_bulk(server, messages):

    all_to_fetch = ['BODYSTRUCTURE', 'RFC822.SIZE', 'BODY.PEEK[HEADER]', 'FLAGS']
    messages_chunked = chunks(messages, 1300)
    fetched = defaultdict()
    [fetched.update(server.fetch([i for i in chunk if i] , all_to_fetch)) for chunk in messages_chunked]
    return fetched

def get_all_emails(host, username, password):
    server = IMAPClient(host)
    server.login(username, password)

    parser = BytesHeaderParser() # Creates a header parser
    

    folders = server.list_folders()

    fetched_emails = []
    
    for folder in folders:
        if is_undesirable_folder(folder):
            continue

        selected_folder = folder[2] # (b'\\HasNoChildren',), b'/', 'INBOX')


        server.select_folder(selected_folder)
        messages = server.search(['All'])
        fetched = fetch_messages_bulk(server, messages)

        
        for msg_id, data in fetched.items():
            parsed_header = parser.parsebytes(data[b'BODY[HEADER]']) # Parse a byte structure as a dictionary structure
            parsed_header = make_readable_headers(parsed_header)
            
            sender_name, sender_email = get_sender_from_header(parsed_header.get('From', ''))

            list_unsubscribe_post = bool(parsed_header.get('List-Unsubscribe-Post', False))

            email_headers = {
                'folder' : selected_folder,
                'uid' : msg_id,
                'subject' : parsed_header.get('Subject', ''),
                'sender_name' : sender_name,
                'sender_email' : sender_email,
                'size' : data[b'RFC822.SIZE'], 
                'received_at' : rfc_date_to_datetime(parsed_header.get('Date', '')),
                'message_id' : get_message_id(parsed_header.get('Message-ID', '')),
                
                'attachments' : get_attachments(data[b'BODYSTRUCTURE']),
                'references' : get_references(parsed_header.get('References', '')),
                'in_reply_to' : get_in_reply_to(parsed_header.get('In-Reply-To', '')),

                'list_unsubscribe' : get_list_unsubscribe(parsed_header.get('List-Unsubscribe', ''), list_unsubscribe_post), # List-Unsubscribe
                'list_unsubscribe_post' : list_unsubscribe_post, # List-Unsubscribe-Post

                'seen': get_seen_flag(data[b'FLAGS']),
            }

            fetched_emails.append(email_headers)
        server.unselect_folder()
    
    server.logout()

    return fetched_emails

def move_to_trash(host, username, password, folder_uids):
    server = IMAPClient(host)
    server.login(username, password)

    trash_folder = server.find_special_folder(imapclient.TRASH)

    for folder_name, uids in folder_uids.items():
        server.select_folder(folder_name)
        server.move(uids, trash_folder)
        server.unselect_folder()

    server.logout()

if __name__ == '__main__':
    pass
    # HOST = 'imap.gmail.com'
    # USERNAME = 'test.memory.20.21@gmail.com'
    # PASSWORD = 'awdlfovxkfxcbbdb'

    # HOST = 'outlook.office365.com'
    # USERNAME = 'test.memory.20.21@outlook.be'
    # PASSWORD = 'ighymaubdccnvjxv'

    # ans = get_all_emails(HOST, USERNAME, PASSWORD)


    # print(count, count_n)
    # for e in ans:
    #     if e['list_unsubscribe']:
    #         print('-------------------------------------------------------')
    #         print('-------------------------------------------------------')
    #         print()
    #         print(e)
    #         print()