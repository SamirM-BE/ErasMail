from email.header import decode_header, make_header
import email.utils
import time
import datetime

def make_readable_header(header_byte):
    """ Decode MIME header into utf-8, making it human readable
    Args:
        header_byte (byte): the full or partial header.
    Returns:
        email.header.Header: the header in a human readable way.
    """
    if type(header_byte) == str:
        header_str = header_byte
    else:
        try:
            header_str = header_byte.decode('utf-8')
        except UnicodeDecodeError:
            header_str = header_byte.decode('latin-1')
        
    return str(make_header(decode_header(header_str))).strip()

def uniq(alist):
    #set = {}
    #return [set.setdefault(e,e) for e in alist if e not in set.keys()]
    return list(set(alist))

def convert_to_datetime(date):
    a = email.utils.parsedate(date)
    b = time.mktime(a)
    c = datetime.datetime.fromtimestamp(b)

    return c