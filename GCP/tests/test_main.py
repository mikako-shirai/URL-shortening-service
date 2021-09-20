from URLshortener.views import short_link, custom_link, short_expiration, custom_expiration, link_analysis, URL_redirect

import unittest
from unittest.mock import PropertyMock, MagicMock, patch
import random, string
import datetime
from dateutil.relativedelta import relativedelta
import re
import os
from google.cloud import firestore


# app = Flask(__name__)
db = MagicMock()

key_length = 5
GCP_URL = 'https://short-321807.an.r.appspot.com/'
keywords = ['custom', 'expiration', 'analysis', 'link', '404', 'error', 'cron', \
            'index', 'index_exp', 'custom_exp', 'result', 'selector']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

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
        print('============================== test_main START ===============================')
 
    def tearDownClass():
        print('=============================== test_main END ================================')
 
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

