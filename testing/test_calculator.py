import unittest
from .calculator import add, subtract
 
class TestCalculator(unittest.TestCase):
 
    def test_add_positive_numbers(self):
        self.assertEqual(add(5,3), 8,"5+3=8")
   
    def test_add_negative_numbers(self):
        self.assertEqual(add(-1,-5),-6,"-1-5=-6")
   
    def test_subtract_non_numeric_raises_typeError(self):
        with self.assertRaises(TypeError):
            subtract("Hello",5)
 