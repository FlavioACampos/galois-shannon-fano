"""
Galois Field implementation and utilities.

This module provides functions for working with Galois Fields GF(2^n) and
related polynomial operations.
"""

from typing import List, Dict, Optional, Union
import csv
import json
import os
import io


def polynomial_form(binary_string: str) -> Optional[str]:
    """
    Convert binary string to polynomial form with superscript notation.
    
    Args:
        binary_string: Binary string to convert
        
    Returns:
        String representation of polynomial or None if input is '0'
    """
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    binary_string = binary_string.strip()
    k = len(binary_string)-1
    
    if binary_string == '0':
        return None
    
    polynomial = []
    for k, x in zip(range(k, -1, -1), binary_string):
        if x == '0':
            continue
            
        if k == 0:
            polynomial.append('1')
        elif k == 1:
            polynomial.append('x')
        else:
            exp = f'{k}'.translate(SUP)
            polynomial.append(f'x{exp}')
                
    return ' + '.join(polynomial)


def filler(bin_list: List[str], bits: int) -> Optional[str]:
    """
    Pad binary list with leading zeros to specified length.
    
    Args:
        bin_list: List of binary digits
        bits: Desired length
        
    Returns:
        Padded binary string or None if input is too long
    """
    limit = bits - len(bin_list)
    if limit == 0:
        return ''.join(bin_list)
    
    if limit < 0:
        return None
    
    for _ in range(limit):
        bin_list.insert(0, '0')
            
    return ''.join(bin_list)


def _load_polynomials() -> Dict:
    """Load polynomial data from JSON file."""
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'polynomials.json')
    with open(json_path, 'r') as f:
        return json.load(f)


def first_polynomials(bits: int) -> List[int]:
    """
    Get the first polynomial for a Galois Field GF(2^n).
    
    Args:
        bits: Field size (n in GF(2^n))
        
    Returns:
        List of coefficients representing the polynomial
    """
    polynomials = _load_polynomials()
    str_bits = str(bits)
    
    if str_bits not in polynomials['first_polynomials']:
        raise ValueError(f"No first polynomial defined for GF(2^{bits})")
    
    return polynomials['first_polynomials'][str_bits]


def primitive_polynomials(bits: int) -> str:
    """
    Get the primitive polynomial for a given field size.
    
    Args:
        bits: Field size (n in GF(2^n))
        
    Returns:
        Binary string representation of the primitive polynomial
    """
    polynomials = _load_polynomials()
    str_bits = str(bits)
    
    if str_bits not in polynomials['primitive_polynomials']:
        raise ValueError(f"No primitive polynomial defined for GF(2^{bits})")
    
    return polynomials['primitive_polynomials'][str_bits]


def field_constructor(bits: int, file: Union[str, io.StringIO]) -> None:
    """
    Construct Galois Field GF(2^n) and write elements to CSV file.
    
    Args:
        bits: Field size (n in GF(2^n))
        file: File or StringIO object to write to
    """
    csv_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
    primitive = primitive_polynomials(bits)
    first_poly = first_polynomials(bits)
    
    # Write header
    main_row = ['Index_form'] + [f'x{i}' for i in range(bits-1, -1, -1)]
    main_row.extend(['binary', 'decimal', 'polynomial_form'])
    csv_writer.writerow(main_row)
    
    # Write zero element
    row2 = ['0'] + ['0'] * bits
    row2.extend([f"{'0'*bits}₂", '0', '0'])
    csv_writer.writerow(row2)
    
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    
    # Generate field elements
    for b in range(int(2**bits)):
        row = []
        if b < bits:
            check = 2**b
            binary = list(bin(check)[2:])
            binary = filler(binary, bits)
            
            row.append((f'α{b}').translate(SUP))
            row.extend(binary)
            row.extend([f"{binary}₂", str(int(f'0b{binary}', 2)), polynomial_form(binary)])
            
        elif b == bits:
            binary = [str(i) for i in first_poly]
            binary = filler(binary, bits)
            
            row.append((f'α{b}').translate(SUP))
            row.extend(binary)
            row.extend([f"{binary}₂", str(int(f'0b{binary}', 2)), polynomial_form(binary)])
            
            current = int(f'0b{binary}', 2)
            
        else:
            current *= 2
            binary = list(bin(current)[2:])
            
            if len(binary) > bits:
                current ^= int(primitive, 2)
                binary = list(bin(current)[2:])
                
            binary = filler(binary, bits)
            
            row.append((f'α{b}').translate(SUP))
            row.extend(binary)
            row.extend([f"{binary}₂", str(current), polynomial_form(binary)])
            
        csv_writer.writerow(row)