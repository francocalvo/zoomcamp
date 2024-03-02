import logging
import urllib.request
from argparse import ArgumentParser
from time import time
from typing import Literal

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
    urllib.request.urlretrieve(args[0].url, "output.csv.gz")  # noqa: S310
    logger.info("Download complete")

    if args[0].type == "postgres":
        engine: Engine
        conn_str: str
        engine, conn_str = PostgresEngineCreator().create_engine(parser)
        logger.info("Connected to %s", engine)
        logger.info("Connected to %s", conn_str)
    else:
        msg = "Only postgres is supported"
        raise Exception(msg)  # noqa: TRY002

    logger.info("Target database is %s", engine)

    logger.info("Reading csv from pyarrow")
    ops: ReadOptions = ReadOptions(block_size=1000000)
    arrow_table: CSVStreamingReader = open_csv(
        "output.csv.gz",
        read_options=ops,
    )

    logger.info("Start timer")
    dt = time()
    logger.info("Writing to database")
    first = True
    for i, batch in enumerate(arrow_table):
        logger.info("Counter: %i. Time elapsed: %f", i, (time() - dt))
        df_batch: pl.DataFrame | pl.Series = pl.from_arrow(batch)
        mode: Literal["replace", "append"] = "replace" if first else "append"

        if type(df_batch) == pl.DataFrame:
            df_batch.write_database(
                "taxi_data", conn_str, if_table_exists=mode, engine="sqlalchemy"
            )

    logger.info("End timer")
    logger.info("Time elapsed: %s", time() - dt)

    return 0
