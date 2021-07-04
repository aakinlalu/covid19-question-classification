import datetime
from dataclasses import dataclass
from typing import Optional, Tuple, Union

import pandas as pd
import psycopg2
from psycopg2 import OperationalError
from eliot import start_action

from configs.configs import POSTGRES_HOST, POSTGRES_NAME, POSTGRES_PORT
from loggings.logger import __LOGGER__

__LOGGER__


def create_connection(
    db_name: str,
    db_host: str,
    db_port: int,
    db_user: str = None,
    db_password: str = None,
) -> Union[psycopg2.extensions.connection, None]:
    """Postgres connector to establish connection with database

    Args:
        db_name (str): database name
        db_host (str): database host
        db_port (int): database port
        db_user (str): username access the database
        db_password (str): password to the database

    Returns:
        Union: connection session or None
    """
    with start_action(action_type="create_connection"):
        connection = None
        try:
            if db_user is None:
                connection = psycopg2.connect(
                    database=db_name,
                    host=db_host,
                    port=db_port,
                )
            else:
                connection = psycopg2.connect(
                    database=db_name,
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    port=db_port,
                )

            print("Connection to PostgreSQL DB successful")
        except Exception as e:
            raise OperationalError(e)
        return connection


@dataclass
class Db:
    db_name: str = POSTGRES_NAME
    db_host: str = POSTGRES_HOST
    db_port: int = POSTGRES_PORT
    mode: str = "append"
    connection: Union[psycopg2.extensions.connection, None] = create_connection(
        db_name, db_host, db_port
    )
    conn: Optional[None] = f"postgresql://{db_host}:{db_port}/{db_name}"

    def execute_query(self, query: str):
        """The function execute any sql query such as create table,run select statement and so on.

        Args:
            query (str): sql query
        """
        with start_action(action_type="execute_query", query=query):
            self.connection.autocommit = True
            cursor = self.connection.cursor()
            try:
                cursor.execute(query)
            except Exception as e:
                raise OperationalError(e)

    def insert_into_table(self, values: Tuple[str, str, datetime.datetime]) -> None:
        """This function is specifically to insert into table 'tbl_question_class'

        Args:
            values (Tuple): list of input elements
        """
        with start_action(action_type="insert_into_table", values=values):
            insert_query = f"INSERT INTO tbl_question_class (question, classification, created_on) VALUES {'%s'}"
            questions = [values]
            self.connection.autocommit = True
            cursor = self.connection.cursor()
            try:
                cursor.execute(insert_query, questions)
            except Exception as e:
                raise OperationalError(e)

    def execute_read_query(self) -> list:
        """Read all data in tbl_question_class

        Returns:
            list: list of rows of data
        """
        with start_action(action_type="execute_read_query"):
            cursor = self.connection.cursor()
            result = None
            query = "SELECT * FROM tbl_question_class"
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
            except Exception as e:
                raise OperationalError(e)

    def read_sql(self, no_of_rows: int = 10) -> pd.DataFrame:
        """Get lastest number of rows from tbl_question_class as pandas dataframe.

        Args:
            no_of_rows (int): number of rows to return

        Returns:
            pd.DataFrame: pandas DataFrame
        """
        with start_action(action_type="read_sql", no_of_rows=no_of_rows):
            try:
                df = pd.read_sql_table(
                    table_name="tbl_question_class",
                    con=self.conn,
                    schema="public",
                    parse_dates=["created_on"],
                )
                return df.tail(no_of_rows)
            except Exception as e:
                raise OperationalError(e)

    def write_df_sql(self, df) -> None:
        df.to_sql(
            name="tbl_question_class", con=self.conn, if_exists=self.mode, index=False
        )
