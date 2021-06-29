from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import pandas as pd
import mlflow
import mlflow.fastai

from data_processing import DataProcessing

from fastai.text.all import *  



@dataclass
class MultiClass:
    data: pd.DataFrame 
    seq_len: int
    text_col: str='Questiom'
    label: str="label"
    dls_lm:Optional=None

    def create_lm(self, valid_pct=0.2, drop_mult=0.3):
        self.dls_lm = TextDataLoaders.from_df(
            self.data, text_col=self.text_col, valid_pct=valid_pct, is_lm=True,  seq_len=self.seq_len, bs=64)
        learn = language_model_learner(self.dls_lm, AWD_LSTM, drop_mult=drop_mult, metrics=[
                                      accuracy, Perplexity()]).to_fp16()

        return learn


    def create_text_cls(self):  

        if self.dls_lm is not None:

            data_clf=DataBlock(
                blocks=(TextBlock.from_df(
                    self.text_col, seq_len=self.dls_lm.seq_len, vocab=self.dls_lm.vocab), CategoryBlock),
                get_x=ColReader('text'),
                get_y=ColReader(self.label),
                splitter=TrainTestSplitter(test_size=0.2, random_state=21)
            )

            data_clf = data_clf.dataloaders(self.data, bs=64)
        
            learn = text_classifier_learner(data_clf, AWD_LSTM, drop_mult=0.5, metrics=[
                                            accuracy, F1Score(average="weighted")]).to_fp16()
        
            return learn
    
    def deploy_learn(self, lm_encoder,save_path):
        
        learn = self.create_lm()
        learn.fit_one_cycle(1, 1e-2)

        learn.unfreeze()
        learn.fit_one_cycle(20, 1e-3)
        learn.save_encoder(lm_encoder)
        
        learn = self.create_text_cls()
        learn.load_encoder(lm_encoder)
        learn.fit_one_cycle(1, 1e-3)

        learn.freeze_to(-2)
        learn.fit_one_cycle(1, slice(1e-2/(2.6**4), 1e-2))

        learn.freeze_to(-3)
        learn.fit_one_cycle(20, slice(5e-3/(2.6**4), 1e-2))

        learn.unfreeze()
        learn.fit_one_cycle(30, slice(1e-3/(2.6**4), 1e-3))

        learn.export(save_path)



        
if __name__ == '__main__':
    path= Path(__file__).resolve().parent.parent.absolute()
    file_path = f'{path}/data/final_master_dataset.csv'

    dataPrep = DataProcessing(file_path, 'Question', 'Category')
    data = dataPrep.data_clean()

    Classifier = MultiClass(data, 72, 'Question', 'label')

    lm_encoder = f'{path}/data/funed_lm_encoderv2'

    model_path = f'{path}/data/modelv2.pkl'

    Classifier.deploy_learn(lm_encoder, model_path)
    
    



    

