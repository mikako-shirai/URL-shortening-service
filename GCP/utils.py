import random, string
import datetime
from dateutil.relativedelta import relativedelta
import re


key_length = 5

# -----------------------------------------------------------------------------------

def generate_key(key_length):
    letters = [random.choice(string.ascii_letters + string.digits) for i in range(key_length)]
    return ''.join(letters)

def get_date():
    dateNow = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    string = dateNow.strftime('%Y%m')
    year = int(string[:4])
    month = int(string[4:])
    if month >= 7:
        years = [str(year), str(year + 1)]
    else:
        years = [str(year)]
    return years

def URL_check(URL):
    if ' ' in URL:
        return False
    validFormat = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    return True if re.match(validFormat, URL) else False

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

