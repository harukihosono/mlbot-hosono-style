import asyncio

#---------------------------------------------------
# GMOコイン価格取得
#---------------------------------------------------
import json
import websocket
async def gmo_get_price():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1')

    def on_open(self):
        message = {
            "command": "subscribe",
            "channel": "ticker",
            "symbol": "BTC"
        }
        ws.send(json.dumps(message))

    def on_message(self, message):
        setDB(message)

    ws.on_open = on_open
    ws.on_message = on_message

    ws.run_forever()

#---------------------------------------------------
# データベース書き込み読み込み
#---------------------------------------------------
from google.cloud import firestore


def setDB(message):
    db = firestore.Client()

    doc_ref = db.collection("price").document()
    doc_ref.set(message)
def getDB():
    db = firestore.Client()
    docs = db.collection("price").get() #データベース読み込み
    data = docs[0].to_dict() #1番上のデータを辞書型に変換
    return data

# #---------------------------------------------------
# # Webアプリ化
# #---------------------------------------------------
import responder

api = responder.API()

@api.route("/")
def hello_world(req, resp):
    resp.text = "hello, world!"

if __name__ == '__main__':
    api.run()

# from flask import Flask

# app = Flask(__name__)



# @app.route("/")
# async def hello_world():
#     try:
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(asyncio.ensure_future(gmo_get_price()))
#         loop.close()
#         data = getDB() #データベース読み込み
#     except Exception as e:
#         print(e)
#     return data

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=8080)