from URLshortener.models import *
import URLshortener.DatabaseWrapper

import unittest
from unittest.mock import MagicMock

# -----------------------------------------------------------------------------------

    # assert(myDatabseWrapper.set).wasCalledWith()

# -------------------------------------------------------------

class TestModels(unittest.TestCase):
    # test class of models.py / DatabaseWrapper.py
    URLshortener.DatabaseWrapper.db = MagicMock()

    def setUpClass():
        print('============================== test_models START ===============================')
        print(' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
 
    def tearDownClass():
        print('=============================== test_models END ================================')
 
    # def setUp(self):
    #     print(' before each test ')
    def tearDown(self):
        print(' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

# -------------------------------------------------------------

    def test_get_keys1(self):
        print(get_keys())
        # self.assertEqual()
        print(' Done: test_get_keys1')

    def test_test_functions1(self):
        print(test_functions())
        # self.assertEqual()
        print(' Done: test_test_functions1')

# -------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

