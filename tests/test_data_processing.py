from pathlib import Path

import pandas as pd
import pytest

from covid19_question_classification.data_processing import DataProcessing

path = Path(__file__).resolve().parent.parent.absolute()
data_path = f"{path}/data/final_master_dataset.csv"

dataPrep = DataProcessing(data_path, "Question", "Category")


def test_data_clean():
    data = dataPrep.data_clean()
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
    assert "label" in data

    assert data["Question"].isnull().sum() == 0
    assert data["label"].isnull().sum() == 0


def test_max_length():
    max_length = dataPrep.max_length()
    assert max_length > 0


def test_dataset_split():
    tuple_list = dataPrep.dataset_split()
    assert isinstance(tuple_list, tuple)
    assert len(tuple_list) == 4
    for df in tuple_list:
        assert len(df) > 0


def test_tokenize_sequence_feature(num_words=5000):
    res = dataPrep.tokenize_sequence_feature(num_words)
    assert len(res) == 4
