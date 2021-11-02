# Do all the logic here
import model


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


def init_theater_tab(obj):
    name = obj.tableWidget_2.selectedItems()[0].text()
    obj.init_theater_tab_ui(name)
    tab = obj.tabWidget.widget(obj.tabWidget.currentIndex())

    sessions = model.get_request('get_sessions', (model.get_request('get_theater_id', (name,)),))
    film_names = [i[0] for i in sessions]
    obj.fill_theater_data(tab, film_names,
                          ["Имя", "Жанр", "Возрастное ограничение", "Цена билета", "Время сеанса"])


def init_session_window(obj, list_widget, sessions):
    current_id = list_widget.currentRow()
    session_id = [i[1] for i in sessions][current_id]
    data = model.get_request('get_session_info', (session_id,))
    print(data)
    obj.init_session_window_ui(data)
