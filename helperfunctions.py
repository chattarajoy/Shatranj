import math

import pygame
from pygame.display import set_mode
from pygame.draw import rect
from pygame.locals import QUIT, KEYUP, K_ESCAPE, Rect
from sys import exit

from tkinter import Tk, messagebox

squareCenters = []
ScreenWidth = BoardWidth = 640
ScreenHeight = BoardHeight = 640
screen = set_mode((ScreenWidth, ScreenHeight))
light_brown = (251, 196, 117)
gray = (100, 100, 100)
violet = (238, 130, 238)
dark_brown = (139, 69, 0)
colors = [dark_brown, light_brown]


def drawboard(_colors):
    increment = BoardWidth / 8
    index = 1  # toswitchcolors (index - 1) * -1
    for column in range(8):
        for row in range(8):
            Square = Rect(row * increment, column * increment, increment + 1, increment + 1)
            if Square not in squareCenters:
                squareCenters.append(Square)
            rect(screen, _colors[index], Square)
            index = (index - 1) * -1
        index = (index - 1) * -1


def make_lines(position, positionlist, anglelist):

    listofpossiblelines = []
    for Square in positionlist:
        for angle in anglelist:
            dx = Square.centerx - position.centerx
            dy = Square.centery - position.centery
            newangle = math.atan2(-dy, dx)
            if angle == newangle:
                listofpossiblelines.append([Square, angle])
    return listofpossiblelines


def square(x):
    return x * x


def distance_formula(pos1, pos2):
    # pos1 and pos2 are tuples of 2 numbers
     return math.sqrt(square(pos2[0] - pos1[0]) + square(pos2[1] - pos1[1]))


def isfarther(start, pos1, pos2):
    # Returns T/F whether pos2 is farther away than pos1

    if type(pos2) == int:  # for pawns
        return pos2 > distance_formula(start.center, pos1)
    else:
        return distance_formula(start.center, pos2) > distance_formula(start.center, pos1)


def nearest_piece(position, listof):
    nearest = None
    posCounter = 50000  # a very high number/ could use board dimension^2
    for piece in listof:
        if distance_formula(piece.rect.center, position) < posCounter:
            nearest = piece
            posCounter = distance_formula(piece.rect.center, position)
    if posCounter < BoardWidth / 8 - 30:
        return nearest  # only works when close
    else:
        return None

def show_checkmate(teams):
    Tk().wm_withdraw()  # to hide the main window
    messagebox.showinfo("CheckMate", teams[1] + " wins!")

def show_check(teams):
    Tk().wm_withdraw()  # to hide the main window
    messagebox.showinfo("Check!", teams[0] + "'s King under check")


def checkquitgame():
    for _ in pygame.event.get(QUIT):
        print len(squareCenters)
        pygame.quit()
        exit()

    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            exit()
        pygame.event.post(event)