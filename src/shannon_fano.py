"""
Shannon-Fano coding implementation.

This module provides functions for generating Shannon-Fano codes from input text
or frequency distributions.
"""

from typing import List, Dict, Tuple, Generator, Union
from fractions import Fraction
import string
from collections import Counter


def arr_namer(arr: List[Union[float, Fraction]], 
             names: List[str] = None) -> Generator[List[Union[float, str]], None, None]:
    """
    Name array elements with sequential letters.
    
    Args:
        arr: List of frequencies
        names: Optional list of names to use instead of default alphabet
        
    Yields:
        Lists containing [frequency, name] pairs
    """
    if names is None:
        names = list(string.ascii_lowercase)
        
    index, n, r = 0, 0, ''
    if names == list(string.ascii_lowercase):
        for element in arr:
            if index == 26:
                index = 0
                n += 1
                r = f'{n}'
            yield [element, names[index]+r]
            index += 1
    else:
        for element, name in zip(arr, names):
            yield [element, name]


def best_pair(arr: List[List[Union[float, str]]]) -> List[tuple]:
    """
    Find the best division point for Shannon-Fano coding.
    
    Args:
        arr: List of [frequency, name] pairs
        
    Returns:
        List containing two tuples of the divided groups
    """
    if len(arr) == 2:
        return [tuple(arr[0]), tuple(arr[1])]
    if len(arr) < 2:
        return arr
        
    current = 1
    for i, _ in enumerate(arr):
        if i == 0 or i == len(arr)-1:
            continue
            
        left = sum(n[0] for n in arr[:i])
        right = sum(n[0] for n in arr[i:])
        
        if abs(left-right) < current:
            best = [tuple(arr[:i]), tuple(arr[i:])]
            current = abs(left-right)
            
    return best


def shannon_fano(freq: List[Union[float, Fraction]], 
                 names: List[str]) -> Tuple[Dict, Dict, List[str], str, tuple]:
    """
    Generate Shannon-Fano codes for given frequencies.
    
    Args:
        freq: List of frequencies
        names: List of symbols
        
    Returns:
        Tuple containing:
        - graph: Dict representing the encoding tree
        - number: Dict mapping nodes to binary digits
        - names: List of symbol names
        - start: String representing the root node
        - freq: Original frequency tuples
    """
    freq = tuple(sorted(tuple(arr_namer(freq, names)), reverse=True))
    freq = sorted(freq, key=lambda x: (-x[0], x[1]))
    
    graph = {}
    number = {}
    arr = [freq]
    names = [i[1] for i in freq]
    
    start = ''.join(element[1] for group in arr for element in group)
    
    while arr:
        temp_arr = []
        for group in arr:
            name = ''.join(element[1] for element in group)
            graph[name] = []
            pair = best_pair(group)
            
            for i, each in enumerate(pair):
                if isinstance(each[0], (float, Fraction)):
                    graph[name].append(each[1])
                    number[each[1]] = i
                    graph[each[1]] = []
                else:
                    temp_arr.append(each)
                    name2 = ''.join(element[1] for element in each)
                    graph[name].append(name2)
                    number[name2] = i
                    
        arr = temp_arr
        
    return graph, number, names, start, freq