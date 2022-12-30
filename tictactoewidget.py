from PyQt6.QtWidgets import QPushButton, QGridLayout, QSizePolicy
from PyQt6.QtGui import QResizeEvent

import switch

import random


class TicTacToeWidget(QPushButton):
    def __init__(self, main=True, parent=None, rand=False):
        super().__init__()
        self.parent = parent
        self.complete_board = None
        self.mass_enabled = True
        self.random = rand

        if not main:
            self.setStyleSheet(r"TicTacToeWidget {border-image:url(board.png) 0 0 0 0 stretch stretch; "
                               r"background-position:center center; background-repeat: no-repeat;"
                               r"background-color: qradialgradient(cx: 0.5, cy: 0.5, radius: 1.2, fx: 0.5, fy: 0.5, "
                               r"stop: 0 rgba(240,210,20,144), stop: 0.2 rgba(240,210,20,100), stop: 0.4 rgba(240,240,240,0));}")
        else:
            self.setStyleSheet(r"TicTacToeWidget {border-image:url(board.png) 0 0 0 0 stretch stretch; "
                               r"background-position:center center; background-repeat: no-repeat;}")

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.widgets = []

        self.layout = QGridLayout()
        # self.layout.setSpacing(5)
        self.setLayout(self.layout)
        if main:
            self.add_widgets()
        else:
            self.add_buttons()

    def disable_buttons(self):
        for button in self.widgets:
            button.setDisabled(True)
        if self.complete_board:
            self.setStyleSheet("TicTacToeWidget {border-image:url(big%s.png) 0 0 0 0 stretch stretch; "
                               "background-position:center center; "
                               "background-repeat: no-repeat;}" % self.complete_board)
        else:
            self.setStyleSheet("background-color: light grey")

    def enable_buttons(self, m=False):
        for button in self.widgets:
            if button.mark is None:
                button.setEnabled(True)
        self.setStyleSheet("TicTacToeWidget {background-color: qradialgradient("
                           "cx: 0.5, cy: 0.5, radius: 1.2, fx: 0.5, fy: 0.5, "
                           "stop: 0 rgba(240,210,20,144), stop: 0.2 rgba(240,210,20,100), stop: 0.4 rgba(240,240,240,0));}")
        enabled = [button.mark for button in self.widgets]
        if None not in enabled and not self.parent.mass_enabled:
            self.parent.mass_enable()
        if self.random and not m and not switch.switch:
            self.choose_random()

    def mass_disable(self):
        self.mass_enabled = False
        for board in self.widgets:
            board.disable_buttons()

    def mass_enable(self):
        self.mass_enabled = True
        for board in self.widgets:
            board.enable_buttons(True)

    def board_test(self, p):
        if self.parent.mass_enabled:
            self.parent.mass_disable()
        else:
            self.disable_buttons()
        self.parent.widgets[p].enable_buttons()
        if self.complete_board:
            return
        tests = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for line in tests:
            marks = [self.widgets[i].mark for i in line]
            if marks[0] and marks[0] == marks[1] and marks[1] == marks[2]:
                print("tictactoe")
                self.complete_board = self.widgets[line[0]].mark
                self.setStyleSheet(
                    "TicTacToeWidget {border-image:url(big%s.png) 0 0 0 0 stretch stretch; "
                    "background-position:center center; "
                    "background-repeat: no-repeat;}" % self.complete_board)

    def add_buttons(self):
        count = 0
        for i in range(3):
            for o in range(3):
                temp = XO(self, count)
                self.widgets.append(temp)
                self.layout.addWidget(temp, i, o)
                count += 1

    def add_widgets(self):
        self.blockSignals(True)
        for i in range(3):
            for o in range(3):
                temp = TicTacToeWidget(False, self, self.random)
                self.widgets.append(temp)
                self.layout.addWidget(temp, i, o)

    def choose_random(self):
        possible = [button.p for button in self.widgets if button.mark is None]
        if not possible:
            num = random.choice([i for i in range(9) if not self.parent.widgets[i].complete_board])
            self.parent.widgets[num].choose_random()
            return
        num = random.choice(possible)
        self.widgets[num].clicked.emit()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.setFixedWidth(self.height())
        self.layout.setSpacing((self.height() // 50))


class XO(QPushButton):
    def __init__(self, parent, p):
        super(XO, self).__init__()
        self.parent = parent
        self.p = p
        self.mark = None
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("border: None")
        self.clicked.connect(self.fill)

    def fill(self):
        if switch.switch:
            self.setStyleSheet(
                "border: None; border-image:url(X.png) 0 0 0 0 stretch stretch; background-position:center center; "
                "background-repeat: no-repeat;")
            self.mark = "X"
        else:
            self.setStyleSheet(
                "border: None; border-image:url(O.png) 0 0 0 0 stretch stretch; background-position:center center; "
                "background-repeat: no-repeat;")
            self.mark = "O"
        self.disconnect()
        switch.switch = not switch.switch
        self.parent.board_test(self.p)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.setMaximumWidth(self.height())
