from URLshortener.views import get_date
from URLshortener.utils import *

import unittest
import datetime
from dateutil.relativedelta import relativedelta

# -----------------------------------------------------------------------------------

class TestUtils(unittest.TestCase):
    # test class of utils.py
    
    def setUpClass():
        print(' ============================== test_utils START ==============================')
        print(' ')
 
    def tearDownClass():
        print('=============================== test_utils END ===============================')

# -----------------------------------------------------------------------------------

    def test_get_date(self):
        years = get_date()

        self.assertTrue(0 < len(years['years']) <= 2)
        
        for year in years['years']:
            self.assertIsInstance(year, str)
        
        dateNow = datetime.datetime.now()
        yearNow = dateNow.strftime('%Y')
        self.assertTrue(yearNow in years['years'])

        print(u' \u2713 Done: test_get_date\n')

# -----------------------------------------------------------------------------------

    def test_generate_key(self):   
        key_length = 5
        generatedKey = generate_key(key_length)

        self.assertEqual(len(generatedKey), key_length)
        self.assertIsInstance(generatedKey, str)
        self.assertTrue(generatedKey.isalnum())

        print(u' \u2713 Done: test_generate_key\n')

# -----------------------------------------------------------------------------------

    def test_URL_check(self):
        self.assertTrue(URL_check('https://short-321807.an.r.appspot.com'))
        self.assertTrue(URL_check('http://short-321807'))
        self.assertFalse(URL_check('https://short 321807.an.r.appspot.com'))
        self.assertFalse(URL_check('https:/short-321807.an.r.appspot.com'))
        self.assertFalse(URL_check('https://'))
        self.assertFalse(URL_check('https.short-321807'))

        print(u' \u2713 Done: test_URL_check\n')

# -----------------------------------------------------------------------------------

    def test_key_check(self):
        self.assertTrue(key_check('short-321807'))
        self.assertFalse(key_check('short'))
        self.assertFalse(key_check('https:short-321807.an.r.appspot.com'))
        self.assertFalse(key_check('short/321807'))
        self.assertFalse(key_check('short\\321807'))
        self.assertFalse(key_check('short 321807'))

        print(u' \u2713 Done: test_key_check\n')

# -----------------------------------------------------------------------------------

    def test_date_check(self):
        dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

        date = '2021/2/31 00:00:00+0900'
        self.assertFalse(date_check(date))

        date1months = (dateNow + relativedelta(months=+1)).strftime('%Y/%m/%d %H:%M:%S%z')
        self.assertTrue(date_check(date1months))

        date1days = (dateNow + relativedelta(days=-1)).strftime('%Y/%m/%d %H:%M:%S%z')
        self.assertFalse(date_check(date1days))
    
        date6months1days = (dateNow + relativedelta(months=+6, days=+1)).strftime('%Y/%m/%d %H:%M:%S%z')
        self.assertFalse(date_check(date6months1days))

        print(u' \u2713 Done: test_date_check\n')

# -----------------------------------------------------------------------------------

    def test_GCPURL_check(self):
        self.assertTrue(GCPURL_check('https://short-321807.an.r.appspot.com/TESTtest'))
        self.assertFalse(GCPURL_check('https://short-321807.an.r.appspot.com/'))
        self.assertFalse(GCPURL_check('https://short-321807.an.r.appspot.com/TESTtest TEST'))
        self.assertFalse(GCPURL_check('https://test-321807.test.test.test.com/TESTtest'))

        print(u'  \u2713 Done: test_GCPURL_check\n')

# -----------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

