import logging
import urllib.request
from argparse import ArgumentParser
from time import time

import polars as pl
from pyarrow.csv import CSVStreamingReader, ReadOptions, open_csv
from sqlalchemy import Engine

from m1_module.pg_conn import PostgresEngineCreator

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def main() -> int | None:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--type", type=str, default="postgres")
    parser.add_argument(
        "--url",
        type=str,
        default="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz",
        help="URL to file csv.gz",
    )
    args = parser.parse_known_args()

    logger.info("Downloading the CSV.GZ file")
    urllib.request.urlretrieve(args[0].url, "output.csv.gz")
    logger.info("Download complete")

    if args[0].type == "postgres":
        engine: Engine
        conn_str: str
        engine, conn_str = PostgresEngineCreator().create_engine(parser)
        logger.info("Connected to %s", engine)
        logger.info("Connected to %s", conn_str)
    else:
        msg = "Only postgres is supported"
        raise Exception(msg)

    logger.info("Target database is %s", engine)

    logger.info("Reading csv from pyarrow")
    ops: ReadOptions = ReadOptions(block_size=100000)  # type: ignore
    arrow_table: CSVStreamingReader = open_csv(  # type: ignore
        "output.csv.gz",
        read_options=ops,
    )

    logger.info("Start timer")
    dt = time()
    logger.info("Writing to database")
    first = True
    c = 0
    for batch in arrow_table:  # type: ignore
        logger.info("Counter: %i", c)
        c += 1
        df_batch: pl.DataFrame = pl.from_arrow(batch)  # type: ignore
        mode = "replace" if first else "append"
        df_batch.write_database(
            "taxi_data", conn_str, if_table_exists=mode, engine="sqlalchemy"
        )

    logger.info("End timer")
    logger.info("Time elapsed: %s", {time() - dt})
