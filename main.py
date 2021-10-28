import sys
from PyQt5.QtWidgets import QApplication
from view import Example
import control


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    control.init_logic(ex)
    ex.show()
    sys.exit(app.exec())
