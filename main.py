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

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    setDB() #データベース書き込み
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)