from flask import Flask, render_template, request, redirect, abort, url_for
import random, string
import datetime
from dateutil.relativedelta import relativedelta
import re
import os
from google.cloud import firestore


db = firestore.Client()
app = Flask(__name__)

key_length = 5
GCP_URL = 'https://short-321807.an.r.appspot.com/'
keywords = ['custom', 'expiration', 'link', '404', 'cron']

# -----------------------------------------------------------------------------------

def generate_key(key_length):
    letters = [random.choice(string.ascii_letters + string.digits) for i in range(key_length)]
    return ''.join(letters)

def get_date():
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    string = dateNow.strftime('%Y%m')
    year1 = int(string[:4])
    month = int(string[4:])
    if month >= 7:
        year2 = year1 + 1
    else:
        year2 = None
    return year1, year2

def URL_check(originalURL):
    validFormat = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return True if re.match(validFormat, originalURL) else False

def key_check(customKey):
    if len(customKey) < 6 or len(customKey) > 30:
        return False
    invalid = '/ \\'
    for char in customKey:
        if char in invalid:
            return False
    return True

def date_check(dateSet):
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    date6months = dateNow + relativedelta(months=+6, minutes=-30)
    try:
        expirationDate = datetime.datetime.strptime(dateSet, '%Y/%m/%d %H:%M:%S%z')
    except ValueError:
        return False
    if expirationDate < dateNow or expirationDate > date6months:
        return False
    return True

# -----------------------------------------------------------------------------------

def DB_generatedKey(originalURL, expirationDate=None):
    generatedKey = generate_key(key_length)
    keys = db.collection(u'keys').stream()
    keyIDs = [key.id for key in keys] + keywords
    while generatedKey in keyIDs:
        generatedKey = generate_key(key_length)
    if expirationDate:
        append_data(originalURL, generatedKey, expirationDate)
    else:
        expirationDate = append_data(originalURL, generatedKey)
    return [generatedKey, expirationDate]

def DB_customKey(originalURL, customKey, expirationDate=None):
    keys = db.collection(u'keys').stream()
    keyIDs = [key.id for key in keys] + keywords
    if customKey in keyIDs:
        return False
    if expirationDate:
        append_data(originalURL, customKey, expirationDate)
    else:
        expirationDate = append_data(originalURL, customKey)
    return expirationDate

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
    URLs = list(dic['list'])
    if originalURL not in URLs:
        db.collection(u'random').document(u'random').update({
            u'list': firestore.ArrayUnion([originalURL]),
            u'total': firestore.Increment(1)
        })
    return expirationDate

# -----------------------------------------------------------------------------------

@app.route('/', methods=["GET","POST"])
def short_link():
    if request.method == 'GET':
        return render_template('index.html')

    originalURL = request.form.get('originalURl')
    if URL_check(originalURL):
        result = DB_generatedKey(originalURL)
        generatedKey, dateSet = result[0], result[1]
        generatedURL = GCP_URL + generatedKey
        dateSet = dateSet.strftime('%Y/%m/%d %H:%M')
        message_post1 = 'link  :  '
        message_post2 = 'alias  :  '
        message_post3 = 'expires on  :  '
        flg = True
        return render_template('index.html', message_post1 = message_post1, message_post2 = message_post2, \
                               message_post3 = message_post3, originalURL = originalURL, generatedURL = generatedURL, \
                               dateSet = dateSet, flg = flg)
    else:
        message_error = 'Please enter a valid URL'
        return render_template('index.html', message_error = message_error)

@app.route('/custom', methods=["GET","POST"])
def custom_link():
    if request.method == 'GET':
        return render_template('custom_link.html')

    customKey = request.form.get('customKey')
    originalURL = request.form.get('originalURl')
    if URL_check(originalURL) and key_check(customKey):
        dateSet = DB_customKey(originalURL, customKey)
        if dateSet:
            generatedURL = GCP_URL + customKey
            dateSet = dateSet.strftime('%Y/%m/%d %H:%M')
            message_post1 = 'link  :  '
            message_post2 = 'alias  :  '
            message_post3 = 'expires on  :  '
            flg = True
            return render_template('custom_link.html', message_post1 = message_post1, message_post2 = message_post2, \
                                   message_post3 = message_post3, originalURL = originalURL, generatedURL = generatedURL, \
                                   dateSet = dateSet, flg = flg)
        else:
            message_error1 = 'Sorry, this alias is already taken'
            message_error2 = 'Please try different characters'
    else:
        message_error1 = 'Please enter valid characters and URL'
        message_error2 = ''
    return render_template('custom_link.html', message_error1 = message_error1, message_error2 = message_error2)

# -----------------------------------------------------------------------------------------NEW

@app.route('/custom/expiration', methods=["GET","POST"])
def custom_expiration():
    year1, year2 = get_date()
    if request.method == 'GET':
        return render_template('custom_expiration.html', year1 = year1, year2 = year2)

    year = request.form.get('year')
    month = request.form.get('month')
    date = request.form.get('date')
    hour = request.form.get('hour')
    minute = request.form.get('minute')
    customKey = request.form.get('customKey')
    originalURL = request.form.get('originalURl')
    dateSet = year + '/' + month + '/' + date + ' ' + hour + ':' + minute + ':00+0900'

    if date_check(dateSet) and URL_check(originalURL) and key_check(customKey):
        expirationDate = datetime.datetime.strptime(dateSet, '%Y/%m/%d %H:%M:%S%z')
        dateSet = DB_customKey(originalURL, customKey, expirationDate)
        if dateSet:
            generatedURL = GCP_URL + customKey
            dateSet = dateSet.strftime('%Y/%m/%d %H:%M')
            message_post1 = 'link  :  '
            message_post2 = 'alias  :  '
            message_post3 = 'expires on  :  '
            flg = True
            return render_template('custom_expiration.html', year1 = year1, year2 = year2, message_post1 = message_post1, \
                                   message_post2 = message_post2, message_post3 = message_post3, \
                                   originalURL = originalURL, generatedURL = generatedURL, dateSet = dateSet, flg = flg)
        else:
            message_error1 = 'Sorry, this alias is already taken'
            message_error2 = 'Please try different characters'
            message_error3 = ''
    else:
        message_error1 = 'Please enter a valid date' if not date_check(dateSet) else ''
        message_error2 = 'Please enter valid characters' if not key_check(customKey) else ''
        message_error3 = 'Please enter a valid URL' if not URL_check(originalURL) else ''
    return render_template('custom_expiration.html', year1 = year1, year2 = year2, message_error1 = message_error1, \
                           message_error2 = message_error2, message_error3 = message_error3)

# -----------------------------------------------------------------------------------------NEW

@app.route('/<string>')
def URL_redirect(string):
    if len(string) < key_length or len(string) > 30:
        abort(404)

    key = db.collection(u'keys').document(string).get()
    if key.exists:
        db.collection(u'URLs').document(string).update({
            u'pageViews': firestore.Increment(1)
        })
        db.collection(u'keys').document(string).update({
            u'pageViews': firestore.Increment(1)
        })
        originalURL = key.to_dict()['originalURL']
        return redirect(originalURL)
    else:
        abort(404)

@app.route('/cron', methods=['GET'])
def expiration_check():
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    URLs = db.collection(u'URLs').stream()

    for URL in URLs:
        expirationDate = URL.to_dict()['expirationDate']
        if dateNow >= expirationDate:
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
            originalURL = URL.to_dict()['originalURL']
            db.collection(u'random').document(u'random').update({
                u'list': firestore.ArrayRemove([originalURL]),
                u'total': firestore.Increment(-1)
            })
    return '', 200

# -----------------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    dic = db.collection(u'random').document(u'random').get().to_dict()
    total = dic['total']
    if total == 0:
        URL = 'https://www.google.com/'
    else:
        URLs = list(dic['list'])
        randomNum = random.randrange(0, total)
        URL = URLs[randomNum]
    return render_template('404.html', URL = URL), 404

# -----------------------------------------------------------------------------------

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, \
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    app.run()

