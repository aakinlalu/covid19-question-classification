from typing import Optional
from dataclasses import dataclass 
from fastai.text.all import load_learner


class Predict: 
    def __init__(self, model_path):
        self.model_path = model_path
        if model_path is not None: 
            self.learner = load_learner(model_path, cpu=True)
    

    def predict_one(self, question): 
        result = self.learner.predict(question)
        return result[0]


