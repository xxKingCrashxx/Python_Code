import os
import platform


def create_menue(options):
    print(f"\nOptions:");
    for index, option in enumerate(options):
        print(f"\t{index + 1}: {option}");

    usr_input = get_user_input("choice: ", valid_type="int");
    
    return usr_input - 1 #converting the option back to 0 based indexing

def clear_terminal():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def get_user_input(prompt, valid_type="string"):
    match valid_type:
        case "string":
            response = str(input(prompt));
            return response;

        case "int":

            while True:
                try:
                    response = int(input(prompt))
                    return response;
                except ValueError:
                    print("invalid input, please retype your response.");
        case "float":

            while True:
                try:
                    response = float(input(prompt));
                    return response;
                except ValueError:
                    print("invalid input, please retype your response.")
        case "boolean":
            while True:
                try:
                    response = input(prompt)
                    if response.lower() == 'y':
                        return True
                    elif response.lower() == 'n':
                        return False
                    else:
                        raise ValueError()
                except ValueError:
                    print("invalid input, please retype your response")
        case _:
            print("feature not implemented")

def dict_to_table(list_object: list[dict]):
    list_size = len(list_object)
    headers = []
    rows = []

    if list_size >= 1:
        headers = list(list_object[0].keys())
    
    for obj in list_object:
        row = [str(obj.get(key, "")) for key in headers]
        rows.append(row)

    return (headers, rows)


def create_query(query_object, response_list):
    for query in query_object["questions_list"]:

        response_type = query["response_type"]
        prompt = query["prompt"]
        validator = query.get("validator") 
        user_response = get_user_input(prompt + ": ", valid_type=response_type)

        if validator is not None:
            while not validator(user_response):
                user_response = get_user_input(prompt + ": ", valid_type=response_type)
        response_list.append(user_response)


def create_table(table_title, headers, rows):
    def format_row(row):
        return "".join(f"{item:<{column_lengths[index]}} | " for index, item in enumerate(row)) + "\n"

    print(table_title + "\n")
    column_lengths = [len(header) for header in headers]

    for row in rows:
        for index, item in enumerate(row):
            column_lengths[index] = max(column_lengths[index], len(item))

    table_str = format_row(headers)
    table_str += "-" * (sum(column_lengths) + len(headers) * 3) + "\n"

    for row in rows:
        table_str += format_row(row)

    print(table_str)
    
