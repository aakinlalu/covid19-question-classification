from dataclasses import dataclass
from typing import Optional

from fastai.text.all import load_learner


class Predict:
    def __init__(self, model_path):
        """[summary]

        Args:
            model_path ([type]): [description]
        """
        self.model_path = model_path
        if model_path is not None:
            self.learner = load_learner(model_path, cpu=True)

    def predict_one(self, question):
        """[summary]

        Args:
            question ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            result = self.learner.predict(question)
            return result[0]
        except Exception as e:
            raise ValueError(e)
