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
    data = docs.to_dict()
    return data

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = getDB() #データベース読み込み
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)