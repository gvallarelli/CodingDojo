import Tkinter


class CellSquare(Tkinter.Label):
    def __init__(self, parent):
        Tkinter.Label.__init__(self, parent, relief="raised", width=2, borderwidth=1)

    def displayState(self, alive):
        self["bg"] = "black" if alive else "white"


class NullRenderer(object):

    def update_board(self):
        pass


class BoardRenderer(object):
    # Can eat your kittens!

    def __init__(self, board, height=25, width=25):
        self.board = board

        self.root = Tkinter.Tk()
        self.frame = Tkinter.Frame(self.root)
        self.frame.pack()
        self._create_buttons()
        self._create_grid(height, width)
        self.update_board()


    def _create_buttons(self):
        self.bottomFrame = Tkinter.Frame(self.root)
        self.bottomFrame.pack(side=Tkinter.BOTTOM)
        self.buttonStep = Tkinter.Button(self.bottomFrame, text="Step", command=self.step)
        self.buttonStep.pack(side=Tkinter.TOP)

    def _create_grid(self, height, width):
        self.cells = [[None for col in range(height)]
                        for row in range(width)]
        for x in range(0, width):
            for y in range(0, height):
                c = CellSquare(self.frame)
                c.grid(row=x, column=y)
                self.cells[x][y] = c

    def update_board(self):
        for loc, alive in self.board.all_cells().items():
            self.cells[loc[0]][loc[1]].displayState(alive)

    def run(self):
        self.root.mainloop()

    def step(self):
        self.board.tick()
