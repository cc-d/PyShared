import base64 as b64
from typing import Union


def is_jwt(s: Union[str, bytes]) -> bool:
    """Check if a string is a valid JWT (JSON Web Token).
    Args:
        s (Union[str, bytes]): Input suspected jwt bytes or string.
    Returns:
        bool: True if the input is a valid JWT, False otherwise.
    """
    # If the input is bytes, try to decode it as UTF-8
    if isinstance(s, bytes):
        try:
            s = s.decode('utf-8')
        except UnicodeDecodeError:
            return False

    parts = s.split('.')

    # A valid JWT should have exactly three parts separated by dots
    if len(parts) != 3:
        return False

    try:
        for part in parts:
            # Ensure that the part has proper padding to be a valid base64 string
            while len(part) % 4 != 0:
                part += '='
            # Attempt to decode the part as base64
            b64.urlsafe_b64decode(part)
    except ValueError:
        return False
    return True
