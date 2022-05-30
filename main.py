import time
import requests
from google.cloud import firestore

class Get_price:
    #---------------------------------------------------
    # 1分間起動させる
    #---------------------------------------------------
    
    def for_1_minute(self):
        prices=[]
        for i in range(20):
            symbol="BTC" #symbolを指定
            price = self.get_gmo_price(symbol) #GMOに価格を取得
            prices.append(price)
            time.sleep(3)
        self.setDB(prices) #priceをデータベースに書き込む
        return "価格取得とDB書き込み完了"
    #---------------------------------------------------
    # GMOから価格を取得
    #---------------------------------------------------
    def get_gmo_price(self,symbol):
        endPoint = 'https://api.coin.z.com/public'
        path     = '/v1/ticker?symbol='+symbol
        response = requests.get(endPoint + path)
        data = response.json()
        price = data["data"][0]
        return price
    #---------------------------------------------------
    # DB
    #---------------------------------------------------
    def setDB(self,prices):
        db = firestore.Client()
        doc_ref = db.collection("price").document()
        doc_ref.set({
        'created': firestore.SERVER_TIMESTAMP,
        'price': prices
        })
    def getDB(self):
        db = firestore.Client()
        docs = db.collection("price").stream() #データベース読み込み
        data = docs[0].to_dict() #最新データを辞書型に変換
        return data
class Create_Candle:
    #---------------------------------------------------
    # DB
    #---------------------------------------------------
    def deleteDB(self):
        db = firestore.Client()
        docs = db.collection("price").stream() #データベース読み込み
        for doc in docs:
            db.collection("price").document(doc.id).delete()
#---------------------------------------------------
# Webアプリ化
#---------------------------------------------------
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    get_price=Get_price()
    data = get_price.for_1_minute()
    return data

@app.route("/trade")
def trade():
    create_Candle=Create_Candle()
    create_Candle.deleteDB()
    return "データベース削除"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)