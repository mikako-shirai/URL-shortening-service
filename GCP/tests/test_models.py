from URLshortener.models import *
import URLshortener.DatabaseWrapper as DatabaseWrapper

import unittest
from unittest.mock import patch

# -----------------------------------------------------------------------------------

class TestModels(unittest.TestCase):
    # test class of models.py / DatabaseWrapper.py

    def setUpClass():
        print(' ============================== test_models START ===============================')
        print(' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
 
    def tearDownClass():
        print('=============================== test_models END ================================')
 
    # def setUp(self):
    #     print(' before each test ')
    def tearDown(self):
        print(' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

# -----------------------------------------------------------------------------------

    keywords = ['custom', 'expiration', 'analysis', 'link', '404', 'error', 'cron', \
            'index', 'index_exp', 'custom_exp', 'result', 'selector']

    @patch('URLshortener.models.collection_stream')
    @patch('URLshortener.models.id')
    def test_get_keys1(self, mock_id, mock_stream):
        mock_stream.return_value = [1, 2, 3]
        mock_id.return_value = 'TEST'
        keys = get_keys()
        print(keys)
        self.assertEqual(len(keys), len(keywords) + 3)
        print(' Done: test_get_keys1')

# -----------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

