from URLshortener.DatabaseWrapper import *

import datetime
from dateutil.relativedelta import relativedelta
import random


GCP_URL = 'https://short-321807.an.r.appspot.com/'
keywords = ['custom', 'expiration', 'analysis', 'link', '404', 'error', 'cron', \
            'index', 'index_exp', 'custom_exp', 'result', 'selector']

# -----------------------------------------------------------------------------------

def get_keys():
    keysDB = c_stream(u'keys')
    keys = [key.id for key in keysDB] + keywords
    return keys

def append_data(originalURL, key, expirationDate=None):
    generatedURL = GCP_URL + key
    dateCreated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    if not expirationDate:
        expirationDate = dateCreated + relativedelta(days=+14)

    cd_set(u'URLs', key, {
        u'originalURL': originalURL,
        u'generatedURL': generatedURL,
        u'dateCreated': dateCreated,
        u'expirationDate': expirationDate,
        u'pageViews': 0
    })
    cd_set(u'keys', key, {
        u'originalURL': originalURL,
        u'pageViews': 0
    })

    dic = cd_get_toDict(u'random', u'random')
    URLs = dic['list']
    if originalURL not in URLs:
        fs_arrayUnion(u'random', u'random', u'list', originalURL)
        fs_increment(u'random', u'random', u'total', 1)

# -----------------------------------------------------------------------------------

def get_analysis(generatedURL, key):
    dicData = {}
    URLactive = cd_get(u'URLs', key)
    URLold = cd_get(u'expiredURLs', key)
    
    if exists(URLactive):
        URLactive = cd_toDict(URLactive)
        dateCreated = URLactive['dateCreated']
        expirationDate = URLactive['expirationDate']
        dateCreated = (dateCreated + relativedelta(hours=+9)).strftime('%Y/%m/%d %H:%M') + ' (UTC+09:00)'
        expirationDate = (expirationDate + relativedelta(hours=+9)).strftime('%Y/%m/%d %H:%M') + ' (UTC+09:00)'

        dicData['availability'] = 'Available'
        dicData['originalURL'] = URLactive['originalURL']
        dicData['generatedURL'] = generatedURL
        dicData['dateCreated'] = dateCreated
        dicData['expirationDate'] = expirationDate
        dicData['pageViews'] = URLactive['pageViews']

    elif exists(URLold):
        URLold = cd_toDict(URLold)
        dateCreated = URLold['dateCreated']
        expirationDate = URLold['expirationDate']
        dateCreated = (dateCreated + relativedelta(hours=+9)).strftime('%Y/%m/%d %H:%M') + ' (UTC+09:00)'
        expirationDate = (expirationDate + relativedelta(hours=+9)).strftime('%Y/%m/%d %H:%M') + ' (UTC+09:00)'

        dicData['availability'] = 'Not Available'
        dicData['originalURL'] = URLold['originalURL']
        dicData['generatedURL'] = generatedURL
        dicData['dateCreated'] = dateCreated
        dicData['expirationDate'] = expirationDate
        dicData['pageViews'] = URLold['pageViews']
    return dicData

def get_redirect(string):
    key = cd_get(u'keys', string)
    if exists(key):
        fs_increment(u'URLs', string, u'pageViews', 1)
        fs_increment(u'keys', string, u'pageViews', 1)
        originalURL = cd_toDict(key)['originalURL']
        return originalURL
    return False

# -----------------------------------------------------------------------------------

def cron_job():
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    URLs = c_stream(u'URLs')

    for URL in URLs:
        dic = cd_toDict(URL)
        expirationDate = dic['expirationDate']
        if dateNow >= expirationDate:
            originalURL = dic['originalURL']
            # add expired URL information to 'expiredURLs' collection
            data = cd_get_toDict(u'URLs', URL.id)
            cd_set(u'expiredURLs', URL.id, data)

            # deletion
            fs_delete(u'URLs', URL.id, u'originalURL')
            fs_delete(u'URLs', URL.id, u'generatedURL')
            fs_delete(u'URLs', URL.id, u'dateCreated')
            fs_delete(u'URLs', URL.id, u'expirationDate')
            fs_delete(u'URLs', URL.id, u'pageViews')
            cd_delete(u'URLs', URL.id)

            fs_delete(u'keys', URL.id, u'originalURL')
            fs_delete(u'keys', URL.id, u'pageViews')
            cd_delete(u'keys', URL.id)

        dic = cd_get_toDict(u'random', u'random')
        URLs = dic['list']
        if originalURL in URLs:
            fs_arrayRemove(u'random', u'random', u'list', originalURL)
            fs_increment(u'random', u'random', u'total', -1)

# -----------------------------------------------------------------------------------

def error_handler():
    dic = cd_get_toDict(u'random', u'random')
    total = dic['total']
    if total == 0:
        URL = 'https://www.google.com/'
    else:
        URLs = dic['list']
        randomNum = random.randrange(0, total)
        URL = URLs[randomNum]
    return URL

