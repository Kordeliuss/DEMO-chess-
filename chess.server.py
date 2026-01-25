#server.py
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import json
from chess_logic import *

board = [
 ["r","n","b","q","k","b","n","r"],
 ["p","p","p","p","p","p","p","p"],
 ["","","","","","","",""],
 ["","","","","","","",""],
 ["","","","","","","",""],
 ["","","","","","","",""],
 ["P","P","P","P","P","P","P","P"],
 ["R","N","B","Q","K","B","N","R"]
]

clients=[]
turn=True  # white

def broadcast(data):
    msg=json.dumps(data).encode()
    for c in clients:
        c.send(msg)

def handle(client, idx):
    global turn
    while True:
        data=json.loads(client.recv(1024).decode())
        if idx!=turn: continue

        r1,c1,r2,c2=data
        if (r2,c2) in moves(board,r1,c1):
            board[r2][c2]=board[r1][c1]
            board[r1][c1]=""
            turn=not turn

            state={"board":board,"turn":turn}
            if mate(board,turn):
                state["mate"]=True
            broadcast(state)

s=socket(AF_INET,SOCK_STREAM)
s.bind(("0.0.0.0",5555))
s.listen(2)
print("Server started")

while len(clients)<2:
    c,_=s.accept()
    clients.append(c)
    Thread(target=handle,args=(c,len(clients)-1),daemon=True).start()
    print("Client connected")

broadcast({"board":board,"turn":turn})
