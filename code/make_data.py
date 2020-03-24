#!/usr/bin/env python3
from argparse import ArgumentParser
import random as rand
from io import StringIO
import csv
import json
import sys
import logging

logger = logging.getLogger(__name__)

COLUMNS = list("abcd")
CATEGORIES = ["potato", "spade", "fence", "pipe", "donkey!"]
DTYPES = [
    lambda x: int(x*100),
    float,
    lambda x: int(x < 0.5),
    lambda x: CATEGORIES[int(x*len(CATEGORIES))],
]
DEFAULT_N = 100
rand.seed(2020)


def make_row():
    return {k: fn(rand.random()) for k, fn in zip(COLUMNS, DTYPES)}


def make_data(n):
    logger.info("Creating data with %s rows", n)
    data = [make_row() for _ in range(n)]
    return sorted(data, key=lambda r: [r[k] for k in COLUMNS])


def to_csv(data):
    logger.info("Converting data to CSV format")
    buf = StringIO()
    writer = csv.DictWriter(buf, COLUMNS)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
    buf.seek(0)
    return buf.read()


def main():
    parser = ArgumentParser(description="Make some fake data")
    parser.add_argument(
        "out", 
        help="'json' or 'csv' to print those formats to stdout; "
        "otherwise output path with one of those extensions"
    )
    parser.add_argument("-n", "--number", type=int, default=DEFAULT_N, help="Number of rows to generate")
    parsed = parser.parse_args()

    data = make_data(parsed.number)
    if parsed.out.endswith("csv"):
        s = to_csv(data)
    elif parsed.out.endswith("json"):
        s = json.dumps(data, indent=2, sort_keys=True)
    else:
        raise ValueError("Target must be JSON or CSV")

    if parsed.out in ["csv", "json"]:
        logger.info("Writing data to stdout")
        print(s)
    else:
        logger.info("Writing data to %s", parsed.out)
        with open(parsed.out, "w") as f:
            f.write(s)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

