from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QRect, QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QPainter
from dataclasses import dataclass
import numpy as np
import random as rd

BACKGROUND_COLOR = 'black'
CELL_COLOR = 'white'
N_ROWS = 50
N_COLS = 50
GAME_WIDTH = 500
GAME_HEIGHT = 500
THRESHOLD = 0.5
PERIOD = 100 # time between updates in ms

@dataclass
class Cell:
    alive: bool = False
    alive_next: bool = False

class Game(QWidget):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        # Set GUI attributes
        self.setWindowTitle("Conway's Game of Life")
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )

        # initialize game
        self._timer = QTimer()
        self._cells = np.zeros((N_ROWS, N_COLS), Cell) # init cell grid

        self._setup_game()
        self._run_game()

    def paintEvent(self, event):
        """Draws the current state of the game in the window."""
        painter = QPainter(self)
        brush = QBrush()

        window_width = painter.device().width()
        window_height = painter.device().height()

        # Paint background
        brush.setColor(QColor(BACKGROUND_COLOR))
        brush.setStyle(Qt.SolidPattern)
        background = QRect(0, 0, window_width, window_height)
        painter.fillRect(background, brush)

        # Paint cells
        start_x = (window_width - GAME_WIDTH) / 2
        start_y = (window_height - GAME_HEIGHT) / 2
        cell_width = GAME_WIDTH / N_COLS
        cell_height = GAME_HEIGHT / N_ROWS

        for i in range(N_ROWS):
            for j in range(N_COLS):
                if self._cells[i][j].alive:
                    brush.setColor(QColor(CELL_COLOR))
                    cell_x = start_x + cell_width*j
                    cell_y = start_y + cell_height*i
                    cell = QRect(cell_x, cell_y, cell_width, cell_height)
                    painter.fillRect(cell, brush)

    def sizeHint(self):
        """Starting size of the window. 
        
        Used as the minimum size by setSizePolicy()
        """
        return QSize(GAME_WIDTH, GAME_HEIGHT)

    def _setup_game(self):
        """Initializes array of cells to represent game."""

        rd.seed() # use in case you want to keep using the same values

        for i in range(N_ROWS):
            for j in range(N_COLS):
                self._cells[i][j] = Cell()
                self._cells[i][j].alive = rd.random() < THRESHOLD

        self._get_next_state()

    def _run_game(self):
        """ Updates the game after the given time period. """
        self._timer.setInterval(PERIOD)
        self._timer.timeout.connect(self._update_game)
        self._timer.start()

    def _update_game(self):
        for i in range(N_ROWS):
            for j in range(N_COLS):
                # update current state to next state
                self._cells[i][j].alive = self._cells[i][j].alive_next

        # calculate new next state
        self._get_next_state()
        self.update()

    def _get_next_state(self):
        for i in range(N_ROWS):
            for j in range(N_COLS):
                nb = self._count_live_neighbors(i, j)

                if self._cells[i][j].alive:
                    if nb < 2:
                        # dies of underpopulation
                        self._cells[i][j].alive_next = False
                    elif nb < 4:
                        # lives on to next generation
                        self._cells[i][j].alive_next = True
                    else:
                        # dies of overpopulation
                        self._cells[i][j].alive_next = False
                else:
                    if nb == 3:
                        # lives by reproduction
                        self._cells[i][j].alive_next = True
                    else:
                        # remains dead
                        self._cells[i][j].alive_next = False  

    def _count_live_neighbors(self, row, col):
        """Counts the number of lives neighbors for the cell at given position. """

        sum = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                # only count cells that are in bounds and don't count yourself
                if (i >= 0 and i < N_ROWS) and (j >= 0 and j < N_COLS) and not (i == row and j == col):
                    sum += self._cells[i][j].alive

        return sum

def main():
    app = QApplication([])
    game = Game()
    game.show()
    app.exec_()

if __name__ == "__main__":
    main()