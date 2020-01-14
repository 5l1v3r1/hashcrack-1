
from prompt_toolkit.completion import WordCompleter
from .config import config

def Show(command):
    command = command[4:].strip()
    command = command.split(" ")

    if command[0] == "wordlist":
        print(config["wordlist"])

    elif command[0] == "hashes":
        print(config["hashes"])

    elif command[0] == "hashtype":
        print(config["hash_type"])


SHOW_COMPLETER = WordCompleter(['wordlist', 'hashes', 'hashtype'])