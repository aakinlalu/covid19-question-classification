import datetime
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from covid19_question_classification.predict import Predict
from db.db import Db

path = Path(__file__).resolve().parent.absolute()
MODEL_PATH = f"{path}/model/model.pkl"

Pred = Predict(MODEL_PATH)

create_users_table = """
        CREATE TABLE IF NOT EXISTS tbl_question_class (
        id SERIAL PRIMARY KEY,
        question TEXT NOT NULL,
        classification TEXT NOT NULL,
        created_on TIMESTAMP NOT NULL
        )
"""

dB = Db()


@st.cache
def load_data():
    return dB.read_sql()


def chart(data: pd.DataFrame):
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(x="classification", y="count", tooltip=["classification", "count"])
    )


st.title("Covid19-Question Classification")

question = st.text_area(
    "Paste Question here:",
)

if question is not None:
    with st.spinner("wait for it..."):
        st.write("**Question:**", question)
        pred = Pred.predict_one(question)
        st.write("**Classification:**", pred)
        values = (question, pred, datetime.datetime.now())
        dB.execute_query(create_users_table)
        dB.insert_into_table(values)

data = load_data()
st.subheader("Question Classification Chart")
gp_class_df = data.groupby("classification")["id"].count().reset_index()
gp_class_df.rename(columns={"id": "count"}, inplace=True)

ct = chart(gp_class_df)
st.altair_chart(ct, use_container_width=True)

if st.checkbox("Show detail question classiication data"):
    st.subheader("10 Questions Classification data")
    st.write(data.tail(10))
