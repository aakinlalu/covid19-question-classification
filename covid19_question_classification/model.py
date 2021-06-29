from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


@dataclass
class Classifier:
    input_dim: int
    output_dim: int
    input_length: int

    def create_model(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        model = Sequential()
        model.add(
            layers.Embedding(
                input_dim=self.input_dim,
                output_dim=self.output_dim,
                input_length=self.input_length,
            )
        )
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation="relu"))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(128, activation="relu"))
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(1, activation="softmax"))
        return model

    def compile_model(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        model = self.create_model()
        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )
        return model

    def plot_history(self, history):
        """[summary]

        Args:
            history ([type]): [description]
        """
        accuracy = history.history["accuracy"]
        val_accuracy = history.history["val_accuracy"]
        loss = history.history["loss"]
        val_loss = history.history["val_loss"]
        x = range(1, len(accuracy) + 1)
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(x, accuracy, "b", label="Training accuracy")
        plt.plot(x, val_accuracy, "r", label="Validation accuracy")
        plt.title("Training and validation accuracy")
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(x, loss, "b", label="Training loss")
        plt.plot(x, val_loss, "r", label="Validation loss")
        plt.title("Training and validation loss")
        plt.legend()
