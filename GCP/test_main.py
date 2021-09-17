import unittest
from unittest.mock import MagicMock, patch

from flask import Flask, render_template, request, redirect, abort, url_for
from utils import generate_key, get_date, URL_check, key_check, date_check
from main import append_data, DB_generatedKey, DB_customKey, URL_redirect, expiration_check

import random, string
import datetime
from dateutil.relativedelta import relativedelta
import re
import os
from google.cloud import firestore


app = Flask(__name__)
db = firestore.Client()

key_length = 5
GCP_URL = 'https://short-321807.an.r.appspot.com/'
keywords = ['custom', 'expiration', 'analysis', 'link', '404', 'error', 'cron', \
            'index', 'index_exp', 'custom_exp', 'result', 'selector']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

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

