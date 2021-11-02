import sqlite3


class UnfilledFields(Exception):
    pass


class NonNumericBuildingNumber(Exception):
    pass


class DuplicateAddress(Exception):
    pass


class DuplicateName(Exception):
    pass


connection = sqlite3.connect('cinema.db')
cursor = connection.cursor()


# 1: fetchone, 2: fetchone[0], 3: fetchall, 4: fetchall[0]
requests = {
    'get_countries': ("""select name from countries
     where id in (select country from theaters)""", 4),

    'get_cities': ("""select name from cities where countryId =
     (select id from countries where name = ?)""", 4),

    'get_streets': ("""select name from streets where cityId = 
    (select id from cities where name = ?)""", 4),

    'get_country_id': ("""select id from countries where name = ?""", 2),

    'get_city_id': ("""select id from cities where name = ?""", 2),

    'get_street_id': ("""select id from streets where name = ?""", 2),

    'get_all_theaters': ("""select
                        theaters.name,
                        countries.name as country,
                        cities.name as city,
                        streets.name as street,
                        theaters.building
                        from theaters
                        left join countries on countries.id = theaters.country
                        left join cities on cities.id = theaters.city
                        left join streets on streets.id = theaters.street""", 3),

    'get_theaters': ("""select
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
                        street = (select id from streets where name = ?)""", 3),

    'get_theater_id': ("""select id from theaters where name  = ?""", 2),

    'get_sessions': ("""select
                        films.title as film,
                        sessions.id
                        from sessions
                        left join films on sessions.filmId = films.id
                        where roomId in (select id from rooms where theaterId = ?)""", 3),

    'get_session_info': ("""select
                            films.title as film,
                            genres.title as genre,
                            films.age_limit,
                            films.description as description,
                            ticket_price,
                            time
                            from sessions
                            left join films on films.id = sessions.filmId
                            left join genres on genres.id = films.genre
                            where sessions.id = ?""", 1)
}


def get_request(request, args):
    sql_request, data_type = requests[request]
    raw_data = cursor.execute(sql_request, args)
    try:
        if data_type == 1:
            result = raw_data.fetchone()
        elif data_type == 2:
            result = raw_data.fetchone()[0]
        elif data_type == 3:
            result = raw_data.fetchall()
        elif data_type == 4:
            result = [i[0] for i in raw_data]
    except:
        result = ''
    return result


def add_country(name):
    request =\
            """insert into countries(name)
               values (?)"""
    cursor.execute(request, (name,))
    connection.commit()


def add_city(name, country):
    request = """insert into cities(name, countryId)
                 values (?, ?)"""
    cursor.execute(request, (name, country))
    connection.commit()


def add_street(name, city):
    request = """insert into streets(name, cityId)
                     values (?, ?)"""
    cursor.execute(request, (name, city))
    connection.commit()


def add_theater(name, country, city, street, building):
    request = """insert into theaters(name, country, city, street, building)
values (?, ?, ?, ?, ?)"""
    country_id = get_request('get_country_id', (country,))
    city_id = get_request('get_city_id', (city,))
    street_id = get_request('get_street_id', (street,))
    if not country_id:
        add_country(country)
        country_id = get_request('get_country_id', (country,))
    if not city_id:
        add_city(city, country_id)
        city_id = get_request('get_city_id', (city,))
    if not street_id:
        add_street(street, city_id)
        street_id = get_request('get_street_id', (street,))
    cursor.execute(request, (name, country_id, city_id, street_id, int(building)))
    connection.commit()


def approve_theater_record(*args):
    if any([i == '' for i in args]):
        raise UnfilledFields
    if not args[-1].isdigit():
        raise NonNumericBuildingNumber
    address = (*args[1:-1], int(args[-1]))
    if any([theater[1:] == address for theater in get_request('get_all_theaters', ())]):
        raise DuplicateAddress
    if any([theater[:3] == args[:3] for theater in get_request('get_all_theaters', ())]):
        raise DuplicateName
    return True
