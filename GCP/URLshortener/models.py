from URLshortener import db

from google.cloud import firestore
import datetime
import random


GCP_URL = 'https://short-321807.an.r.appspot.com/'
keywords = ['custom', 'expiration', 'analysis', 'link', '404', 'error', 'cron', \
            'index', 'index_exp', 'custom_exp', 'result', 'selector']

# -----------------------------------------------------------------------------------

def get_keys():
    keysDB = db.collection(u'keys').stream()
    keys = [key.id for key in keysDB] + keywords
    return keys

def append_data(originalURL, key, expirationDate=None):
    generatedURL = GCP_URL + key
    dateCreated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    if not expirationDate:
        expirationDate = dateCreated + datetime.timedelta(days=14)

    db.collection(u'URLs').document(key).set({
        u'originalURL': originalURL,
        u'generatedURL': generatedURL,
        u'dateCreated': dateCreated,
        u'expirationDate': expirationDate,
        u'pageViews': 0
    })
    db.collection(u'keys').document(key).set({
        u'originalURL': originalURL,
        u'pageViews': 0
    })

    dic = db.collection(u'random').document(u'random').get().to_dict()
    URLs = dic['list']
    if originalURL not in URLs:
        total = len(URLs)
        db.collection(u'random').document(u'random').update({
            u'list': firestore.ArrayUnion([originalURL]),
            u'total': total + 1
        })

# -----------------------------------------------------------------------------------

def get_analysis(generatedURL, key):
    dicData = {}
    URLactive = db.collection(u'URLs').document(key).get()
    URLold = db.collection(u'expiredURLs').document(key).get()
    
    if URLactive.exists:
        URLactive = URLactive.to_dict()
        dateCreated = URLactive['dateCreated']
        expirationDate = URLactive['expirationDate']
        dateCreated = dateCreated.strftime('%Y/%m/%d %H:%M')
        expirationDate = expirationDate.strftime('%Y/%m/%d %H:%M')

        dicData['availability'] = 'Available'
        dicData['originalURL'] = URLactive['originalURL']
        dicData['generatedURL'] = generatedURL
        dicData['dateCreated'] = dateCreated
        dicData['expirationDate'] = expirationDate
        dicData['pageViews'] = URLactive['pageViews']

    elif URLold.exists:
        URLold = URLold.to_dict()
        dateCreated = URLold['dateCreated']
        expirationDate = URLold['expirationDate']
        dateCreated = dateCreated.strftime('%Y/%m/%d %H:%M')
        expirationDate = expirationDate.strftime('%Y/%m/%d %H:%M')

        dicData['availability'] = 'Not Available'
        dicData['originalURL'] = URLold['originalURL']
        dicData['generatedURL'] = generatedURL
        dicData['dateCreated'] = dateCreated
        dicData['expirationDate'] = expirationDate
        dicData['pageViews'] = URLold['pageViews']
    return dicData

def get_redirect(string):
    key = db.collection(u'keys').document(string).get()
    if key.exists:
        db.collection(u'URLs').document(string).update({
            u'pageViews': firestore.Increment(1)
        })
        db.collection(u'keys').document(string).update({
            u'pageViews': firestore.Increment(1)
        })
        originalURL = key.to_dict()['originalURL']
        return originalURL
    return False

# -----------------------------------------------------------------------------------

def cron_job():
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    URLs = db.collection(u'URLs').stream()

    for URL in URLs:
        dic = URL.to_dict()
        expirationDate = dic['expirationDate']
        if dateNow >= expirationDate:
            originalURL = dic['originalURL']
            # add expired URL information to 'expiredURLs' collection
            data = db.collection(u'URLs').document(URL.id).get().to_dict()
            db.collection(u'expiredURLs').document(URL.id).set(data)

            # deletion
            db.collection(u'URLs').document(URL.id).update({
                u'originalURL': firestore.DELETE_FIELD,
                u'generatedURL': firestore.DELETE_FIELD,
                u'dateCreated': firestore.DELETE_FIELD,
                u'expirationDate': firestore.DELETE_FIELD,
                u'pageViews': firestore.DELETE_FIELD
            })
            db.collection(u'URLs').document(URL.id).delete()
            db.collection(u'keys').document(URL.id).update({
                u'originalURL': firestore.DELETE_FIELD,
                u'pageViews': firestore.DELETE_FIELD
            })
            db.collection(u'keys').document(URL.id).delete()
            db.collection(u'random').document(u'random').update({
                u'list': firestore.ArrayRemove([originalURL]),
                u'total': firestore.Increment(-1)
            })

# -----------------------------------------------------------------------------------

def error_handler():
    dic = db.collection(u'random').document(u'random').get().to_dict()
    total = dic['total']
    if total == 0:
        URL = 'https://www.google.com/'
    else:
        URLs = dic['list']
        randomNum = random.randrange(0, total)
        URL = URLs[randomNum]
    return URL

