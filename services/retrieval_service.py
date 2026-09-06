from services.embedding_service import EmbeddingService
from services.keyword_search import KeywordSearch
from services.reranker import Reranker
from services.vector_store import VectorStore
from utils.logger import setup_logger


class RetrievalService:

    def __init__(self):

        self.logger = setup_logger()

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore()

        self.keyword_search = KeywordSearch()

        self.reranker = Reranker()

    def retrieve(
        self,
        query,
        vector_limit=5,
        keyword_limit=5,
        final_limit=5,
        document_name=None
    ):

        self.logger.info(
            "Starting hybrid retrieval."
        )

        # -------------------------
        # Vector Search
        # -------------------------

        query_embedding = (
            self.embedding_service
            .generate_embedding(query)
        )

        vector_results = (
            self.vector_store
            .search(
                query_embedding,
                limit=vector_limit
            )
        )

        vector_documents = []

        for result in vector_results:

            document = {
                "text": result.payload.get(
                    "text",
                    ""
                ),

                "document_name": result.payload.get(
                    "document_name",
                    "Unknown"
                ),

                "document_id": result.payload.get(
                    "document_id"
                ),

                "chunk_id": result.payload.get(
                    "chunk_id"
                ),

                "vector_score": float(
                    result.score
                )
            }

            # Apply document filter

            if document_name:

                if (
                    document["document_name"]
                    != document_name
                ):
                    continue

            vector_documents.append(
                document
            )

        # -------------------------
        # Keyword Search
        # -------------------------

        all_documents = (
            self.vector_store
            .get_all_documents()
        )

        if document_name:

            all_documents = [
                document
                for document in all_documents
                if document.get(
                    "document_name"
                ) == document_name
            ]

        keyword_results = (
            self.keyword_search
            .search(
                query,
                all_documents,
                limit=keyword_limit
            )
        )

        # -------------------------
        # Combine Results
        # -------------------------

        combined = []

        combined.extend(
            vector_documents
        )

        combined.extend(
            keyword_results
        )

        # -------------------------
        # Remove Duplicate Chunks
        # -------------------------

        unique_documents = {}

        for document in combined:

            text = document.get(
                "text",
                ""
            )

            unique_documents[text] = document

        candidates = list(
            unique_documents.values()
        )

        # -------------------------
        # Reranking
        # -------------------------

        results = self.reranker.rerank(
            query,
            candidates,
            limit=final_limit
        )

        self.logger.info(
            "Hybrid retrieval completed. "
            "Candidates: %s, Final: %s",
            len(candidates),
            len(results)
        )

        return results