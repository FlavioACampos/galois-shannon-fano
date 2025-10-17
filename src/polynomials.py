"""
Polynomial management for Galois Fields.

This module provides functions for working with polynomials in Galois Fields,
including both pre-computed polynomials and dynamic generation capabilities.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Union, Optional
import numpy as np

# Load pre-computed polynomials from JSON
DATA_PATH = Path(__file__).parent / 'data' / 'polynomials.json'

def load_polynomials() -> Dict:
    """Load polynomial data from JSON file."""
    try:
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"first_polynomials": {}, "primitive_polynomials": {}}

_POLY_DATA = load_polynomials()

def is_primitive(poly: List[int], degree: int) -> bool:
    """
    Check if a polynomial is primitive over GF(2).
    
    Args:
        poly: Polynomial coefficients [a_n, ..., a_1, a_0]
        degree: Degree of the polynomial
        
    Returns:
        bool: True if polynomial is primitive
    """
    if len(poly) != degree + 1 or poly[0] != 1:
        return False
        
    # Convert to numpy polynomial
    p = np.polynomial.polynomial.Polynomial(poly[::-1])
    
    # Check if irreducible first (necessary condition)
    x = np.polynomial.polynomial.Polynomial([0, 1])
    
    # Test powers up to degree
    current = x
    for i in range(1, 2**degree - 1):
        current = (current * x) % p
        if np.array_equal(current.coef, np.array([1])):
            return i == 2**degree - 2
    
    return False

def generate_primitive_polynomial(degree: int) -> List[int]:
    """
    Generate a primitive polynomial of given degree over GF(2).
    
    Args:
        degree: Degree of polynomial to generate
        
    Returns:
        List of coefficients [a_n, ..., a_1, a_0]
    """
    if degree < 1:
        raise ValueError("Degree must be positive")
        
    # Start with the simplest possible polynomial of given degree
    poly = [1] + [0] * (degree-1) + [1]
    
    while not is_primitive(poly, degree):
        # Generate next polynomial systematically
        for i in range(degree - 1, -1, -1):
            if poly[i] == 0:
                poly[i] = 1
                for j in range(i + 1, degree):
                    poly[j] = 0
                break
        if all(x == 1 for x in poly):
            raise ValueError(f"No primitive polynomial of degree {degree} found")
            
    return poly

def first_polynomials(bits: int) -> List[int]:
    """
    Get the first polynomial for given field size.
    
    Args:
        bits: Field size (n in GF(2^n))
        
    Returns:
        List of coefficients [a_n, ..., a_1, a_0]
    """
    # Try pre-computed first
    if str(bits) in _POLY_DATA["first_polynomials"]:
        return _POLY_DATA["first_polynomials"][str(bits)]
    
    # Generate if not available
    return generate_primitive_polynomial(bits)

def primitive_polynomials(bits: int) -> str:
    """
    Get the primitive polynomial for given field size.
    
    Args:
        bits: Field size (n in GF(2^n))
        
    Returns:
        Binary string representation of polynomial
    """
    # Try pre-computed first
    if str(bits) in _POLY_DATA["primitive_polynomials"]:
        return _POLY_DATA["primitive_polynomials"][str(bits)]
    
    # Generate if not available
    poly = generate_primitive_polynomial(bits)
    return ''.join(str(x) for x in poly)