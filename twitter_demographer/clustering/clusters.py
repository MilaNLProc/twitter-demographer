from twitter_demographer.components import Component
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import umap
import hdbscan



class BaseClustering(Component):

    def outputs(self):
        return ["clusters"]

    def inputs(self):
        return ["text"]

    def __init__(self, embedding_model):
        super().__init__()
        self.embedding_model = embedding_model

    def infer(self, data):
        texts = data["text"].fillna(" ")

        embeddings = SentenceTransformer(self.embedding_model).encode(texts)

        embeddings = umap.UMAP(n_neighbors=3,
                              min_dist=0.1,
                              metric='cosine').fit_transform(embeddings)

        clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
        cluster_labels = clusterer.fit_predict(embeddings)

        return {"clusters": cluster_labels}

