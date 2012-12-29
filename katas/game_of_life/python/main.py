import game, gui


if __name__ == "__main__":
    # Board initialized with simple spaceship pattern
    first = game.Cell(5, 5)
    second = game.Cell(6, 5)
    third = game.Cell(6, 6)
    fourth = game.Cell(7, 5)
    board = game.Board([first, second, third, fourth])

    tk_renderer = gui.BoardRenderer(board)
    board.renderer = tk_renderer
    tk_renderer.run()
