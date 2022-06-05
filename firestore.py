import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

docs = db.collection("price").get()
from pprint import pprint
pprint(docs[0].to_dict()["price"][0]["last"])
pprint(docs[0].to_dict()["price"][0]["timestamp"])