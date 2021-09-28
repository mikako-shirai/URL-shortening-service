from URLshortener.models import *
import URLshortener.DatabaseWrapper as DatabaseWrapper

import unittest
from unittest.mock import patch, call

# -----------------------------------------------------------------------------------

class TestModels(unittest.TestCase):
    # test class of models.py / DatabaseWrapper.py

    GCP_URL = 'https://short-321807.an.r.appspot.com/'
    keywords = ['custom', 'expiration', 'analysis', 'link', '404', 'error', 'cron', \
                'index', 'index_exp', 'custom_exp', 'result', 'selector']

    def setUpClass():
        print(' ============================== test_models START ===============================')
        print(' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
 
    def tearDownClass():
        print('=============================== test_models END ================================')
 
    def setUp(self):
        print(' ')
    def tearDown(self):
        print(' ')
        print(' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_stream')
    @patch('URLshortener.models.id')
    def test_get_keys(self, mock_id, mock_stream):
        mock_stream.return_value = [1, 2, 3]
        mock_id.return_value = 'TEST_key'
        keys = get_keys()
        print(f" {keys}\n")

        self.assertIsInstance(keys, list)
        print(u"  \u2713 class type of the return value :", f"{type(keys)}\n")

        self.assertEqual(mock_stream.call_count, 1)
        self.assertEqual(mock_id.call_count, 3)
        print(u"  \u2713 'collection_stream()' was called :", f"{mock_stream.call_count} times")
        print(u"  \u2713 'id()' was called                :", f"{mock_id.call_count} times\n")

        mock_id.assert_any_call(1)
        mock_id.assert_any_call(2)
        mock_id.assert_any_call(3)
        expected = (1, 2, 3)
        print(u"  \u2713 'id()' was called with :", f"{(expected)}\n")

        for element in keys:
            self.assertIsInstance(element, str)
        print(u"  \u2713 class type of each element in the list :", f"{type(keys[0])}\n")

        self.assertEqual(len(keys), len(keywords) + 3)
        print(u"  \u2713 number of elements that were added to the list :", f"{len(keys) - len(keywords)}\n")

        expected = ['TEST_key', 'TEST_key', 'TEST_key']
        self.assertEqual(keys[:3], expected)
        print(u"  \u2713 first 3 elements in the list should be equal to :", f"'{keys[0]}'\n")

        print("\n Done: test_get_keys")

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_document_set')
    @patch('URLshortener.models.collection_document_get_todict')
    @patch('URLshortener.models.firestore_ArrayUnion')
    @patch('URLshortener.models.firestore_Increment')
    def test_append_data(self, mock_increment, mock_arrayunion, mock_get_todict, mock_set):
        mock_set.return_value = None
        mock_get_todict.return_value = {'list': ['TEST_original'], 'total': 1}
        mock_arrayunion.return_value = None
        mock_increment.return_value = None
        append_data('TEST_url', 'TEST_key')
        
        self.assertEqual(mock_set.call_count, 2)
        self.assertEqual(mock_get_todict.call_count, 1)
        self.assertEqual(mock_arrayunion.call_count, 1)
        self.assertEqual(mock_increment.call_count, 1)
        print(u"  \u2713 'collection_document_set()' was called        :", f"{mock_set.call_count} times")
        print(u"  \u2713 'collection_document_get_todict()' was called :", f"{mock_get_todict.call_count} times")
        print(u"  \u2713 'firestore_ArrayUnion()' was called           :", f"{mock_arrayunion.call_count} times")
        print(u"  \u2713 'firestore_Increment()' was called            :", f"{mock_increment.call_count} times\n")

        call1, call2 = mock_set.call_args_list
        call1, call2 = call1[0], call2[0]
        self.assertEqual(call1[1], 'TEST_key')
        self.assertEqual(call2[1], 'TEST_key')
        self.assertEqual(call1[2]['originalURL'], 'TEST_url')
        self.assertEqual(call2[2]['originalURL'], 'TEST_url')
        print(u"  \u2713 value of the second argument                      :", f"'{call1[1]}'")
        print(u"  \u2713 value for 'originalURL' key in the third argument :", f"'{call1[2]['originalURL']}'\n")

        kwargs1 = call1[2]
        kwargs2 = call2[2]
        self.assertEqual(len(kwargs1), 5)
        self.assertEqual(len(kwargs2), 2)
        print(u"  \u2713 length of the dictionary in the first call  :", f"{len(kwargs1)}")
        print(u"  \u2713 length of the dictionary in the second call :", f"{len(kwargs2)}\n")

        print("\n Done: test_append_data")

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_document_get')
    @patch('URLshortener.models.exists')
    @patch('URLshortener.models.data_todict')
    def test_get_analysis1(self, mock_todict, mock_exists, mock_get):
        dateCreated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        expirationDate = dateCreated + relativedelta(days=+14)
        mock_get.return_value = None
        mock_exists.return_value = True
        mock_todict.return_value = {'originalURL': 'TEST_original', 'generatedURL': 'TEST_generated', \
                                    'dateCreated': dateCreated, 'expirationDate': expirationDate, 'pageViews': '0'}
        dicData = get_analysis('TEST_url', 'TEST_key')
        print(f" {dicData}\n")

        self.assertIsInstance(dicData, dict)
        print(u"  \u2713 class type of the return value :", f"{type(dicData)}")
        self.assertEqual(len(dicData), 6)
        print(u"  \u2713 length of the return value :", f"{len(dicData)}\n")

        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_exists.call_count, 1)
        self.assertEqual(mock_todict.call_count, 1)
        print(u"  \u2713 'collection_document_get()' was called :", f"{mock_get.call_count} times")
        print(u"  \u2713 'exists()' was called                  :", f"{mock_exists.call_count} times")
        print(u"  \u2713 'data_todict()' was called             :", f"{mock_todict.call_count} times\n")

        mock_exists.assert_any_call(None)
        mock_todict.assert_any_call(None)
        expected = None
        print(u"  \u2713 'exists()' was called with      :", f"{(expected)}")
        print(u"  \u2713 'data_todict()' was called with :", f"{(expected)}\n")

        for value in dicData.values():
            self.assertIsInstance(value, str)
        print(u"  \u2713 class type of each value in the dictionary :", f"{type(list(dicData.values())[0])}\n")

        self.assertEqual(dicData['originalURL'], 'TEST_original')
        self.assertEqual(dicData['generatedURL'], 'TEST_url')
        self.assertEqual(dicData['pageViews'], '0')
        print(u"  \u2713 value for 'originalURL' key  :", f"'{dicData['originalURL']}'")
        print(u"  \u2713 value for 'generatedURL' key :", f"'{dicData['generatedURL']}'")

        print("\n Done: test_get_analysis1")

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_document_get')
    @patch('URLshortener.models.exists')
    @patch('URLshortener.models.data_todict')
    def test_get_analysis2(self, mock_todict, mock_exists, mock_get):
        dateCreated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        expirationDate = dateCreated + relativedelta(days=+14)
        mock_get.return_value = None
        mock_exists.return_value = False
        mock_todict.return_value = {'originalURL': 'TEST_original', 'generatedURL': 'TEST_generated', \
                                    'dateCreated': dateCreated, 'expirationDate': expirationDate, 'pageViews': '0'}
        dicData = get_analysis('TEST_url', 'TEST_key')
        print(f" {dicData}\n")

        self.assertIsInstance(dicData, dict)
        print(u"  \u2713 class type of the return value :", f"{type(dicData)}")
        self.assertEqual(len(dicData), 0)
        print(u"  \u2713 length of the return value :", f"{len(dicData)}\n")

        self.assertEqual(mock_get.call_count, 2)
        self.assertEqual(mock_exists.call_count, 2)
        self.assertEqual(mock_todict.call_count, 0)
        print(u"  \u2713 'collection_document_get()' was called :", f"{mock_get.call_count} times")
        print(u"  \u2713 'exists()' was called                  :", f"{mock_exists.call_count} times")
        print(u"  \u2713 'data_todict()' was called             :", f"{mock_todict.call_count} times\n")

        mock_exists.assert_any_call(None)
        expected = None
        print(u"  \u2713 'exists()' was called with :", f"{(expected)}")

        print("\n Done: test_get_analysis2")

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_document_get')
    @patch('URLshortener.models.exists')
    @patch('URLshortener.models.firestore_Increment')
    @patch('URLshortener.models.data_todict')
    def test_get_redirect1(self, mock_todict, mock_increment, mock_exists, mock_get):
        mock_get.return_value = None
        mock_exists.return_value = True
        mock_increment.return_value = None
        mock_todict.return_value = {'originalURL': 'TEST_original'}
        originalURL = get_redirect('TEST_key')
        print(f" '{originalURL}'\n")

        self.assertIsInstance(originalURL, str)
        print(u"  \u2713 class type of the return value :", f"{type(originalURL)}")
        self.assertEqual(originalURL, 'TEST_original')
        print(u"  \u2713 return value should be equal to :", f"'{originalURL}'\n")

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(mock_exists.call_count, 1)
        self.assertEqual(mock_increment.call_count, 2)
        self.assertEqual(mock_todict.call_count, 1)
        print(u"  \u2713 'collection_document_get()' was called :", f"{mock_get.call_count} times")
        print(u"  \u2713 'exists()' was called                  :", f"{mock_exists.call_count} times")
        print(u"  \u2713 'firestore_Increment()' was called     :", f"{mock_exists.call_count} times")
        print(u"  \u2713 'data_todict()' was called             :", f"{mock_todict.call_count} times\n")

        mock_exists.assert_any_call(None)
        expected = None
        print(u"  \u2713 'exists()' was called with :", f"{(expected)}")

        print("\n Done: test_get_redirect1")

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_document_get')
    @patch('URLshortener.models.exists')
    @patch('URLshortener.models.firestore_Increment')
    @patch('URLshortener.models.data_todict')
    def test_get_redirect2(self, mock_todict, mock_increment, mock_exists, mock_get):
        mock_get.return_value = None
        mock_exists.return_value = False
        mock_increment.return_value = None
        mock_todict.return_value = {'originalURL': 'TEST_original'}
        originalURL = get_redirect('TEST_key')
        print(f" {originalURL}\n")

        self.assertIsInstance(originalURL, bool)
        print(u"  \u2713 class type of the return value :", f"{type(originalURL)}")
        self.assertFalse(originalURL)
        print(u"  \u2713 return value should be equal to :", f"{originalURL}\n")

        self.assertEqual(mock_get.call_count, 1)
        self.assertEqual(mock_exists.call_count, 1)
        self.assertEqual(mock_increment.call_count, 0)
        self.assertEqual(mock_todict.call_count, 0)
        print(u"  \u2713 'collection_document_get()' was called :", f"{mock_get.call_count} times")
        print(u"  \u2713 'exists()' was called                  :", f"{mock_exists.call_count} times")
        print(u"  \u2713 'firestore_Increment()' was called     :", f"{mock_exists.call_count} times")
        print(u"  \u2713 'data_todict()' was called             :", f"{mock_todict.call_count} times\n")

        mock_exists.assert_any_call(None)
        expected = None
        print(u"  \u2713 'exists()' was called with :", f"{(expected)}")

        print("\n Done: test_get_redirect2")

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_stream')
    @patch('URLshortener.models.data_todict')
    @patch('URLshortener.models.collection_document_get_todict')
    @patch('URLshortener.models.id')
    @patch('URLshortener.models.collection_document_set')
    @patch('URLshortener.models.firestore_DeleteField')
    @patch('URLshortener.models.collection_document_delete')
    @patch('URLshortener.models.firestore_ArrayRemove')
    @patch('URLshortener.models.firestore_Increment')
    def test_cron_job(self, mock_increment, mock_arrayremove, mock_delete, mock_deletefield, \
                      mock_set, mock_id, mock_get_todict, mock_todict, mock_stream):
        expirationDate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) + relativedelta(months=-1)
        mock_stream.return_value = ['TEST_key']
        mock_todict.return_value = {'originalURL': 'TEST_original', 'expirationDate': expirationDate}
        mock_get_todict.return_value = {'list': ['TEST_original']}
        mock_id.return_value = 'TEST_key'
        mock_set.return_value = None
        mock_deletefield.return_value = None
        mock_delete.return_value = None
        mock_arrayremove.return_value = None
        mock_increment.return_value = None
        cron_job()

        self.assertEqual(mock_stream.call_count, 1)
        self.assertEqual(mock_todict.call_count, 1)
        self.assertEqual(mock_get_todict.call_count, 2)
        self.assertEqual(mock_id.call_count, 11)
        self.assertEqual(mock_set.call_count, 1)
        self.assertEqual(mock_deletefield.call_count, 7)
        self.assertEqual(mock_delete.call_count, 2)
        self.assertEqual(mock_arrayremove.call_count, 1)
        self.assertEqual(mock_increment.call_count, 1)
        print(u"  \u2713 'collection_stream()' was called              :", f"{mock_stream.call_count} times")
        print(u"  \u2713 'data_todict()' was called                    :", f"{mock_todict.call_count} times")
        print(u"  \u2713 'collection_document_get_todict()' was called :", f"{mock_get_todict.call_count} times")
        print(u"  \u2713 'id()' was called                             :", f"{mock_id.call_count} times")
        print(u"  \u2713 'collection_document_set()' was called        :", f"{mock_set.call_count} times")
        print(u"  \u2713 'firestore_DeleteField()' was called          :", f"{mock_deletefield.call_count} times")
        print(u"  \u2713 'collection_document_delete()' was called     :", f"{mock_delete.call_count} times")
        print(u"  \u2713 'firestore_ArrayRemove()' was called          :", f"{mock_arrayremove.call_count} times")
        print(u"  \u2713 'firestore_Increment()' was called            :", f"{mock_increment.call_count} times\n")

        mock_set.assert_any_call(u'expiredURLs', 'TEST_key', {'list': ['TEST_original']})
        expected = (u'expiredURLs', 'TEST_key', {'list': ['TEST_original']})
        print(u"  \u2713 'collection_document_set()' was called with :", f"{expected}\n")

        print("\n Done: test_cron_job")

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_document_get_todict')
    def test_error_handler1(self, mock_get_todict):
        mock_get_todict.return_value = {'list': ['TEST_original', 'TEST_original', 'TEST_original'], 'total': 3}
        URL = error_handler()
        print(f" '{URL}'\n")

        self.assertIsInstance(URL, str)
        print(u"  \u2713 class type of the return value :", f"{type(URL)}")
        self.assertEqual(URL, 'TEST_original')
        print(u"  \u2713 return value should be equal to :", f"'{URL}'\n")

        self.assertEqual(mock_get_todict.call_count, 1)
        print(u"  \u2713 'collection_document_get_todict()' was called :", f"{mock_get_todict.call_count} times\n")

        print("\n Done: test_error_handler1")

# -----------------------------------------------------------------------------------

    @patch('URLshortener.models.collection_document_get_todict')
    def test_error_handler2(self, mock_get_todict):
        mock_get_todict.return_value = {'list': [], 'total': 0}
        URL = error_handler()
        print(f" '{URL}'\n")

        self.assertIsInstance(URL, str)
        print(u"  \u2713 class type of the return value :", f"{type(URL)}")
        self.assertEqual(URL, 'https://www.google.com/')
        print(u"  \u2713 return value should be equal to :", f"'{URL}'\n")

        self.assertEqual(mock_get_todict.call_count, 1)
        print(u"  \u2713 'collection_document_get_todict()' was called :", f"{mock_get_todict.call_count} times\n")

        print("\n Done: test_error_handler2")

# -----------------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()

