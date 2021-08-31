from flask import Flask, render_template, request, redirect, abort, url_for
import random, string
import datetime
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

# -----------------------------------------------------------------------------------

def DB_generatedKey(originalURL):
    generatedKey = generate_key(key_length)
    keys = db.collection(u'keys').stream()
    keyIDs = [key.id for key in keys] + keywords
    while generatedKey in keyIDs:
        generatedKey = generate_key(key_length)
    append_data(originalURL, generatedKey)
    return generatedKey

def DB_customKey(originalURL, customKey):
    keys = db.collection(u'keys').stream()
    keyIDs = [key.id for key in keys] + keywords
    if customKey in keyIDs:
        return False
    append_data(originalURL, customKey)
    return True

def append_data(originalURL, key, expirationDate=None):
    key = key
    originalURL = originalURL
    generatedURL = GCP_URL + key
    dateCreated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    if expirationDate:
        pass
    else:
        expirationDate = dateCreated + datetime.timedelta(days=7)
    
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
    db.collection(u'random').document(u'random').update({
        u'list': firestore.ArrayUnion([originalURL]),
        u'total': firestore.Increment(1)
    })

# -----------------------------------------------------------------------------------

@app.route('/', methods=["GET","POST"])
def short_link():
    if request.method == 'GET':
        return render_template('index.html')

    originalURL = request.form.get('originalURl')
    if URL_check(originalURL):
        generatedURL = GCP_URL + DB_generatedKey(originalURL)
        message_post1 = 'link  :  '
        message_post2 = 'alias  :  '
        return render_template('index.html', message_post1 = message_post1, message_post2 = message_post2, \
                                originalURL = originalURL, generatedURL = generatedURL)
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
        if DB_customKey(originalURL, customKey):
            generatedURL = GCP_URL + customKey
            message_post1 = 'link  :  '
            message_post2 = 'alias  :  '
            return render_template('custom_link.html', message_post1 = message_post1, message_post2 = message_post2, \
                                   originalURL = originalURL, generatedURL = generatedURL)
        else:
            message_error1 = 'Sorry, this alias is already taken'
            message_error2 = 'Please try different characters'
            return render_template('custom_link.html', message_error1 = message_error1, message_error2 = message_error2)
    else:
        message_error1 = 'Please enter a valid URL and characters'
        return render_template('custom_link.html', message_error1 = message_error1)

# -----------------------------------------------------------------------------------------NEW

@app.route('/custom/expiration', methods=["GET","POST"])
def custom_expiration():
    if request.method == 'GET':
        return render_template('custom_expiration.html')

    inputYear = request.form.get('year')
    inputMonth = request.form.get('month')
    inputDate = request.form.get('date')
    inputHour = request.form.get('hour')
    inputMinute = request.form.get('minute')
    customKey = request.form.get('customKey')
    originalURL = request.form.get('originalURl')

    generatedURL = GCP_URL + customKey
    inputDate = inputYear + ' ' + inputMonth + ' ' + inputDate + ' ' + inputHour + ' ' + inputMinute
    message_post1 = 'link  :  '
    message_post2 = 'alias  :  '
    message_post3 = 'date  :  '
    return render_template('custom_expiration.html', message_post1 = message_post1, message_post2 = message_post2, \
                            message_post3 = message_post3, originalURL = originalURL, generatedURL = generatedURL, inputDate = inputDate)




    # if URL_check(originalURL) and key_check(customKey):
    #     if DB_customKey(originalURL, customKey):
    #         generatedURL = GCP_URL + customKey
    #         message_post1 = 'link  :  '
    #         message_post2 = 'alias  :  '
    #         return render_template('custom_expiration.html', message_post1 = message_post1, message_post2 = message_post2, \
    #                                originalURL = originalURL, generatedURL = generatedURL)
    #     else:
    #         message_error1 = 'Sorry, this alias is already taken'
    #         message_error2 = 'Please try different characters'
    #         return render_template('custom_expiration.html', message_error1 = message_error1, message_error2 = message_error2)
    # else:
    #     message_error1 = 'Please enter a valid URL and characters'
    #     return render_template('custom_expiration.html', message_error1 = message_error1)

# -----------------------------------------------------------------------------------------NEW

@app.route('/<string>')
def URL_redirect(string):
    string = string
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
        if dateNow == expirationDate or dateNow > expirationDate:
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

