from collections import defaultdict

from imapclient import IMAPClient, imapclient
from email.parser import BytesHeaderParser
from .utils import *
from .message import MailMessage



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

        
        for uid, data in fetched.items():
            parsed_header = parser.parsebytes(data[b'BODY[HEADER]']) # Parse a byte structure as a dictionary structure
            parsed_header = make_readable_headers(parsed_header)

            email_headers = MailMessage(selected_folder, uid, parsed_header.get('Subject', ''), parsed_header.get('From', ''),
                                        data[b'RFC822.SIZE'], parsed_header.get('Date', ''), parsed_header.get("Message-ID", ""), data[b'BODYSTRUCTURE'], 
                                        parsed_header.get('References', ''), parsed_header.get('In-Reply-To', ''), parsed_header.get('List-Unsubscribe', ''),
                                        parsed_header.get('List-Unsubscribe-Post', False), data[b'FLAGS'])

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
    HOST = 'imap.gmail.com'
    USERNAME = 'test.memory.20.21@gmail.com'
    PASSWORD = 'awdlfovxkfxcbbdb'

    # HOST = 'outlook.office365.com'
    # USERNAME = 'test.memory.20.21@outlook.be'
    # PASSWORD = 'ighymaubdccnvjxv'

    ans = get_all_emails(HOST, USERNAME, PASSWORD)


    for e in ans:
        print('-------------------------------------------------------')
        print('-------------------------------------------------------')
        print()
        print(e)
        print()