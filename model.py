import sqlite3

connection = sqlite3.connect('cinema.db')
cursor = connection.cursor()


def get_countries():
    request = """select name from countries
     where id in (select country from theaters)"""
    countries = [i[0] for i in cursor.execute(request).fetchall()]

    return countries


def get_cities(country):
    request = """select name from cities where countryId =
     (select id from countries where name = ?)"""
    cities = [i[0] for i in cursor.execute(request, (country,)).fetchall()]

    return cities


def get_streets(city):
    request = """select name from streets where cityId = 
    (select id from cities where name = ?)"""
    streets = [i[0] for i in cursor.execute(request, (city,)).fetchall()]

    return streets


def get_theaters(country, city, street):
    request = """select
theaters.name,
countries.name as country,
cities.name as city,
streets.name as street,
theaters.building
from theaters
left join countries on countries.id = theaters.country
left join cities on cities.id = theaters.city
left join streets on streets.id = theaters.street
where
country = (select id from countries where name = ?) and
city = (select id from cities where name = ?) and
street = (select id from streets where name = ?)"""
    theaters = cursor.execute(request, (country, city, street)).fetchall()
    return theaters


def get_theater_id(name):
    request = """select id from theaters where name  = ?"""
    id = cursor.execute(request, (name,)).fetchone()[0]
    return id


def get_sessions(theater):
    request = \
        """select title from films
           where id in
           (select filmId from sessions
           where roomId in
           (select id from rooms
           where theaterId = ?))"""
    film_names = [i[0] for i in cursor.execute(request, (theater,)).fetchall()]
    return film_names

