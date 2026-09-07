import json
import os

from utils.logger import setup_logger


class RAGEvaluator:

    def __init__(self, rag_service):

        self.logger = setup_logger()

        self.rag_service = rag_service

    def load_questions(self, file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def evaluate(self, questions):

        results = []

        for item in questions:

            question = item["question"]

            expected_keywords = item.get(
                "expected_keywords",
                []
            )

            self.logger.info(
                "Evaluating question: %s",
                question
            )

            try:

                response = (
                    self.rag_service
                    .answer_question(question)
                )

                answer = response.get(
                    "answer",
                    ""
                )

                keyword_score = (
                    self._keyword_score(
                        answer,
                        expected_keywords
                    )
                )

                results.append({
                    "question": question,
                    "answer": answer,
                    "keyword_score": keyword_score,
                    "success": True
                })

            except Exception as error:

                self.logger.error(
                    "Evaluation failed: %s",
                    error
                )

                results.append({
                    "question": question,
                    "answer": "",
                    "keyword_score": 0,
                    "success": False
                })

        return results

    def _keyword_score(
        self,
        answer,
        expected_keywords
    ):

        if not expected_keywords:
            return 0

        answer = answer.lower()

        matched = 0

        for keyword in expected_keywords:

            if keyword.lower() in answer:
                matched += 1

        return matched / len(
            expected_keywords
        )

    def calculate_summary(self, results):

        successful_results = [
            result
            for result in results
            if result["success"]
        ]

        if not successful_results:

            return {
                "total_questions": len(results),
                "successful_questions": 0,
                "average_keyword_score": 0
            }

        average_score = sum(
            result["keyword_score"]
            for result in successful_results
        ) / len(successful_results)

        return {
            "total_questions": len(results),
            "successful_questions": len(
                successful_results
            ),
            "average_keyword_score": round(
                average_score,
                2
            )
        }

    def evaluate_retrieval(
    self,
    documents,
    expected_document
    ):

        if not documents:

            return 0

        for document in documents:

            if (
                document.get("document_name")
                == expected_document
            ):

                return 1

        return 0