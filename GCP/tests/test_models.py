from URLshortener.models import *
import URLshortener.DatabaseWrapper

import unittest
from unittest.mock import PropertyMock, MagicMock, patch


# db = MagicMock()

# -----------------------------------------------------------------------------------

    # assert(myDatabseWrapper.set).wasCalledWith()

# -------------------------------------------------------------

class TestModels(unittest.TestCase):
    # test class of main.py

    def setUpClass():
        print('============================== test_models START ===============================')
 
    def tearDownClass():
        print('=============================== test_models END ================================')
 
    # def setUp(self):
    #     print(' before each test ')
    # def tearDown(self):
    #     print(' after each test ')

# -------------------------------------------------------------

    def test_get_keys1(self):
        test = MagicMock()
        test.id = 'test'
        URLshortener.DatabaseWrapper.collection_stream = MagicMock(return_value=[test])
        print(get_keys())
        # self.assertEqual()
        print(' Done: test_get_keys1')

# -------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

