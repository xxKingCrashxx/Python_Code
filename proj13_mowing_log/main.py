from utils import get_user_input, create_query, create_menue, clear_terminal, create_table, dict_to_table
import db_functions

def create_client():
    
    print("===Create Client===\n")
    query = {
        'questions_list': [
            {
                'prompt': "Name of the Client",
                'response_type': "string",
                'validator': None,
            },
        ]
    }

    response = []
    create_query(query, response)

    client_name = response[0]
    results = db_functions.create_client(client_name)

    if results:
        print(f"[Mowing Log] client {client_name} was created")
    else:
        print(f"[Mowing Log] client with that name already exists")


def view_clients():
    print("===Client List===\n")
    clients_list = db_functions.get_all_clients()

    (headers, rows) = dict_to_table(clients_list)
    create_table("Client List", headers, rows)
    

def view_client_mowing_log():
    print("===Client Mowing Log History===\n")
    query = {
        'questions_list': [
            {
                'prompt': "Name of the Client",
                'response_type': "string",
                'validator': None,
            },
        ]
    }

    response = []
    create_query(query, response)

    client_name = response[0]
    mowing_log_list = db_functions.get_client_mowing_logs(client_name)
    (headers, rows) = dict_to_table(mowing_log_list)

    create_table("Client Mowing Log History", headers, rows)
    

def create_new_mowing_log():
    print("===Create Mowing Log===\n")

    query = {
        'questions_list': [
            {
                'prompt': "Name of the Client",
                'response_type': "string",
                'validator': None,
            },
            {
                'prompt': "payment due",
                'response_type': "float",
                'validator': None,
            },
            {
                'prompt': "Date Mowed format=('YYYY-MM-DD') or leave blank for todays date",
                'response_type': "string",
                'validator': None,
            },
            {
                'prompt': "Did the client pay? (y/n)",
                'response_type': "boolean",
                'validator': None,
            }
        ]
    }

    response = []
    create_query(query, response)

    db_functions.create_mowing_log(
        client_name=response[0],
        amount_due=response[1],
        mowing_date=None if response[2] == "" else response[2],
        paid=response[3]
    )
    

def update_client_mowing_log():
    pass

def main():
    running = True
    while running:
        
        print("\n===Mowing Manager===")
        user_option = create_menue(
            [
                "Create Client",
                "View Clients",
                "View Client Mowing Log",
                "Update Client Mowing Log",
                "Create New Mowing Log",
                "Exit Program"
            ]
        )
        match user_option:
            case 0:
                create_client()
            case 1:
                view_clients()
            case 2:
                view_client_mowing_log()
            case 3:
                update_client_mowing_log()
            case 4:
                create_new_mowing_log()
            case 5:
                running = False
            case _:
                print("[Mowing Log] Not a valid option.")
    print("[Mowing Log] Exiting Program")

if __name__ == "__main__":
    main()