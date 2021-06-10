# POC
from flask import Flask, render_template, request,  redirect, url_for
import random, string
import json
from ast import literal_eval
# import shelve


'''
{
    {'original1': 
        {'generatedURL': 'n4anlvi', 
         'customURL': 'this',
         'exp': '20211001'
        }
    }, 
    {'original2': 
        {'generatedURL': 'm07aliq', 
         'customURL': 'that',
         'exp': '20211102'
        }
    }
}

{'original1': {'generatedURL': 'n4anlvi', 'customURL': 'this', 'exp': '20211001'}}
'''


app = Flask(__name__)


def generateURL(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

def checkDB(originalURL):
    with open('random_check.txt', 'r') as f:
        randoms = f.read().split(',')
    generatedURL = generateURL(7)
    while generatedURL in randoms:
        generatedURL = generateURL(7)
    append_data(originalURL, generatedURL)
    return generatedURL

def append_data(originalURL, generatedURL):
    new_data = { f'{generatedURL}': f'{originalURL}' }
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
        f.write(',\n' + generatedURL)

@app.route('/', methods=["GET","POST"])
def get_post():
    if request.method == 'GET':
        message = 'enter a URL to be shortened'
        return render_template('index.html', message_get = message)
    else:
        originalURL = request.form.get('originalURl')
        generatedURL = 'http://127.0.0.1:5000/' + checkDB(originalURL)
        message1 = 'original link  :   '
        message3 = 'short link  :  '
        return render_template('index.html', message_post1 = message1, message_post2 = originalURL, \
                               message_post3 = message3, message_post4 = generatedURL)

@app.route('/<URL>')
def redirect_to_URL(URL):
    with open('database.json', "r") as f:
        db_read = f.read()
        db_list = literal_eval(db_read)
    originalURL = [key.get(URL) for key in db_list if key.get(URL)]
    return redirect(originalURL[0])


if __name__ == "__main__":
    app.run()






# def get_post() Python shelve使用時
    # if request.method == 'GET':
    #     message = 'enter a URL to be shortened'
    #     return render_template('index.html', message_get = message)
    # else:
    #     originalURL = request.form.get('originalURl')
    #     result = checkDB(originalURL)
    #     generatedURL = 'http://URLshortening.com/' + result[0]

    #     if len(result) == 1:
    #         message1 = 'short link for '
    #         message3 = ' already exists'
    #         message4 = 'use this one  :  '
    #         return render_template('index.html', message_post1 = message1, \
    #                                message_post2 = originalURL, message_post3 = message3, \
    #                                message_post4 = message4, message_post5 = generatedURL)
    #     else:
    #         message1 = 'short link for '
    #         message3 = ' has been generated'
    #         message4 = 'new link  :  '
    #         return render_template('index.html', message_post1 = message1, \
    #                                message_post2 = originalURL, message_post3 = message3, \
    #                                message_post4 = message4, message_post5 = generatedURL)

# def checkDB(originalURL) Python shelve使用時
    # result = []
    # URLdata = shelve.open('URL_data')
    # if originalURL in URLdata:
    #     result.append(URLdata[originalURL]['generatedURL'])
    # URLdata.close()

    # with open('random_check.txt', 'r') as f:
    #     randoms = f.read().split(',')
    # generatedURL = generateURL(7)
    # while generatedURL in randoms:
    #     generatedURL = generateURL(7)
    # append_data(originalURL, generatedURL)
    # result.append(generatedURL)
    # result.append(originalURL)
    # return result

# def append_data(originalURL, generatedURL) Python shelve使用時
    # shelve
    # URLdata = shelve.open('URL_data')
    # URLdata[originalURL] = {'generatedURL':generatedURL}
    # URLdata.close()
