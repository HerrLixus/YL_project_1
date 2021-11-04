# Do all the logic here
from PyQt5 import QtWidgets
import model

"""Binding functions to buttons etc"""


def bind_main_logic(obj):
    obj.country_box.currentTextChanged.connect(obj.update_cities_list)
    obj.city_box.currentTextChanged.connect(obj.update_streets_list)

    obj.street_box.currentTextChanged.connect(obj.update_theaters_list)

    obj.tableWidget_2.itemDoubleClicked.connect(lambda: init_theater_tab(obj))
    obj.new_theater_button.clicked.connect(obj.open_new_theater_window)


def bind_new_theater_logic(obj):
    obj.country_box.currentTextChanged.connect(obj.update_cities_list)
    obj.country_box.currentTextChanged.connect(obj.toggle_line_edit)

    obj.city_box.currentTextChanged.connect(obj.update_streets_list)
    obj.city_box.currentTextChanged.connect(obj.toggle_line_edit)

    obj.street_box.currentTextChanged.connect(obj.toggle_line_edit)

    obj.add_room_button.clicked.connect(obj.init_new_room_window)

    obj.commit_button.clicked.connect(lambda: try_to_save_theater(obj))


"""Initializing new windows"""


def init_theater_tab(obj):
    name = obj.tableWidget_2.selectedItems()[0].text()
    obj.init_theater_tab_ui(name)
    tab = obj.tabWidget.widget(obj.tabWidget.currentIndex())

    sessions = model.get_request('get_sessions', (model.get_request('get_theater_id', (name,)),))
    film_names = [i[0] for i in sessions]
    obj.fill_theater_data(tab, film_names)

    list_widget = tab.findChild(QtWidgets.QListWidget)
    list_widget.itemDoubleClicked.connect(lambda: init_session_window(obj, list_widget, sessions))


def init_session_window(obj, list_widget, sessions):
    current_id = list_widget.currentRow()
    session_id = [i[1] for i in sessions][current_id]
    data = model.get_request('get_session_info', (session_id,))

    session_form = obj.init_session_window_ui(data)
    session_form.purchase_button.clicked.connect(lambda: init_purchase_window(session_form, session_id))


"""Generating seats template"""


def bind_generating_template_buttons_logic(window):
    window.add_row.clicked.connect(lambda: add_row(window))
    window.remove_row.clicked.connect(lambda: remove_row(window))
    window.add_column.clicked.connect(lambda: add_column(window))
    window.remove_column.clicked.connect(lambda: remove_column(window))

    window.save_button.clicked.connect(lambda: save_templates(window))

    for row in window.buttons:
        for button in row:
            button.clicked.connect(lambda: set_no_seat(window))


def add_row(window):
    row = list()
    for i in range(len(window.buttons[0])):
        new_button = window.init_button(i, len(window.buttons), '1')
        new_button.clicked.connect(lambda: set_no_seat(new_button))
        row.append(new_button)
    window.buttons.append(row)
    update_generated_window(window)


def remove_row(window):
    if len(window.buttons) > 1:
        for button in window.buttons[-1]:
            button.deleteLater()
        window.buttons.pop()
    update_generated_window(window)


def add_column(window):
    for i, row in enumerate(window.buttons):
        new_button = window.init_button(len(row), i, '1')
        new_button.clicked.connect(lambda: set_no_seat(new_button))
        row.append(new_button)
    update_generated_window(window)


def remove_column(window):
    if len(window.buttons[0]) > 1:
        for row in window.buttons:
            row[-1].deleteLater()
            row.pop()
    update_generated_window(window)


def set_no_seat(window):
    window.sender().setText('X')


def generate_template(button_list):
    template = ''
    for row in button_list:
        for button in row:
            if button.text() == '':
                template += '1'
            else:
                template += '0'
        template += 'n'
    return template[:-1]


def save_templates(window):
    reply = QtWidgets.QMessageBox.question(window, "Внимание", "Сохранить введённые данные?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)
    if reply == QtWidgets.QMessageBox.Yes:
        room_schemes.append(generate_template(window.buttons))
        window.close()


def update_generated_window(window):
    window.resize_window()


"""Adding new theater"""
room_schemes = list()


def try_to_save_theater(widget):
    name = widget.name_input.text()
    country = widget.country_box.currentText() if widget.country_box.currentText() != "Другое" \
        else widget.country_input.text()
    city = widget.city_box.currentText() if widget.city_box.currentText() != "Другое" \
        else widget.city_input.text()
    street = widget.street_box.currentText() if widget.street_box.currentText() != "Другое" \
        else widget.street_input.text()
    building = widget.building_input.text()

    try:
        model.approve_theater_record(name, country, city, street, building)
        if widget.check():
            model.add_theater(name, country, city, street, building, room_schemes)
            widget.close()
    except Exception as exception:
        widget.show_error_message(type(exception).__name__)


"""Buying tickets logic"""


def init_purchase_window(session_window, session_id):
    seat_schema_window = session_window.init_seat_schema_window()
    template = model.get_request('get_seat_schema', (session_id,))
    seat_schema_window.set_buttons_from_template(template)
    bind_seat_window_logic(seat_schema_window, session_id)


def bind_seat_window_logic(window, session_id):
    for row in window.buttons:
        for button in row:
            button.clicked.connect(lambda: change_button_state(window))
    window.save_button.clicked.connect(lambda: save_template(session_id, window))


def change_button_state(window):
    statuses = {"Free": "",
                "Purchased": "background-color:green",
                "Booked": "background-color:blue"}

    button = window.sender()

    status = button.objectName()
    status_names = list(statuses.keys())
    new_status_index = (status_names.index(status) + 1) % len(status_names)
    new_status = status_names[new_status_index]

    button.setObjectName(new_status)
    button.setStyleSheet(statuses[new_status])


def save_template(session_id, window):
    template = ''
    template_mapping = {
        'Hidden': '0',
        'Free': '1',
        'Booked': 'b',
        'Purchased': 'p'
    }
    for row in window.buttons:
        for button in row:
            template += template_mapping[button.objectName()]
        template += 'n'
    model.update_seats(session_id, template)
    window.close()
