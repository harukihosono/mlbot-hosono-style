#---------------------------------------------------
# 1分間起動させる
#---------------------------------------------------
import time
def for_1_minute():
    for i in range(20):
        db = firestore.Client()
        docs = db.collection("price").get() #データベース読み込み
        data = docs[0].to_dict() #最新データを辞書型に変換
        time.sleep(3)
    return data

#---------------------------------------------------
# GMOから価格を取得
#---------------------------------------------------
import requests
def get_gmo_price(symbol):
    endPoint = 'https://api.coin.z.com/public'
    path     = '/v1/ticker?symbol='+symbol

    response = requests.get(endPoint + path)
    data = response.json()
    price = data["data"][0]
    return price

#---------------------------------------------------
# DB
#---------------------------------------------------
from google.cloud import firestore
def setDB(price):
    db = firestore.Client()

    doc_ref = db.collection("price").document()
    doc_ref.set({
    'created': firestore.SERVER_TIMESTAMP,
    'price': price
    })
def getDB():
    db = firestore.Client()
    docs = db.collection("price").get() #データベース読み込み
    data = docs[0].to_dict() #最新データを辞書型に変換
    return data
#---------------------------------------------------
# Webアプリ化
#---------------------------------------------------
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    data = for_1_minute()
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)