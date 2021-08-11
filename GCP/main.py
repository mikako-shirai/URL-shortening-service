from flask import Flask, render_template, request, redirect, abort
import random, string

# -------------------------------------------------------------------------
from google.cloud import firestore
import datetime
# import firebase_admin
import re

db = firestore.Client()
# default_app = firebase_admin.initialize_app()
# -------------------------------------------------------------------------


app = Flask(__name__)

key_length = 6
GCP_URL = 'https://firestoretest-319604.an.r.appspot.com/'


def generate_key(key_length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(key_length)])

# -------------------------------------------------------------------------
def URL_check(originalURL):
    validFormat = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return True if re.match(validFormat, originalURL) else False
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# def DB_check(originalURL):
#     generatedKey = generate_key(key_length)
#     keys = db.collection(u'generatedKeys').stream()

#     while generatedKey in keys:
#         generatedKey = generate_key(key_length)
#     append_data(originalURL, generatedKey)
#     return generatedKey
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# def append_data(originalURL, generatedKey):
#     generatedKey = generatedKey
#     originalURL = originalURL
#     generatedURl = GCP_URL + generatedKey
#     dateCreated = datetime.datetime.now()
    
#     db.collection(u'URLs').document(generatedKey).set({
#         u'originalURL': originalURL,
#         u'generatedURL': generatedURl,
#         u'generatedKey': generatedKey,
#         u'dateCreated': dateCreated,
#         u'pageView': 0
#     })
#     db.collection(u'generatedKeys').document(generatedKey).set({
#         u'pageView': 0
#     })
# -------------------------------------------------------------------------

# --------------------------------------------------------------------------
# @app.route('/', methods=["GET","POST"])
# def get_post():
#     if request.method == 'GET':
#         message = 'enter a URL to be shortened'
#         return render_template('index.html', message_get = message)
#     else:
#         originalURL = request.form.get('originalURl')
#         if URL_check(originalURL):
#             generatedURL = GCP_URL + DB_check(originalURL)
#             message1 = 'original link  :   '
#             message3 = 'short link  :  '
#             return render_template('index.html', \
#                                    message_post1 = message1, message_post2 = originalURL, \
#                                    message_post3 = message3, message_post4 = generatedURL)
#         else:
#             message_error = 'Please enter a valid URL'
#             return render_template('index.html', message_error = message_error)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# @app.route('/<string>')
# def URL_redirect(string):
#     generatedKey = string
#     if len(generatedKey) != key_length:
#         abort(404)

#     URL = db.collection(u'URLs').document(generatedKey).get()
#     if URL.exists:
#         db.collection(u'URLs').document(generatedKey).update({
#             u'pageView': firestore.Increment(1)
#         })
#         db.collection(u'generatedKeys').document(generatedKey).update({
#             u'pageView': firestore.Increment(1)
#         })

#         originalURL = URL.to_dict()['originalURL']
#         return redirect(originalURL)
#     else:
#         abort(404)
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------cron TEST

def DB_check(originalURL):
    generatedKey = generate_key(key_length)
    keys = db.collection(u'generatedKeys_test').stream()

    while generatedKey in keys:
        generatedKey = generate_key(key_length)
    append_data_TEST(originalURL, generatedKey)
    return generatedKey

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

    URL = db.collection(u'URLs_test').document(generatedKey).get()
    if URL.exists:
        db.collection(u'URLs_test').document(generatedKey).update({
            u'pageView': firestore.Increment(1)
        })
        db.collection(u'generatedKeys_test').document(generatedKey).update({
            u'pageView': firestore.Increment(1)
        })
        originalURL = URL.to_dict()['originalURL']
        return redirect(originalURL)
    else:
        abort(404)

# ---------------------------------------------------------------------------HERE
@app.route('/cron', methods=['GET'])
def expiration_check():
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    keys = db.collection(u'generatedKeys_test').stream()

    for key in keys:
        expirationDate = key.to_dict()['expirationDate']
        if dateNow > expirationDate:
            # add expired URL information to 'expiredURL_test' collection
            data = db.collection(u'URLs_test').document(key.id).get().to_dict()
            db.collection(u'expiredURL_test').document(key.id).set(data)

            # deletion
            db.collection(u'URLs_test').document(key.id).update({
                u'originalURL' : firestore.DELETE_FIELD,
                u'generatedURL' : firestore.DELETE_FIELD,
                u'dateCreated' : firestore.DELETE_FIELD,
                u'expirationDate' : firestore.DELETE_FIELD,
                u'pageView' : firestore.DELETE_FIELD
            })
            db.collection(u'URLs_test').document(key.id).delete()
            db.collection(u'generatedKeys_test').document(key.id).update({
                u'expirationDate' : firestore.DELETE_FIELD,
                u'pageView' : firestore.DELETE_FIELD
            })
            db.collection(u'generatedKeys_test').document(key.id).delete()
    return '', 200

def append_data_TEST(originalURL, generatedKey):
    generatedKey = generatedKey
    originalURL = originalURL
    generatedURl = GCP_URL + generatedKey
    dateCreated = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    expirationDate = dateCreated + datetime.timedelta(minutes=1)
    
    db.collection(u'URLs_test').document(generatedKey).set({
        u'originalURL' : originalURL,
        u'generatedURL' : generatedURl,
        u'dateCreated' : dateCreated,
        u'expirationDate' : expirationDate,
        u'pageView' : 0
    })
    db.collection(u'generatedKeys_test').document(generatedKey).set({
        u'expirationDate' : expirationDate,
        u'pageView' : 0
    })
# ---------------------------------------------------------------------------HERE
# -------------------------------------------------------------------------cron TEST

@app.errorhandler(404)
def page_not_found(e):
    message = 'The requested URL was not found'
    return render_template('404.html', message = message), 404


if __name__ == "__main__":
    app.run(debug=True)



 
#deletion (GCP consoleのfirestore上で消すと全てのネストされたデータも消されるためそちらが好ましい)
        # db.collection(u'URLs_test').document(URL.id).update({
        #     u'originalURL' : firestore.DELETE_FIELD,
        #     u'generatedURL' : firestore.DELETE_FIELD,
        #     u'dateCreated' : firestore.DELETE_FIELD,
        #     u'expirationDate' : firestore.DELETE_FIELD,
        #     u'pageView' : firestore.DELETE_FIELD
        # })
        # db.collection(u'URLs_test').document(URL.id).delete()

        # db.collection(u'generatedKeys_test').document(URL.id).update({
        #     u'expirationDate' : firestore.DELETE_FIELD,
        #     u'pageView' : firestore.DELETE_FIELD
        # })
        # db.collection(u'generatedKeys_test').document(URL.id).delete()


        # db.collection(u'TEST').document(URL.id).update({
        #     u'difference' : firestore.DELETE_FIELD
        # })
        # db.collection(u'TEST').document(URL.id).delete()


        # db.collection(u'expiredURL_test').document(URL.id).update({
        #     u'originalURL' : firestore.DELETE_FIELD,
        #     u'generatedURL' : firestore.DELETE_FIELD,
        #     u'dateCreated' : firestore.DELETE_FIELD,
        #     u'dateRemoved' : firestore.DELETE_FIELD,
        #     u'pageView' : firestore.DELETE_FIELD
        # })
        # db.collection(u'expiredURL_test').document(URL.id).delete()

