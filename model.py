import sqlite3

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
    if data_type == 1:
        result = raw_data.fetchone()
    elif data_type == 2:
        result = raw_data.fetchone()[0]
    elif data_type == 3:
        result = raw_data.fetchall()
    elif data_type == 4:
        result = [i[0] for i in raw_data]

    return result
