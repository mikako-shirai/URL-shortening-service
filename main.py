from flask import Flask, render_template, request,  redirect, abort
import random, string
import re
import json
from ast import literal_eval


app = Flask(__name__)

key_length = 6

def generate_key(key_length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(key_length)])

def URL_check(originalURL):
    validFormat = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return True if re.match(validFormat, originalURL) else False

def checkDB(originalURL):
    with open('random_check.txt', 'r') as f:
        randoms = f.read().split(',')
    generatedKey = generate_key(key_length)
    while generatedKey in randoms:
        generatedKey = generate_key(key_length)
    append_data(originalURL, generatedKey)
    return generatedKey

def append_data(originalURL, generatedKey):
    new_data = { f'{generatedKey}': f'{originalURL}' }
    with open('database.json', 'ab+') as f:
        f.seek(0,2)  
        if f.tell() == 0 :
            f.write(json.dumps([new_data]).encode())
        else :
            f.seek(-1,2)
            f.truncate()
            f.write(',\n'.encode())
            f.write(json.dumps(new_data).encode())
            f.write(']'.encode())
    with open('random_check.txt', 'a') as f:
        f.write(',\n' + generatedKey)

@app.route('/', methods=["GET","POST"])
def get_post():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        originalURL = request.form.get('originalURl')
        if URL_check(originalURL):
            generatedURL = 'http://127.0.0.1:5000/' + checkDB(originalURL)
            message1 = 'original link  :   '
            message2 = 'new link  :  '
            return render_template('index.html', message_post1 = message1, message_post2 = message2, \
                                originalURL = originalURL, generatedURL = generatedURL)
        else:
            message_error = 'Please enter a valid URL'
            return render_template('index.html', message_error = message_error)

@app.route('/<string>')
def redirect_to_URL(string):
    if len(string) != key_length:
        abort(404)
    with open('database.json', "r") as f:
        db_read = f.read()
        db_list = literal_eval(db_read)
    originalURL = [key.get(string) for key in db_list if key.get(string)]
    if len(originalURL) > 0:
        return redirect(originalURL[0])
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    message = 'The requested URL was not found'
    return render_template('404.html', message = message), 404


if __name__ == "__main__":
    app.run()

