from imapclient import IMAPClient, imapclient
import email


HELP_STRING = """Cet email contenait une pièce jointe qui a été supprimé via ErasMail.\nLa pièce jointe s'appelait: %(filename)s"""


def set_email_payload(msg):

    fn = msg.get_filename()
    if msg.get_content_maintype() != "multipart":
        params = msg.get_params()[1:]
        params = ", ".join(["=".join(p) for p in params])
        replace = HELP_STRING % dict(filename=fn)

        if (
            msg.get_content_type() != "text/plain"
            and msg.get_content_type() != "text/html"
        ):
            msg.set_payload(replace)
            for k, v in msg.get_params()[1:]:
                msg.del_param(k)
            msg.set_type("text/plain")
            del msg["Content-Transfer-Encoding"]
            del msg["Content-Disposition"]

    else:
        if msg.is_multipart():
            payload = [set_email_payload(x) for x in msg.get_payload()]
            msg.set_payload(payload)
    # msg.set_type("text/plain")
    return msg



def remove_attachments(host, username, password, folder_uids):

    server = IMAPClient(host)
    server.login(username, password)

    # trash_folder = server.find_special_folder(imapclient.TRASH)

    for folder_name, uids in folder_uids.items():
        server.select_folder(folder_name)

        to_fetch = ["RFC822", "FLAGS", "INTERNALDATE"]
        fetched = server.fetch(uids, to_fetch)
        for uid, msg in fetched.items():
            email_message = email.message_from_bytes(msg[b"RFC822"])
            final_msg = set_email_payload(email_message)
            
            # server.move(uid, trash_folder)
            # server.expunge(uid)
            server.delete_messages(uid)
            server.append(
                folder="INBOX",
                msg=final_msg.as_string().encode(),
                flags=msg[b"FLAGS"],
                msg_time=msg[b"INTERNALDATE"],
            )
        server.unselect_folder()

    server.logout()