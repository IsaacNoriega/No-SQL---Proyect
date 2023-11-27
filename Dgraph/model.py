# model.py

import pydgraph
import json
import datetime

def set_schema(client):
    schema = """
        airline: string .
        from: string .
        to: string .
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
        txn = client.txn()
        try:
            mutation = pydgraph.Mutation(commit_now=True)
            response = txn.mutate(set_obj=data)

            txn.mutate(mutation)

            print(f"Data created for flight passengers.")
        finally:
            txn.discard()

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
