import json
import os

from config import Config
from services.rag_service import RAGService
from evaluation.evaluator import RAGEvaluator


def main():

    rag_service = RAGService(
        api_key=Config.OPENAI_API_KEY
    )

    evaluator = RAGEvaluator(
        rag_service
    )

    base_path = os.path.dirname(
        os.path.abspath(__file__)
    )

    question_path = os.path.join(
        base_path,
        "test_questions.json"
    )

    questions = evaluator.load_questions(
        question_path
    )

    results = evaluator.evaluate(
        questions
    )

    summary = evaluator.calculate_summary(
        results
    )

    output = {
        "summary": summary,
        "results": results
    }

    output_path = os.path.join(
        base_path,
        "evaluation_results.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nEvaluation completed.")
    print(
        f"Average score: "
        f"{summary['average_keyword_score']}"
    )


if __name__ == "__main__":
    main()