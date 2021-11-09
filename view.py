from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QListWidget, \
    QWidget, QMessageBox, QPushButton

import control

import ui_main
import ui_new_film
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
        self.tableWidget_2.clearContents()
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
        list_widget.clear()
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

    def init_film_list(self):
        self.film_list = FilmListWindow()
        self.film_list.show()
        return self.film_list

    def closeEvent(self, event):
        if hasattr(self, 'session_window'):
            self.session_window.close()
        if hasattr(self, 'new_theater_window'):
            self.new_theater_window.close()
        if hasattr(self, 'edit_window'):
            self.edit_window.close()
        if hasattr(self, 'film_list'):
            self.film_list.close()


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

    def closeEvent(self, event):
        if hasattr(self, 'seat_window'):
            self.seat_window.close()
        if hasattr(self, 'edit_window'):
            self.edit_window.close()


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

    def closeEvent(self, event):
        if hasattr(self, 'film_choice_window'):
            self.film_choice_window.close()
        if hasattr(self, 'room_choice_window'):
            self.room_choice_window.close()


class FilmChoiceWindow(QWidget, ui_film_choice.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setup_table(self, table):
        self.tableWidget.clearContents()
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

    def closeEvent(self, event):
        if hasattr(self, 'room_show_window'):
            self.room_show_window.close()


class FilmListWindow(FilmChoiceWindow):
    def setupUi(self, Form):
        super().setupUi(Form)
        Form.resize(700, 400)
        self.new_film_button = QPushButton(Form)
        self.new_film_button.setGeometry(10, 360, 150, 25)
        self.new_film_button.setText('Добавить новый фильм')

    def open_new_film_window(self):
        self.new_film_window = NewFilmWindow()
        self.new_film_window.show()
        return self.new_film_window

    def closeEvent(self, event):
        if hasattr(self, 'new_film_window'):
            self.new_film_window.close()


class NewTheaterWindow(QWidget, ui_new_theater.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.country_input.hide()
        self.city_input.hide()
        self.street_input.hide()

    def update_country_list(self, countries):
        self.country_box.clear()
        self.country_box.addItems(countries)
        self.country_box.addItem("Другое")
        return self.country_box

    def update_cities_list(self, cities):
        self.city_box.clear()
        self.city_box.addItems(cities)
        self.city_box.addItem("Другое")
        return self.city_box

    def update_streets_list(self, streets):
        self.street_box.clear()
        self.street_box.addItems(streets)
        self.street_box.addItem("Другое")
        return self.street_box

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

    def init_room_list_window(self):
        self.room_list_window = RoomChoiceWindow()
        self.room_list_window.show()
        return self.room_list_window

    def check(self):
        reply = QMessageBox.question(self, "Внимание", "Сохранить введённые данные?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def show_error_message(self, error):
        self.error_label.setText(f"Возникла ошибка {error}")

    def closeEvent(self, event):
        if hasattr(self, 'new_room_window'):
            self.new_room_window.close()
        if hasattr(self, 'room_list_window'):
            self.room_list_window.close()


class NewFilmWindow(QWidget, ui_new_film.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setup_genres_list(self, names):
        self.genre_input.clear()
        self.genre_input.addItems(names)

    def check(self):
        reply = QMessageBox.question(self, "Внимание", "Сохранить введённые данные?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def show_error_message(self, text):
        self.error_label.setText(f"Возникла ошибка {text}")
