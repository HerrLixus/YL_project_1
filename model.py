import sqlite3
import datetime


class UnfilledFields(Exception):
    pass


class NonNumericBuildingNumber(Exception):
    pass


class DuplicateAddress(Exception):
    pass


class DuplicateName(Exception):
    pass


class IntersectingSessions(Exception):
    pass


class InvalidFilmId(Exception):
    pass


class InvalidRoomId(Exception):
    pass


class NonNumericPrice(Exception):
    pass


class ZeroTime(Exception):
    pass


class InvalidGenre(Exception):
    pass


class NonNumericAgeLimit(Exception):
    pass


class NonNumericYear(Exception):
    pass


class InvalidYear(Exception):
    pass


class DuplicateFilm(Exception):
    pass


def connect():
    connection = sqlite3.connect('cinema.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


connection = connect()
cursor = connection.cursor()
# 1: fetchone, 2: fetchone[0], 3: fetchall, 4: fetchall[0]
requests = {
    'get_countries': ("""select * from countries
     where id in (select country from theaters)""", 3),

    'get_cities': ("""select id, name from cities where countryId = ?""", 3),

    'get_streets': ("""select id, name from streets where cityId = ?""", 3),

    'get_country_id': ("""select id from countries where name = ?""", 2),

    'get_city_id': ("""select id from cities where name = ?""", 2),

    'get_street_id': ("""select id from streets where name = ?""", 2),

    'get_genres': ("""select * from genres""", 3),

    'get_all_theaters': ("""select
                        theaters.name,
                        countries.name as country,
                        cities.name as city,
                        streets.name as street,
                        theaters.building,
                        theaters.id
                        from theaters
                        left join countries on countries.id = theaters.country
                        left join cities on cities.id = theaters.city
                        left join streets on streets.id = theaters.street""", 3),

    'get_all_theater_names': ("""select name from theaters""", 4),

    'get_theaters': ("""select
                        theaters.name,
                        countries.name as country,
                        cities.name as city,
                        streets.name as street,
                        theaters.building,
                        theaters.id
                        from theaters
                        left join countries on countries.id = theaters.country
                        left join cities on cities.id = theaters.city
                        left join streets on streets.id = theaters.street
                        where
                        country = ? and
                        city = ? and
                        street = ?""", 3),

    'get_theater_id': ("""select id from theaters where name  = ?""", 2),

    'get_sessions': ("""select
                        films.title as film,
                        sessions.id
                        from sessions
                        left join films on sessions.filmId = films.id
                        where roomId in (select id from rooms where theaterId = ?)""", 3),

    'get_session_info': ("""select
                            films.title as film,
                            `genres`.title as genre,
                            films.age_limit,
                            films.description as description,
                            ticket_price,
                            time
                            from sessions
                            left join films on films.id = sessions.filmId
                            left join genres on genres.id = films.genre
                            where sessions.id = ?""", 1),

    'get_seat_schema': ("""select seat_schema from sessions where id = ?""", 2),

    'get_film_data': ("""select
                        films.id,
                        films.title,
                        films.year,
                        genres.title as genre,
                        films.age_limit,
                        films.duration,
                        films.description
                        from films
                        left join genres on films.genre = genres.id""", 3),

    'get_film': ("""select
                        films.id,
                        films.title,
                        films.year,
                        genres.title as genre,
                        films.age_limit,
                        films.duration,
                        films.description
                        from films
                        left join genres on films.genre = genres.id
                        where films.id = ?""", 1),

    'get_films': ("""select title, year, genre, age_limit, duration, description from films""", 3),

    'get_rooms_list': ("""select * from rooms where theaterId =
(select theaterId from rooms where id = (select roomId from sessions where id = ?))""", 3),

    'get_rooms': ("""select * from rooms where theaterId = ?""", 3),

    'get_all_film_durations': ("""select
films.id as id,
sessions.time,
films.duration as duration
from sessions
left join films on sessions.filmId = films.id
where sessions.roomId = ?""", 3),

    'get_film_ids': ("""select id from films""", 4),

    'get_room_ids': ("""select id from rooms""", 4)
}


def get_request(request, args):
    sql_request, data_type = requests[request]
    raw_data = cursor.execute(sql_request, args)
    result = ''
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
        pass
    return result


"""add new data"""


def add_country(name):
    request = \
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


def add_room(number, theater_id, seat_scheme):
    request = """insert into rooms(number, theaterId, seat_schema)
                 values (?, ?, ?)"""
    cursor.execute(request, (number, theater_id, seat_scheme))
    connection.commit()


def add_theater(name, country, city, street, building, room_schemes):
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
    for i, scheme in enumerate(room_schemes):
        add_room(i + 1, get_request('get_theater_id', (name,)), scheme)


def add_session(*args):
    request = """insert into sessions(filmId, roomId, time, ticket_price, seat_schema)
values (?, ?, ?, ?, (select seat_schema from rooms where id = ?))"""
    cursor.execute(request, args)
    connection.commit()


def add_film(*args):
    name, year, genre, age_limit, time, description = args
    year = int(year)
    if age_limit.endswith('+'):
        age_limit = int(age_limit[:-1])
    else:
        age_limit = int(age_limit)
    duration = datetime.datetime.combine(datetime.datetime(2000, 1, 1), time)

    request = """insert into films(title, year, genre, age_limit, duration, description)
values (?, ?, ?, ?, ?, ?)"""
    cursor.execute(request, (name, year, genre, age_limit, duration, description))
    connection.commit()


"""change existing data"""


def update_session(session_id, *args):
    request = """update sessions
set filmId = ?,
roomId = ?,
time = ?,
ticket_price = ?,
seat_schema = (select seat_schema from rooms where id = roomId)
where id = ?"""
    cursor.execute(request, (*args, session_id))
    connection.commit()


def update_seats(session_id, template):
    request = """update sessions
                 set seat_schema = ?
                 where id = ?"""
    cursor.execute(request, (template, session_id))
    connection.commit()


"""delete existing records"""


def delete_theater(theater_id):
    request = """delete from theaters where id = ?"""
    cursor.execute(request, (theater_id,))
    connection.commit()


def delete_film(film_id):
    request = """delete from films where id = ?"""
    cursor.execute(request, (film_id,))
    connection.commit()


def delete_session(session_id):
    request = """delete from sessions where id = ?"""
    cursor.execute(request, (session_id,))
    connection.commit()


"""check if all the given data is correct"""


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


def approve_session_record(*args):
    film_id, room_id, ticket_price = args[:3]
    time = args[3]

    if film_id not in get_request('get_film_ids', ()):
        raise InvalidFilmId
    if room_id not in get_request('get_room_ids', ()):
        raise InvalidRoomId
    if not ticket_price.isdigit():
        raise NonNumericPrice

    film_duration = get_request('get_film', (film_id,))[5].time()
    new_film_start = time
    new_film_duration_delta = datetime.timedelta(hours=film_duration.hour,
                                                 minutes=film_duration.minute, seconds=film_duration.second)
    new_film_end = new_film_start + new_film_duration_delta
    for film in get_request('get_all_film_durations', (room_id,)):
        if film[0] == film_id:
            continue
        film_start = film[1]
        duration = film[2].time()
        duration_delta = datetime.timedelta(hours=duration.hour,
                                            minutes=duration.minute, seconds=duration.second)
        film_end = film_start + duration_delta
        if new_film_start > film_end > new_film_end or\
            new_film_start > film_start > new_film_end or\
                (new_film_start > film_start and film_end > new_film_end):
            raise IntersectingSessions


def approve_film_record(name, year, genre, age_limit, time, description):
    if any([i == '' for i in [name, year, age_limit, description]]):
        raise UnfilledFields
    if time == datetime.time(0, 0):
        raise ZeroTime
    if not year.isdigit():
        raise NonNumericYear
    if not 0 < int(year) < datetime.datetime.now().year:
        raise InvalidYear
    if genre not in [i[0] for i in get_request('get_genres', ())]:
        raise InvalidGenre
    if age_limit.endswith('+'):
        if not age_limit[:-1].isdigit():
            raise NonNumericAgeLimit
    else:
        if not age_limit.isdigit():
            raise NonNumericAgeLimit
