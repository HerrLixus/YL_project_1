# Do all the logic here

from PyQt5.QtWidgets import QListWidget
import model


def init_logic(obj):
    obj.country_box.currentTextChanged.connect(obj.update_cities_list)
    obj.city_box.currentTextChanged.connect(obj.update_streets_list)
    obj.tableWidget_2.itemDoubleClicked.connect(lambda: init_theater_tab(obj))


def init_theater_tab(obj):
    name = obj.tableWidget_2.selectedItems()[0].text()
    obj.init_theater_tab_ui(name)
    tab = obj.tabWidget.widget(obj.tabWidget.currentIndex())

    list_widget = tab.findChild(QListWidget)
    sessions = model.get_request('get_sessions', (model.get_request('get_theater_id', (name,)),))
    film_names = [i[0] for i in sessions]
    obj.update_sessions_list(list_widget, film_names)
    list_widget.itemDoubleClicked.connect(
        lambda: init_session_window(obj, list_widget, sessions))


def init_session_window(obj, list_widget, sessions):
    film_names = [i[0] for i in sessions]
    current_item = list_widget.currentItem().text()
    session_id = [i[1] for i in sessions][film_names.index(current_item)]
    obj.init_session_window_ui(model.get_request('get_session_info', (session_id,)))
