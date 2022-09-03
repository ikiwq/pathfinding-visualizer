import pygame as pg
from Settings import *

def drawRectText(win, xpos, ypos, width, height, color, Font, Text):
    pg.draw.rect(win,(color), (xpos, ypos, width, height))
    text = Font.render(Text, True, BLACK)
    win.blit(text,(xpos + (width - text.get_rect().width)/2, ypos + (height - text.get_rect().height)/2 ))

def drawTitle(win,xpos, ypos, Font, Text, color):
    text = Font.render(Text, True, color)
    win.blit(text,((xpos+(SCREEN_WH-text.get_rect().width)/2), ypos))

def HeurDist(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1-x2) + abs(y1-y2)
