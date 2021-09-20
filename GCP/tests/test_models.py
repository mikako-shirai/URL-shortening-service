from URLshortener.models import *

import unittest
from unittest.mock import PropertyMock, MagicMock, patch


db = MagicMock()

# -----------------------------------------------------------------------------------

    # DatabaseWrapper.set(u'URLs', {
    #     u'originalURL': originalURL,
    #     u'generatedURL': generatedURL,
    #     u'dateCreated': dateCreated,
    #     u'expirationDate': expirationDate,
    #     u'pageViews': 0
    # })
    # DatabaseWrapper.set(u'keys', {
    #     u'originalURL': originalURL,
    #     u'pageViews': 0
    # })
    # assert(myDatabseWrapper.set).wasCalledWith()

# -------------------------------------------------------------

class TestMain(unittest.TestCase):
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

    # def test_append_data1(self):
    #     self.assertEqual(len(generatedKey), key_length)
    #     print(' Done: test_generate_key1')

# -------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

