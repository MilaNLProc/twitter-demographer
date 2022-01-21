from transformers import Trainer
from twitter_demographer.support.dataset import prepare_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from datasets import Dataset
import numpy as np
from twitter_demographer.components import Component

class HuggingFaceClassifier(Component):

    def __init__(self, model_name):
        super().__init__()
        self.model_name = model_name

    def inputs(self):
        return ["text"]

    def outputs(self):
        return [f"{self.model_name}"]

    def infer(self, data):

        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

        df = pd.DataFrame({"texts": data["text"].values.tolist()})

        df = df[~df["texts"].isna()]

        train_dataset = Dataset.from_pandas(df)
        train_dataset = prepare_dataset(train_dataset, tokenizer)

        trainer = Trainer(
            model=model,
        )

        local_results = np.argmax(trainer.predict(train_dataset)[0], axis=1)

        returned = [None]*len(data)

        for index, value in zip(df.index.values.tolist(), local_results):
            returned[index] = value

        return {self.model_name: returned}