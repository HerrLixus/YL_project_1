from PyQt5 import QtCore, QtGui, QtWidgets


class SeatWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(300, 300, 300, 300)

    def set_buttons_from_template(self, template):
        for i, line in enumerate(template.split('n')):
            for j, symbol in enumerate(line):
                if symbol != '0':
                    self.init_button(j, i, symbol)
                self.resize(20 + (j + 1) * 30, 20 + (i + 1) * 30)

    def init_button(self, i, j, type):
        button = QtWidgets.QPushButton(self)
        button.move(10 + i * 30, 10 + j * 30)
        button.resize(25, 25)
        if type == 'b':
            button.setStyleSheet('background-color:blue')
        elif type == 'p':
            button.setStyleSheet('background-color:green')
