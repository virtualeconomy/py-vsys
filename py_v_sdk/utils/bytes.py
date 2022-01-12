"""
bytes contains utility functions related to bytes
"""

import base58


def bytes_to_int(b: bytes) -> int:
    """
    bytes_to_int converts the given bytes to an integer
    E.g.
    b'\xaa\xbb' => ['aa', 'bb'] => 'aabb' => 43707

    Args:
        b (bytes): The bytes to convert

    Returns:
        int: The conversion result
    """
    hex_list = [bytes([i]).hex() for i in b]
    return int("".join(hex_list), 16)


def bytes_to_str(b: bytes) -> str:
    """
    bytes_to_str converts the given bytes to a string

    Args:
        b (bytes): The bytes to convert

    Returns:
        str: The conversion result
    """
    return b.decode("latin-1")


def bytes_to_b58_str(b: bytes) -> str:
    """
    bytes_to_b58_str converts the given bytes to a b58 encoded string

    Args:
        b (bytes): The bytes to convert

    Returns:
        str: The conversion result
    """
    return bytes_to_str(base58.b58encode(b))


def str_to_bytes(s: str) -> bytes:
    """
    str_to_bytes converts the given string to bytes

    Args:
        s (str): The string to convert

    Returns:
        bytes: The conversion result
    """
    return s.encode("latin-1")
