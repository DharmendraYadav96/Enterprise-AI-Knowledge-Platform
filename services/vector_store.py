import os
import uuid
from config import Config
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams
)

from utils.logger import setup_logger


class VectorStore:

    COLLECTION_NAME = "enterprise_documents"

    _client = None

    def __init__(self):

        self.logger = setup_logger()

        if VectorStore._client is None:

            VectorStore._client = QdrantClient(
                path=Config.QDRANT_PATH
            )

            self.logger.info(
                "Qdrant client initialized successfully."
            )

        self.client = VectorStore._client
        self._create_collection()

    def _create_collection(self):

        collections = self.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if self.COLLECTION_NAME not in collection_names:

            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

            self.logger.info(
                "Qdrant collection created: %s",
                self.COLLECTION_NAME
            )

    def add_document_chunks(
        self,
        chunks,
        embeddings,
        document_name
    ):
        document_id = str(uuid.uuid4())
        points = []

        for index, chunk in enumerate(chunks):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings,
                payload={
                    "text": chunk,
                    "document_name": document_name,
                    "document_id": document_id,
                    "chunk_id": index
                }
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points
        )

        self.logger.info(
            "Stored %s chunks in Qdrant.",
            len(points)
        )

        return len(points)


    def search(self, query_embedding, limit=5):

        results = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_embedding,
            limit=limit
        )

        return results.points

    def get_all_documents(self):

        results = self.client.scroll(
            collection_name=self.COLLECTION_NAME,
            limit=1000,
            with_payload=True,
            with_vectors=False
        )

        points = results[0]

        documents = []

        for point in points:

                    documents.append({
            "id": point.id,
            "text": point.payload.get(
                "text",
                ""
            ),
            "document_name": point.payload.get(
                "document_name",
                "Unknown"
            ),
            "document_id": point.payload.get(
                "document_id"
            ),
            "chunk_id": point.payload.get(
                "chunk_id"
            )
        })

        return documents