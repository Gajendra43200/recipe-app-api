# Sample test
from django.test import SimpleTestCase
from app  import calc

class ClacTests(SimpleTestCase):
    # Test added number together
    def test_add_bumbers(self):
        res = calc.add(5,6)
        self.assertEqual(res, 11)
    

    # Useing TDD 
    def test_subtract_numbers(self):
        # Test subtracting number
        res = calc.subtract(15, 10)
        self.assertEqual(res,5)
