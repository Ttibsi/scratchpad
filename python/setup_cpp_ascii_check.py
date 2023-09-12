import argparse
from collections.abc import Sequence
from typing import Union

def out(num: int, start: int) -> None:
    out = "\t"
    for i in range(start, num):
        out += """\n} """
        out += r"""else if (substrings[0] == "\\x%(id)s") {
    k.code = '%(ch)s';""" % {
                "id": hex(i), "ch": (chr(i) if i >= 31 else ' '
                )}

    return out


def to_file(s: str) -> None:
    with open("a.out", "w") as f:
        f.write(s.strip().lstrip())


def main(argv: Union[Sequence[str], None] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument( "-c", "--count", action="store")
    parser.add_argument( "-s", "--start", action="store")
    parser.add_argument( "-f", "--file", action="store_true")
    args: argparse.Namespace = parser.parse_args(argv)

    if args.file:
        count = int(args.count) if args.count else 128
        start = int(args.start) if args.start else 1
        to_file(out(count, start))
    else:
        count = int(args.count) if args.count else 128
        start = int(args.start) if args.start else 1
        print(out(count, start))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

