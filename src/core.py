"""
Core utilities for Shannon-Fano coding and Galois Fields.
"""

from typing import List, Dict, Tuple, Optional
from fractions import Fraction
import random


def sum_equals_one(arr: List[Fraction]) -> bool:
    """Check if a list of fractions sums to 1."""
    return sum(arr) == 1


def generate_random_frequencies(n: int = 5) -> List[Fraction]:
    """Generate n random frequencies that sum to 1."""
    values = [random.random() for _ in range(n)]
    total = sum(values)
    return [Fraction(v/total).limit_denominator() for v in values]


def find_path(graph: Dict[str, List[str]], start: str, end: str, path: List[str] = None) -> Optional[List[str]]:
    """Find a path between two nodes in a graph."""
    if path is None:
        path = []
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath:
                return newpath
    return None