from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QListWidget, QWidget
from ui_main import Ui_MainWindow
from ui_session_window import Ui_Form

import model


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_country_list()

    def init_theater_tab(self):
        self.init_theater_tab_ui()
        self.update_sessions_list(self.tabWidget.currentIndex())

    def update_country_list(self):
        self.country_box.clear()
        self.country_box.addItems(model.get_countries())
        self.update_cities_list()

    def update_cities_list(self):
        self.city_box.clear()
        self.city_box.addItems(model.get_cities(self.country_box.currentText()))
        self.update_streets_list()

    def update_streets_list(self):
        self.street_box.clear()
        self.street_box.addItems(model.get_streets(self.city_box.currentText()))
        self.update_theaters_list()

    def update_theaters_list(self):
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(["Название", "Страна", "Город", "Улица", "Здание"])
        theaters = model.get_theaters(self.country_box.currentText(),
                                      self.city_box.currentText(),
                                      self.street_box.currentText())
        self.tableWidget_2.setRowCount(len(theaters))
        for i, line in enumerate(theaters):
            for j, label in enumerate(line):
                item = QTableWidgetItem(str(label))
                self.tableWidget_2.setItem(i, j, item)

    def update_sessions_list(self, tab_id):
        widget = self.tabWidget.widget(tab_id)
        name = self.tabWidget.tabText(tab_id)
        list_widget = widget.findChild(QListWidget)
        list_widget.addItems(model.get_sessions(model.get_theater_id(name)))

    def init_session_window(self):
        self.session_window = SessionWindow()
        self.session_window.show()


class SessionWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
