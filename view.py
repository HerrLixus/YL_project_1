from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QListWidget, \
    QWidget, QMessageBox

import control
import model

import ui_main
import ui_new_theater
import ui_seat_schema
import ui_session_window
import ui_session_edit
import ui_film_choice
import ui_room_choice


class MainWindow(QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def update_theaters_list(self, theaters):
        self.tableWidget_2.setColumnCount(5)
        self.tableWidget_2.setHorizontalHeaderLabels(["Название", "Страна", "Город", "Улица", "Здание"])
        self.tableWidget_2.setRowCount(len(theaters))
        for i, line in enumerate(theaters):
            for j, label in enumerate(line):
                if j == 5:
                    continue
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
        return self.new_theater_window

    def init_new_session_window_ui(self):
        self.edit_window = EditSessionWindow()
        self.edit_window.show()
        return self.edit_window


class SessionWindow(QWidget, ui_session_window.Ui_Form):
    def __init__(self, args):
        super().__init__()
        self.setupUi(self)
        self.args = args
        self.fill_data(args)

    def fill_data(self, args):
        self.name_label.setText(str(args[0]))
        self.genre_label.setText(str(args[1]))
        self.age_limit_label.setText(str(args[2]) + "+")
        self.description_label.setText(str(args[3]))
        self.price_label.setText(str(args[4]))
        self.time_label.setText(str(args[5]))

    def init_seat_schema_window(self):
        self.seat_window = ui_seat_schema.SeatWidget()
        self.seat_window.show()
        return self.seat_window

    def init_edit_window_ui(self):
        self.edit_window = EditSessionWindow()
        self.edit_window.show()
        return self.edit_window


class EditSessionWindow(QWidget, ui_session_edit.Ui_Form):
    def __init__(self):
        super(EditSessionWindow, self).__init__()
        self.setupUi(self)

    def fill_data(self, *args):
        self.film_name.setText(str(args[0]))
        self.room_name.setText(str(args[1]))
        self.price_input.setText(str(args[2]))
        self.time_input.setDateTime(args[3])

    def init_film_choice_window(self):
        self.film_choice_window = FilmChoiceWindow()
        self.film_choice_window.show()
        return self.film_choice_window

    def init_room_choice_window(self):
        self.room_choice_window = RoomChoiceWindow()
        self.room_choice_window.show()
        return self.room_choice_window

    def check(self):
        reply = QMessageBox.question(self, "Внимание", "Сохранить введённые данные?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def show_error_message(self, error):
        self.error_output.setText(f"Возникла ошибка {error}")


class FilmChoiceWindow(QWidget, ui_film_choice.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setup_table(self, table):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(len(table))
        self.tableWidget.setHorizontalHeaderLabels(['Название', "Год выпуска",
                                                    "Жанр", "Возрастное ограничение",
                                                    "Продолжительность", "Описание"])
        for i in range(6):
            self.tableWidget.setColumnWidth(i, self.tableWidget.width() // 6)
        for i, row in enumerate(table):
            for j, label in enumerate(row):
                if j == 0:
                    continue
                self.tableWidget.setItem(i, j - 1, QTableWidgetItem(str(label)))
        return self.tableWidget


class RoomChoiceWindow(QWidget, ui_room_choice.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setup_list(self, rooms):
        for room in rooms:
            self.listWidget.addItem(str(room))
        return self.listWidget

    def show_room(self, template):
        self.room_show_window = ui_seat_schema.SeatWidget()
        self.room_show_window.set_buttons_from_template(template)
        self.room_show_window.save_button.hide()
        self.room_show_window.show()


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

    def init_new_room_window(self):
        self.new_room_window = ui_seat_schema.InputSeatWidget()
        self.new_room_window.show()
        control.bind_generating_template_buttons_logic(self.new_room_window)

    def check(self):
        reply = QMessageBox.question(self, "Внимание", "Сохранить введённые данные?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def show_error_message(self, error):
        self.error_label.setText(f"Возникла ошибка {error}")
