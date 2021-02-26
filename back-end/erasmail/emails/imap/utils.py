from email.header import decode_header, make_header
import email.utils
from itertools import zip_longest


def uniq(alist):
    l = []
    [l.append(x) for x in alist if x not in l]
    return l


def chunks(iterable: iter, n: int, fill_value=None) -> iter:
    # https://github.com/ikvk/imap_tools/blob/fb1db4aa83d8451afd627b8a7e35f72f6d1c4534/imap_tools/utils.py#L139
    """
    Group data into fixed-length chunks or blocks
    Examples:
        chunks('ABCDEFGH', 3, '?') --> [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', '?')]
        chunks([1, 2, 3, 4, 5], 2) --> [(1, 2), (3, 4), (5, None)]
    """
    return zip_longest(*[iter(iterable)] * n, fillvalue=fill_value)


def decode_value(value: bytes or str, encoding=None) -> str:
    """Converts value to utf-8 encoding"""
    if isinstance(encoding, str):
        encoding = encoding.lower()
    if isinstance(value, bytes):
        try:
            return value.decode(encoding or "utf-8", "ignore")
        except LookupError:  # unknown encoding
            return value.decode("utf-8", "ignore")
    return value