# chess.server.py

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import json
from chess_logic import *

board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

clients = []
turn = True  # True = white, False = black


def broadcast(data):
    msg = json.dumps(data).encode()
    for c in clients[:]:
        try:
            c.send(msg)
        except:
            clients.remove(c)


def handle(client, idx):
    global turn
    while True:
        try:
            raw = client.recv(1024)
            if not raw:
                break

            data = json.loads(raw.decode())

            if idx != turn:
                continue

            r1, c1, r2, c2 = data
            piece = board[r1][c1]

            if piece == "":
                continue

            # white = uppercase, black = lowercase
            if piece.isupper() != turn:
                continue

            if (r2, c2) in moves(board, r1, c1):
                board[r2][c2] = board[r1][c1]
                board[r1][c1] = ""
                turn = not turn

                state = {"board": board, "turn": turn}
                if mate(board, turn):
                    state["mate"] = True

                broadcast(state)

        except:
            break

    if client in clients:
        clients.remove(client)
    client.close()


s = socket(AF_INET, SOCK_STREAM)
s.bind(("127.0.0.1", 8081))
s.listen(2)
print("Server started on 8081")

while len(clients) < 2:
    c, _ = s.accept()
    clients.append(c)
    Thread(target=handle, args=(c, len(clients) - 1), daemon=True).start()
    print(f"Client {len(clients)} connected")

broadcast({"board": board, "turn": turn})
while True:
    pass


