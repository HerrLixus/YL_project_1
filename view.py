import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from main_ui import Ui_MainWindow

import model


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_country_list()
        self.tableWidget_2.itemDoubleClicked.connect(self.init_theater_tab)

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
        self.tableWidget_2.setColumnCount(4)
        self.tableWidget_2.setHorizontalHeaderLabels(["Название", "Страна", "Город", "Улица"])
        theaters = model.get_theaters(self.country_box.currentText(),
                                      self.city_box.currentText(),
                                      self.street_box.currentText())
        self.tableWidget_2.setRowCount(len(theaters))
        for i, line in enumerate(theaters):
            for j, label in enumerate(line):
                item = QTableWidgetItem(label)
                self.tableWidget_2.setItem(i, j, item)
