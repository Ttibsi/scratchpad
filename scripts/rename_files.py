from __future__ import annotations
import argparse
import os
import subprocess
from typing import Sequence
from typing import Union

# USAGE
# python3 rename_files.py path/to/root/dir
# For some reason this won't work properly in 3.8 but does in 3.10

# Character to search for in file names
SEARCH_CHAR = ' '

def validate_path(path_str:str) -> str:
    if os.path.exists(os.path.expanduser(path_str)):
        return path_str
    else:
        raise RuntimeError('Invalid filepath')


def search_dir(file_path) -> list[str]:
    files_with_spaces:list[str] = []

    for dirpath, dirnames, filenames in os.walk(file_path):
        for file in filenames:
            if SEARCH_CHAR in file or SEARCH_CHAR in dirpath:
                files_with_spaces.append(f'{dirpath}/{file}')

    return files_with_spaces


def print_list(file_list:list[str]) -> None:
    for item in file_list:
        print(item)
 

def rename_files(path:str, symbol:str, dry_run:bool) -> int:
    count = 0

    os.chdir(path)

    for entry in os.listdir(path):
        if SEARCH_CHAR in entry:
            count += 1
            new_name = f'{entry.replace(SEARCH_CHAR, symbol)}'
            print(os.path.abspath(new_name))

            if not dry_run:
                os.rename(entry, new_name)

                if os.path.isdir(os.path.join(path, new_name)):
                    count += rename_files(os.path.join(path, new_name), symbol, dry_run)

        if os.path.isdir(os.path.join(path, entry)):
            count += rename_files(os.path.join(path, entry), symbol, dry_run)

    return count


def main(argv: Union[Sequence[str], None] = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', action='store')
    parser.add_argument('-f', '--find', action='store_true')
    parser.add_argument('-c', '--count', action='store_true')
    parser.add_argument('-r', '--rename', action='store')
    parser.add_argument('-d', '--dry_run', action='store_true')


    args = parser.parse_args(argv)
    path = validate_path(args.file_path)
    files_to_check = []

    if args.find:
        files_to_check = search_dir(path)
        print_list(files_to_check)
    if args.count:
        if not files_to_check:
            files_to_check = search_dir(path)

        print(f'\nFiles found: {len(files_to_check)}')
    if args.rename:
        count = rename_files(path, args.rename, args.dry_run)

        if args.dry_run:
            print(f'Files to change: {count}')
        else:
            print(f'Files changed: {count}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
