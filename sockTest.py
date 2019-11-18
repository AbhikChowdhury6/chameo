import websocket
import time

ws = websocket.create_connection("ws://192.168.8.155:9001")

while True:
	result = ws.recv()
	print(result)
	time.sleep(1)
