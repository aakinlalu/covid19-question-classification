import asyncio
import datetime
import uuid
from typing import List

import databases
import pandas as pd

from .config import DATABASE_URLs

# async def session():
#     async with databases.Database(DATABASE_URL) as database:
#         session = await database.connect()
#         return session
database = databases.Database(DATABASE_URLs)

# Create table
async def create_table():
    await database.connect()

    query = """
        CREATE TABLE IF NOT EXISTS tbl_question_class (
            id TEXT NOT NULL, 
            question TEXT NOT NULL,
            classification TEXT NOT NULL,
            created_on TIMESTAMP NOT NULL
            )
    """
    await database.execute(query=query)
    await database.disconnect()


async def insert_one_into_table(question, classification):
    await database.connect()
    # if question is None:
    #     return None
    id = str(uuid.uuid4())
    created_on = datetime.datetime.now()
    query = f"""INSERT INTO tbl_question_class (id, question, classification, created_on)
             VALUES (:id, :question, :classification, :created_on)
    """
    values = {
        "id": id,
        "question": question,
        "classification": classification,
        "created_on": created_on,
    }
    await database.execute(query=query, values=values)

    query = "SELECT * FROM tbl_question_class limit 10"
    rows = await database.fetch_all(query=query)
    # return rows
    # await database.disconnect()
    return rows


async def insert_many_into_table(values: List[dict]):
    await database.connect()
    query = f"""INSERT INTO tbl_question_class (id, question, classification, created_on)
             VALUES (:id, :question, :classification, :created_on)
    """
    await database.execute_many(query=query, values=values)
    await database.disconnect()


def read_table():
    df = pd.read_sql_table("tbl_question_class", con=DATABASE_URLs, schema="public")
    return df


if __name__ == "__main__":
    asyncio.run(insert_one_into_table("question", "Answer"))
