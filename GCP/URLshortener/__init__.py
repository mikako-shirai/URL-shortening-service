from flask import Flask
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

