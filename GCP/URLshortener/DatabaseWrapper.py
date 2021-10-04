from URLshortener import db

from google.cloud import firestore

# -----------------------------------------------------------------------------------

"""
db.collection().stream()

db.collection().document().get()
db.collection().document().get().to_dict()
.to_dict()

db.collection().document().set()
db.collection().document().update()
db.collection().document().delete()

.exists
.id

firestore.Increment()
firestore.ArrayUnion([])
firestore.ArrayRemove([])
firestore.DELETE_FIELD
"""

# -----------------------------------------------------------------------------------

def collection_stream(collection):
    data = db.collection(collection).stream()
    return data

def collection_document_get(collection, document):
    data = db.collection(collection).document(document).get()
    return data

def collection_document_get_todict(collection, document):
    data = db.collection(collection).document(document).get().to_dict()
    return data

def collection_document_set(collection, document, data):
    db.collection(collection).document(document).set(data)

def collection_document_update(collection, document, data):
    db.collection(collection).document(document).update(data)

def collection_document_delete(collection, document):
    db.collection(collection).document(document).delete()

def data_todict(data):
    data = data.to_dict()
    return data

def exists(data):
    return data.exists

def id(data):
    return data.id

def firestore_Increment(collection, document, field, num):
    data = db.collection(collection).document(document)
    current = data.get().to_dict()[field]
    data.update({
        field: current + num
    })

def firestore_ArrayUnion(collection, document, field, data):
    db.collection(collection).document(document).update({
        field: firestore.ArrayUnion([data])
    })

def firestore_ArrayRemove(collection, document, field, data):
    db.collection(collection).document(document).update({
        field: firestore.ArrayRemove([data])
    })

def firestore_DeleteField(collection, document, field):
    db.collection(collection).document(document).update({
        field: firestore.DELETE_FIELD
    })
    
