from game import Cell, Board

import unittest


class GameOfLife(unittest.TestCase):

    def setUp(self):
        self.fst_cell = Cell(6, 6)
        self.snd_cell = Cell(5, 6)
        self.trd_cell = Cell(5, 7)
        self.fourth_cell = Cell(6, 7)
        self.fifth_cell = Cell(7, 5)

    def test_cell_neighbourhood(self):
        expected_neighbourhood = set([(6, 7), (5, 5), (5, 6),
                                      (7, 6), (5, 7), (7, 7),
                                      (7, 5), (6, 5)])

        self.assertEqual(expected_neighbourhood,
            self.fst_cell.neighbourhood_locations())

    def test_a_cell_without_neighbours_dies_after_tick(self):
        dying_cell = Cell(4, 4)
        my_board = Board([self.fst_cell, self.snd_cell, self.trd_cell, dying_cell])
        my_board.tick()

        self.assertFalse(my_board.cell_alive_at(4, 4))
        self.assertTrue(my_board.cell_alive_at(6, 6))
        self.assertTrue(my_board.cell_alive_at(5, 6))
        self.assertTrue(my_board.cell_alive_at(5, 7))

    def test_a_cell_with_2or3_neighbours_stays_alive_after_tick(self):
        my_board = Board([self.fst_cell, self.snd_cell, self.trd_cell, self.fourth_cell])
        my_board.tick()

        self.assertTrue(my_board.cell_alive_at(6, 6))
        self.assertTrue(my_board.cell_alive_at(5, 6))
        self.assertTrue(my_board.cell_alive_at(5, 7))
        self.assertTrue(my_board.cell_alive_at(6, 7))

    def test_a_cell_with_more_then_3_neighbours_dies(self):
        my_board = Board([self.fst_cell, self.snd_cell,
            self.trd_cell, self.fourth_cell, self.fifth_cell])

        my_board.tick()

        # dying cells: first and fifth.
        self.assertFalse(my_board.cell_alive_at(6, 6))
        self.assertFalse(my_board.cell_alive_at(7, 5))

        self.assertTrue(my_board.cell_alive_at(5, 6))
        self.assertTrue(my_board.cell_alive_at(5, 7))
        self.assertTrue(my_board.cell_alive_at(6, 7))

    def test_a_died_cell_with_3_alive_neighbours_resurrects(self):
        my_board = Board([self.fst_cell, self.snd_cell, self.trd_cell])
        my_board.tick()

        self.assertTrue(my_board.cell_alive_at(6, 6))
        self.assertTrue(my_board.cell_alive_at(5, 6))
        self.assertTrue(my_board.cell_alive_at(5, 7))

        # Having 3 alive neighbours comes back to life.
        self.assertTrue(my_board.cell_alive_at(6, 7))

    def test_acceptance_different_generations(self):
        # simple spaceship pattern
        first = Cell(5, 5)
        second = Cell(6, 5)
        third = Cell(6, 6)
        fourth = Cell(7, 5)
        my_board = Board([first, second, third, fourth])

        # First generation
        # cells: (5, 5), (6, 5), (6, 6), (7, 5)
        # and these new borns (6, 4), (5, 6), (7, 6)
        my_board.tick()

        self.assertTrue(my_board.cell_alive_at(5, 5))
        self.assertTrue(my_board.cell_alive_at(6, 5))
        self.assertTrue(my_board.cell_alive_at(6, 6))
        self.assertTrue(my_board.cell_alive_at(7, 5))

        self.assertTrue(my_board.cell_alive_at(6, 4))
        self.assertTrue(my_board.cell_alive_at(5, 6))
        self.assertTrue(my_board.cell_alive_at(7, 6))

        # Second generation
        # dying cells: (5, 5), (6, 5), (6, 6), (7, 5)
        # new borns: (5, 4), (6, 7), (7, 4)
        # alive cells: (5, 4), (6, 7), (7, 4), (5, 6),
        # (6, 4), (7, 6)
        my_board.tick()

        self.assertFalse(my_board.cell_alive_at(5, 5))
        self.assertFalse(my_board.cell_alive_at(6, 5))
        self.assertFalse(my_board.cell_alive_at(6, 6))
        self.assertFalse(my_board.cell_alive_at(7, 5))

        self.assertTrue(my_board.cell_alive_at(5, 4))
        self.assertTrue(my_board.cell_alive_at(6, 7))
        self.assertTrue(my_board.cell_alive_at(7, 4))

        self.assertTrue(my_board.cell_alive_at(5, 6))
        self.assertTrue(my_board.cell_alive_at(6, 4))
        self.assertTrue(my_board.cell_alive_at(7, 6))

        # Third generation:
        # dying cells: (5, 4), (5, 6), (7, 4), (7, 6)
        # new borns: (5, 5), (6, 3), (6, 6), (7, 5)
        # alive cells: (5, 5), (6, 3), (6, 6), (7, 5),
        # (6, 4), (6, 7)
        my_board.tick()

        self.assertFalse(my_board.cell_alive_at(5, 4))
        self.assertFalse(my_board.cell_alive_at(5, 6))
        self.assertFalse(my_board.cell_alive_at(7, 4))
        self.assertFalse(my_board.cell_alive_at(7, 6))

        self.assertTrue(my_board.cell_alive_at(5, 5))
        self.assertTrue(my_board.cell_alive_at(6, 3))
        self.assertTrue(my_board.cell_alive_at(6, 6))
        self.assertTrue(my_board.cell_alive_at(7, 5))
        self.assertTrue(my_board.cell_alive_at(6, 4))
        self.assertTrue(my_board.cell_alive_at(6, 7))
