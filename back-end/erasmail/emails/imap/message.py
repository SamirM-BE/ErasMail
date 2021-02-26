from utils import *
import re
from email.header import decode_header
from email.parser import BytesHeaderParser

parser = BytesHeaderParser()  # Creates a header parser


# BODYSTRUCTURE is a complex header containing multiple parts of informations
# This function extracts the attachment part of the bodystructure
def get_attachments(bodystructure_header):
    attachments = list()
    if type(bodystructure_header[0]) == list:
        for part in bodystructure_header[0]:
            attachments += get_attachments(part)
    else:
        for part in bodystructure_header:
            if (
                type(part) == tuple
                and len(part) > 0
                and (part[0] == b"attachment" or part[0] == b"ATTACHMENT")
            ):
                if (
                    type(bodystructure_header[2]) == tuple
                    and bodystructure_header[2][1]
                ):  # bodystructure_header[2][1] possible position du ficher
                    # bodystructure_header[6] position de la taille
                    attachment_name = decode_header(bodystructure_header[2][1].decode())
                    attachment_name = decode_value(
                        attachment_name[0][0], attachment_name[0][1]
                    )
                    attachments += [
                        tuple(
                            (
                                attachment_name,
                                bodystructure_header[6],
                            )
                        )
                    ]
                elif (
                    type(part[1]) == tuple and part[1][1]
                ):  # part[1][1] possible position du ficher
                    attachment_name = decode_header(part[1][1].decode())
                    attachment_name = decode_value(
                        attachment_name[0][0], attachment_name[0][1]
                    )
                    attachments += [
                        tuple(
                            (
                                attachment_name,
                                bodystructure_header[6],
                            )
                        )
                    ]
    return attachments


# FROM header might contain a name and an email or only an email
# this functions extracts the email and the name (if possible)
def get_sender_from_header(from_header):
    redeable_from_header = decode_value(decode_header(from_header))

    idx = redeable_from_header.find("<")
    if idx == -1:
        return ("", redeable_from_header)

    sender_name = redeable_from_header[0:idx].lower().strip('" ')
    sender_email = redeable_from_header[idx + 1 : -1].lower()

    return (sender_name, sender_email)


def get_message_id(message_id_header):
    if message_id_header:
        message_id = decode_header(message_id_header.decode())
        message_id_re = re.compile("<([^>]+)>")
        message_id = message_id_re.search(
            decode_value(message_id[0][0], message_id[0][1])
        )
        if message_id:
            return message_id.group(1)
        else:
            return ""
    return ""


def get_references(references_header):
    refences_re = re.compile("<([^>]+)>")
    references = decode_header(str(references_header))
    references = refences_re.findall(decode_value(references[0][0], references[0][1]))
    references = uniq(references)
    return references


def get_in_reply_to(in_reply_to_header):
    if in_reply_to_header:
        in_reply_tos = decode_header(in_reply_to_header.decode())
        in_reply_to_re = re.compile("<([^>]+)>")
        in_reply_tos = in_reply_to_re.findall(
            decode_value(in_reply_tos[0][0], in_reply_tos[0][1])
        )
        return uniq(in_reply_tos)
    else:
        return []


def get_seen_flag(flags):
    return b"\\Seen" in flags


def get_list_unsubscribe(list_unsubscribe, list_unsubscribe_post):
    list_unsubscribe = str(list_unsubscribe)
    if list_unsubscribe:
        list_unsubscribe_url = re.search("<(http.*?)>", list_unsubscribe)
        list_unsubscribe_mailto = re.search("<(mailto.*?)>", list_unsubscribe)
        if list_unsubscribe_post and list_unsubscribe_url:
            return list_unsubscribe_url.group(1)
        elif list_unsubscribe_mailto:
            return list_unsubscribe_mailto.group(1)
        elif list_unsubscribe_url:
            return list_unsubscribe_url.group(1)
        elif (
            list_unsubscribe[:6] == "mailto" or list_unsubscribe[:4] == "http"
        ):  # in this case the header has only one field without <>
            return list_unsubscribe
    return ""


def get_subject(subject_header) -> str:
    if subject_header:
        msg_subject = decode_header(subject_header.decode())
        return decode_value(msg_subject[0][0], msg_subject[0][1])
    else:
        return ""


def get_sender_name(from_header) -> str:
    if from_header:
        msg_sender_name = decode_header(from_header.decode())
        return decode_value(msg_sender_name[0][0], msg_sender_name[0][1])
    else:
        return ""


def get_sender_email(mailbox, host) -> str:
    if mailbox and host:
        return mailbox.decode() + "@" + host.decode()
    else:
        return ""


class MailMessage:
    def __init__(
        self,
        folder,
        uid,
        flags,
        size,
        envelope,
        references,
        list_unsubscribe,
        list_unsubscribe_post,
        bodystructure,
    ):
        self.folder = folder
        self.uid = uid
        self.seen = get_seen_flag(flags)
        self.size = size
        self.subject = get_subject(envelope.subject)
        self.sender_name = get_sender_name(envelope.from_[0].name)
        self.sender_email = get_sender_email(
            envelope.from_[0].mailbox, envelope.from_[0].host
        )
        self.received_at = envelope.date
        self.message_id = get_message_id(envelope.message_id)
        self.in_reply_to = get_in_reply_to(envelope.in_reply_to)  # [] if none
        self.references = get_references(references)  # [] if none
        self.list_unsubscribe = get_list_unsubscribe(list_unsubscribe, list_unsubscribe)
        self.list_unsubscribe_post = b"One-Click" in list_unsubscribe_post
        self.attachments = get_attachments(bodystructure)

    def __str__(self):
        return str(
            {
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
            }
        )
