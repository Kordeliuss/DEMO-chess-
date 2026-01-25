#chess/
 #server.py
 #client.py
 #chess_logic.

#chess_logic.py
def is_white(p): return p.isupper()
def clone(b): return [r[:] for r in b]

def king_pos(b, w):
    k = "K" if w else "k"
    for r in range(8):
        for c in range(8):
            if b[r][c] == k:
                return r, c

def in_bounds(r,c): return 0<=r<8 and 0<=c<8

def moves(b,r,c):
    p=b[r][c]; res=[]
    d=-1 if is_white(p) else 1

    def add(rr,cc):
        if in_bounds(rr,cc):
            if b[rr][cc]=="" or is_white(b[rr][cc])!=is_white(p):
                res.append((rr,cc))

    if p.lower()=="p":
        if in_bounds(r+d,c) and b[r+d][c]=="":
            add(r+d,c)
        for dc in (-1,1):
            if in_bounds(r+d,c+dc) and b[r+d][c+dc]!="":
                add(r+d,c+dc)

    if p.lower() in "rq":
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            rr,cc=r+dr,c+dc
            while in_bounds(rr,cc):
                if b[rr][cc]=="":
                    res.append((rr,cc))
                else:
                    if is_white(b[rr][cc])!=is_white(p):
                        res.append((rr,cc))
                    break
                rr+=dr; cc+=dc

    if p.lower() in "bq":
        for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
            rr,cc=r+dr,c+dc
            while in_bounds(rr,cc):
                if b[rr][cc]=="":
                    res.append((rr,cc))
                else:
                    if is_white(b[rr][cc])!=is_white(p):
                        res.append((rr,cc))
                    break
                rr+=dr; cc+=dc

    if p.lower()=="n":
        for dr,dc in ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)):
            add(r+dr,c+dc)

    if p.lower()=="k":
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr or dc:
                    add(r+dr,c+dc)

    return res

def check(b,w):
    kr,kc=king_pos(b,w)
    for r in range(8):
        for c in range(8):
            p=b[r][c]
            if p and is_white(p)!=w:
                if (kr,kc) in moves(b,r,c):
                    return True
    return False

def mate(b,w):
    if not check(b,w): return False
    for r in range(8):
        for c in range(8):
            p=b[r][c]
            if p and is_white(p)==w:
                for mr,mc in moves(b,r,c):
                    nb=clone(b)
                    nb[mr][mc]=nb[r][c]
                    nb[r][c]=""
                    if not check(nb,w):
                        return False
    return True
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
#client.py
import pygame, json
from socket import socket, AF_INET, SOCK_STREAM

pygame.init()
WIN=pygame.display.set_mode((640,640))
FONT=pygame.font.SysFont("arial",48)
SQ=80

s=socket(AF_INET,SOCK_STREAM)
s.connect(("SERVER_IP",5555))

board=[]
selected=None

def draw():
    for r in range(8):
        for c in range(8):
            col=(240,217,181) if (r+c)%2==0 else (181,136,99)
            pygame.draw.rect(WIN,col,(c*SQ,r*SQ,SQ,SQ))
            if board[r][c]:
                t=FONT.render(board[r][c],1,(0,0,0))
                WIN.blit(t,(c*SQ+25,r*SQ+20))

while True:
    msg=json.loads(s.recv(2048).decode())
    board=msg["board"]

    draw()
    pygame.display.update()

    for e in pygame.event.get():
        if e.type==pygame.MOUSEBUTTONDOWN:
            r,c=pygame.mouse.get_pos()[1]//SQ,pygame.mouse.get_pos()[0]//SQ
            if selected:
                s.send(json.dumps([*selected,r,c]).encode())
                selected=None
            else:
                selected=(r,c)

