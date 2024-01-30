import polars as pl
import sys


def main() -> int | None:
    # Read the first argument from the command line
    try:
        date = sys.argv[1]
    except IndexError:
        print(f"No date specified")
        return 0

    print(f"Data to process for day: {date}")
    data = pl.DataFrame({"a": [1, 2, 3], "b": [1, 2, 3]})
    print(data)
