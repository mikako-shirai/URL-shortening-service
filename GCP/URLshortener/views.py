from URLshortener.controllers import DB_generatedKey, DB_customKey
from URLshortener.models import get_analysis, get_redirect, cron_job, error_handler
from URLshortener.utils import URL_check, key_check, date_check

from flask import Blueprint, render_template, request, redirect, abort, url_for
import datetime
import os


app_views = Blueprint('views', __name__)

key_length = 5
GCP_URL = 'https://short-321807.an.r.appspot.com/'
keywords = ['custom', 'expiration', 'analysis', 'link', '404', 'error', 'cron', \
            'index', 'index_exp', 'custom_exp', 'result', 'selector']

# -----------------------------------------------------------------------------------

    # myDatabaseWrapper.set(u'URLs', {
    #     u'originalURL': originalURL,
    #     u'generatedURL': generatedURL,
    #     u'dateCreated': dateCreated,
    #     u'expirationDate': expirationDate,
    #     u'pageViews': 0
    # })
    # myDatabaseWrapper.set(u'keys', {
    #     u'originalURL': originalURL,
    #     u'pageViews': 0
    # })
    # assert(myDatabseWrapper.set).wasCalledWith()

# -----------------------------------------------------------------------------------

@app_views.route('/', methods=["GET","POST"])
def short_link():
    if request.method == 'GET':
        return render_template('index.html')

    dicData, errors, flg = {}, [], False
    originalURL = request.form.get('originalURl')

    if URL_check(originalURL):
        generatedKey = DB_generatedKey(originalURL)
        generatedURL = GCP_URL + generatedKey
        flg = True
        dicData['originalURL'] = originalURL
        dicData['generatedURL'] = generatedURL
    else:
        errors.append('Please enter a valid URL')
    return render_template('index.html', dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

@app_views.route('/custom', methods=["GET","POST"])
def custom_link():
    if request.method == 'GET':
        return render_template('custom.html')

    dicData, errors, flg = {}, [], False
    customKey = request.form.get('customKey')
    originalURL = request.form.get('originalURl')

    if key_check(customKey) and URL_check(originalURL):
        if DB_customKey(originalURL, customKey):
            generatedURL = GCP_URL + customKey
            flg = True
            dicData['originalURL'] = originalURL
            dicData['generatedURL'] = generatedURL
        else:
            errors.append('Sorry, this alias is already taken')
            errors.append('Please try different characters')
    else:
        if not key_check(customKey): errors.append('Please enter valid characters')
        if not URL_check(originalURL): errors.append('Please enter a valid URL')
    return render_template('custom.html', dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

@app_views.route('/expiration', methods=["GET","POST"])
def short_expiration():
    if request.method == 'GET':
        return render_template('index_exp.html')

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
        generatedKey = DB_generatedKey(originalURL, expirationDate)
        generatedURL = GCP_URL + generatedKey
        flg = True
        dicData['originalURL'] = originalURL
        dicData['generatedURL'] = generatedURL
        dicData['expirationDate'] = {'year': year, 'month': month, 'date': date, 'hour': hour, 'minute': minute}
    else:
        if not date_check(dateSet): errors.append('Please enter a valid date')
        if not URL_check(originalURL): errors.append('Please enter a valid URL')
    return render_template('index_exp.html', dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

@app_views.route('/custom/expiration', methods=["GET","POST"])
def custom_expiration():
    if request.method == 'GET':
        return render_template('custom_exp.html')

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
        if DB_customKey(originalURL, customKey, expirationDate):
            generatedURL = GCP_URL + customKey
            flg = True
            dicData['originalURL'] = originalURL
            dicData['generatedURL'] = generatedURL
            dicData['expirationDate'] = {'year': year, 'month': month, 'date': date, 'hour': hour, 'minute': minute}
        else:
            errors.append('Sorry, this alias is already taken')
            errors.append('Please try different characters')
    else:
        if not date_check(dateSet): errors.append('Please enter a valid date')
        if not key_check(customKey): errors.append('Please enter valid characters')
        if not URL_check(originalURL): errors.append('Please enter a valid URL')
    return render_template('custom_exp.html', dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

@app_views.route('/analysis', methods=["GET","POST"])
def link_analysis():
    if request.method == 'GET':
        return render_template('analysis.html')

    dicData, errors, flg = {}, [], False
    generatedURL = request.form.get('generatedURL')

    if GCP_URL in generatedURL and len(generatedURL) >= 43:
        key = generatedURL[38:]
        dicData = get_analysis(generatedURL, key)
        if dicData:
            flg = True
        else:
            errors.append('The requested link was not found')
    else:
        errors.append('Please enter a valid URL')
    return render_template('analysis.html', dicData = dicData, errors = errors, flg = flg)

# -----------------------------------------------------------------------------------

@app_views.route('/<string>')
def URL_redirect(string):
    if len(string) < key_length or len(string) > 30:
        abort(404)

    originalURL = get_redirect(string)
    return redirect(originalURL) if originalURL else abort(404)

# -----------------------------------------------------------------------------------

@app_views.route('/cron', methods=['GET'])
def expiration_check():
    cron_job()
    return '', 200

# -----------------------------------------------------------------------------------

@app_views.errorhandler(404)
def page_not_found(e):
    URL = error_handler()
    return render_template('404.html', URL = URL), 404

# -----------------------------------------------------------------------------------

@app_views.context_processor
def get_date():
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    string = dateNow.strftime('%Y%m')
    year = int(string[:4])
    month = int(string[4:])
    if month >= 7:
        years = [str(year), str(year + 1)]
    else:
        years = [str(year)]
    return dict(years=years)

@app_views.context_processor
def get_months():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return dict(months=months)

# -----------------------------------------------------------------------------------

@app_views.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app_views.root_path, \
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

