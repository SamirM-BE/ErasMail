from imapclient import IMAPClient, imapclient

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

    