
import os
import logging
import lzma
import platform
import argparse
from .config import config, HERE
from .add import Add, ADD_COMPLETER
from .set import Set, SET_COMPLETER
from .show import Show, SHOW_COMPLETER
from .identify import Identify
from .crack import Crack, CRACK_COMPLETER
from .help import Help
from .version import version
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion, NestedCompleter

def parse_args():
    parser = argparse.ArgumentParser(description="Wrapper to help with cracking hashes.")

    parser.add_argument('hashfile', nargs='?', default=None,
            help="File containing hashes to crack.")

    args = parser.parse_args()

    if args.hashfile is not None:
        Set("set hashfile " + args.hashfile)

def main():
    parse_args()
    print(BANNER)
    setup()
    
    prompt = [
            ('class:hashcrack', 'hashcrack'),
            ('class:white', ' > ')
    ]

    session = PromptSession(prompt, style=STYLE, completer=COMPLETER, complete_while_typing=True)

    while True:

        try:
            out = session.prompt().strip()
        except EOFError:
            return
        except KeyboardInterrupt:
            continue

        if out == "":
            continue

        try:
            MENU[out.split(" ")[0]](out)
        except KeyError:
            print("Invalid option.")

def setup():
    rockyou_path = os.path.join(HERE, "static", "wordlists", "rockyou.txt.xz")

    if os.path.exists(rockyou_path):

        print("Performing initial setup ... ", end='', flush=True)

        rockyou_decomp_path = os.path.join(HERE, "static", "wordlists", "rockyou.txt")
        
        with lzma.open(rockyou_path) as rockyou:
            with open(rockyou_decomp_path, "wb") as f:
                f.write(rockyou.read())

        os.unlink(rockyou_path)

        print("[ DONE ]", flush=True)

def do_exit(*args):
    exit(0)

logging.basicConfig(
        level=logging.WARN,
        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M'
)


# Assume Windows can't handle better colors
if platform.uname().system == "Windows":

    STYLE = Style.from_dict({
        # User input (default text).
        '':          'ansibrightblue',

        # Prompt.
        'hashcrack':  'ansibrightmagenta',
        'white':   'ansiwhite',
    })

else:

    STYLE = Style.from_dict({
        # User input (default text).
        '':          '#8e89cb',

        # Prompt.
        'hashcrack':  '#89a3cb',
        'white':   '#ffffff',
    })

MENU = {
        "add": Add,
        "crack": Crack,
        "exit": do_exit,
        "help": Help,
        "set": Set,
        "show": Show,
        "identify": Identify,
}

COMPLETER = NestedCompleter({
    'add': ADD_COMPLETER,
    'crack': CRACK_COMPLETER,
    'exit': None,
    'help': None,
    'identify': None,
    'set': SET_COMPLETER,
    'show': SHOW_COMPLETER,
})

BANNER = r"""   ▄█    █▄       ▄████████    ▄████████    ▄█    █▄     ▄████████    ▄████████    ▄████████  ▄████████    ▄█   ▄█▄ 
  ███    ███     ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███ ▄███▀ 
  ███    ███     ███    ███   ███    █▀    ███    ███   ███    █▀    ███    ███   ███    ███ ███    █▀    ███▐██▀   
 ▄███▄▄▄▄███▄▄   ███    ███   ███         ▄███▄▄▄▄███▄▄ ███         ▄███▄▄▄▄██▀   ███    ███ ███         ▄█████▀    
▀▀███▀▀▀▀███▀  ▀███████████ ▀███████████ ▀▀███▀▀▀▀███▀  ███        ▀▀███▀▀▀▀▀   ▀███████████ ███        ▀▀█████▄    
  ███    ███     ███    ███          ███   ███    ███   ███    █▄  ▀███████████   ███    ███ ███    █▄    ███▐██▄   
  ███    ███     ███    ███    ▄█    ███   ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███ ▀███▄ 
  ███    █▀      ███    █▀   ▄████████▀    ███    █▀    ████████▀    ███    ███   ███    █▀  ████████▀    ███   ▀█▀ 
                                                                     ███    ███                           ▀         
Version {version} (https://github.com/bannsec/hashcrack)
Powered by: Hashcat (hashcat.net)
""".format(version=version)

if __name__ == "__main__":
    main()
