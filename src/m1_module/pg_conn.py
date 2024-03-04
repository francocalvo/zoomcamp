"""
EngineCreator class and its subclasses.
"""
import argparse
import csv
import logging
from abc import abstractmethod
from io import StringIO

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
    def create_engine(self, args: argparse.Namespace) -> tuple[Engine, str]:
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

    def create_engine(self, args: argparse.Namespace) -> tuple[Engine, str]:
        """
        Create a PostgreSQL engine.
        """
        logger.info(
            [
                args.pg_user,
                args.pg_password,
                args.pg_host,
                args.pg_port,
                args.pg_db,
            ]
        )

        conn_str = f"postgresql://{args.pg_user}:{args.pg_password}@{args.pg_host}/{args.pg_db}"
        engine = create_engine(conn_str, use_insertmanyvalues=True)

        # check if the connection is successful
        try:
            with engine.connect():
                logger.info("Connection to PostgreSQL is successful")
        except Exception as e:
            logger.exception("Connection to PostgreSQL failed.")
            raise e  # noqa: TRY201

        return engine, conn_str


def psql_insert_copy(table, conn, keys, data_iter):  # mehod
    """
    Execute SQL statement inserting data.

    Parameters
    ----------
    table : pandas.io.sql.SQLTable
    conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys : list of str
        Column names
    data_iter : Iterable that iterates the values to be inserted

    """
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ", ".join(f'"{k}"' for k in keys)
        if table.schema:
            table_name = f"{table.schema}.{table.name}"
        else:
            table_name = table.name

        sql = f"COPY {table_name} ({columns}) FROM STDIN WITH CSV"
        cur.copy_expert(sql=sql, file=s_buf)
