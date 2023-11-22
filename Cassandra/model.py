#!/usr/bin/env python3
import logging
from collections import defaultdict  # Agrega esta línea
from tabulate import tabulate
from colorama import init, Fore, Style
init()
import statistics
import collections
import options

# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_PRINCIPAL_TABLE = '''
CREATE TABLE IF NOT EXISTS airport_wait_time (
  airline text,
  de text,
  hacia text,
  day int,
  month int,
  year int,
  age int,
  gender text,
  reason text,
  stay text,
  transit text,
  connection text,
  wait int,
  PRIMARY KEY ((airline, month,de, hacia, year, day), age, gender, reason, stay, transit, connection)
) WITH CLUSTERING ORDER BY (age DESC, gender DESC, reason DESC, stay DESC, transit DESC, connection DESC);
'''
CREATE_INDEXES = '''
    CREATE INDEX IF NOT EXISTS airport_wait_time_wait_idx ON airport_wait_time (wait);
    '''

CREATE_INDEXES2 = '''
    CREATE INDEX IF NOT EXISTS year_index ON airport_wait_time (year);
    '''

MAIN_QUERY = '''
    SELECT airline, month
    FROM airport_wait_time
    WHERE year = ? AND airline = ?
    ALLOW FILTERING;
'''



QUANTITY_ALL = '''
    SELECT COUNT(*) AS total_count FROM airport_wait_time;
    '''

SELECT_ALL = '''
SELECT * FROM airport_wait_time;
'''



SELECT_BY_AIRLINE = '''
    SELECT * FROM airport_wait_time WHERE airline = ? ALLOW FILTERING;
    '''

SELECT_BY_AIRLINE_WAIT = '''
    SELECT * FROM airport_wait_time WHERE airline = ? AND wait = ? ALLOW FILTERING;
    '''

SELECT_BY_WAIT_LESS_0 = '''
    SELECT * FROM airport_wait_time WHERE wait <= ? ALLOW FILTERING;
    '''
SELECT_BY_WAIT_MORE_0 = '''
    SELECT * FROM airport_wait_time WHERE wait >= ? ALLOW FILTERING;
    '''

SELECT_BY_MONTH_YEAR = '''
    SELECT * FROM airport_wait_time WHERE month = ? AND year = ? ALLOW FILTERING;
    '''

SELECT_BY_FROM_TO = '''
    SELECT * FROM airport_wait_time WHERE de = ? AND hacia = ?  ALLOW FILTERING;
    '''

SELECT_BY_FROM_TO_WAIT = '''
    SELECT * FROM airport_wait_time WHERE de = ? AND hacia = ? AND wait = ? ALLOW FILTERING;
    '''

SELECT_BY_STAY_CONNECTION = '''
    SELECT * FROM airport_wait_time WHERE stay = ? AND connection = ? ALLOW FILTERING;
    '''


SELECT_BY_AIRLINE_FROM = '''
    SELECT * FROM airport_wait_time WHERE airline = ? AND de = ? ALLOW FILTERING;
    '''

SELECT_BY_TRANSIT_WAIT = '''
    SELECT * FROM airport_wait_time WHERE transit = ? AND wait >= ? ALLOW FILTERING;
    '''

SELECT_BY_FROM_TO_MONTH = '''
    SELECT * FROM airport_wait_time WHERE de = ? AND hacia = ? AND month = ? ALLOW FILTERING;   
    '''

SELECT_RECOMMENDED_AIRPORTS = '''
    SELECT * FROM airport_details WHERE airport_code IN ?;
'''
def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_PRINCIPAL_TABLE)
    session.execute(CREATE_INDEXES)


def select_all(session):
    log.info("Retrieving all airport wait times")
    stmt = session.prepare(SELECT_ALL)
    rows = session.execute(stmt)
    print(f"=== All airport flight")
    print("\n")

    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_airline(session, airline):
    log.info(f"Retrieving airport wait times for airline {airline}")
    stmt = session.prepare(SELECT_BY_AIRLINE)
    rows = session.execute(stmt, [airline])
    print(f"=== Airport wait times for airline {airline}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_airline_wait(session, airline, wait_time):
    log.info(f"Retrieving airport wait times for airline {airline} and wait time {wait_time}")
    stmt = session.prepare(SELECT_BY_AIRLINE_WAIT)
    rows = session.execute(stmt, [airline, wait_time])
    print(f"=== Airport wait times for airline {airline} and wait time {wait_time}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_wait_less_0(session, wait_time):
    log.info(f"Retrieving airport wait times with wait time less than or equal to {wait_time}")
    stmt = session.prepare(SELECT_BY_WAIT_LESS_0)
    rows = session.execute(stmt, [wait_time])
    print(f"=== Airport wait times with wait time less than or equal to {wait_time}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_wait_more_0(session, wait_time):
    log.info(f"Retrieving airport wait times with wait time greater than or equal to {wait_time}")
    stmt = session.prepare(SELECT_BY_WAIT_MORE_0)
    rows = session.execute(stmt, [wait_time])
    print(f"=== Airport wait times with wait time greater than or equal to {wait_time}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_month_year(session, month, year):
    log.info(f"Retrieving airport wait times for month {month} and year {year}")
    stmt = session.prepare(SELECT_BY_MONTH_YEAR)
    rows = session.execute(stmt, [month, year])
    print(f"=== Airport wait times for month {month} and year {year}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_from_to(session, origin, destination):
    log.info(f"Retrieving airport wait times for origin {origin} and destination {destination}")
    stmt = session.prepare(SELECT_BY_FROM_TO)
    rows = session.execute(stmt, [origin, destination])
    print(f"=== Airport wait times for origin {origin} and destination {destination}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_from_to_wait(session, origin, destination, wait_time):
    log.info(f"Retrieving airport wait times for origin {origin}, destination {destination} and wait time {wait_time}")
    stmt = session.prepare(SELECT_BY_FROM_TO_WAIT)
    rows = session.execute(stmt, [origin, destination, wait_time])
    print(f"=== Airport wait times for origin {origin}, destination {destination} and wait time {wait_time}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_stay_connection(session, stay, connection):
    log.info(f"Retrieving airport wait times for stay {stay} and connection {connection}")
    stmt = session.prepare(SELECT_BY_STAY_CONNECTION)
    rows = session.execute(stmt, [stay, connection])
    print(f"=== Airport wait times for stay {stay} and connection {connection}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_airline_from(session, airline, origin):
    log.info(f"Retrieving airport wait times for airline {airline} and origin {origin}")
    stmt = session.prepare(SELECT_BY_AIRLINE_FROM)
    rows = session.execute(stmt, [airline, origin])
    print(f"=== Airport wait times for airline {airline} and origin {origin}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_transit_wait(session, transit, wait_time):
    log.info(f"Retrieving airport wait times for transit {transit} and wait time greater than {wait_time}")
    stmt = session.prepare(SELECT_BY_TRANSIT_WAIT)
    rows = session.execute(stmt, [transit, wait_time])
    print(f"=== Airport wait times for transit {transit} and wait time greater than {wait_time}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def select_by_from_to_month(session, origin, destination, month):
    log.info(f"Retrieving airport wait time for flights from {origin} to {destination} in {month}")
    stmt = session.prepare(SELECT_BY_FROM_TO_MONTH)
    rows = session.execute(stmt, [origin, destination, month])
    print(f"=== Airport wait time for flights from {origin} to {destination} in {month}")
    print("\n")
    data = []
    for row in rows:
        airline = f"{Style.BRIGHT}{Fore.GREEN}{row.airline}{Style.RESET_ALL}"
        day = f"{Style.BRIGHT}{Fore.BLUE}{row.day}{Style.RESET_ALL}"
        month = f"{Style.BRIGHT}{Fore.BLUE}{row.month}{Style.RESET_ALL}"
        year = f"{Style.BRIGHT}{Fore.BLUE}{row.year}{Style.RESET_ALL}"
        wait = f"{Style.BRIGHT}{Fore.RED}{row.wait}{Style.RESET_ALL}"

        data.append([airline, row.de, row.hacia, day, month, year, row.age, row.reason, wait])

    headers = ["Airline", "From", "To", "Day", "Month", "Year", "Age", "Reason", "Wait"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))


##Modelo que recomiende en que aeropuertos es recomendable abrir servicios de alimentos/bebidas. 


def recomendar_aeropuertos_para_servicios(session):
    log.info("Generating airport recommendations for food/beverage services")

    # Obtener la cantidad total de vuelos
    total_flights_stmt = session.prepare(QUANTITY_ALL)
    total_flights = session.execute(total_flights_stmt).one().total_count

    # Obtener todos los datos de la tabla
    select_all_stmt = session.prepare("SELECT de, wait FROM airport_wait_time")
    all_data = session.execute(select_all_stmt)

    # Organizar datos por aeropuerto
    airport_data = defaultdict(list)
    for row in all_data:
        airport_data[row.de].append(row.wait)

    # Calcular la frecuencia y el tiempo de espera promedio por aeropuerto
    recommendations = []
    for aeropuerto, wait_times in airport_data.items():
        if aeropuerto is not None and wait_times:
            frecuencia = len(wait_times) / total_flights
            tiempo_espera_promedio = sum(wait_times) / len(wait_times)

            # Puntuación de recomendación: cuanto mayor sea la frecuencia y menor el tiempo de espera, mejor
            puntuacion = frecuencia * (1 / tiempo_espera_promedio)

            recommendations.append({"Aeropuerto": aeropuerto, "Puntuacion": puntuacion})

    # Ordenar por la puntuación de recomendación de mayor a menor
    recommendations = sorted(recommendations, key=lambda x: x["Puntuacion"], reverse=True)

    # Imprimir las recomendaciones como porcentajes relativos
    print("\nAirport Recommendations for Food/Beverage Services:")
    max_score = recommendations[0]["Puntuacion"]  # Obtener la mejor puntuación
    for recommendation in recommendations:
        airport = recommendation["Aeropuerto"]
        score_percentage = (recommendation["Puntuacion"] / max_score) * 100
        print(f"{airport} is {score_percentage:.2f}% recommended")

