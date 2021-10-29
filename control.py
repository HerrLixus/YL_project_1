# Do all the logic here

def init_logic(obj):
    obj.country_box.currentTextChanged.connect(obj.update_cities_list)
    obj.city_box.currentTextChanged.connect(obj.update_streets_list)
    obj.tableWidget_2.itemDoubleClicked.connect(obj.init_theater_tab)
