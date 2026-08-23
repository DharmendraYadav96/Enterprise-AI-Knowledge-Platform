import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams
)

from utils.logger import setup_logger


class VectorStore:

    COLLECTION_NAME = "enterprise_documents"

    def __init__(self):

        self.logger = setup_logger()

        self.client = QdrantClient(
            path="data/qdrant"
        )

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

        points = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "document_name": document_name
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