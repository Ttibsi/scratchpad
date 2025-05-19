#!/usr/bin/env python3
import os
import shutil


def main() -> int:
    for root, dirs, _ in os.walk(os.getcwd()):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Deleting: {pycache_path}")
            shutil.rmtree(pycache_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

