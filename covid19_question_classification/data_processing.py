from dataclasses import dataclass
from json import encoder 
from typing import Tuple
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences


@dataclass
class DataProcessing:
    raw_path: str 
    feature: str
    label: str
    data: pd.DataFrame= None
    test_size:float=0.25

    @property
    def read_file(self) -> None:
        self.data = pd.read_csv(self.raw_path) 

    def max_length(self) -> int: 
        data = self.data_clean()
        return max([len(item.split(' ')) for item in data[self.feature] if isinstance(item, str)])

    def data_clean(self): 
        if self.data is None:
            self.read_file
        
        self.data = self.data[self.data[self.feature].notnull()]
        self.data = self.data[self.data[self.label].notnull()]

        self.data['label'] = self.data[self.label].apply(
            lambda x: str(x).split('-')[0].strip())
        
        # self.data['label_code'] = self.data['label'].astype('category').cat.codes

        return self.data

    
    
    def dataset_split(self) -> Tuple[pd.DataFrame]: 
        self.data = self.data_clean()
        self.x_train, self.x_test, self.y_train, self.y_test= train_test_split(self.data[self.feature], self.data['label'], test_size=self.test_size, random_state=0)
        return self.x_train, self.x_test, self.y_train, self.y_test


    def tokenize_sequence(self, text, num_words, padding:str="post"):
        self.tokenizer = Tokenizer(
            num_words=num_words, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True)
        self.tokenizer.fit_on_texts(text.values)
        text = self.tokenizer.texts_to_sequences(text)
        self.maxlen = self.max_length() + 10
        text = pad_sequences(text, padding=padding, maxlen=self.maxlen)
        return text 

    def tokenize_sequence_feature(self, num_words, padding: str = "post"):  
        res = []
        x_train, x_test, y_train, y_test = self.dataset_split()
        x_train = self.tokenize_sequence(x_train, num_words, padding)
        x_test = self.tokenize_sequence(x_test, num_words, padding)
        encoder = LabelEncoder()
        y_train = encoder.fit_transform(y_train)
        y_test = encoder.fit_transform(y_test)
        
        
        return x_train, x_test, y_train, y_test

            

        



    




    

        
