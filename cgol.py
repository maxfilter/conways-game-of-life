from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QRect, QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QPainter
from dataclasses import dataclass
import numpy as np
import random as rd

BACKGROUND_COLOR = 'black'
CELL_COLORS = ['#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#ffffbf', '#e6f598', '#abdda4', '#66c2a5', '#3288bd', '#5e4fa2']
N_ROWS = 50
N_COLS = 50
GAME_WIDTH = 500
GAME_HEIGHT = 500
THRESHOLD = 0.5  # probability that a cell is alive at start
PERIOD = 100  # time between updates in ms

@dataclass
class Cell:
    alive: bool = False
    alive_next: bool = False
    age: int = -1

    def get_color(self):
        """ Determines cell color based on age. """
        if self.age < 0:
            return BACKGROUND_COLOR
        elif self.age >= len(CELL_COLORS):
            # Stay at last color after reaching age
            return CELL_COLORS[len(CELL_COLORS) - 1]
        else:
            return CELL_COLORS[self.age]

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

        # Keep game centered in window
        start_x = (window_width - GAME_WIDTH) / 2
        start_y = (window_height - GAME_HEIGHT) / 2
        cell_width = GAME_WIDTH / N_COLS
        cell_height = GAME_HEIGHT / N_ROWS

        # Paint living cells
        for i in range(N_ROWS):
            for j in range(N_COLS):
                if self._cells[i][j].alive:
                    # Get cell color based on age
                    brush.setColor(QColor(self._cells[i][j].get_color()))

                    # Calculate cell coordinates
                    cell_x = start_x + cell_width*j
                    cell_y = start_y + cell_height*i

                    # Draw cell in window
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

                if rd.random() < THRESHOLD:
                    self._cells[i][j].alive = True
                    self._cells[i][j].age += 1

        self._get_next_state()

    def _run_game(self):
        """Refreshes the current game state after a given time period. """
        self._timer.setInterval(PERIOD)
        self._timer.timeout.connect(self._update_game)
        self._timer.start()

    def _update_game(self):
        """Change the current game state and calculate the next game state. """
        for i in range(N_ROWS):
            for j in range(N_COLS):
                # update current state to next state
                self._cells[i][j].alive = self._cells[i][j].alive_next

                if self._cells[i][j].alive:
                    self._cells[i][j].age += 1
                else:
                    self._cells[i][j].age = -1

        # calculate new next state
        self._get_next_state()
        self.update()

    def _get_next_state(self):
        """Determine the next game state using the current game state and the rules. """
        for i in range(N_ROWS):
            for j in range(N_COLS):
                nb = self._count_live_neighbors(i, j)
                self._cells[i][j].alive_next = (nb == 3 or (nb == 2 and self._cells[i][j].alive))

    def _count_live_neighbors(self, row, col):
        """Counts the number of live neighbors for the cell at given position. """
        sum = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                # only count cells in bounds and don't let cell count itself
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