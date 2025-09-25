import unittest
import app

class TestCalculatorAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.app.test_client()
    
    def test_addition(self):
        response = self.app.post('/calculate', 
            json={'a': 10, 'b': 5, 'op': '+'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 15)
    
    def test_division_by_zero(self):
        response = self.app.post('/calculate', 
            json={'a': 10, 'b': 0, 'op': '/'})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()