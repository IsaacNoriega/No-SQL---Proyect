# model.py

import pydgraph
import json
import datetime

def set_schema(client):
    schema = """
        airline: string .
        from: uid @reverse .
        to: uid @reverse .
        day: int .
        month: int .
        year: int .
        age: int .
        gender: string .
        reason: string .
        stay: string .
        transit: string .
        connection: bool .
        wait: int .

        airport.code: string @index(hash) .
        airport.name: string @index(hash) .
    """

    return client.alter(pydgraph.Operation(schema=schema))

def create_data(client):
    with open('data/flight_passengers.json', 'r') as json_file:
        data = json.load(json_file)
        mutation = pydgraph.Mutation(commit_now=True)

        for record in data:
            from_airport_code = record.get("from")
            to_airport_code = record.get("to")

            # Crear aeropuertos si no existen
            mutation.set_json({
                "uid": "_:from_airport",
                "airport.code": from_airport_code,
                "airport.name": "Unknown Airport",
            })

            mutation.set_json({
                "uid": "_:to_airport",
                "airport.code": to_airport_code,
                "airport.name": "Unknown Airport",
            })

            # Crear el pasajero con referencias a los aeropuertos
            mutation.set_json(record)
            mutation.set_json({
                "uid": "_:from_airport",
                "from": {"uid": "_:from_airport"}
            })
            mutation.set_json({
                "uid": "_:to_airport",
                "to": {"uid": "_:to_airport"}
            })

        # Realizar la mutación
        client.txn().mutate(mutation)
        print("Data created for flight passengers.")

def visualize_data(client):
    query = """
        {
            passengers(func: has(airline)) {
                uid
                airline
                from {
                    uid
                    airport.code
                    airport.name
                }
                to {
                    uid
                    airport.code
                    airport.name
                }
                day
                month
                year
                age
                gender
                reason
                stay
                transit
                connection
                wait
            }
        }
    """

    res = client.txn().query(query)
    data = json.loads(res.json)
    print(json.dumps(data, indent=2))



def suggest_good_travel_days(client):
    query = """
    {
      suggestGoodTravelDays(func: has(airline)) @filter(eq(connection, false) AND ge(wait, 0) AND le(wait, 60)) {
        day
        month
        year
        from
      }
    }
    """

    response = client.txn().query(query)
    data = json.loads(response.json)

    # Verifica si la respuesta está en bytes y conviértela a JSON si es necesario
    if isinstance(data, bytes):
        data = data.decode("utf-8")
        data = json.loads(data)

    suggested_days = []
    for day_info in data.get("suggestGoodTravelDays", [])[:5]:  # Limita a los 5 mejores
        day = day_info.get("day")
        month = day_info.get("month")
        year = day_info.get("year")
        from_airport = day_info.get("from", "Unknown Airport")

        suggested_date = datetime.date(year, month, day)
        suggested_days.append({"Date": suggested_date, "from": from_airport})

    return suggested_days
