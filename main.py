from google.cloud import firestore
#---------------------------------------------------
# DB
#---------------------------------------------------

def setDB(price):
    db = firestore.Client()

    doc_ref = db.collection("test").document()
    doc_ref.set({
    'created': firestore.SERVER_TIMESTAMP,
    'price': price
    })
def getDB():
    db = firestore.Client()
    docs = db.collection("test").get() #データベース読み込み
    data = docs[0].to_dict() #データを辞書型に変換
    return data

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = getDB() #データベース読み込み
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)