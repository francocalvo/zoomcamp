"""
Create a parser for the module
"""

import os
from argparse import ArgumentParser


def create_parser() -> ArgumentParser:
    """
    Create a parser for the module.
    """

    parser: ArgumentParser = ArgumentParser()

    # Basic command lines
    parser.add_argument("--type", type=str, default="postgres")
    parser.add_argument(
        "--url",
        type=str,
        default="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_{year}-{month}.csv.gz",
        help="URL to file csv.gz",
    )

    parser.add_argument(
        "--from_date",
        type=str,
        default="2019-01-01",
        help="From which month",
    )

    parser.add_argument(
        "--until_date",
        type=str,
        default="2021-07-01",
        help="Until which month",
    )


    # Specific for Postgres
    # Read env variables with default values
    pg_user: str = os.getenv("PG_USER", "postgres")
    pg_password: str = os.getenv("PG_PASSWORD", "postgres")
    pg_host: str = os.getenv("PG_HOST", "localhost")
    pg_port: str = os.getenv("PG_PORT", "5432")
    pg_db = os.getenv("PG_DB", "postgres")

    # Overwrite env variables with command line arguments
    parser.add_argument("--pg_user", type=str, default=pg_user)
    parser.add_argument("--pg_password", type=str, default=pg_password)
    parser.add_argument("--pg_host", type=str, default=pg_host)
    parser.add_argument("--pg_port", type=str, default=pg_port)
    parser.add_argument("--pg_db", type=str, default=pg_db)

    return parser
