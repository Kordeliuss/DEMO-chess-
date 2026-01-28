import pygame, json, threading
from socket import socket, AF_INET, SOCK_STREAM

pygame.init()
WIN = pygame.display.set_mode((640, 640))
FONT = pygame.font.SysFont("arial", 48)
SQ = 80

s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 8081))

board = [["" for _ in range(8)] for _ in range(8)]
selected = None

def receive():
    global board
    while True:
        try:
            data = s.recv(2048).decode()
            if data:
                msg = json.loads(data)
                board = msg["board"]
        except: break

threading.Thread(target=receive, daemon=True).start()

def draw():
    WIN.fill((0,0,0))
    for r in range(8):
        for c in range(8):
            col = (240, 217, 181) if (r + c) % 2 == 0 else (181, 136, 99)
            if selected == (r, c): col = (200, 255, 200)
            pygame.draw.rect(WIN, col, (c * SQ, r * SQ, SQ, SQ))
            if board[r][c]:
                t = FONT.render(board[r][c], 1, (0, 0, 0))
                WIN.blit(t, (c * SQ + 25, r * SQ + 20))

run = True
while run:
    draw()
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT: run = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            r, c = e.pos[1] // SQ, e.pos[0] // SQ
            if selected:
                s.send(json.dumps([*selected, r, c]).encode())
                selected = None
            else:
                if board[r][c] != "": selected = (r, c)
pygame.quit()
