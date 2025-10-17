import unittest
from src.galois_field import polynomial_form, filler, field_constructor
import io

class TestGaloisField(unittest.TestCase):
    def test_polynomial_form(self):
        self.assertEqual(polynomial_form('101'), 'x² + 1')
        self.assertEqual(polynomial_form('1101'), 'x³ + x² + 1')
        self.assertEqual(polynomial_form('0'), None)
        
    def test_filler(self):
        self.assertEqual(filler(['1', '0', '1'], 5), '00101')
        self.assertEqual(filler(['1'], 3), '001')
        self.assertEqual(filler(['1', '0', '1'], 2), None)
        
    def test_field_constructor(self):
        output = io.StringIO()
        field_constructor(3, output)
        output.seek(0)
        lines = output.readlines()
        
        # Check header
        self.assertTrue('Index_form' in lines[0])
        
        # Check number of elements (2^3 = 8 elements including 0)
        self.assertEqual(len(lines), 9)

if __name__ == '__main__':
    unittest.main()