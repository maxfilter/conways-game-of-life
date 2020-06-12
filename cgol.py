from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QRect, QTimer, QSize
from PyQt5.QtGui import QBrush, QColor, QPainter
from dataclasses import dataclass
import numpy as np

BACKGROUND_COLOR = 'black'
CELL_COLOR = 'white'
N_ROWS = 50
N_COLS = 50
GAME_WIDTH = 500
GAME_HEIGHT = 500

@dataclass
class Cell:
    alive: bool = True
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
        self._cells = self._init_cells()

        # run game
        self._timer = QTimer()
        self._timer.setInterval(1000) # time between updates in ms
        self._timer.timeout.connect(self.update_state)
        self._timer.start()

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

    @staticmethod
    def _init_cells():
        """Initializes array of cells to represent the game."""
        cells = np.zeros((N_ROWS, N_COLS), Cell)
        for i in range(N_ROWS):
            for j in range(N_COLS):
                cells[i][j] = Cell()

        return cells

    def update_state(self):
        self._cells[1][1].alive = not self._cells[1][1].alive
        self.update()

def main():
    app = QApplication([])
    game = Game()
    game.show()
    app.exec_()

if __name__ == "__main__":
    main()