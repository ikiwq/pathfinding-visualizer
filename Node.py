import math

import pygame as pg
from Settings import *


class Node(pg.sprite.Sprite):
    def __init__(self, pos, tilesize, COLOR, maxRows):
        super().__init__()
        self.x, self.y = pos
        self.maxRows = maxRows
        self.tilex, self.tiley = self.x // tilesize, self.y //tilesize

        self.color = COLOR
        self.image = pg.Surface([tilesize, tilesize])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = ([self.x, self.y])

        self.neighbours = []

        self.hscore = math.inf
        self.gscore = math.inf
        self.fscore = self.hscore + self.gscore

        self.cameFrom = None

    def get_pos(self):
        return self.tilex, self.tiley

    def make_open(self):
        self.color = WHITE
    def make_start(self):
        self.color = PURPLE
    def make_end(self):
        self.color = GREEN
    def make_explor(self):
        self.color = DARK_BLUE
    def make_explored(self):
        self.color = BLUE
    def make_barrier(self):
        self.color = BLACK
    def make_path(self):
        self.color = RED

    def is_open(self):
        return self.color == WHITE
    def is_start(self):
        return self.color == PURPLE
    def is_end(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK

    def inspect_neighbours(self, grid):
        if self.tiley > 0 and not grid[self.tilex][self.tiley-1].is_barrier():    #CHECK UP
            self.neighbours.append(grid[self.tilex][self.tiley - 1])

        if self.tiley < self.maxRows-1 and not grid[self.tilex][self.tiley+1].is_barrier(): #CHECK DOWN
            self.neighbours.append(grid[self.tilex][self.tiley + 1])

        if self.tilex >  0 and not grid[self.tilex-1][self.tiley].is_barrier(): #CHECK LEFT
            self.neighbours.append(grid[self.tilex-1][self.tiley])

        if self.tilex < self.maxRows-1 and not grid[self.tilex+1][self.tiley].is_barrier(): #CHECK RIGHT
            self.neighbours.append(grid[self.tilex + 1][self.tiley])

    def update(self):
        self.image.fill(self.color)
        self.fscore = self.hscore + self.gscore

    def __lt__(self, other):
        return False