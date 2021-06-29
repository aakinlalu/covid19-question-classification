import datetime
from dataclasses import dataclass
from typing import Optional

import pandas as pd
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_host, db_port):
    """[summary]

    Args:
        db_name ([type]): [description]
        db_host ([type]): [description]
        db_port ([type]): [description]

    Returns:
        [type]: [description]
    """
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            # user=db_user,
            # password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


@dataclass
class Db:
    db_name: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5438
    connection: Optional[None] = create_connection(db_name, db_host, db_port)
    conn: Optional[None] = f"postgresql://{db_host}:{db_port}/{db_name}"

    def create_database(self, query):
        """[summary]

        Args:
            query ([type]): [description]
        """
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Query executed successfully")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, query):
        """[summary]

        Args:
            query ([type]): [description]
        """
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Query executed successfully")
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def insert_into_table(self, values):
        """[summary]

        Args:
            values ([type]): [description]
        """
        insert_query = f"INSERT INTO tbl_question_class (question, classification, created_on) VALUES {'%s'}"
        questions = [values]
        self.connection.autocommit = True
        cursor = self.connection.cursor()
        cursor.execute(insert_query, questions)

    def execute_read_query(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        cursor = self.connection.cursor()
        result = None
        query = "SELECT * FROM tbl_question_class"
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except OperationalError as e:
            print(f"The error '{e}' occurred")

    def read_sql(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        df = pd.read_sql_table(
            table_name="tbl_question_class",
            con=self.conn,
            schema="public",
            parse_dates=["created_on"],
        )
        return df
