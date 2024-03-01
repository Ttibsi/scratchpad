import argparse
from enum import Enum

# A simple approach at lexical analysis as a syntax highlighting engine
# This needs to be improved to have a "basic" collection of keywords and
# types that applies to all C-style languages (if, for, while etc) to
# decrease the amount of work needed to include a new language

# This may also need to use regex anyway, for example for strings
# or integer/float literals, or finding function calls. 

class Lang(Enum):
    CPP = 0
    PYTHON = 0

lang_strings = {
        "cpp" : Lang.CPP,
        "py" : Lang.PYTHON,

        }

class Token(Enum):
    KEYWORD = 1
    TYPE=2


token_map = {
        Lang.CPP: {
            "int": Token.TYPE,
            "std::string": Token.TYPE,
            "enum": Token.KEYWORD,
            "class": Token.KEYWORD,
            "struct": Token.KEYWORD,
            "return": Token.KEYWORD,
            },
        Lang.PYTHON: {
            "False": Token.KEYWORD,
            "await": Token.KEYWORD,
            "else": Token.KEYWORD,
            "import": Token.KEYWORD,
            "pass": Token.KEYWORD,
            "None": Token.KEYWORD,
            "break": Token.KEYWORD,
            "except": Token.KEYWORD,
            "in": Token.KEYWORD,
            "raise": Token.KEYWORD,
            "True": Token.KEYWORD,
            "class": Token.KEYWORD,
            "finally": Token.KEYWORD,
            "is": Token.KEYWORD,
            "return": Token.KEYWORD,
            "and": Token.KEYWORD,
            "continue": Token.KEYWORD,
            "for": Token.KEYWORD,
            "lambda": Token.KEYWORD,
            "try": Token.KEYWORD,
            "as": Token.KEYWORD,
            "def": Token.KEYWORD,
            "from": Token.KEYWORD,
            "nonlocal": Token.KEYWORD,
            "while": Token.KEYWORD,
            "assert": Token.KEYWORD,
            "del": Token.KEYWORD,
            "global": Token.KEYWORD,
            "not": Token.KEYWORD,
            "with": Token.KEYWORD,
            "async": Token.KEYWORD,
            "elif": Token.KEYWORD,
            "if": Token.KEYWORD,
            "or": Token.KEYWORD,
            "yield": Token.KEYWORD,
            "string": Token.TYPE,
            "int": Token.TYPE,
            "float": Token.TYPE,
            "bool": Token.TYPE,
            "list": Token.TYPE,
            "dict": Token.TYPE,
            "tuple": Token.TYPE,
            "set": Token.TYPE,
            "bytes": Token.TYPE,
            "frozenset": Token.TYPE,
            "None": Token.TYPE,
            }
        }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    # check file language
    file_ext = args.file.split(".")[-1]
    try:
        lang = lang_strings[file_ext]
    except KeyError:
        print(f"Language not defined: {file_ext}")
        return

    # reead file to string
    with open(args.file) as f:
        txt = f.read()

    buf = ""
    for c in txt:
        if c.isspace() or not c.isalpha():
            if buf in token_map[lang].keys():
                buf += c
                print(f"\x1b[33m{buf}\x1b[0m", end="")
            else:
                buf += c
                print(buf, end="")

            buf = ""
        else:
            buf += c



if __name__ == "__main__":
    raise SystemExit(main())
