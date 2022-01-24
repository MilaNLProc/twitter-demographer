import numpy as np
import pandas as pd
from contextualized_topic_models.models.ctm import ZeroShotTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessingStopwords

class TopicModeler:
    """
    A simple topic modeler based on Contextualized Topic Models. This topic model is multilingual by default

    see: https://aclanthology.org/2021.acl-short.96/
    """

    def __init__(self, topic_num, embedding_model="paraphrase-multilingual-mpnet-base-v2"):
        self.topic_num = topic_num
        self.embedding_model = embedding_model


    def infer(self, data):
        df = pd.DataFrame({"text": data["text"].values.tolist()})
        df = df[~df["text"].isna()]

        documents = df["text"].values.tolist()

        sp = WhiteSpacePreprocessingStopwords(documents)
        preprocessed_documents, unpreprocessed_corpus, vocab = sp.preprocess()

        tp = TopicModelDataPreparation(self.embedding_model)

        training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)

        ctm = ZeroShotTM(bow_size=len(tp.vocab), contextual_size=768, n_components=self.topic_num, num_epochs=2)
        ctm.fit(training_dataset)
        topics_predictions = np.argmax(ctm.get_thetas(training_dataset, n_samples=15), axis=1).tolist()

        returned = [None] * len(data)

        for index, value in zip(df.index.values.tolist(), topics_predictions):
            returned[index] = value

        return {"topic": returned}
