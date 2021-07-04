from dataclasses import dataclass
from typing import Optional, Union

from fastai.text.all import load_learner
from ludwig.api import LudwigModel
import pandas as pd
from eliot import start_action, start_task

from loggings.logger import __LOGGER__

__LOGGER__


class Predict:
    def __init__(self, model_path, flag=False):
        """[summary]

        Args:
            model_path ([type]): [description]
        """
        self.model_path = model_path
        self.model = LudwigModel.load(model_path)
        if flag == True:
            self.learner = load_learner(model_path, cpu=True)

    def predict_one(self, question):
        """[summary]

        Args:
            question ([type]): [description]

        Returns:
            [type]: [description]
        """
        with start_task(action_type="predict_one", question=question) as action:
            try:
                result = self.learner.predict(question)
                action.log(message_type="prediction", predict=result[0])
                return result[0]
            except Exception as e:
                raise ValueError(e)

    def predict(self, question: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """[summary]

        Args:
            question (Union[str, pd.DataFrame]): [description]

        Raises:
            ValueError: [description]

        Returns:
            pd.DataFrame: [description]
        """
        with start_task(action_type="predict") as action:
            try:
                if isinstance(question, str):
                    predictions, _ = self.model.predict(
                        dataset={"Question": [question]}
                    )
                    predictions["Question"] = question
                    action.log(
                        message_type="info",
                        question=question,
                        prediction_label=predictions["label_predictions"][0],
                    )
                else:
                    predictions, _ = self.model.predict(dataset=question)
                    predictions = pd.concat([predictions, question], axis=1)
                    action.log(message_type="info", question=len(question))

                return predictions[
                    ["Question", "label_predictions", "label_probability"]
                ]
            except Exception as e:
                raise ValueError(e)
