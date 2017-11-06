import math

from pygame.display import set_mode
from pygame.draw import rect
from pygame.locals import Rect
from tkinter import *
from tkinter import messagebox


squareCenters = []
ScreenWidth = BoardWidth = 640
ScreenHeight = BoardHeight = 640
screen = set_mode((ScreenWidth, ScreenHeight))
black = (0, 0, 0)
white = (255, 255, 255)
light_brown = (251, 196, 117)
gray = (100, 100, 100)
green = (34, 139, 34)
violet = (238, 130, 238)
blue = (0, 0, 128)
gold = (255, 215, 0)
dark_brown = (139, 69, 0)
colors = [dark_brown, light_brown]


def drawboard(_colors):
    # 0 1 2 3 4 5 6 7
    # 9 10 11 12 13 14 15  etc
    increment = BoardWidth / 8
    index = 1  # toswitchcolors (index - 1) * -1
    for column in range(8):
        for row in range(8):
            Square = Rect(row * increment, column * increment, increment+1, increment+1)
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