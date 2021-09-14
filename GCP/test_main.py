import unittest
# from main import 

import random, string
import datetime
from dateutil.relativedelta import relativedelta
import re
import os
from google.cloud import firestore


class TestMain(unittest.TestCase):
    # test class of main.py
# -------------------------------------------------------------

    def setUpClass():
        print('============================== test_main START ===============================')
 
    def tearDownClass():
        print('=============================== test_main END ================================')
 
    # def setUp(self):
    #     print(' before each test ')
    # def tearDown(self):
    #     print(' after each test ')

# -------------------------------------------------------------

    # def test_generate_key1(self):   
    #     key_length = 5
    #     generatedKey = generate_key(key_length)
    #     self.assertEqual(len(generatedKey), key_length)
    #     print(' Done: test_generate_key1')

# -------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

