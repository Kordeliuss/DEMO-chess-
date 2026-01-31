import pygame, json, threading
from socket import socket, AF_INET, SOCK_STREAM

pygame.init()
WIN = pygame.display.set_mode((640, 640))

P1=pygame.transform.scale(pygame.image.load('images/P1.png'),(80,90))
R1=pygame.transform.scale(pygame.image.load('images/R1.png'),(80,90))
K1=pygame.transform.scale(pygame.image.load('images/K1.png'),(80,90))
Q1=pygame.transform.scale(pygame.image.load('images/Q1.png'),(80,90))
B1=pygame.transform.scale(pygame.image.load('images/B1.png'),(80,90))
N1=pygame.transform.scale(pygame.image.load('images/N1.png'),(80,90))

P2=pygame.transform.scale(pygame.image.load('images/P1.png'),(80,90))
R2=pygame.transform.scale(pygame.image.load('images/R1.png'),(80,90))
K2=pygame.transform.scale(pygame.image.load('images/K1.png'),(80,90))
Q2=pygame.transform.scale(pygame.image.load('images/Q1.png'),(80,90))
B2=pygame.transform.scale(pygame.image.load('images/B1.png'),(80,90))
N2=pygame.transform.scale(pygame.image.load('images/N1.png'),(80,90))

HYB={
    "p":P1,"r":R1,"k":K1,"q":Q1,"b":B1,"n":N1,
    "P":P2,"R":R2,"K":K2,"Q":Q2,"B":B2,"N":N2
}


s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 8081))

board = [["" for _ in range(8)] for _ in range(8)]
selected = None

def receive():
    global board
    while True:
        try:
            data = s.recv(4096).decode()
            if data:
                msg = json.loads(data)
                board = msg["board"]
        except: break

threading.Thread(target=receive, daemon=True).start()

def draw():
    for r in range(8):
        for c in range(8):
            col = (240, 217, 181) if (r + c) % 2 == 0 else (181, 136, 99)
            if selected == (r, c): col = (200, 255, 200)
            pygame.draw.rect(WIN, col, (c * 80, r * 80, 80, 80))
            char = board[r][c]
            if char in HYB:

                WIN.blit(HYB[char], (c * 80, r * 80))

run = True
while run:
    draw()
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            r, c = e.pos[1] // 80, e.pos[0] // 80
            if selected:
                s.send(json.dumps([*selected, r, c]).encode())
                selected = None
            else:
                if board[r][c] != "": selected = (r, c)
pygame.quit()
