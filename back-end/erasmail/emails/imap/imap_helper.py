from collections import defaultdict

from imapclient import IMAPClient, imapclient
from email.parser import BytesHeaderParser
from utils import *
from message import MailMessage


def is_undesirable_folder(folder):
    return (
        b"\\Noselect" in folder[0]
        or imapclient.JUNK in folder[0]
        or imapclient.TRASH in folder[0]
        or imapclient.DRAFTS in folder[0]
        or imapclient.ALL in folder[0]
    )


def fetch_messages_bulk(server, messages):

    all_to_fetch = [
        "ENVELOPE",
        "BODYSTRUCTURE",
        "RFC822.SIZE",
        "BODY.PEEK[HEADER.FIELDS (References)]",
        "BODY.PEEK[HEADER.FIELDS (List-Unsubscribe)]",
        "BODY.PEEK[HEADER.FIELDS (List-Unsubscribe-Post)]",
        "FLAGS",
    ]
    messages_chunked = chunks(messages, 1300)
    fetched = defaultdict()
    [
        fetched.update(server.fetch([i for i in chunk if i], all_to_fetch))
        for chunk in messages_chunked
    ]
    return fetched


def get_all_emails(host, username, password):
    server = IMAPClient(host)
    server.login(username, password)

    # parser = BytesHeaderParser()  # Creates a header parser

    folders = server.list_folders()

    fetched_emails = []

    for folder in folders:
        if is_undesirable_folder(folder):
            continue

        selected_folder = folder[2]  # (b'\\HasNoChildren',), b'/', 'INBOX')

        server.select_folder(selected_folder)
        messages = server.search(["All"])
        fetched = fetch_messages_bulk(server, messages)

        for uid, data in fetched.items():
            # parsed_header = parser.parsebytes(
            #     data[b"BODY[HEADER]"]
            # )  # Parse a byte structure as a dictionary structure
            # parsed_header = make_readable_headers(parsed_header)

            email_headers = MailMessage(
                folder,
                uid,
                data[b"FLAGS"],
                data[b"RFC822.SIZE"],
                data[b"ENVELOPE"],
                data[b"BODY[HEADER.FIELDS (REFERENCES)]"],
                data[b"BODY[HEADER.FIELDS (LIST-UNSUBSCRIBE)]"],
                data[b"BODY[HEADER.FIELDS (LIST-UNSUBSCRIBE-POST)]"],
                data[b"BODYSTRUCTURE"],
            )

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


if __name__ == "__main__":
    HOST = "imap.gmail.com"
    USERNAME = "test.memory.20.21@gmail.com"
    PASSWORD = "awdlfovxkfxcbbdb"

    # HOST = 'outlook.office365.com'
    # USERNAME = 'test.memory.20.21@outlook.be'
    # PASSWORD = 'ighymaubdccnvjxv'

    emails = get_all_emails(HOST, USERNAME, PASSWORD)

    for mail in emails:
        print(mail)
        print("_____________________________________________________")