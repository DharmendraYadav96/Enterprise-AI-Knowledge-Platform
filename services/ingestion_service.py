import os

from ingestion.document_loader import DocumentLoader
from ingestion.text_cleaner import TextCleaner
from ingestion.chunker import DocumentChunker
from utils.exceptions import ApplicationError
from utils.logger import setup_logger
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStore


class IngestionService:

    def __init__(self):

        self.loader = DocumentLoader()
        self.cleaner = TextCleaner()
        self.chunker = DocumentChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

        self.logger = setup_logger()

    def process_document(self, file_path):

        if not os.path.exists(file_path):
            raise ApplicationError(
                "Document file not found.",
                404
            )

        try:

            self.logger.info(
                "Starting document processing: %s",
                file_path
            )

            text = self.loader.load(file_path)

            if not text.strip():
                raise ApplicationError(
                    "No text could be extracted from the document.",
                    400
                )

            cleaned_text = self.cleaner.clean(text)

            chunks = self.chunker.split(cleaned_text)

            embeddings = []

            for chunk in chunks:

                embedding = self.embedding_service.generate_embedding(
                chunk)

            embeddings.append(embedding)

            stored_chunks = self.vector_store.add_document_chunks(
            chunks=chunks,
            embeddings=embeddings,
            document_name=os.path.basename(file_path)
            )

            self.logger.info(
                "Document processed successfully. Chunks: %s",
                len(chunks)
            )

            return {
                "file_path": file_path,
                "character_count": len(cleaned_text),
                "chunk_count": len(chunks),
                "chunks": chunks
            }

        except ApplicationError:
            raise

        except Exception as error:

            self.logger.exception(
                "Unexpected document processing error."
            )

            raise ApplicationError(
                "Failed to process document.",
                500
            ) from error