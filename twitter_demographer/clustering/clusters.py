from twitter_demographer.components import Component
from sentence_transformers import SentenceTransformer
import umap
import hdbscan

class BaseClustering(Component):
    """
    This BaseClustering is strongly inspired to BERTopic way of creating the clusters

    See: https://github.com/MaartenGr/BERTopic
    """

    def __init__(self, embedding_model):
        """

        :param embedding_model: SentenceBERT embedding model
        """
        super().__init__()
        self.embedding_model = embedding_model

    def outputs(self):
        return ["clusters"]

    def inputs(self):
        return ["text"]

    def infer(self, data):
        texts = data["text"].fillna(" ")

        embeddings = SentenceTransformer(self.embedding_model).encode(texts)

        embeddings = umap.UMAP(n_neighbors=3,
                              min_dist=0.1,
                              metric='cosine').fit_transform(embeddings)

        clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
        cluster_labels = clusterer.fit_predict(embeddings)

        return {"clusters": cluster_labels}

