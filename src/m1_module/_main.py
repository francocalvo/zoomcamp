import logging
import urllib.request
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from time import time
from typing import Literal

import pandas as pd
from dateutil import rrule
from sqlalchemy import Engine

from m1_module.parser import create_parser
from m1_module.pg_conn import PostgresEngineCreator, psql_insert_copy

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def main() -> int | None:
    parser = create_parser()
    args: Namespace = parser.parse_args()

    if args.type == "postgres":
        engine: Engine
        conn_str: str
        engine, conn_str = PostgresEngineCreator().create_engine(args)
        logger.info("Connected to %s", engine)
        logger.info("Connected to %s", conn_str)
    else:
        msg = "Only postgres is supported"
        raise Exception(msg)  # noqa: TRY002

    logger.info("Target database is %s", engine)

    logger.info("Start timer")
    gt = time()
    first = True

    for period in rrule.rrule(
        rrule.MONTHLY,
        dtstart=datetime.fromisoformat(args.from_date),
        until=datetime.fromisoformat(args.until_date),
    ):
        logger.info("Start table timer")
        dt = time()
        logger.info("Downloading the CSV.GZ file for %s", period)

        url_period: str = args.url.format(
            year=period.year, month=str(period.month).zfill(2)
        )
        urllib.request.urlretrieve(url_period, "output.csv.gz")  # noqa: S310
        logger.info("Download complete")

        logger.info("Reading the CSV.GZ file")
        df_batch = pd.read_csv(
            "output.csv.gz", low_memory=False, encoding="unicode_escape"
        )

        mode: Literal["replace", "append"] = "replace" if first else "append"
        first = False
        logger.info("Writing to database")

        df_batch.to_sql(
            "fhv_tripdata",
            con=engine,
            schema="staging",
            index=False,
            if_exists=mode,
            method=psql_insert_copy,
        )

        logger.info("Deleting the CSV.GZ file")
        Path("output.csv.gz").unlink()
        logger.info("Time elapsed for period %s: %s", period, time() - dt)

    logger.info("Total time elapsed: %s", time() - gt)
    return 0
