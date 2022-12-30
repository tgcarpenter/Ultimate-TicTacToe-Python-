from PyQt6.QtWidgets import QMainWindow, QApplication, QMenu
from PyQt6.QtGui import QAction, QIcon
import sys

from tictactoewidget import *


class Display(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate TicTacToe")
        self.setWindowIcon(QIcon("bigX.png"))
        self.setGeometry(100, 100, 480, 500)
        self.setMinimumSize(480, 500)

        board = TicTacToeWidget(rand=True)

        self.menu = QMenu("File")
        reset = QAction("New Game", self)
        reset.triggered.connect(self.reset)
        reset.setShortcut("Ctrl+N")
        self.menu.addAction(reset)

        multi = QAction("2-Player", self)
        multi.triggered.connect(self.two_player)
        multi.setShortcut("Ctrl+Shift+N")
        self.menu.addAction(multi)

        self.menuBar().addMenu(self.menu)

        self.setCentralWidget(board)

        self.center_window(self)

    def reset(self):
        board = TicTacToeWidget(rand=True)
        self.setCentralWidget(board)
        switch.switch = True

    def two_player(self):
        board = TicTacToeWidget()
        self.setCentralWidget(board)
        switch.switch = True


    @staticmethod
    def center_window(win):
        a = win.frameGeometry()
        a.moveCenter(win.screen().availableGeometry().center())
        win.move(a.topLeft())


app = QApplication(sys.argv)

display = Display()
display.show()

app.exec()
