from dataclasses import dataclass
from json import encoder
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from eliot import start_action, start_task

from loggings.logger import __LOGGER__

__LOGGER__


@dataclass
class DataProcessing:
    raw_path: str
    feature: str
    label: str
    test_size: float = 0.25
    data: pd.DataFrame = None
    x_train: pd.DataFrame = None
    x_test: pd.DataFrame = None
    y_train: pd.DataFrame = None
    y_test: pd.DataFrame = None

    @property
    def read_file(self) -> None:
        """[summary]"""
        self.data = pd.read_csv(self.raw_path)

    def data_clean(self, save_flag=False):
        """[summary]

        Returns:
            [type]: [description]
        """
        with start_task(action_type="data_clean") as action:
            try:
                if self.data is None:
                    self.read_file
                action.log(message_type="info", length_of_data=len(self.data))

                with start_action(action_type="filter_data") as action:
                    self.data = self.data[self.data[self.feature].notnull()]
                    self.data = self.data[self.data[self.label].notnull()]
                    action.log(message_type="info", length_of_data=len(self.data))

                self.data["label"] = self.data[self.label].apply(
                    lambda x: str(x).split("-")[0].strip()
                )
                if save_flag == True:
                    self.data.to_csv(
                        "s3://ml-artifact-store/data/filtered.csv", index=False
                    )

            except Exception as e:
                raise ValueError(e)

            return self.data

    def dataset_split(self) -> Tuple[pd.DataFrame]:
        """[summary]

        Returns:
            Tuple[pd.DataFrame]: [description]
        """
        with start_action(action_type="dataset_split", test_size=self.test_size):
            try:
                self.data = self.data_clean()
                self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
                    self.data[self.feature],
                    self.data["label"],
                    test_size=self.test_size,
                    random_state=0,
                )
            except Exception as e:
                raise ValueError(e)
            return self.x_train, self.x_test, self.y_train, self.y_test
