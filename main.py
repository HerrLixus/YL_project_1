import sys
from PyQt5.QtWidgets import QApplication
from view import MainWindow
import control


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    control.init_theater_list(ex)
    ex.show()
    sys.exit(app.exec())
