from flask import Flask, render_template, request, redirect, abort
import random, string
import datetime
import re
from google.cloud import firestore


db = firestore.Client()
app = Flask(__name__)

key_length = 6
GCP_URL = 'https://firestoretest-319604.an.r.appspot.com/'

# -----------------------------------------------------------------------------------

def generate_key(key_length):
    letters = [random.choice(string.ascii_letters + string.digits) for i in range(key_length)]
    return ''.join(letters)

def URL_check(originalURL):
    validFormat = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return True if re.match(validFormat, originalURL) else False

# -----------------------------------------------------------------------------------

def DB_check(originalURL):
    generatedKey = generate_key(key_length)
    keys = db.collection(u'keys').stream()
    keyIDs = [key.id for key in keys]

    while generatedKey in keyIDs:
        generatedKey = generate_key(key_length)
    append_data(originalURL, generatedKey)
    return generatedKey

def append_data(originalURL, generatedKey):
    generatedKey = generatedKey
    originalURL = originalURL
    generatedURl = GCP_URL + generatedKey
    dateCreated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    expirationDate = dateCreated + datetime.timedelta(minutes=1)
    
    db.collection(u'URLs').document(generatedKey).set({
        u'originalURL': originalURL,
        u'generatedURL': generatedURl,
        u'dateCreated': dateCreated,
        u'expirationDate': expirationDate,
        u'pageViews': 0
    })
    db.collection(u'keys').document(generatedKey).set({
        u'originalURL': originalURL,
        u'pageViews': 0
    })

# -----------------------------------------------------------------------------------

@app.route('/', methods=["GET","POST"])
def get_post():
    if request.method == 'GET':
        message = 'enter a URL to be shortened'
        return render_template('index.html', message_get = message)
    else:
        originalURL = request.form.get('originalURl')
        if URL_check(originalURL):
            generatedURL = GCP_URL + DB_check(originalURL)
            message1 = 'original link  :   '
            message3 = 'short link  :  '
            return render_template('index.html', \
                                   message_post1 = message1, message_post2 = originalURL, \
                                   message_post3 = message3, message_post4 = generatedURL)
        else:
            message_error = 'Please enter a valid URL'
            return render_template('index.html', message_error = message_error)

@app.route('/<string>')
def URL_redirect(string):
    generatedKey = string
    if len(generatedKey) != key_length:
        abort(404)

    key = db.collection(u'keys').document(generatedKey).get()
    if key.exists:
        db.collection(u'URLs').document(generatedKey).update({
            u'pageViews': firestore.Increment(1)
        })
        db.collection(u'keys').document(generatedKey).update({
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
        if dateNow > expirationDate:
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
    return '', 200

# -----------------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    message = 'The requested URL was not found'
    return render_template('404.html', message = message), 404


if __name__ == "__main__":
    app.run()

