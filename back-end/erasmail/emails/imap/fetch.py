from imapclient import IMAPClient, imapclient

from .message import MailMessage
from .utils import *


def is_undesirable_folder(folder):
    return (
        b"\\Noselect" in folder[0]
        or b'\\Important' in folder[0]
        or imapclient.JUNK in folder[0]
        or imapclient.TRASH in folder[0]
        or imapclient.DRAFTS in folder[0]
        or imapclient.ALL in folder[0]
        or imapclient.FLAGGED in folder[0]
    )


def fetch_messages_bulk(server, messages, to_fetch):
    THRESHOLD = 1600

    messages_chunked = chunks(messages, THRESHOLD)
    for chunk in messages_chunked:
        fetched = server.fetch([i for i in chunk if i], to_fetch)
        for uid, data in fetched.items():
            yield uid, data

def fetch_messages(server, messages, to_fetch):

    fetched = server.fetch(messages, to_fetch)
    return ((uid, data) for uid, data in fetched.items())


def get_emails_count(host, username, password):
    server = IMAPClient(host)
    server.login(username, password)

    total = 0
    for folder in server.list_folders():
        if is_undesirable_folder(folder):
            continue
        
        res = server.select_folder(folder[2], readonly=True)
        total += int(res[b'EXISTS'])     

    server.logout()

    return total


def get_emails(host, username, password):
    server = IMAPClient(host)
    server.normalise_times = False
    server.login(username, password)

    # parser = BytesHeaderParser()  # Creates a header parser

    folders = server.list_folders()

    for folder in folders:
        if is_undesirable_folder(folder):
            continue


        selected_folder = folder[2]  # (b'\\HasNoChildren',), b'/', 'INBOX')

        server.select_folder(selected_folder)
        messages = server.search(["All"])

        all_to_fetch = [
            "ENVELOPE",
            "BODYSTRUCTURE",
            "RFC822.SIZE",
            "BODY.PEEK[HEADER.FIELDS (References)]",
            "BODY.PEEK[HEADER.FIELDS (List-Unsubscribe)]",
            "BODY.PEEK[HEADER.FIELDS (List-Unsubscribe-Post)]",
            "FLAGS",
        ]

        if host == "imap.gmail.com":
            fetched = fetch_messages(server, messages, all_to_fetch)
        else:
            fetched = fetch_messages_bulk(server, messages, all_to_fetch)

        for uid, data in fetched:
            # parsed_header = parser.parsebytes(
            #     data[b"BODY[HEADER]"]
            # )  # Parse a byte structure as a dictionary structure
            # parsed_header = make_readable_headers(parsed_header)
            email_headers = MailMessage(
                selected_folder,
                uid,
                data[b"FLAGS"],
                data[b"RFC822.SIZE"],
                data[b"ENVELOPE"],
                data[b"BODY[HEADER.FIELDS (REFERENCES)]"],
                data[b"BODY[HEADER.FIELDS (LIST-UNSUBSCRIBE)]"],
                data[b"BODY[HEADER.FIELDS (LIST-UNSUBSCRIBE-POST)]"],
                data[b"BODYSTRUCTURE"],
            )

            yield email_headers.to_dict()
        server.unselect_folder()

    server.logout()
