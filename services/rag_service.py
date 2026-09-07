from openai import OpenAI
import time

from services.retrieval_service import RetrievalService

from utils.exceptions import ApplicationError
from utils.logger import setup_logger


class RAGService:

    def __init__(self, api_key):

        self.logger = setup_logger()

        self.retrieval_service = RetrievalService()

        self.client = OpenAI(
            api_key=api_key
        )

    def answer_question(
        self,
        question,
        document_name=None,
        limit=5
    ):

        if not question or not question.strip():

            raise ApplicationError(
                "Question cannot be empty.",
                400
            )

        # Start timer for this RAG request
        start_time = time.perf_counter()

        try:

            self.logger.info(
                "Processing RAG question: %s",
                question
            )

            # -------------------------
            # Step 1: Retrieval
            # -------------------------

            retrieval_start = time.perf_counter()

            results = self.retrieval_service.retrieve(
                query=question,
                final_limit=limit,
                document_name=document_name
            )

            retrieval_time = (
                time.perf_counter()
                - retrieval_start
            )

            self.logger.info(
                "Retrieval completed in %.2f seconds.",
                retrieval_time
            )

            # -------------------------
            # No Results
            # -------------------------

            if not results:

                total_time = (
                    time.perf_counter()
                    - start_time
                )

                self.logger.info(
                    "RAG request completed in %.2f seconds.",
                    total_time
                )

                return {
                    "answer": (
                        "I could not find relevant "
                        "information in the documents."
                    ),
                    "sources": []
                }

            # -------------------------
            # Step 2: Build Context
            # -------------------------

            context_parts = []
            sources = []

            for result in results:

                text = result.get(
                    "text",
                    ""
                )

                context_parts.append(text)

                sources.append({
                    "document": result.get(
                        "document_name",
                        "Unknown"
                    ),
                    "chunk_id": result.get(
                        "chunk_id"
                    ),
                    "score": result.get(
                        "rerank_score"
                    )
                })

            context = "\n\n".join(
                context_parts
            )

            # -------------------------
            # Step 3: Generate Answer
            # -------------------------

            generation_start = time.perf_counter()

            answer = self._generate_answer(
                question,
                context
            )

            generation_time = (
                time.perf_counter()
                - generation_start
            )

            self.logger.info(
                "Answer generation completed in %.2f seconds.",
                generation_time
            )

            # -------------------------
            # Total RAG Time
            # -------------------------

            total_time = (
                time.perf_counter()
                - start_time
            )

            self.logger.info(
                "RAG request completed in %.2f seconds.",
                total_time
            )

            return {
                "answer": answer,
                "sources": sources
            }

        except ApplicationError:

            raise

        except Exception as error:

            self.logger.exception(
                "RAG processing failed."
            )

            raise ApplicationError(
                "Failed to process the question.",
                500
            ) from error

    def _generate_answer(
        self,
        question,
        context
    ):

        prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using ONLY
the information provided in the context.

If the answer cannot be found in the context,
say that you do not have enough information.

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful enterprise "
                        "knowledge assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        return response.choices[0].message.content