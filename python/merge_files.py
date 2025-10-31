#!/usr/bin/env python3

import argparse
import os

def collect_files(exclude: str | None) -> list[str]:
    return [
        entry
        for entry in os.listdir()
        if os.path.isfile(entry)
        and entry != "a.out"
        and (exclude is None or exclude not in entry)
    ]


def write_to_file(files: list[str]):
    with open("a.out", "w") as f:
        for file in files:
            print(f"Adding {file}...")
            f.write(f"=== {file} ===\n")

            with open(file) as g:
                lines = g.readlines()

            for line in lines:
                if line.isspace():
                    continue
                f.write(line)

            f.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', help='Only list selected files')
    parser.add_argument('--exclude', help='String to exclude from all file names. Can be partial')
    args = parser.parse_args()

    files = collect_files(args.exclude)

    if not args.list:
        write_to_file(files)

    print("Complete")


if __name__ == "__main__":
    raise SystemExit(main())
