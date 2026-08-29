from sentence_transformers import SentenceTransformer

from utils.logger import setup_logger


class EmbeddingService:

    def __init__(self):

        self.logger = setup_logger()

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.logger.info(
            "Embedding model loaded successfully."
        )

    def generate_embedding(self, text):

        embedding = self.model.encode(text)

        return embedding.tolist()

    def generate_embeddings(self, texts):

        embeddings = self.model.encode(texts)

        return embeddings.tolist()