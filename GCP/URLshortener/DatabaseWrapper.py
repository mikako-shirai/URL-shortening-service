from URLshortener import db

from google.cloud import firestore


"""
db.collection().stream()

db.collection().document().get()
db.collection().document().get().to_dict()

db.collection().document().set()
db.collection().document().update()
db.collection().document().delete()

.exists

firestore.Increment()
firestore.DELETE_FIELD
firestore.ArrayUnion([])
firestore.ArrayRemove([])
"""

# -----------------------------------------------------------------------------------

def c_stream(collection):
    data = db.collection(collection).stream()
    return data

def cd_get(collection, document):
    data = db.collection(collection).document(document).get()
    return data

def cd_get_toDict(collection, document):
    data = db.collection(collection).document(document).get().to_dict()
    return data

def cd_set(collection, document, data):
    db.collection(collection).document(document).set(data)

def cd_update(collection, document, data):
    db.collection(collection).document(document).update(data)

def cd_delete(collection, document):
    db.collection(collection).document(document).delete()

def cd_toDict(data):
    data = data.to_dict()
    return data

def exists(data):
    return True if data.exists else False

def fs_increment(collection, document, field, num):
    data = db.collection(collection).document(document)
    current = data.get().to_dict()[field]
    data.update({
        field: current + num
    })

def fs_arrayUnion(collection, document, field, data):
    db.collection(collection).document(document).update({
        field: firestore.ArrayUnion([data])
    })

def fs_arrayRemove(collection, document, field, data):
    db.collection(collection).document(document).update({
        field: firestore.ArrayRemove([data])
    })

def fs_delete(collection, document, field):
    db.collection(collection).document(document).update({
        field: firestore.DELETE_FIELD
    })
    
