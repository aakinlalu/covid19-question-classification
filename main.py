from pathlib import Path
import asyncio
import streamlit as st 
from covid19_question_classification.predict import Predict
from db.db import insert_one_into_table, create_table

path = Path(__file__).resolve().parent.absolute()
model_path = f'{path}/data/model.pkl'

Pred = Predict(model_path)

st.title('Covid19-Question Classification')

question = st.text_area('Paste question',)


st.write(f"Question: {question}")
if question is not None:
    pred = Pred.predict_one(question)
    st.write(f"Classification: {pred}")
    st.write(asyncio.run(insert_one_into_table(question, pred)))
