"""
Binary data utilities for error detection/correction.

This module provides functions for converting between strings and binary,
as well as introducing and detecting errors in binary data.
"""

from typing import Optional
from random import randrange, sample


def string_to_binary(string: str = 'ok') -> str:
    """
    Convert string to space-separated binary representation.
    
    Args:
        string: Input string to convert
        
    Returns:
        Space-separated binary string
    """
    string = string.encode('utf-8')
    return ' '.join(format(x, 'b') for x in bytearray(string))


def binary_to_string(binary: str) -> str:
    """
    Convert space-separated binary string back to text.
    
    Args:
        binary: Space-separated binary string
        
    Returns:
        Decoded text string
    """
    binary = binary.split()
    return ''.join(chr(int(x, 2)) for x in binary)


def edit_bit(binary: str) -> str:
    """
    Randomly flip one bit in binary string.
    
    Args:
        binary: Binary string
        
    Returns:
        Binary string with one bit flipped
    """
    binary = list(binary)
    bit = randrange(0, len(binary))
    binary[bit] = '1' if binary[bit] == '0' else '0'
    return ''.join(binary)


def binary_errors(binary: str) -> str:
    """
    Introduce random bit errors in binary string.
    
    Args:
        binary: Space-separated binary string
        
    Returns:
        Binary string with random errors
    """
    binary = binary.split()
    if len(binary) <= 2:
        n_errors = 1
    else:
        n_errors = randrange(1, len(binary)//2)
        
    errors = sample(range(len(binary)), n_errors)
    for x in errors:
        binary[x] = edit_bit(binary[x])
        
    return ' '.join(binary)