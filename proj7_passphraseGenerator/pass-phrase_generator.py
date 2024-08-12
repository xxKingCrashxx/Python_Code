import argparse, random, sys
# ideal use: python pass-phrase_generator.py --length [num] --sep [string].
# python pass-phrase_generator.py --help - returns flags.
FILE_PATH = "nouns/nouns_db.txt"
def main():
    parser = argparse.ArgumentParser(
                        prog="pass-phrase_generator",
                        description="generates a random passphrase given nouns in a txt file.")

    parser.add_argument('--length',
                        type=int,
                        default=5,
                        help="number of random nouns in the pass-phrase")

    parser.add_argument('--sep',
                        type=str,
                        default='-',
                        help="character that will be seperating the nouns")

    parser.add_argument('--filepath',
                        default=FILE_PATH,
                        help="filepath to custom nouns txt file"
                        )

    arguments = parser.parse_args();
    nouns = read_file(arguments.filepath)

    if len(nouns) == 0:
        sys.exit(0);
    print(generate_pass_phrase(nouns,
                               arguments.length, arguments.sep))

def read_file(file_path):
    nouns_list = [];
    try:
        with open(file_path, "r") as file:
            nouns_list = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("file does not exist.")
    return nouns_list

def generate_pass_phrase(nouns, length, seperator):
    random.shuffle(nouns)
    pass_phrase = random.choice(nouns)

    for i in range(1, length):
        pass_phrase = pass_phrase + seperator + random.choice(nouns)
    return pass_phrase

if __name__ == "__main__":
    main()


