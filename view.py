from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QListWidget, QWidget
from ui_main import Ui_MainWindow
from ui_session_window import Ui_Form

import model


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_country_list()

    def update_country_list(self):
        self.country_box.clear()
        self.country_box.addItems(model.get_request('get_countries', ()))
        self.update_cities_list()

    def update_cities_list(self):
        self.city_box.clear()
        self.city_box.addItems(model.get_request('get_cities', (self.country_box.currentText(),)))
        self.update_streets_list()

    def update_streets_list(self):
        self.street_box.clear()
        self.street_box.addItems(model.get_request('get_streets', (self.city_box.currentText(),)))
        self.update_theaters_list()

    def update_theaters_list(self):
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(["Название", "Страна", "Город", "Улица", "Здание"])
        theaters = model.get_request('get_theaters', (self.country_box.currentText(),
                                                      self.city_box.currentText(),
                                                      self.street_box.currentText()))
        self.tableWidget_2.setRowCount(len(theaters))
        for i, line in enumerate(theaters):
            for j, label in enumerate(line):
                item = QTableWidgetItem(str(label))
                self.tableWidget_2.setItem(i, j, item)

    def update_sessions_list(self, list_widget, film_names):
        list_widget.addItems(film_names)

    def init_session_window_ui(self, args):
        self.session_window = SessionWindow(args)
        self.session_window.show()


class SessionWindow(QWidget, Ui_Form):
    def __init__(self, args):
        super().__init__()
        self.setupUi(self)
        self.fill_data(args)

    def fill_data(self, args):
        self.name_label.setText(str(args[0]))
        self.genre_label.setText(str(args[1]))
        self.age_limit_label.setText(str(args[2]) + "+")
        self.description_label.setText(str(args[3]))
        self.price_label.setText(str(args[4]))
        self.time_label.setText(str(args[5]))
