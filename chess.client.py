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
