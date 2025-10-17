import unittest
from src.shannon_fano import shannon_fano, arr_namer, best_pair
from fractions import Fraction

class TestShannonFano(unittest.TestCase):
    def test_arr_namer(self):
        freqs = [0.5, 0.25, 0.25]
        names = ['a', 'b', 'c']
        result = list(arr_namer(freqs, names))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], [0.5, 'a'])
        self.assertEqual(result[1], [0.25, 'b'])
        self.assertEqual(result[2], [0.25, 'c'])

    def test_best_pair(self):
        arr = [[0.5, 'a'], [0.25, 'b'], [0.25, 'c']]
        result = best_pair(arr)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (arr[0],))
        self.assertEqual(result[1], (arr[1], arr[2]))

    def test_shannon_fano(self):
        freqs = [Fraction('1/2'), Fraction('1/4'), Fraction('1/4')]
        names = ['a', 'b', 'c']
        graph, number, out_names, start, freq = shannon_fano(freqs, names)
        
        self.assertTrue(isinstance(graph, dict))
        self.assertTrue(isinstance(number, dict))
        self.assertEqual(set(out_names), set(names))
        self.assertTrue(isinstance(start, str))
        self.assertTrue(isinstance(freq, tuple))

if __name__ == '__main__':
    unittest.main()