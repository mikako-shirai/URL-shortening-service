import unittest
from main import generate_key, get_date, URL_check, key_check, date_check

import datetime
from dateutil.relativedelta import relativedelta


class TestMain(unittest.TestCase):
    # test class of main.py
# -------------------------------------------------------------
    def test_generate_key1(self):   
        key_length = 5
        generatedKey = generate_key(key_length)
        self.assertEqual(len(generatedKey), key_length)

    def test_generate_key2(self):
        key_length = 5
        generatedKey = generate_key(key_length)
        self.assertIsInstance(generatedKey, str)

    def test_generate_key3(self):
        key_length = 5
        generatedKey = generate_key(key_length)
        self.assertTrue(generatedKey.isalnum())

# -------------------------------------------------------------

    def test_get_date1(self):
        years = get_date()
        self.assertTrue(0 < len(years) <= 2)

    def test_get_date2(self):
        dateNow = datetime.datetime.now()
        year = dateNow.strftime('%Y')
        years = get_date()
        self.assertEqual(years[0], year)

# -------------------------------------------------------------

    def test_URL_check1(self):
        URL = 'https://short-321807.an.r.appspot.com'
        self.assertTrue(URL_check(URL))

    def test_URL_check2(self):
        URL = 'http://short-321807.an.r.appspot.com'
        self.assertTrue(URL_check(URL))
    
    def test_URL_check3(self):
        URL = 'https:/short-321807.an.r.appspot.com'
        self.assertFalse(URL_check(URL))

    def test_URL_check4(self):
        URL = 'https://'
        self.assertFalse(URL_check(URL))

    def test_URL_check5(self):
        URL = 'https.short-321807'
        self.assertFalse(URL_check(URL))

    def test_URL_check6(self):
        URL = 'https short-321807'
        self.assertFalse(URL_check(URL))

# -------------------------------------------------------------

    def test_key_check1(self):
        key = 'short-321807'
        self.assertTrue(key_check(key))
    
    def test_key_check2(self):
        key = 'short'
        self.assertFalse(key_check(key))

    def test_key_check3(self):
        key = 'https:short-321807.an.r.appspot.com'
        self.assertFalse(key_check(key))

    def test_key_check4(self):
        key = 'short/321807'
        self.assertFalse(key_check(key))

    def test_key_check5(self):
        key = 'short\\321807'
        self.assertFalse(key_check(key))

    def test_key_check6(self):
        key = 'short 321807'
        self.assertFalse(key_check(key))

# -------------------------------------------------------------

    def test_date_check1(self):
        date = '2021/2/31 00:00:00+0900'
        self.assertFalse(date_check(date))
    
    def test_date_check2(self):
        dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        date1month = dateNow + relativedelta(months=+1)
        date = date1month.strftime('%Y/%m/%d %H:%M:%S%z')
        self.assertTrue(date_check(date))
    
    def test_date_check3(self):
        dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        date1month = dateNow + relativedelta(months=-1)
        date = date1month.strftime('%Y/%m/%d %H:%M:%S%z')
        self.assertFalse(date_check(date))

    def test_date_check4(self):
        dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        date7month = dateNow + relativedelta(months=+7)
        date = date7month.strftime('%Y/%m/%d %H:%M:%S%z')
        self.assertFalse(date_check(date))

# -------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

