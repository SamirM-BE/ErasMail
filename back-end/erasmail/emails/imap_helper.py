import re

from imapclient import IMAPClient
from email.parser import BytesHeaderParser
from imap_utils import *

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
                attachments += [ tuple((bodystructure_header[2], bodystructure_header[6])) ]
    return attachments

def get_references(references_header):
    refences_re = re.compile('<([^>]+)>')
    references = refences_re.findall(make_readable_header(references_header))
    references = uniq(references)
    
    return references


def get_all_emails(host, username, password):

    # all_to_fetch =  ['BODYSTRUCTURE', 'RFC822.SIZE', 'BODY.PEEK[HEADER.FIELDS (From)]' ,'BODY.PEEK[HEADER.FIELDS (Subject)]','BODY.PEEK[HEADER.FIELDS (References)]', 'BODY.PEEK[HEADER.FIELDS (In-Reply-To)]', 'BODY.PEEK[HEADER.FIELDS (Message-ID)]', 'BODY.PEEK[HEADER.FIELDS (List-Unsubscribe)]', 'BODY.PEEK[HEADER.FIELDS (List-Unsubscribe-Post)]' ]
    all_to_fetch = ['BODYSTRUCTURE', 'RFC822.SIZE', 'BODY.PEEK[HEADER]']
    

    server = IMAPClient(host)
    server.login(username, password)

    parser = BytesHeaderParser() # Creates a header parser
    

    folders = server.list_folders()
    fetched_emails_folder = []
    
    for folder in folders:
        if b'\\Noselect' in folder[0]:
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
                'message_id' : parsed_header['Message-ID'],
                
                'attachments' : [],
                'references' : [],
                'in_reply_to' : [],
                'list_unsubscribe' : [],
                'list_unsubscribe_post' : False,
            }
           
            attachements = get_attachments(data[b'BODYSTRUCTURE'])
            if attachements:
                for attachement in attachements:
                    # [0][1] is the name in the of the attachment in the attachment part of the bodystructure
                    # [-1] is the size
                    email_headers['attachments'].append((make_readable_header(attachement[0][1]), attachement[-1])) 


            references = parsed_header.get('References', '')
            references = get_references(references)
            
            

            

        server.unselect_folder()

    
    server.logout()


get_all_emails('outlook.office365.com', 'test.memory.20.21@outlook.be', 'ighymaubdccnvjxv')



