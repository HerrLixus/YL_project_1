import sqlite3

connection = sqlite3.connect('cinema.db')
cursor = connection.cursor()


def get_countries():
    request = """select country from theaters"""
    countries = [i[0] for i in cursor.execute(request).fetchall()]

    return countries


def get_cities(country):
    request = """select city from theaters where country = ?"""
    cities = [i[0] for i in cursor.execute(request, (country,)).fetchall()]

    return cities


def get_streets(city):
    request = """select street from theaters where city = ?"""
    streets = [i[0] for i in cursor.execute(request, (city,)).fetchall()]

    return streets


def get_theaters(country, city, street):
    request = """select name, country, city, street from theaters
     where country = ?
     and city = ?
     and street = ?"""
    theaters = cursor.execute(request, (country, city, street)).fetchall()
    return theaters
