"""
EngineCreator class and its subclasses.
"""
import argparse
import logging
import os
from abc import abstractmethod

from sqlalchemy import Engine, create_engine

logger = logging.getLogger()


class EngineCreator:
    """
    Abstract class for creating a SQLAlchemy engine.
    """

    def __init__(self) -> None:
        """
        Create EngineCreator class.
        """

    @abstractmethod
    def create_engine(self, parser: argparse.ArgumentParser) -> tuple[Engine, str]:
        """Create a SQLAlchemy engine."""


class PostgresEngineCreator(EngineCreator):
    """
    Create a PostgreSQL engine.
    """

    def __init__(self) -> None:
        """
        Create PostgresEngineCreator class.
        """
        super().__init__()

    def create_engine(self, parser: argparse.ArgumentParser) -> tuple[Engine, str]:
        """
        Create a PostgreSQL engine.
        """
        # Read env variables with default values
        logger.info("Reading environmental variables")
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

        args = parser.parse_known_args()

        logger.info(
            [
                args[0].pg_user,
                args[0].pg_password,
                args[0].pg_host,
                args[0].pg_port,
                args[0].pg_db,
            ]
        )

        conn_str = f"postgresql://{args[0].pg_user}:{args[0].pg_password}@{args[0].pg_host}/{args[0].pg_db}"
        engine = create_engine(conn_str), conn_str

        # check if the connection is successful
        try:
            with engine[0].connect():
                logger.info("Connection to PostgreSQL is successful")
        except Exception as e:
            logger.exception("Connection to PostgreSQL failed.")
            raise e  # noqa: TRY201

        return engine
