from .utils import *
import re

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

class MailMessage:
    def __init__(self, folder, uid, subject, sender, size, received_at, message_id, attachments, references, in_reply_to, list_unsubscribe, list_unsubscribe_post, seen):
        self.folder = folder
        self.uid = uid
        self.subject = subject
        self.sender_name, self.sender_email = get_sender_from_header(sender)
        self.size = size 
        self.received_at = rfc_date_to_datetime(received_at)
        self.message_id = get_message_id(message_id)
        self.attachments = get_attachments(attachments)
        self.references = get_references(references)
        self.in_reply_to = get_in_reply_to(in_reply_to)
        self.list_unsubscribe = get_list_unsubscribe(list_unsubscribe, list_unsubscribe_post)
        self.list_unsubscribe_post = bool(list_unsubscribe_post)
        self.seen = get_seen_flag(seen)

    def __str__(self):
        return str({
                "folder": self.folder,
                "uid": self.uid,
                "subject": self.subject,
                "sender_name": self.sender_name,
                "sender_email": self.sender_email,
                "size": self.size,
                "received_at": self.received_at,
                "message_id": self.message_id,
                "attachments": self.attachments,
                "references": self.references,
                "in_reply_to": self.in_reply_to,
                "list_unsubscribe": self.list_unsubscribe,  # List-Unsubscribe
                "list_unsubscribe_post": self.list_unsubscribe_post,  # List-Unsubscribe-Post
                "seen": self.seen,
            })

        
        