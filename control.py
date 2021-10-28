# Do all the logic here

def init_logic(obj):
    obj.country_box.currentTextChanged.connect(obj.update_cities_list)
    obj.city_box.currentTextChanged.connect(obj.update_streets_list)
