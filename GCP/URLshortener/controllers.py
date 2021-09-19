from URLshortener.models import get_keys, append_data
from URLshortener.utils import generate_key


key_length = 5

# -----------------------------------------------------------------------------------

def DB_generatedKey(originalURL, expirationDate=None):
    generatedKey = generate_key(key_length)
    keys = get_keys()
    while generatedKey in keys:
        generatedKey = generate_key(key_length)
    if expirationDate:
        append_data(originalURL, generatedKey, expirationDate)
    else:
        append_data(originalURL, generatedKey)
    return generatedKey

def DB_customKey(originalURL, customKey, expirationDate=None):
    keys = get_keys()
    if customKey in keys:
        return False
    if expirationDate:
        append_data(originalURL, customKey, expirationDate)
    else:
        append_data(originalURL, customKey)
    return True

