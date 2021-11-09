from PyQt5 import QtCore, QtWidgets


class SeatWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = list()
        self.initUi()

    def initUi(self):
        self.setGeometry(300, 300, 300, 300)
        self.save_button = QtWidgets.QPushButton("Сохранить", self)
        self.save_button.setGeometry(QtCore.QRect(self.width() - 105, self.height() - 30,
                                                  100, 25))

    def set_buttons_from_template(self, template):
        self.buttons = [[self.init_button(j, i, symbol) for j, symbol in enumerate(line)]
                        for i, line in enumerate(template.split('n'))]
        self.resize_window()

    def init_button(self, i, j, seat_type):
        button = QtWidgets.QPushButton(self)
        button.move(10 + i * 55, 10 + j * 55)
        button.resize(50, 50)
        button.show()

        if seat_type == '0':
            button.hide()
            button.setObjectName('Hidden')
        elif seat_type == 'b':
            button.setStyleSheet('background-color:blue')
            button.setObjectName('Booked')
        elif seat_type == 'p':
            button.setStyleSheet('background-color:green')
            button.setObjectName('Purchased')
        elif seat_type == '1':
            button.setObjectName('Free')
        return button

    def resize_window(self):
        i, j = len(self.buttons), len(self.buttons[0])
        self.resize(75 + j * 55, 75 + i * 55)
        self.save_button.setGeometry(QtCore.QRect(self.width() - 105, self.height() - 30,
                                                  100, 25))


class InputSeatWidget(SeatWidget):
    def __init__(self):
        super().__init__()
        self.buttons = [[self.init_button(j, i, '1') for j in range(3)] for i in range(3)]

    def initUi(self):
        super().initUi()
        self.add_row = QtWidgets.QPushButton("+", self)
        self.remove_row = QtWidgets.QPushButton("-", self)
        self.add_column = QtWidgets.QPushButton("+", self)
        self.remove_column = QtWidgets.QPushButton("-", self)

        self.move_buttons()

    def init_button(self, i, j, seat_type):
        button = QtWidgets.QPushButton(self)
        button.move(10 + i * 55, 10 + j * 55)
        button.resize(50, 50)
        button.show()

        if seat_type == '0':
            button.setText('X')
            button.setObjectName('Hidden')
        return button

    def move_buttons(self):
        self.add_row.setGeometry(QtCore.QRect(35, self.height() - 30, 25, 25))
        self.remove_row.setGeometry(QtCore.QRect(5, self.height() - 30, 25, 25))
        self.add_column.setGeometry(QtCore.QRect(self.width() - 30, 35, 25, 25))
        self.remove_column.setGeometry(QtCore.QRect(self.width() - 30, 5, 25, 25))

    def resize_window(self):
        super().resize_window()
        self.move_buttons()
