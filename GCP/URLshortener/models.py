from URLshortener.DatabaseWrapper import *

import datetime
from dateutil.relativedelta import relativedelta
import random


GCP_URL = 'https://short-321807.an.r.appspot.com/'
keywords = ['custom', 'expiration', 'analysis', 'link', '404', 'error', 'cron', \
            'index', 'index_exp', 'custom_exp', 'result', 'selector']

# -----------------------------------------------------------------------------------

def get_keys():
    keysDB = collection_stream(u'keys')
    keys = [key.id for key in keysDB] + keywords
    return keys

def append_data(originalURL, key, expirationDate=None):
    generatedURL = GCP_URL + key
    dateCreated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    if not expirationDate:
        expirationDate = dateCreated + relativedelta(days=+14)

    collection_document_set(u'URLs', key, {
        u'originalURL': originalURL,
        u'generatedURL': generatedURL,
        u'dateCreated': dateCreated,
        u'expirationDate': expirationDate,
        u'pageViews': 0
    })
    collection_document_set(u'keys', key, {
        u'originalURL': originalURL,
        u'pageViews': 0
    })

    dic = collection_document_get_todict(u'random', u'random')
    URLs = dic['list']
    if originalURL not in URLs:
        firestore_ArrayUnion(u'random', u'random', u'list', originalURL)
        firestore_Increment(u'random', u'random', u'total', 1)

# -----------------------------------------------------------------------------------

def get_analysis(generatedURL, key):
    dicData = {}
    URLactive = collection_document_get(u'URLs', key)
    URLold = collection_document_get(u'expiredURLs', key)
    
    if exists(URLactive):
        URLactive = data_todict(URLactive)
        dateCreated = URLactive['dateCreated']
        expirationDate = URLactive['expirationDate']
        dateCreated = (dateCreated + relativedelta(hours=+9)).strftime('%Y/%m/%d %H:%M') + ' (UTC+09:00)'
        expirationDate = (expirationDate + relativedelta(hours=+9)).strftime('%Y/%m/%d %H:%M') + ' (UTC+09:00)'

        dicData['status'] = 'Available'
        dicData['originalURL'] = URLactive['originalURL']
        dicData['generatedURL'] = generatedURL
        dicData['dateCreated'] = dateCreated
        dicData['expirationDate'] = expirationDate
        dicData['pageViews'] = URLactive['pageViews']

    elif exists(URLold):
        URLold = data_todict(URLold)
        dateCreated = URLold['dateCreated']
        expirationDate = URLold['expirationDate']
        dateCreated = (dateCreated + relativedelta(hours=+9)).strftime('%Y/%m/%d %H:%M') + ' (UTC+09:00)'
        expirationDate = (expirationDate + relativedelta(hours=+9)).strftime('%Y/%m/%d %H:%M') + ' (UTC+09:00)'

        dicData['status'] = 'Not Available'
        dicData['originalURL'] = URLold['originalURL']
        dicData['generatedURL'] = generatedURL
        dicData['dateCreated'] = dateCreated
        dicData['expirationDate'] = expirationDate
        dicData['pageViews'] = URLold['pageViews']
    return dicData

def get_redirect(string):
    key = collection_document_get(u'keys', string)
    if exists(key):
        firestore_Increment(u'URLs', string, u'pageViews', 1)
        firestore_Increment(u'keys', string, u'pageViews', 1)
        originalURL = data_todict(key)['originalURL']
        return originalURL
    return False

# -----------------------------------------------------------------------------------

def cron_job():
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    URLs = collection_stream(u'URLs')

    for URL in URLs:
        dic = data_todict(URL)
        expirationDate = dic['expirationDate']
        if dateNow >= expirationDate:
            originalURL = dic['originalURL']
            # add expired URL information to 'expiredURLs' collection
            data = collection_document_get_todict(u'URLs', URL.id)
            collection_document_set(u'expiredURLs', URL.id, data)

            # deletion
            firestore_DeleteField(u'URLs', URL.id, u'originalURL')
            firestore_DeleteField(u'URLs', URL.id, u'generatedURL')
            firestore_DeleteField(u'URLs', URL.id, u'dateCreated')
            firestore_DeleteField(u'URLs', URL.id, u'expirationDate')
            firestore_DeleteField(u'URLs', URL.id, u'pageViews')
            collection_document_delete(u'URLs', URL.id)

            firestore_DeleteField(u'keys', URL.id, u'originalURL')
            firestore_DeleteField(u'keys', URL.id, u'pageViews')
            collection_document_delete(u'keys', URL.id)

        dic = collection_document_get_todict(u'random', u'random')
        URLs = dic['list']
        if originalURL in URLs:
            firestore_ArrayRemove(u'random', u'random', u'list', originalURL)
            firestore_Increment(u'random', u'random', u'total', -1)

# -----------------------------------------------------------------------------------

def error_handler():
    dic = collection_document_get_todict(u'random', u'random')
    total = dic['total']
    if total == 0:
        URL = 'https://www.google.com/'
    else:
        URLs = dic['list']
        randomNum = random.randrange(0, total)
        URL = URLs[randomNum]
    return URL

