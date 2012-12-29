from collections import namedtuple
from itertools import product

import gui


class Cell(namedtuple('Cell', 'x y alive')):

    __slots__ = ()

    def __new__(cls, x, y, alive=True):
        return super(Cell, cls).__new__(cls, x, y, alive)

    def neighbourhood_locations(self):
        x_coordinates = [self.x - 1, self.x, self.x + 1]
        y_coordinates = [self.y - 1, self.y, self.y + 1]
        positions = set(list(product(x_coordinates, y_coordinates)))
        positions.remove((self.x, self.y))
        return positions

    def is_alive_with(self, num_neighbours):
        if num_neighbours < 2 or num_neighbours > 3:
            return False
        elif self.alive is False and num_neighbours == 3:
            return True
        return self.alive


class Board(object):

    X, Y = 0, 1

    def __init__(self, cells, renderer=gui.NullRenderer()):
        self.cells = {(cell.x, cell.y): cell for cell in cells}
        self.add_surrounding_dead_cells()
        self.renderer = renderer

    def add_surrounding_dead_cells(self):
        for cell in self.cells.values():
            nl = cell.neighbourhood_locations()
            for loc in nl:
                if self.cells.get(loc, None) is None:
                    self.cells[loc] = Cell(
                        loc[Board.X], loc[Board.Y], alive=False)

    def cell_alive_at(self, x, y):
        cell = self.cells.get((x, y), None)
        if cell:
            return cell.alive
        return False

    def all_cells(self):
        return {cell[0]: cell[1].alive for cell in self.cells.items()}

    def alive_neighbours(self, cell):
        positions_to_visit = cell.neighbourhood_locations()
        alive_neighbours = 0

        for pos in positions_to_visit:
            if self.cell_alive_at(pos[Board.X], pos[Board.Y]):
                alive_neighbours += 1
        return alive_neighbours

    def tick(self):
        cells = {}
        for cell in self.cells.values():
            alive_neighbours = self.alive_neighbours(cell)
            if cell.is_alive_with(alive_neighbours):
                cells[(cell.x, cell.y)] = Cell(cell.x, cell.y)

        self.cells = cells
        self.add_surrounding_dead_cells()
        self.renderer.update_board()
