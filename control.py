# Do all the logic here
from PyQt5 import QtWidgets

import model
import datetime

theaters = list()
tabs = list()
films = list()
theater_list = None
film_list = None


def check_delete():
    reply = QtWidgets.QMessageBox.question(theater_list, "Внимание", "Удалить выделенные данные?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)
    return reply == QtWidgets.QMessageBox.Yes


def init_theater_list(obj):
    global theater_list
    theater_list = obj

    fill_theater_list()
    bind_theater_list_logic(obj)


def fill_theater_list():
    global theaters
    theaters = model.get_request('get_all_theaters', ())
    theaters = sorted(theaters, key=lambda x: x[1:4])
    theater_list.update_theaters_list(theaters)


def bind_theater_list_logic(obj):
    obj.tableWidget_2.itemDoubleClicked.connect(lambda: open_theater_tab(obj, theaters))
    obj.new_theater_button.clicked.connect(lambda: init_new_theater(obj))
    obj.open_film_list_button.clicked.connect(lambda: init_film_list(obj))


def init_film_list(obj):
    global film_list
    film_list = obj.init_film_list()
    fill_film_table()
    film_list.new_film_button.clicked.connect(lambda: init_adding_film(film_list))


def fill_film_table():
    global films
    films = model.get_request('get_film_data', ())
    film_list.setup_table(films)


def open_theater_tab(obj, theaters):
    index = obj.tableWidget_2.currentRow()
    name, theater_id = theaters[index][0], theaters[index][5]
    tab = obj.init_theater_tab_ui(name, theater_id)
    tabs.append(tab)
    obj.tableWidget_2.selectionModel().clearSelection()

    update_sessions_data()

    sessions = model.get_request('get_sessions', (theater_id,))
    list_widget = tab.findChild(QtWidgets.QListWidget)
    list_widget.itemDoubleClicked.connect(lambda: init_session_window(obj, list_widget, sessions))
    obj.add_session_button.clicked.connect(lambda: init_session_add(obj, theater_id))


def update_sessions_data():
    for tab in tabs:
        theater_id = int(tab.objectName())
        sessions = model.get_request('get_sessions', (theater_id,))
        film_names = [item[0] for item in sessions]
        theater_list.fill_theater_data(tab, film_names)


def init_session_window(obj, list_widget, sessions):
    index = list_widget.currentRow()
    session_id = sessions[index][1]
    data = model.get_request('get_session_info', (session_id,))
    session_window = obj.init_session_window_ui(data)
    session_window.purchase_button.clicked.connect(
        lambda: init_purchase_window(session_window, session_id))
    session_window.edit_button.clicked.connect(lambda: init_session_edit(session_window, session_id))
    session_window.delete_button.clicked.connect(lambda: delete_session(session_window, session_id))


"""Generating seats template"""


def bind_generating_template_buttons_logic(window):
    window.add_row.clicked.connect(lambda: add_row(window))
    window.remove_row.clicked.connect(lambda: remove_row(window))
    window.add_column.clicked.connect(lambda: add_column(window))
    window.remove_column.clicked.connect(lambda: remove_column(window))

    window.save_button.clicked.connect(lambda: save_templates(window))

    for row in window.buttons:
        for button in row:
            button.clicked.connect(lambda: flick_state(window))


def add_row(window):
    row = list()
    for i in range(len(window.buttons[0])):
        new_button = window.init_button(i, len(window.buttons), '1')
        new_button.clicked.connect(lambda: flick_state(new_button))
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
        new_button.clicked.connect(lambda: flick_state(new_button))
        row.append(new_button)
    update_generated_window(window)


def remove_column(window):
    if len(window.buttons[0]) > 1:
        for row in window.buttons:
            row[-1].deleteLater()
            row.pop()
    update_generated_window(window)


def flick_state(window):
    if window.sender().text() == '':
        window.sender().setText('X')
    else:
        window.sender().setText('')


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


"""Adding and deleting theater"""
countries, cities, streets, = [None] * 3
room_schemes = list()


def init_new_theater(obj):
    new_theater_window = obj.open_new_theater_window()
    bind_new_theater_logic(new_theater_window)
    update_countries(new_theater_window)


def bind_new_theater_logic(obj):
    obj.country_box.currentTextChanged.connect(lambda: update_cities(obj))
    obj.city_box.currentTextChanged.connect(lambda: update_streets(obj))

    obj.country_box.currentTextChanged.connect(obj.toggle_line_edit)
    obj.city_box.currentTextChanged.connect(obj.toggle_line_edit)
    obj.street_box.currentTextChanged.connect(obj.toggle_line_edit)

    obj.add_room_button.clicked.connect(obj.init_new_room_window)
    obj.commit_button.clicked.connect(lambda: try_to_save_theater(obj))


def update_countries(obj):
    global countries
    countries = model.get_request('get_countries', ())
    names = [country[1] for country in countries]
    obj.update_country_list(names)

    update_cities(obj)


def update_cities(obj):
    global cities
    country_box = obj.country_box
    index = country_box.currentIndex()
    names = []
    try:
        country_id = countries[index][0]
        cities = model.get_request('get_cities', (country_id,))
        names = [city[1] for city in cities]
    except IndexError:
        cities = []
    obj.update_cities_list(names)

    update_streets(obj)


def update_streets(obj):
    global streets
    city_box = obj.city_box
    index = city_box.currentIndex()
    names = []
    try:
        city_id = cities[index][0]
        streets = model.get_request('get_streets', (city_id,))
        names = [street[1] for street in streets]
    except IndexError:
        streets = []
    obj.update_streets_list(names)


def try_to_save_theater(widget):
    global theaters
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
            theaters = model.get_request('get_all_theaters', ())
            fill_theater_list()
            widget.close()
    except Exception as exception:
        widget.show_error_message(type(exception).__name__)


def delete_theaters(indexes):
    if check_delete():
        for index in indexes:
            theater_id = theaters[index][5]
            model.delete_theater(theater_id)
    fill_theater_list()


"""Adding and deleting films"""


def init_adding_film(obj):
    new_film_window = obj.open_new_film_window()
    genres = model.get_request('get_genres', ())
    titles = [i[1] for i in genres]
    new_film_window.setup_genres_list(titles)
    new_film_window.save_button.clicked.connect(lambda: try_to_save_film(new_film_window, genres))


def delete_films(indexes):
    if check_delete():
        for index in indexes:
            film_id = films[index][0]
            model.delete_film(film_id)
    fill_film_table()


def try_to_save_film(window, genres):
    global films
    title = window.title_input.text()
    year = window.year_input.text()
    genre = genres[window.genre_input.currentIndex()][0]
    age_limit = window.age_limit_input.text()
    duration = window.time_input.time().toPyTime()
    description = window.description_input.toPlainText()

    try:
        model.approve_film_record(title, year, genre, age_limit, duration, description)
        if window.check():
            model.add_film(title, year, genre, age_limit, duration, description)
            fill_film_table()
            window.close()
    except Exception as exception:
        window.show_error_message(type(exception).__name__)


"""Editing, adding adn deleting sessions"""
session_edit_window = None
film_id, room_id, time, ticket_price = [None] * 4
film_name, room_number = '', 0


def init_session_add(obj, theaterId):
    global session_edit_window
    edit_window = obj.init_new_session_window_ui()
    session_edit_window = edit_window
    edit_window.film_choose.clicked.connect(lambda: get_new_film(edit_window))
    edit_window.room_choose.clicked.connect(lambda: get_room(edit_window, theaterId))
    edit_window.save_button.clicked.connect(try_to_save_new_session)


def init_session_edit(session_window, session_id):
    global session_edit_window
    edit_window = session_window.init_edit_window_ui()
    session_edit_window = edit_window
    edit_window.film_choose.clicked.connect(lambda: get_new_film(edit_window))
    edit_window.room_choose.clicked.connect(lambda: get_new_room(edit_window, session_id))
    edit_window.save_button.clicked.connect(lambda: try_to_save_session_data(session_window, session_id))


def get_new_film(window):
    choice_window = window.init_film_choice_window()
    film_list = model.get_request('get_film_data', ())
    table = choice_window.setup_table(film_list)

    table.itemDoubleClicked.connect(lambda: record_film_data(choice_window, table, film_list))


def record_film_data(window, table, film_list):
    global film_id, film_name
    film_id, film_name = film_list[table.currentRow()][:2]
    update_displayed_data()
    window.close()


def get_room(window, theater_id):
    choice_window = window.init_room_choice_window()
    room_list = model.get_request('get_rooms', (theater_id,))
    room_numbers = [room[1] for room in room_list]
    list_widget = choice_window.setup_list(room_numbers)
    list_widget.itemDoubleClicked.connect(lambda:
                                          open_room_scheme(choice_window, list_widget, room_list))
    choice_window.submit_button.clicked.connect(lambda: record_room_data(choice_window, list_widget, room_list))


def get_new_room(window, session_id):
    choice_window = window.init_room_choice_window()
    room_list = model.get_request('get_rooms_list', (session_id,))
    room_numbers = [room[1] for room in room_list]
    list_widget = choice_window.setup_list(room_numbers)
    list_widget.itemDoubleClicked.connect(lambda:
                                          open_room_scheme(choice_window, list_widget, room_list))
    choice_window.submit_button.clicked.connect(lambda: record_room_data(choice_window, list_widget, room_list))


def open_room_scheme(window, list_widget, room_list):
    index = list_widget.currentRow()
    template = room_list[index][-1]
    window.show_room(template)


def record_room_data(window, list_widget, room_list):
    global room_id, room_number
    room_id, room_number = room_list[list_widget.currentRow()][:2]
    update_displayed_data()
    window.close()


def update_displayed_data():
    session_edit_window.fill_data(film_name, room_number, 100, datetime.datetime.now())


def try_to_save_new_session():
    ticket_price = session_edit_window.price_input.text()
    try:
        model.approve_session_record(film_id, room_id, ticket_price,
                                     session_edit_window.time_input.dateTime().toPyDateTime())
        if session_edit_window.check():
            model.add_session(film_id, room_id,
                              session_edit_window.time_input.dateTime().toPyDateTime(), ticket_price, room_id)
            update_sessions_data()
            session_edit_window.close()
    except Exception as exception:
        session_edit_window.show_error_message(type(exception).__name__)


def try_to_save_session_data(session_window, session_id):
    ticket_price = session_edit_window.price_input.text()
    try:
        model.approve_session_record(film_id, room_id, ticket_price,
                                     session_edit_window.time_input.dateTime().toPyDateTime())
        if session_edit_window.check():
            model.update_session(session_id, film_id, room_id,
                                 session_edit_window.time_input.dateTime().toPyDateTime(), ticket_price)
            session_edit_window.close()
            update_sessions_data()
            session_window.close()
    except Exception as exception:
        session_edit_window.show_error_message(type(exception).__name__)


def delete_session(session_window, session_id):
    if check_delete():
        model.delete_session(session_id)
        session_window.close()
    update_sessions_data()


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
