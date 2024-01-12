import base64 as b64
from typing import Union
import json


def _pad(s: str) -> str:
    """
    Pad a string with '=' to make it base64 decodable.
    Args:
        s (str): Input string.
    Returns:
        str: The padded string.
    """
    padding = len(s) % 4
    return s if padding == 0 else s + '=' * (4 - padding)


def is_jwt(s: Union[str, bytes]) -> bool:
    """
    Check if a string is a valid JWT (JSON Web Token).
    Args:
        s (Union[str, bytes]): Input suspected JWT bytes or string.
    Returns:
        bool: True if the input is a valid JWT, False otherwise.
    """
    try:
        if isinstance(s, bytes):
            s = s.decode('utf-8')

        segments = s.split('.')
        if len(segments) != 3:
            return False

        # Decoding header and payload to check if they are valid JSON
        header, payload, signature = segments
        json.loads(b64.urlsafe_b64decode(_pad(header)).decode('utf-8'))
        json.loads(b64.urlsafe_b64decode(_pad(payload)).decode('utf-8'))

        # Rudimentary check for signature length
        if (
            len(signature) < 10
        ):  # Minimum length for a JWT signature is typically more than 10 characters
            return False

        return True
    except Exception:
        return False
