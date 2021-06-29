from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
from data_processing import DataProcessing
from fastai.text.all import *


@dataclass
class MultiClass:
    data: pd.DataFrame
    seq_len: int
    text_col: str = "Questiom"
    label: str = "label"
    dls_lm: Optional = None

    def create_lm(self, valid_pct=0.2, drop_mult=0.3):
        """
        :TODO
        """
        self.dls_lm = TextDataLoaders.from_df(
            self.data,
            text_col=self.text_col,
            valid_pct=valid_pct,
            is_lm=True,
            seq_len=self.seq_len,
            bs=64,
        )
        learn = language_model_learner(
            self.dls_lm, AWD_LSTM, drop_mult=drop_mult, metrics=[accuracy, Perplexity()]
        ).to_fp16()

        return learn

    def create_text_cls(self):
        """
        :TODO
        """
        if self.dls_lm is not None:

            data_clf = DataBlock(
                blocks=(
                    TextBlock.from_df(
                        self.text_col,
                        seq_len=self.dls_lm.seq_len,
                        vocab=self.dls_lm.vocab,
                    ),
                    CategoryBlock,
                ),
                get_x=ColReader("text"),
                get_y=ColReader(self.label),
                splitter=TrainTestSplitter(test_size=0.2, random_state=21),
            )

            data_clf = data_clf.dataloaders(self.data, bs=64)

            learn = text_classifier_learner(
                data_clf,
                AWD_LSTM,
                drop_mult=0.5,
                metrics=[accuracy, F1Score(average="weighted")],
            ).to_fp16()

            return learn

    def deploy_learn(self, lm_encoder, save_path, epochs=10, learning_rate=1e-3):
        """[summary]

        Args:
            lm_encoder ([type]): [description]
            save_path ([type]): [description]

        Raises:
            ValueError: [description]
        """
        try:
            path = Path(__file__).resolve().parent.parent.absolute()
            learn = self.create_lm()
            learn.fit_one_cycle(1, 1e-2)

            learn.unfreeze()
            learn.fit_one_cycle(epochs, learning_rate)
            learn.save_encoder(lm_encoder)

            learn = self.create_text_cls()
            learn.load_encoder(lm_encoder)

            learn.fit_one_cycle(1, learning_rate)

            learn.unfreeze()
            learn.fit_one_cycle(epochs, slice(1e-3 / (2.6 ** 4), learning_rate))

            learn.export(save_path)
        except Exception as e:
            raise ValueError(e)


if __name__ == "__main__":
    path = Path(__file__).resolve().parent.parent.absolute()
    file_path = f"{path}/data/final_master_dataset.csv"

    dataPrep = DataProcessing(file_path, "Question", "Category")
    data = dataPrep.data_clean()

    Classifier = MultiClass(data, 72, "Question", "label")

    lm_encoder = f"{path}/data/funed_lm_encoderv2"

    model_path = f"{path}/data/modelv2.pkl"

    Classifier.deploy_learn(lm_encoder, model_path)
