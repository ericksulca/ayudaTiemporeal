from ayuda.models import *
import json
def Enviar_msg(request,msgData):
	ws = create_connection("ws://localhost:8000/ws/chat/home/",sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),), class_=MyWebSocket)
	ws.send(json.dumps(msgData))


import socket
from websocket import create_connection, WebSocket
class MyWebSocket(WebSocket):
	def recv_frame(self):
		frame = super().recv_frame()
		print('yay! I got this frame: ', frame)
		return frame