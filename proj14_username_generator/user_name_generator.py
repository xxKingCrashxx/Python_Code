import random


def get_random_adjective() -> str:
    result = None
    with open("./adjectives.txt") as fs:
        
        for i, word in enumerate(fs, start=1):
            if random.randint(1, i) == 1:
                result = word.strip()
    return result

def get_random_noun():
    result = None
    with open("./nouns.txt") as fs:
        for i, word in enumerate(fs, start=1):
            if random.randint(1, i) == 1:
                result = word.strip()
    return result

def get_random_number(start: int, end: int) -> int:
    return random.randint(start, end)

def build_username(num_of_unames_to_generate=1) -> str | list[str]:
    generated_usernames = []
    if num_of_unames_to_generate == 1:
        return f"{get_random_adjective()}_{get_random_noun()}_{get_random_number(1, 999)}"
    for i in range(num_of_unames_to_generate):
        random_adjective = get_random_adjective()
        random_noun = get_random_noun()
        random_num = get_random_number(1, 999)

        generated_usernames.append(f"{random_adjective}_{random_noun}_{random_num}")
    return generated_usernames


def main():
    try:
        gen_unames_count = int(input("How many usernames do you wish to generate?: "))
        user_names = build_username(gen_unames_count)

        for name in user_names:
            print(name)
    except:
        print("Invalid input, please provide a number")
        exit(-1)

if __name__ == "__main__":
    main()