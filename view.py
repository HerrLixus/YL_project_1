from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QListWidget, QWidget, QMessageBox

from ui_main import Ui_MainWindow
import ui_session_window
import ui_new_theater
import ui_seat_schema

import model
import control


class Example(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_country_list()
        control.bind_main_logic(self)

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

    def fill_theater_data(self, tab, args):
        list_widget = tab.findChild(QListWidget)
        list_widget.addItems(args)

    def init_session_window_ui(self, args):
        self.session_window = SessionWindow(args)
        self.session_window.show()
        return self.session_window

    def open_new_theater_window(self):
        self.new_theater_window = NewTheaterWindow()
        self.new_theater_window.show()


class SessionWindow(QWidget, ui_session_window.Ui_Form):
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

    def init_seat_schema_window(self, session_id):
        seat_schema = model.get_request('get_seat_schema', (session_id,))
        self.seat_window = ui_seat_schema.SeatWidget()
        self.seat_window.show()
        self.seat_window.set_buttons_from_template(seat_schema)
        control.bind_seat_window_logic(self.seat_window)


class NewTheaterWindow(QWidget, ui_new_theater.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.country_input.hide()
        self.city_input.hide()
        self.street_input.hide()
        self.update_country_list()
        control.bind_new_theater_logic(self)

    def update_country_list(self):
        self.country_box.clear()
        self.country_box.addItems(model.get_request('get_countries', ()))
        self.country_box.addItem("Другое")
        self.update_cities_list()

    def update_cities_list(self):
        self.city_box.clear()
        self.city_box.addItems(model.get_request('get_cities', (self.country_box.currentText(),)))
        self.city_box.addItem("Другое")
        self.update_streets_list()

    def update_streets_list(self):
        self.street_box.clear()
        self.street_box.addItems(model.get_request('get_streets', (self.city_box.currentText(),)))
        self.street_box.addItem("Другое")

    def toggle_line_edit(self):
        if self.country_box.currentText() == "Другое":
            self.country_input.show()
        else:
            self.country_input.hide()

        if self.city_box.currentText() == "Другое":
            self.city_input.show()
        else:
            self.city_input.hide()

        if self.street_box.currentText() == "Другое":
            self.street_input.show()
        else:
            self.street_input.hide()

    def check(self):
        reply = QMessageBox.question(self, "Внимание", "Сохранить введённые данные?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def show_error_message(self, error):
        self.error_label.setText(f"Возникла ошибка {error}")
