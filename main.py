import sys
from PyQt5.QtWidgets import QApplication
from view import Example


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
