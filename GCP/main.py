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
keywords = ['custom', 'short', 'expiration', 'link', '404', 'cron', \
            'index', 'custom_exp', 'short_exp', 'result']

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
    return [year1, year2]

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
    date6months = dateNow + relativedelta(months=+6, minutes=-1)
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
    return generatedKey, expirationDate

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

    dicData, errors, flg = {}, [], False
    originalURL = request.form.get('originalURl')

    if URL_check(originalURL):
        generatedKey, dateSet = DB_generatedKey(originalURL)
        generatedURL = GCP_URL + generatedKey
        dateSet = dateSet.strftime('%Y/%m/%d %H:%M')
        flg = True
        dicData['URL'] = originalURL
        dicData['alias'] = generatedURL
        dicData['expiration'] = dateSet
    else:
        errors.append('Please enter a valid URL')
    return render_template('index.html', dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

@app.route('/custom', methods=["GET","POST"])
def custom_link():
    if request.method == 'GET':
        return render_template('custom.html')

    dicData, errors, flg = {}, [], False
    customKey = request.form.get('customKey')
    originalURL = request.form.get('originalURl')

    if key_check(customKey) and URL_check(originalURL):
        dateSet = DB_customKey(originalURL, customKey)
        if dateSet:
            generatedURL = GCP_URL + customKey
            dateSet = dateSet.strftime('%Y/%m/%d %H:%M')
            flg = True
            dicData['URL'] = originalURL
            dicData['alias'] = generatedURL
            dicData['expiration'] = dateSet
        else:
            errors.append('Sorry, this alias is already taken')
            errors.append('Please try different characters')
    else:
        if not key_check(customKey): errors.append('Please enter valid characters')
        if not URL_check(originalURL): errors.append('Please enter a valid URL')
    return render_template('custom.html', dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

@app.route('/expiration', methods=["GET","POST"])
def short_expiration():
    years = get_date()
    if request.method == 'GET':
        return render_template('index_exp.html', years = years)

    dicData, errors, flg = {}, [], False
    year = request.form.get('year')
    month = request.form.get('month')
    date = request.form.get('date')
    hour = request.form.get('hour')
    minute = request.form.get('minute')
    originalURL = request.form.get('originalURl')
    dateSet = year + '/' + month + '/' + date + ' ' + hour + ':' + minute + ':00+0900'

    if date_check(dateSet) and URL_check(originalURL):
        expirationDate = datetime.datetime.strptime(dateSet, '%Y/%m/%d %H:%M:%S%z')
        generatedKey, dateSet = DB_generatedKey(originalURL, expirationDate)
        generatedURL = GCP_URL + generatedKey
        dateSet = dateSet.strftime('%Y/%m/%d %H:%M')
        flg = True
        dicData['URL'] = originalURL
        dicData['alias'] = generatedURL
        dicData['expiration'] = dateSet
    else:
        if not date_check(dateSet): errors.append('Please enter a valid date')
        if not URL_check(originalURL): errors.append('Please enter a valid URL')
    return render_template('index_exp.html', years = years, dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

@app.route('/expiration/custom', methods=["GET","POST"])
def custom_expiration():
    years = get_date()
    if request.method == 'GET':
        return render_template('custom_exp.html', years = years)

    dicData, errors, flg = {}, [], False
    year = request.form.get('year')
    month = request.form.get('month')
    date = request.form.get('date')
    hour = request.form.get('hour')
    minute = request.form.get('minute')
    customKey = request.form.get('customKey')
    originalURL = request.form.get('originalURl')
    dateSet = year + '/' + month + '/' + date + ' ' + hour + ':' + minute + ':00+0900'

    if date_check(dateSet) and key_check(customKey) and URL_check(originalURL):
        expirationDate = datetime.datetime.strptime(dateSet, '%Y/%m/%d %H:%M:%S%z')
        dateSet = DB_customKey(originalURL, customKey, expirationDate)
        if dateSet:
            generatedURL = GCP_URL + customKey
            dateSet = dateSet.strftime('%Y/%m/%d %H:%M')
            flg = True
            dicData['URL'] = originalURL
            dicData['alias'] = generatedURL
            dicData['expiration'] = dateSet
        else:
            errors.append('Sorry, this alias is already taken')
            errors.append('Please try different characters')
    else:
        if not date_check(dateSet): errors.append('Please enter a valid date')
        if not key_check(customKey): errors.append('Please enter valid characters')
        if not URL_check(originalURL): errors.append('Please enter a valid URL')
    return render_template('custom_exp.html', years = years, dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

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
        # URLs = list(dic['list'])
        URLs = dic['list']
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

