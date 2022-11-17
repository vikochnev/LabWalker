# Модуль, отвечающий за создание уровня-лабиринта

import copy
from enum import Enum

import numpy as np


class CellType(Enum):
    """Класс, отвечающий за тип тайла"""
    Empty = 1
    Block = 2


class CellMark(Enum):
    """Класс, отвечающий за определение, является ли тайл началом либо концом"""
    No = 0
    Start = 1
    End = 2


class Cell:
    """Класс, отвечающий за параметры единичного тайла"""

    def __init__(self, type=CellType.Empty, mark=CellMark.No, pos=None):
        self.type = type
        self.count = 0
        self.mark = mark
        self.path_from = None
        self.pos = pos

    def get_type(self):
        return self.type

    def get_mark(self):
        return self.mark

    def get_count(self):
        return self.count


class CellGrid:
    """Класс, отвечающий за поле, состоящее из тайлов"""

    def __init__(self, board):
        self.board = board

    def get_size(self):
        """Получить размеры поля"""
        return [len(self.board), len(self.board[0])]

    def get_cell_type(self, pos_x, pos_y):
        return self.board[pos_x][pos_y].get_type()

    def get_cell_mark(self, pos_x, pos_y):
        return self.board[pos_x][pos_y].get_mark()

    def get_count(self, pos_x, pos_y):
        return self.board[pos_x][pos_y].get_count()

    def get_start(self):
        for ix in range(len(self.board)):
            for iy in range(len(self.board[0])):
                if self.get_cell_mark(ix, iy) == CellMark.Start:
                    return [ix, iy]

    def get_end(self):
        for ix in range(len(self.board)):
            for iy in range(len(self.board[0])):
                if self.get_cell_mark(ix, iy) == CellMark.End:
                    return [ix, iy]

    def at(self, pos):
        """Получить текущую позицию на поле"""
        return self.board[pos[0]][pos[1]]

    def clone(self):
        """Получить копию поля"""
        return CellGrid(copy.deepcopy(self.board))

    def clear_count(self, count):
        """Задаёт всем клеткам определенный счётчик, удаляет предыдущий шаг"""
        for o in self.board:
            for i in o:
                i.count = count
                i.path_from = None

    def is_valid_point(self, pos):
        """Проверка на выход за пределы поля"""
        sz = self.get_size()
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < sz[0] and pos[1] < sz[1]


def add_point(a, b):
    return [a[0] + b[0], a[1] + b[1]]

def create_labyrinth(file):
    file = open(file, "r")
    lab = file.readlines()
    file.close()
    nboard = []

    for ix in range(len(lab)):
        col = []
        for iy in range(len(lab[0]) - 1):
            if lab[ix][iy] == "0":
                bcell = Cell(type=CellType.Empty, pos=[ix, iy])
            elif lab[ix][iy] == "W":
                bcell = Cell(type=CellType.Block, pos=[ix, iy])
            elif lab[ix][iy] == "S":
                bcell = Cell(type=CellType.Empty, mark=CellMark.Start, pos=[ix, iy])
                #start_x, start_y = ix, iy
            elif lab[ix][iy] == "F":
                bcell = Cell(type=CellType.Empty, mark=CellMark.End, pos=[ix, iy])
                #end_x, end_y = ix, iy
            col.append(bcell)
        nboard.append(col)
    tboard = np.transpose(nboard)
    return CellGrid(tboard)
    #return tboard
