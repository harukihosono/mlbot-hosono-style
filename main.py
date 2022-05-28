from google.cloud import firestore
#---------------------------------------------------
# DB
#---------------------------------------------------

def setDB():
    db = firestore.Client()

    doc_ref = db.collection("test").document()
    doc_ref.set({
    'created': firestore.SERVER_TIMESTAMP,
    'name': 'Test'
    })
def getDB():
    db = firestore.Client()
    docs = db.collection("test").get()
    return docs

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    docs = getDB() #データベース読み込み

    return docs

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)