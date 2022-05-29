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
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    await gmo_get_price()
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")