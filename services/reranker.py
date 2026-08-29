from sentence_transformers import CrossEncoder

from utils.logger import setup_logger


class Reranker:

    def __init__(self):

        self.logger = setup_logger()

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        self.logger.info(
            
            "Reranker model loaded successfully."
        )

    def rerank(
        self,
        query,
        documents,
        limit=5
    ):

        if not documents:
            return []

        pairs = []

        for document in documents:

            pairs.append([
                query,
                document["text"]
            ])

        scores = self.model.predict(pairs)

        ranked_documents = []

        for document, score in zip(
            documents,
            scores
        ):

            result = document.copy()

            result["rerank_score"] = float(score)

            ranked_documents.append(result)

        ranked_documents.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        return ranked_documents[:limit]