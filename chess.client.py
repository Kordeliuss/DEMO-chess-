#Chess.client.py

import pygame, json, threading
from socket import socket, AF_INET, SOCK_STREAM

pygame.init()

WIN = pygame.display.set_mode((810, 640))
pygame.display.set_caption("Network Chess")

#  Шрифт
title_font = pygame.font.SysFont(None, 42)
font = pygame.font.SysFont(None, 36)


P1=pygame.transform.scale(pygame.image.load('images/P1.png'),(80,90))
R1=pygame.transform.scale(pygame.image.load('images/R1.png'),(80,90))
K1=pygame.transform.scale(pygame.image.load('images/K1.png'),(80,90))
Q1=pygame.transform.scale(pygame.image.load('images/Q1.png'),(80,90))
B1=pygame.transform.scale(pygame.image.load('images/B1.png'),(80,90))
N1=pygame.transform.scale(pygame.image.load('images/N1.png'),(80,90))

P2=pygame.transform.scale(pygame.image.load('images/P2.png'),(80,90))
R2=pygame.transform.scale(pygame.image.load('images/R2.png'),(80,90))
K2=pygame.transform.scale(pygame.image.load('images/K2.png'),(80,90))
Q2=pygame.transform.scale(pygame.image.load('images/Q1.png'),(80,90))
B2=pygame.transform.scale(pygame.image.load('images/B2.png'),(80,90))
N2=pygame.transform.scale(pygame.image.load('images/N2.png'),(80,90))

HYB={
    "p":P1,"r":R1,"k":K1,"q":Q1,"b":B1,"n":N1,
    "P":P2,"R":R2,"K":K2,"Q":Q2,"B":B2,"N":N2
}

s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 8081))

board = [["" for _ in range(8)] for _ in range(8)]
prev_board = [["" for _ in range(8)] for _ in range(8)]  #
selected = None
turn = True

#  Бали
score_white = 0
score_black = 0

#  Вартість фігур
values = {
    "p": 1, "n": 3, "b": 3, "r": 5, "q": 9
}

def receive():
    global board, turn, score_white, score_black, prev_board
    while True:
        try:
            data = s.recv(4096).decode()
            if data:
                msg = json.loads(data)

                prev_board = [row[:] for row in board]  #
                board = msg["board"]

                # шукаємо зʼїдені фігури
                for r in range(8):
                    for c in range(8):
                        before = prev_board[r][c]
                        after = board[r][c]
                        if before != "" and after == "":
                            key = before.lower()
                            if key in values:
                                if before.isupper():
                                    score_black += values[key]
                                else:
                                    score_white += values[key]

                if "turn" in msg:
                    turn = msg["turn"]
        except:
            break

threading.Thread(target=receive, daemon=True).start()

def draw():
    for r in range(8):
        for c in range(8):
            col = (240, 217, 181) if (r + c) % 2 == 0 else (181, 136, 99)
            if selected == (r, c):
                col = (200, 255, 200)
            pygame.draw.rect(WIN, col, (c * 80, r * 80, 80, 80))
            char = board[r][c]
            if char in HYB:
                WIN.blit(HYB[char], (c * 80, r * 80))

    #  Заголовок
    WIN.blit(title_font.render("ВІЙНА ЗА МОЛОЧКО", True, (255,255,255)), (10, 5))


def draw_turn_panel():
    pygame.draw.rect(WIN, (40, 40, 40), (640, 0, 170, 640))

    white_col = (0, 255, 0) if turn else (200, 200, 200)
    black_col = (0, 255, 0) if not turn else (200, 200, 200)

    WIN.blit(font.render("RED TURN", True, white_col), (650, 240))
    WIN.blit(font.render("WHITE TURN", True, black_col), (650, 280))

    #  Бали
    WIN.blit(font.render(f"RED: {score_black}", True, (255, 255, 255)), (650, 340))
    WIN.blit(font.render(f"WHITE: {score_white}", True, (255, 255, 255)), (650, 380))


run = True
while run:
    draw()
    draw_turn_panel()
    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            r, c = e.pos[1] // 80, e.pos[0] // 80
            if c < 8:
                if selected:
                    s.send(json.dumps([*selected, r, c]).encode())
                    selected = None
                else:
                    if board[r][c] != "":
                        selected = (r, c)

pygame.quit()

