#!/usr/bin/env python3
import argparse
import logging
import os
import requests
from collections import Counter

# Configuración del logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)  # Cambiado a DEBUG para obtener más información detallada
handler = logging.FileHandler('flights.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Lectura de variables de entorno relacionadas con la conexión a la API
FLIGHTS_API_URL = os.getenv("FLIGHTS_API_URL", "http://localhost:8000")


def print_flight_details(flights_data):
    for flight_info in flights_data:
        for key, value in flight_info.items():
            print(f"{key.capitalize()}: {value}")
        print("=" * 50)

def suggest_advertising_months(flights_data):
    # Inicializa un diccionario para almacenar meses por aerolínea
    airline_months = {}

    # Itera sobre los datos de vuelos
    for flight_info in flights_data:
        airline = flight_info.get("airline")
        month = flight_info.get("month")

        if airline and month:
            # Si la aerolínea no está en el diccionario, agrégala con una lista vacía
            if airline not in airline_months:
                airline_months[airline] = []

            # Agrega el mes a la lista de meses para esa aerolínea
            airline_months[airline].append(month)

    # Encuentra el mes más común para cada aerolínea
    most_common_months = {}
    for airline, months in airline_months.items():
        counter = Counter(months)
        most_common_month, count = counter.most_common(1)[0]
        most_common_months[airline] = {"month": most_common_month, "count": count}

    # Encuentra la aerolínea con el mes más común
    max_airline, max_month_info = max(most_common_months.items(), key=lambda x: x[1]["count"])

    # Imprime el resultado
    print(f"The most common advertising month is {max_month_info['month']} for {max_airline} with {max_month_info['count']} occurrences.")

def search_flights():
    # Función para buscar y mostrar la lista de vuelos según la opción y elección del usuario
    option = input("Statistics for airline or airport (airline/airport): ")
    option_chosen = input("Write the specific airline/airport: ")

    # Endpoint específico para búsqueda de vuelos
    suffix = "/flight"
    endpoint = f"{FLIGHTS_API_URL}{suffix}"

    # Parámetros de la consulta
    params = {
        "option": option,
        "option_chosen": option_chosen,
    }

    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        if not json_resp:
            print("No flights found.")
        else:
            print_flight_details(json_resp)
            suggest_advertising_months(json_resp)
    else:
        log.error(f"Error: {response.status_code}")
        log.error(response.text)



def main():
    log.info(f"Welcome to flight catalog. App requests to: {FLIGHTS_API_URL}")

    parser = argparse.ArgumentParser()

    # Definición de acciones permitidas
    list_of_actions = ["search", "get", "update", "delete"]
    parser.add_argument("action", choices=list_of_actions, help="Action for the flight catalog")

    # Argumentos adicionales según la acción
    parser.add_argument("-i", "--id", help="Provide a flight ID for the flight action", default=None)
    parser.add_argument("-r", "--rating", help="Search parameter for flights with average rating equal or above the param (0 to 5)", default=0)
    parser.add_argument("-p", "--num_pages", help="Search parameter for flights with num_pages equal or above the param", default=0)
    parser.add_argument("-rc", "--ratings_count", help="Search parameter for flights with ratings_count equal or above the param", default=0)
    parser.add_argument("-l", "--language", help="Search parameter for flights with a specific author", default=None)

    args = parser.parse_args()

    if args.id and args.action not in ["get", "update", "delete"]:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)

    if args.rating and args.action != "search":
        log.error(f"Rating arg can only be used with search action")
        exit(1)

    if args.action == "search":
        search_flights()




if __name__ == "__main__":
    main()