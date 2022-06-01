import argparse
import os
import subprocess
from typing import Sequence
from typing import Union

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
 

def rename_files(path:str, symbol:str, dry_run:bool) -> None:
    count = 0

    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if SEARCH_CHAR in file:
                count += 1
                new_name = f'{dirpath}/{file.replace(SEARCH_CHAR, symbol)}'
                print(new_name)

                if not dry_run:
                    os.rename(f'{dirpath}/{file}', new_name)

        for directory in os.listdir(dirpath):
            if SEARCH_CHAR in directory and directory != ' ':
                count += 1
                new_name = f'{directory.replace(SEARCH_CHAR, symbol)}'
                print(new_name)

                if not dry_run:
                    subprocess.run(['mv', f'{directory}', f'{new_name}'])
                    breakpoint()

    if dry_run:
        print(f'Files to change: {count}')
    else:
        print(f'Files changed: {count}')

    return


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
        rename_files(path, args.rename, args.dry_run)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
