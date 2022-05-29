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
    data = docs[-1].to_dict() #最新データを辞書型に変換
    return data
#---------------------------------------------------
# Webアプリ化
#---------------------------------------------------
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    symbol="BTC" #symbolを指定
    price = get_gmo_price(symbol) #GMOに価格を取得
    setDB(price) #priceをデータベースに書き込む
    data = getDB() #データベースの最新データを読み込み
    return data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)