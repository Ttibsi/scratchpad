#!/usr/bin/env python3

import os

def main() -> int:
    with open("a.out", "w") as f:
        for file in os.listdir():
            if file == "a.out":
                continue

            if os.path.isfile(file):
                print(f"Adding {file}...")
                file_obj = open(file)
                lines = file_obj.readlines()
                file_obj.close()

                f.write(f"\n=== {file} ===\n")
                for line in lines:
                    if line.isspace():
                        continue
                    f.write(line)
                    
    print("Complete")

if __name__ == "__main__":
    raise SystemExit(main())
