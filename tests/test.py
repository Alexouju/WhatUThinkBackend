import unittest

# Define a simple function to be tested
def add(a, b):
    return a + b

# Define a test case class that inherits from unittest.TestCase
class TestAddFunction(unittest.TestCase):

    # Define a test method starting with "test_"
    def test_add(self):
        # Test the add function with some input values
        self.assertEqual(add(3, 4), 7)  # Test addition of positive numbers
        self.assertEqual(add(-3, -4), -7)  # Test addition of negative numbers
        self.assertEqual(add(0, 0), 0)  # Test addition of zeros

# If this script is run directly, run the tests
if __name__ == '__main__':
    unittest.main()
