import time

import cv2.cv2
import pygame
import os
import random

import cv2 as cv
import numpy as np
import argparse

from hand_cam import Hand_Cam
from api import db, Player, Score, ScoreE, ScoreH
from datetime import date, timedelta

#Get camera parameters
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

#Importing assets
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

START_IMG = pygame.image.load(os.path.join("Assets/Other", "start_btn.png")).convert_alpha()
EXIT_IMG = pygame.image.load(os.path.join("Assets/Other", "exit_btn.png")).convert_alpha()
BACK_BTN = pygame.image.load(os.path.join("Assets/Other", "Back.png")).convert_alpha()

EASY_IMG = pygame.image.load(os.path.join("Assets/Other", "Easy_btn.png")).convert_alpha()
MED_IMG = pygame.image.load(os.path.join("Assets/Other", "Medium_btn.png")).convert_alpha()
HARD_IMG = pygame.image.load(os.path.join("Assets/Other", "Hard_btn.png")).convert_alpha()

BLUE_IMG = pygame.image.load(os.path.join("Assets/Other", "blue_example.png")).convert_alpha()
RED_IMG = pygame.image.load(os.path.join("Assets/Other", "red_example.png")).convert_alpha()
LOGIN_IMG = pygame.image.load(os.path.join("Assets/Other", "login.png")).convert_alpha()

#Camera object definition
HC = Hand_Cam()
HC.load(use_static_image_mode, min_detection_confidence, min_tracking_confidence)

#Global sings arrays
SIGNS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "NH", "O", "P", "Q", "R", "S",
         "T", "U", "V", "W", "X", "Y", "Z"]
RIGHT_SIGNS = []
LEFT_SIGNS = []
NEUTRAL_SIGNS = []

#Player login object
PLAYER1 = ''

#Loading signs assests by difficulty
def default_difficulty():
    global RIGHT_SIGNS, LEFT_SIGNS, NEUTRAL_SIGNS
    RIGHT_SIGNS = [pygame.image.load(os.path.join("Assets/Signs/Right", "A.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "B.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "C.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "D.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "E.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "F.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "G.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "H.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "I.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "J.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "K.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "L.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "M.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "N.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "Ñ.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "O.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "P.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "Q.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "R.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "S.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "T.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "U.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "V.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "W.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "X.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "Y.png")),
                   pygame.image.load(os.path.join("Assets/Signs/Right", "Z.png"))]

    LEFT_SIGNS = [pygame.image.load(os.path.join("Assets/Signs/Left", "A.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "B.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "C.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "D.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "E.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "F.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "G.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "H.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "I.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "J.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "K.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "L.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "M.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "N.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "Ñ.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "O.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "P.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "Q.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "R.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "S.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "T.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "U.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "V.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "W.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "X.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "Y.png")),
                  pygame.image.load(os.path.join("Assets/Signs/Left", "Z.png"))]

    NEUTRAL_SIGNS = [pygame.image.load(os.path.join("Assets/Signs/Neutral", "A.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "B.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "C.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "D.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "E.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "F.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "G.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "H.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "I.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "J.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "K.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "L.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "M.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "N.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "Ñ.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "O.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "P.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "Q.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "R.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "S.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "T.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "U.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "V.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "W.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "X.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "Y.png")),
                     pygame.image.load(os.path.join("Assets/Signs/Neutral", "Z.png"))]

def hard_difficulty():
    global RIGHT_SIGNS, LEFT_SIGNS, NEUTRAL_SIGNS
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

    NEUTRAL_SIGNS = [pygame.image.load(os.path.join("Assets/Signs/NeutralH", "A.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "B.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "C.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "D.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "E.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "F.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "G.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "H.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "I.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "J.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "K.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "L.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "M.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "N.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "Ñ.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "O.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "P.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "Q.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "R.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "S.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "T.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "U.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "V.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "W.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "X.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "Y.png")),
                     pygame.image.load(os.path.join("Assets/Signs/NeutralH", "Z.png"))]

#Class definitions
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, SCREEN):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button on screen
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        return action

#Player class
class Dinosaur:
    #Coordinates on screen
    X_POS = 80
    Y_POS = 510
    Y_POS_DUCK = 540
    JUMP_VEL = 8.5

    def __init__(self):
        #Player status and sprites
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    #change player status by sign recognition
    def update(self, userInput, sign, hand, handID):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        # check player's input to jump
        if userInput == sign and handID == hand:
            if not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
        #elif userInput[pygame.K_DOWN] and not self.dino_jump:
        #    self.dino_duck = True
        #    self.dino_run = False
        #    self.dino_jump = False
        #elif not (self.dino_jump or userInput[pygame.K_DOWN]):
        elif not (self.dino_jump or self.dino_duck):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    #Sprite animations
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        #increase player's vertical height
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        #Move player's height back to the floor
        if self.jump_vel < - self.JUMP_VEL and self.dino_rect.y >= 500:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        #Set initial spawn position offscreen
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(250, 300)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        # Move cloud to the left
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(250, 300)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

#Obstacle superclass
class Obstacle:
    def __init__(self, image, type, id):
        #Get obstacle's sprite and hitbox
        self.image = image
        self.type = type
        self.id = id
        self.rect = self.image[self.type].get_rect()

        #Ppawn obstacle behind sign sprite
        if self.id == 0:
            self.rect.x = SCREEN_WIDTH
        else:
            self.rect.x = SCREEN_WIDTH + 160

    #Move obstacle to the left
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        #Set random small cactus object
        self.type = random.randint(0, 2)
        self.id = 1
        super().__init__(image, self.type, self.id)
        self.rect.y = 525

class LargeCactus(Obstacle):
    def __init__(self, image):
        # Set random large cactus object
        self.type = random.randint(0, 2)
        self.id = 1
        super().__init__(image, self.type, self.id)
        self.rect.y = 500

class Rect_Input(Obstacle):
    def __init__(self, image, type):
        # Set sign's input detection box
        self.type = type
        self.id = 0
        super().__init__(image, self.type, self.id)
        self.rect.y = 500

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        self.id = 1
        super().__init__(image, self.type, self.id)
        self.rect.y = 460
        self.index = 0

    def draw(self, SCREEN):
        # Animate obstacle's sprites
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main(difficulty):
    # Game's variables definition
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 22
    x_pos_bg = 0
    y_pos_bg = 580
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    sign_index = 0
    sign = ''
    hand = ''

    # Update score
    def score(difficulty):
        global points, game_speed
        points += 1
        if difficulty != "e":
            if points % 400 == 0 and 800 < points <= 4000:
                game_speed += 1

        text = font.render("Puntos: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        #textRect.center = (1000, 40)
        SCREEN.blit(text, (1070, 250))

    # Loop background
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    # Game's main loop
    while run:
        # Check if player closes the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Draw screen
        SCREEN.fill((255, 255, 255))

        # Get neural network's output
        img, signID, handID = HC.main_cam(cap)
        #print(signID, handID)
        # succes, cam = cap.read()

        # Convert camera output to game object on screen
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        SCREEN.blit(frame, (960,0))

        #userInput = pygame.key.get_pressed()
        # Set neural network's output to player input
        userInput = signID
        # Check input and update status
        player.update('null', sign, 'null', handID)
        player.draw(SCREEN)

        # Draw screen elements
        background()
        cloud.update()
        cloud.draw(SCREEN)
        score(difficulty)

        # Spawn obstacles
        if len(obstacles) == 0:
            sign_index = random.randint(0, len(SIGNS) - 1)
            sign = SIGNS[sign_index]
            if random.randint(0, 2) == 0:
                hand = 'Right'
                obstacles.append(SmallCactus(SMALL_CACTUS))
                obstacles.append(Rect_Input(RIGHT_SIGNS, sign_index))
            elif random.randint(0, 2) == 1:
                hand = 'Right'
                obstacles.append(LargeCactus(LARGE_CACTUS))
                obstacles.append(Rect_Input(RIGHT_SIGNS, sign_index))
            elif random.randint(0, 2) == 2:
                if difficulty == "e":
                    hand = 'Right'
                    obstacles.append(Bird(BIRD))
                    obstacles.append(Rect_Input(RIGHT_SIGNS, sign_index))
                else:
                    hand = 'Left'
                    obstacles.append(Bird(BIRD))
                    obstacles.append(Rect_Input(LEFT_SIGNS, sign_index))
            #print(sign, hand)

        # Draw sign input request
        SCREEN.blit(NEUTRAL_SIGNS[sign_index], (0, 60))

        # Move obstacles
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(SCREEN)

            # Check if player colided with input rectangle
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.display.update()
                player.update(userInput, sign, hand, handID)
                player.draw(SCREEN)
                obstacle.update()
                obstacle.draw(SCREEN)
                # Check if player colided with obstacle
                if obstacle.id == 1:
                    # Save player's score in the data base
                    player_score = points
                    score_date = date.today()

                    if difficulty == "n":
                        scr = Score(player_score, score_date, PLAYER1)
                    elif difficulty == "e":
                        scr = ScoreE(player_score, score_date, PLAYER1)
                    elif difficulty == "h":
                        scr = ScoreH(player_score, score_date, PLAYER1)
                    db.session.add(scr)
                    db.session.commit()

                    # Break out of main loop
                    pygame.time.delay(2000)
                    death_count += 1
                    run = False

        # Update sprites on screen
        pygame.display.update()
        clock.tick(30)

    # Retry menu
    menu(death_count, difficulty)

def menu(death_count, difficulty):
    global points
    op = 0
    run = True

    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        fontb = pygame.font.Font('freesansbold.ttf', 20)

        # Game start menu
        if death_count == 0:
            text = font.render("Presiona cualquier tecla para comenzar.", True, (0, 0, 0))
            blue_icon = pygame.transform.scale(BLUE_IMG, (BLUE_IMG.get_width() * 0.4, BLUE_IMG.get_height() * 0.4))
            red_icon = pygame.transform.scale(RED_IMG, (RED_IMG.get_width() * 0.4, RED_IMG.get_height() * 0.4))
            SCREEN.blit(red_icon, (350, 425))
            SCREEN.blit(blue_icon, (730, 425))

        # Retry menu
        elif death_count > 0:
            text = font.render("Presiona cualquier tecla para intentarlo de nuevo.", True, (0, 0, 0))
            score = font.render("Puntaje: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))

        # Draw back to main menu button
        back_bttn = Button(50, 50, BACK_BTN, 1)
        back_text = fontb.render("Regresar al menú.", True, (0, 0, 0))
        backRect = back_text.get_rect()
        backRect.center = (230, 85)
        SCREEN.blit(back_text, backRect)
        if back_bttn.draw(SCREEN):
            run = False

        pygame.display.update()
        # Check if player closes the game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
                op = 1

    # Check if player starts the game or goes back to main menu
    if op == 0:
        main_menu()
    else:
        main(difficulty)

def main_menu():
    # Main menu's buttons and status definition
    menu_state = "main"
    start_bttn = Button(SCREEN_WIDTH // 2 - 420, SCREEN_HEIGHT // 2 - 100, START_IMG, 1)
    exit_bttn = Button(SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT // 2 - 100, EXIT_IMG, 1)
    e_bttn = Button(500, 100, EASY_IMG, 1)
    n_bttn = Button(500, 300, MED_IMG, 1)
    h_bttn = Button(500, 500, HARD_IMG, 1)
    op = 0
    run = True

    while run:
        SCREEN.fill((255, 255, 255))
        # Check if player is on the main menu
        if menu_state == "main":
            # Check if player goes to select difficulty menu
            if start_bttn.draw(SCREEN):
                menu_state = "difficulty"
            # Check if player closes the game
            if exit_bttn.draw(SCREEN):
                cap.release()
                cv.destroyAllWindows()
                run = False

        # Check if player is on the select difficulty menu
        elif menu_state == "difficulty":
            # Check for difficulty chosen
            if e_bttn.draw(SCREEN):
                e_bttn.clicked = False
                run = False
                op = 1
            if n_bttn.draw(SCREEN):
                n_bttn.clicked = False
                run = False
                op = 2
            if h_bttn.draw(SCREEN):
                h_bttn.clicked = False
                run = False
                op = 3

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                cv.destroyAllWindows()
                run = False

    # Start the game on the difficulty chosen
    if op == 1:
        default_difficulty()
        menu(death_count=0, difficulty="e")
    elif op == 2:
        default_difficulty()
        menu(death_count=0, difficulty="n")
    elif op == 3:
        hard_difficulty()
        menu(death_count=0, difficulty="h")

def login_screen():
    global PLAYER1
    # Login menu's buttons and status definition
    font = pygame.font.Font('freesansbold.ttf', 24)
    fontb = pygame.font.Font('freesansbold.ttf', 30)
    fontc = pygame.font.Font('freesansbold.ttf', 52)
    fontd = pygame.font.Font('freesansbold.ttf', 18)
    login_bttn = Button(450, 500, LOGIN_IMG, 1)

    # Player's login variables
    user_text = ''
    pass_text = ''
    hidden_pass = ''
    user_input = pygame.Rect(400, 310, 450, 37)
    pass_input = pygame.Rect(400, 410, 450, 37)
    clicked_user = False
    clicked_pass = False
    failed = False
    login = False
    run = True

    while run:
        for event in pygame.event.get():
            # Check if player closes the game
            if event.type == pygame.QUIT:
                cap.release()
                cv.destroyAllWindows()
                run = False
            # Check if player clicked the text input areas
            if event.type == pygame.MOUSEBUTTONDOWN:
                if user_input.collidepoint(event.pos):
                    clicked_user = True
                    clicked_pass = False
                elif pass_input.collidepoint(event.pos):
                    clicked_user = False
                    clicked_pass = True
                else:
                    clicked_user = False
                    clicked_pass = False
            # Get player's input
            if event.type == pygame.KEYDOWN:
                if clicked_user:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
                if clicked_pass:
                    if event.key == pygame.K_BACKSPACE:
                        pass_text = pass_text[:-1]
                        hidden_pass = hidden_pass[:-1]
                    else:
                        pass_text += event.unicode
                        hidden_pass += '*'

        # Display text
        SCREEN.fill((255, 255, 255))
        textu = fontb.render("Nombre de Usuario", True, (0, 0, 0))
        textp = fontb.render("Contraseña", True, (0, 0, 0))
        SCREEN.blit(textu, (400, 277))
        SCREEN.blit(textp, (400, 377))
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 240))

        pygame.draw.rect(SCREEN, (0, 0, 0), user_input, 4)
        pygame.draw.rect(SCREEN, (0, 0, 0), pass_input, 4)
        user_t = font.render(user_text, True, (0, 0, 0))
        # Display hidden password
        user_p = fontc.render(hidden_pass, True, (0, 0, 0))
        SCREEN.blit(user_t, (user_input.x + 5, user_input.y + 5))
        SCREEN.blit(user_p, (pass_input.x + 5, pass_input.y + 5))
        user_input.w = max(450, user_t.get_width() + 10)
        pass_input.w = max(450, user_p.get_width() + 10)

        # Validate player's login info in the database
        if login_bttn.draw(SCREEN):
            found = Player.query.filter_by(name=user_text).first()
            if found:
                if found.validate_password(pass_text):
                    PLAYER1 = found
                    login = True
                    run = False
                else:
                    failed = True
            else:
                failed = True

        if failed:
            error = fontd.render("Nombre de Usuario o Contraseña incorrectos", True, (255, 0, 0))
            SCREEN.blit(error, (425, 235))
        pygame.display.update()

    if login:
        main_menu()

# Start the game on the login screen
login_screen()