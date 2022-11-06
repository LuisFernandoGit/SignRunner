import cv2.cv2
import pygame
import os
import random

import cv2 as cv
import numpy as np
import argparse

from hand_cam import Hand_Cam
from network import Network
import pickle

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    parser.add_argument('--use_static_image_mode', action='store_true')
    parser.add_argument("--min_detection_confidence",
                        help='min_detection_confidence',
                        type=float,
                        default=0.7)
    parser.add_argument("--min_tracking_confidence",
                        help='min_tracking_confidence',
                        type=int,
                        default=0.5)

    args = parser.parse_args()

    return args

pygame.init()

# Global Constants
# Screen properties
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

args = get_args()
cap_device = args.device
cap_width = 320
cap_height = 240

use_static_image_mode = args.use_static_image_mode
min_detection_confidence = args.min_detection_confidence
min_tracking_confidence = args.min_tracking_confidence

cap = cv.VideoCapture(cap_device)
cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

#Camera object definition
HC = Hand_Cam()
HC.load(use_static_image_mode, min_detection_confidence, min_tracking_confidence)

MAIN_IMG = pygame.image.load(os.path.join("Assets/Other", "Logo.png")).convert_alpha()

#Global sings arrays
SIGNS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "NH", "O", "P", "Q", "R", "S",
         "T", "U", "V", "W", "X", "Y", "Z"]

RIGHT_SIGNS = [pygame.image.load(os.path.join("Assets/Signs/RightH", "A.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "B.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "C.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "D.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "E.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "F.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "G.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "H.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "I.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "J.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "K.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "L.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "M.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "N.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "Ñ.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "O.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "P.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "Q.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "R.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "S.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "T.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "U.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "V.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "W.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "X.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "Y.png")),
                   pygame.image.load(os.path.join("Assets/Signs/RightH", "Z.png"))]

LEFT_SIGNS = [pygame.image.load(os.path.join("Assets/Signs/LeftH", "A.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "B.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "C.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "D.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "E.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "F.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "G.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "H.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "I.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "J.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "K.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "L.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "M.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "N.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "Ñ.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "O.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "P.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "Q.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "R.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "S.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "T.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "U.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "V.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "W.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "X.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "Y.png")),
                  pygame.image.load(os.path.join("Assets/Signs/LeftH", "Z.png"))]

def redrawWindow(win, game, p, active):
    if not(game.connected()):
        SCREEN.fill((255, 255, 255))
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Esperando Jugador...", 1, (255,0,0))
        win.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        font2 = pygame.font.SysFont("comicsans", 40)
        text = font.render("Tu seña", 1, (0, 0,0))
        win.blit(text, (200, 400))

        text = font.render("Seña de oponente", 1, (0, 0, 0))
        win.blit(text, (600, 400))

        if active:
            letter1, hand1 = game.get_player_move(0)
            letter2, hand2 = game.get_player_move(1)
            if hand1 == "Right":
                text1 = font.render(letter1, 1, (0, 255, 255))
            else:
                text1 = font.render(letter1, 1, (255, 0, 0))
            if hand2 == "Right":
                text2 = font.render(letter2, 1, (0, 255, 255))
            else:
                text2 = font.render(letter2, 1, (255, 0, 0))

            text3 = font2.render("Marcador", 1, (0, 0, 0))
            text4 = font2.render(str(game.wins[0]), 1, (0, 255, 0))
            text5 = font2.render(str(game.wins[1]), 1, (0, 255, 0))
            win.blit(text3, (20, 10))
            if p == 1:
                win.blit(text5, (30, 75))
                win.blit(text4, (150, 75))

                win.blit(text2, (250, 500))
                win.blit(text1, (800, 500))
            else:
                win.blit(text4, (30, 75))
                win.blit(text5, (150, 75))

                win.blit(text1, (250, 500))
                win.blit(text2, (800, 500))

    pygame.display.update()

def read_input(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_input(tup):
    return str(tup[0]) + "," + str(tup[1])

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    letter = "0"
    hand = "0"
    delay = 0
    active = False
    fontS = pygame.font.SysFont("comicsans", 60)
    textS = fontS.render("Haz esta seña", 1, (0, 0, 0))
    print("Eres el jugador ", player)

    while run:
        clock.tick(30)
        try:
            game = n.send("get")
        except:
            run = False
            print("No se pudo iniciar la partida")
            break

        if not game.isReady() and game.connected():
            try:
                game = n.send("start")
            except:
                run = False
                print("No se pudo iniciar la partida")
                break

        if game.winner() != -1:
            rect = pygame.Rect(250, 500, 200, 200)
            pygame.draw.rect(SCREEN, (255,255,255), rect)
            rect = pygame.Rect(800, 500, 200, 200)
            pygame.draw.rect(SCREEN, (255, 255, 255), rect)
            redrawWindow(SCREEN, game, player, True)
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Eres el ganador", 1, (0,255,0))
            else:
                text = font.render("Perdiste", 1, (255, 0, 0))

            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("No se pudo iniciar la partida")
                break

            SCREEN.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, 260))
            # Update sprites on screen
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw screen
        SCREEN.fill((255, 255, 255))

        # Get neural network's output
        img, signID, handID = HC.main_cam(cap)

        # Convert camera output to game object on screen
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        SCREEN.blit(frame, (960, 0))

        # Set neural network's output to player input
        letter = signID
        hand = handID
        sign_index, hand_index = game.sign_chosen()

        SCREEN.blit(textS, (400, 50))
        if hand_index == "Left":
            SCREEN.blit(LEFT_SIGNS[sign_index], (515, 150))
        elif hand_index == "Right":
            SCREEN.blit(RIGHT_SIGNS[sign_index], (515, 150))

        if delay > 10:
            try:
                playerInput = make_input((letter, hand))
                n.send(playerInput)
                active = True
            except:
                run = False
        else:
            delay += 1
        redrawWindow(SCREEN, game, player, active)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        SCREEN.fill((255, 255, 255))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click para Jugar", 1, (255,0,0))
        SCREEN.blit(MAIN_IMG, (325, 100))
        SCREEN.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, 500))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()