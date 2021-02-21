from email.header import decode_header, make_header
import email.utils
from itertools import zip_longest

def make_readable_header(header):
    """ Decode MIME header into utf-8, making it human readable
    Args:
        header (bytes, str, email.header.Header): the full or partial header.
    Returns:
        email.header.Header: the header in a human readable way.
    """
    if type(header) == email.header.Header:
        header_str =  str(header)
    elif type(header) == bytes:
        try:
            header_str = header.decode('utf-8')
        except UnicodeDecodeError:
            header_str = header.decode('latin-1')
    else:
        header_str = header
    return str(make_header(decode_header(header_str))).strip()

def make_readable_headers(headers):
    return {key: make_readable_header(headers[key]) for key in headers.keys()}

def uniq(alist):
    return list(set(alist))

def rfc_date_to_datetime(date):
    try:
        return email.utils.parsedate_to_datetime(date)
    except Exception:
        return None

def chunks(iterable: iter, n: int, fill_value=None) -> iter:
    # https://github.com/ikvk/imap_tools/blob/fb1db4aa83d8451afd627b8a7e35f72f6d1c4534/imap_tools/utils.py#L139
    """
    Group data into fixed-length chunks or blocks
    Examples:
        chunks('ABCDEFGH', 3, '?') --> [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', '?')]
        chunks([1, 2, 3, 4, 5], 2) --> [(1, 2), (3, 4), (5, None)]
    """
    return zip_longest(*[iter(iterable)] * n, fillvalue=fill_value)