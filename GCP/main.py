from flask import Flask, render_template, request, redirect, abort
import random, string

# -------------------------------------------------------------------------
from google.cloud import firestore
import datetime
import firebase_admin
import re

db = firestore.Client()
default_app = firebase_admin.initialize_app()
# -------------------------------------------------------------------------

app = Flask(__name__)

key_length = 4

def generate_key(key_length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(key_length)])

# -------------------------------------------------------------------------
def checkURL(originalURL):
    validFormat = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return True if re.match(validFormat, originalURL) else False
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def checkDB(originalURL):
    generatedKey = generate_key(key_length)

    key_ref = db.collection(u'generatedKeys')
    keys = key_ref.stream()

    while generatedKey in keys:
        generatedKey = generate_key(key_length)
    append_data(originalURL, generatedKey)
    return generatedKey
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
def append_data(originalURL, generatedKey):
    generatedKey = generatedKey
    originalURL = originalURL
    generatedURl = 'https://firestoretest-319604.an.r.appspot.com/' + generatedKey                    # URL
    dateCreated = datetime.datetime.now()
    
    URL_ref = db.collection(u'URLs').document(generatedKey)
    URL_ref.set({
        u'originalURL': originalURL,
        u'generatedURL': generatedURl,
        u'generatedKey': generatedKey,
        u'dateCreated': dateCreated,
        u'pageView': 0
    })

    data = {
        u'pageView': 0
    }
    db.collection(u'generatedKeys').document(generatedKey).set(data)
# -------------------------------------------------------------------------

# --------------------------------------------------------------------------
@app.route('/', methods=["GET","POST"])
def get_post():
    if request.method == 'GET':
        message = 'enter a URL to be shortened'
        return render_template('index.html', message_get = message)
    else:
        originalURL = request.form.get('originalURl')
        if checkURL(originalURL):
            generatedURL = 'https://firestoretest-319604.an.r.appspot.com/' + checkDB(originalURL)   # URL
            message1 = 'original link  :   '
            message3 = 'short link  :  '
            return render_template('index.html', message_post1 = message1, message_post2 = originalURL, \
                                message_post3 = message3, message_post4 = generatedURL)
        else:
            message_error = 'Please enter a valid URL'
            return render_template('index.html', message_error = message_error)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
@app.route('/<string>')
def redirect_to_URL(string):
    generatedKey = string

    if len(generatedKey) != key_length:
        abort(404)
    
    URL_ref = db.collection(u'URLs').document(generatedKey)
    key_ref = db.collection(u'generatedKeys').document(generatedKey)
    URL = URL_ref.get()

    if URL.exists:
        pageView = URL.to_dict()['pageView']
        URL_ref.set({
            u'pageView': pageView + 1
        }, merge=True)
        key_ref.set({
            u'pageView': pageView + 1
        }, merge=True)

        originalURL = URL.to_dict()['originalURL']
        return redirect(originalURL)
    else:
        abort(404)
# -------------------------------------------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    message = 'The requested URL was not found'
    return render_template('404.html', message = message), 404

# -------------------------------------------------------------------------
# TEST
@app.route('/cron')
def expiration_check():
    dateNow = datetime.datetime.now()
    key_ref = db.collection(u'generatedKeys_test').stream()


    for key in key_ref:
        expirationDate = key.to_dict()['expirationDate']
        if dateNow > expirationDate: # 消す
            # delete


    URL_set = db.collection(u'URLs_test').document(generatedKey)
    key_set = db.collection(u'generatedKeys_test').document(generatedKey)
    expired_set = db.collection(u'generatedKeys_test').document(generatedKey)

    # doc_ref.set({
    #     u'pageView': pageView + 1
    # }, merge=True)
    # key_ref.set({
    #     u'pageView': pageView + 1
    # }, merge=True)


    app.logger.debug(f'data difference: {dateNow - expirationDate}')
    app.logger.debug(f'Document data without .to_dict(): {key_ref}')
    app.logger.debug(f'Document type without .to_dict(): {type(key_ref)}')
    app.logger.debug(f'Document data: {key_ref.to_dict()}')
    app.logger.debug(f'Document type: {type(key_ref.to_dict())}')
    return "", 200

def append_data_TEST(originalURL, generatedKey):
    generatedKey = generatedKey
    originalURL = originalURL
    generatedURl = 'https://firestoretest-319604.an.r.appspot.com/' + generatedKey
    dateCreated = datetime.datetime.now()
    expirationDate = dateCreated + datetime.timedelta(minutes=4)
    
    URL_ref = db.collection(u'URLs_test').document(generatedKey)
    URL_ref.set({
        u'originalURL' : originalURL,
        u'generatedURL' : generatedURl,
        u'dateCreated' : dateCreated,
        u'expirationDate' : expirationDate,
        u'status' : True,
        u'pageView' : 0
    })

    key_data = {
        u'expirationDate' : expirationDate,
        u'status' : True,
        u'pageView' : 0
    }
    db.collection(u'generatedKeys_test').document(generatedKey).set(key_data)
# -------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)

