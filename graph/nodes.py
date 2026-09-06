from services.retrieval_service import RetrievalService
from utils.logger import setup_logger
from openai import OpenAI
from config import Config

class RAGNodes:

    def __init__(self):

        self.logger = setup_logger()

        self.retrieval_service = RetrievalService()

        self.client = OpenAI(
            api_key=Config.OPENAI_API_KEY
            )

    def analyze_query(self, state):

        question = state["question"]

        self.logger.info(
            "Analyzing user question."
        )

        return {
            "rewritten_question": question
        }

    def retrieve_documents(self, state):

        question = state["rewritten_question"]

        self.logger.info(
            "Retrieving documents for question."
        )

        documents = self.retrieval_service.retrieve(
            query=question,
            final_limit=5
        )

        return {
            "documents": documents
        }

    def evaluate_retrieval(self, state):

        documents = state["documents"]

        if not documents:

            self.logger.warning(
                "No relevant documents found."
            )

            return {
                "retrieval_success": False
            }

        best_score = documents[0].get(
            "rerank_score",
            0
        )

        self.logger.info(
            "Best retrieval score: %s",
            best_score
        )

        if best_score > 0:

            return {
                "retrieval_success": True
            }

        return {
            "retrieval_success": False
        }

    def build_context(self, state):

        documents = state["documents"]

        context_parts = []

        for document in documents:

            text = document.get(
                "text",
                ""
            )

            if text:
                context_parts.append(text)

        context = "\n\n".join(
            context_parts
        )

        self.logger.info(
            "Context created from %s documents.",
            len(context_parts)
        )

        return {
            "context": context
        }

    def generate_answer(self, state):

        question = state["rewritten_question"]

        context = state["context"]

        prompt = f"""
    You are an enterprise knowledge assistant.

    Answer the question using ONLY the
    information provided in the context.

    If the answer cannot be found in the
    context, say that you do not have
    enough information.

    Do not invent information.

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
                        "You are an enterprise "
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

        answer = response.choices[0].message.content

        self.logger.info(
            "Answer generated successfully."
        )

        return {
            "answer": answer
        }