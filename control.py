# Do all the logic here
from PyQt5 import QtWidgets
import model

"""Binding functions to buttons etc"""


def bind_main_logic(obj):
    obj.country_box.currentTextChanged.connect(obj.update_cities_list)
    obj.city_box.currentTextChanged.connect(obj.update_streets_list)
    obj.tableWidget_2.itemDoubleClicked.connect(lambda: init_theater_tab(obj))
    obj.new_theater_button.clicked.connect(obj.open_new_theater_window)


def bind_new_theater_logic(obj):
    obj.country_box.currentTextChanged.connect(obj.update_cities_list)
    obj.country_box.currentTextChanged.connect(obj.toggle_line_edit)

    obj.city_box.currentTextChanged.connect(obj.update_streets_list)
    obj.city_box.currentTextChanged.connect(obj.toggle_line_edit)

    obj.street_box.currentTextChanged.connect(obj.toggle_line_edit)

    obj.commit_button.clicked.connect(lambda: try_to_save_theater(obj))


def try_to_save_theater(widget):
    name = widget.name_input.text()
    country = widget.country_box.currentText() if widget.country_box.currentText() != "Другое"\
        else widget.country_input.text()
    city = widget.city_box.currentText() if widget.city_box.currentText() != "Другое" \
        else widget.city_input.text()
    street = widget.street_box.currentText() if widget.street_box.currentText() != "Другое" \
        else widget.street_input.text()
    building = widget.building_input.text()

    try:
        model.approve_theater_record(name, country, city, street, building)
        if widget.check():
            model.add_theater(name, country, city, street, building)
            widget.close()
    except Exception as exception:
        widget.show_error_message(type(exception).__name__)


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
    session_form.purchase_button.clicked.connect(lambda: session_form.init_seat_schema_window(session_id))


"""Buying tickets logic"""


def bind_seat_window_logic(window):
    for button in window.buttons:
        button.clicked.connect(lambda: change_button_state(window))


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


"""Generating seats template"""


def bind_generating_template_buttons_logic(window):
    window.add_row.clicked.connect(lambda: add_row(window))
    window.remove_row.clicked.connect(lambda: remove_row(window))
    window.add_column.clicked.connect(lambda: add_column(window))
    window.remove_column.clicked.connect(lambda: remove_column(window))


def add_row(window):
    window.buttons.append([window.init_button(i, len(window.buttons), '1')
                           for i in range(len(window.buttons[0]))])
    update_generated_window(window)


def remove_row(window):
    for button in window.buttons[-1]:
        button.deleteLater()
    window.buttons.pop()
    update_generated_window(window)


def add_column(window):
    for i, row in enumerate(window.buttons):
        row.append(window.init_button(len(row), i, '1'))
    update_generated_window(window)


def remove_column(window):
    for row in window.buttons:
        row[-1].deleteLater()
        row.pop()
    update_generated_window(window)


def generate_template(window):
    template = ''
    for row in window.buttons:
        for button in row:
            if button.text == '':
                template += '1'
            else:
                template += '0'
        template += 'n'
    return template


def update_generated_window(window):
    window.resize_window()
    print(generate_template(window))
