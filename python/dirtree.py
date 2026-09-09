import argparse
import os
from collections.abc import Sequence

# A simple command that emulates GNU `tree` but only outputs the directories.
# Can be filtered on a specific sub-path or only traverse a given depth

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", action="store")
    parser.add_argument("--indent", "-i", action="store", default=2, type=int)
    parser.add_argument("--depth", action="store", default=2, type=int)
    parser.add_argument("--full", "-f", action="store_true")
    args = parser.parse_args(argv)

    indent_char: str = '|'
    blacklist: list[str] = [
        ".git",
        "__pycache__",
        "venv",
    ]

    starting_path: set[str] = set(args.path.split(os.sep))
    for root, dirs, files in os.walk(args.path):
        path = root.split(os.sep)
        if len(path) > 1 and path[1][0] == ".":
            continue

        depth: int = len(starting_path.difference(set(path)))
        if depth > args.depth:
            continue

        if any([x in blacklist for x in path]):
            continue

        indentation = len(path) - 1
        spaces = " " * (args.indent - 1)
        print(f"{indent_char}{spaces}" * indentation, end="")
        print(path[-1] if not args.full else "/".join(path))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

