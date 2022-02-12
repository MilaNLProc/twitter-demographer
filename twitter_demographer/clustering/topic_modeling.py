import numpy as np
import pandas as pd
from contextualized_topic_models.models.ctm import ZeroShotTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessingStopwords
import re
from twitter_demographer.components import Component, not_null
from twitter_demographer.support.utils import twitter_preprocess

class TopicModeler(Component):
    """
    A simple topic modeler based on Contextualized Topic Models. This topic model is multilingual by default

    see: https://aclanthology.org/2021.acl-short.96/
    """

    def outputs(self):
        return ["topic", "topic_words"]

    def inputs(self):
        return ["text"]

    def __init__(self, topic_num, embedding_model="paraphrase-multilingual-mpnet-base-v2", stopwords=None):
        super().__init__()
        self.topic_num = topic_num
        self.embedding_model = embedding_model
        self.stopwords = stopwords if stopwords else []

    @not_null("text")
    def infer(self, data):
        df = pd.DataFrame({"text": data["text"].values.tolist()})
        df["text"] = df["text"].apply(twitter_preprocess)
        df["text"] = df["text"].apply(lambda x : re.sub(r'\s*(?:https?://)?www\.\S*\.[A-Za-z]{2,5}\s*', '', x))

        documents = df["text"].values.tolist()

        sp = WhiteSpacePreprocessingStopwords(documents, stopwords_list=self.stopwords)
        preprocessed_documents, unpreprocessed_corpus, vocab = sp.preprocess()

        tp = TopicModelDataPreparation(self.embedding_model)

        training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)

        ctm = ZeroShotTM(bow_size=len(tp.vocab), contextual_size=768, n_components=self.topic_num, num_epochs=20)
        ctm.fit(training_dataset)
        topics_predictions = np.argmax(ctm.get_thetas(training_dataset, n_samples=15), axis=1).tolist()
        topic_list = ctm.get_topic_lists(5)

        return {"topic": topics_predictions, "topic_words" : [topic_list[k] for k in topics_predictions]}
