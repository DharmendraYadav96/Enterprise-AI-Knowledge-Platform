import re

from utils.logger import setup_logger


class KeywordSearch:

    def __init__(self):
        self.logger = setup_logger()

    def search(self, query, documents, limit=5):

        query_words = self._extract_words(query)

        results = []

        for document in documents:

            text = document.get("text", "")

            text_words = self._extract_words(text)

            if not text_words:
                continue

            matched_words = set(query_words) & set(text_words)

            score = len(matched_words)

            if score > 0:

                results.append({
                    "text": text,
                    "document_name": document.get(
                        "document_name",
                        "Unknown"
                    ),
                    "keyword_score": score
                })

        results.sort(
            key=lambda item: item["keyword_score"],
            reverse=True
        )

        return results[:limit]

    def _extract_words(self, text):

        return re.findall(
            r"\b\w+\b",
            text.lower()
        )