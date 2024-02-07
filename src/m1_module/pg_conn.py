import argparse
import logging
import os
from abc import abstractmethod

from sqlalchemy import Engine, create_engine

logger = logging.getLogger()



class EngineCreator:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_engine(self, parser: argparse.ArgumentParser) -> tuple[Engine, str]:
        """Create a SQLAlchemy engine."""


class PostgresEngineCreator(EngineCreator):
    def __init__(self) -> None:
        super().__init__()

    def create_engine(self, parser: argparse.ArgumentParser) -> tuple[Engine, str]:
        # Read env variables with default values
        logger.info("Reading environmental variables")
        pg_user: str = os.getenv("PG_USER", "postgres")
        pg_password: str = os.getenv("PG_PASSWORD", "postgres")
        pg_host: str = os.getenv("PG_HOST", "172.17.0.1")
        pg_port: str = os.getenv("PG_PORT", "5432")
        pg_db = os.getenv("PG_DB", "postgres")

        logger.info([pg_user, pg_password, pg_host, pg_db])

        # Overwrite env variables with command line arguments
        parser.add_argument("--pg_user", type=str, default=pg_user)
        parser.add_argument("--pg_password", type=str, default=pg_password)
        parser.add_argument("--pg_host", type=str, default=pg_host)
        parser.add_argument("--pg_port", type=str, default=pg_port)
        parser.add_argument("--pg_db", type=str, default=pg_db)

        args = parser.parse_known_args()

        conn_str = f"postgresql://{args[0].pg_user}:{args[0].pg_password}@{args[0].pg_host}/{args[0].pg_db}"
        return (create_engine(conn_str), conn_str)
