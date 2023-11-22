# main.py
import os
import pydgraph
import model

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)

def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)

def close_client_stub(client_stub):
    client_stub.close()

def print_menu():
    mm_options = {
        1: "Create Schema",
        2: "Create Data",
        3: "Visualize Data",
        4: "Suggest Good Travel Days",
        5: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def main():
    # Init Client Stub and Dgraph Client
    client_stub = create_client_stub()
    client = create_client(client_stub)

    while True:
        print_menu()
        option = input('Enter your choice: ')
        if option == '1':
            model.set_schema(client)
            print("Schema created successfully.")
        elif option == '2':
            model.create_data(client)
            print("Dara created successfully.")
        elif option == '3':
            model.visualize_data(client)
        elif option == '4':
            suggested_days = model.suggest_good_travel_days(client)
            print("Suggested Good Travel Days:")
            for day in suggested_days:
                print(day)
        elif option =='5':
            close_client_stub(client_stub)
            exit(0)      

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {}'.format(e))
    finally:
        close_client_stub(create_client_stub())
