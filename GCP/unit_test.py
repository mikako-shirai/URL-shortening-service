import unittest

from main import generate_key

class TestMain(unittest.TestCase):
    def test_generate_key_length(self):
        """
        It should generate a key of the specified length
        """
        key_length = 6
        generated_key = generate_key(key_length)
        self.assertEqual(len(generated_key), key_length)

if __name__ == '__main__':
    unittest.main()