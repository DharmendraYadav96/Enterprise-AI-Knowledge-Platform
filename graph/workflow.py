from langgraph.graph import StateGraph, END

from graph.state import RAGState
from graph.nodes import RAGNodes


class RAGWorkflow:

    def __init__(self):

        self.nodes = RAGNodes()

        self.graph = self._build_graph()

    def _build_graph(self):

        workflow = StateGraph(
            RAGState
        )

        workflow.add_node(
            "analyze_query",
            self.nodes.analyze_query
        )

        workflow.add_node(
            "retrieve",
            self.nodes.retrieve_documents
        )

        workflow.add_node(
            "evaluate",
            self.nodes.evaluate_retrieval
        )

        workflow.add_node(
            "build_context",
            self.nodes.build_context
        )

        workflow.add_node(
            "generate_answer",
            self.nodes.generate_answer
        )

        workflow.set_entry_point(
            "analyze_query"
        )

        workflow.add_edge(
            "analyze_query",
            "retrieve"
        )

        workflow.add_edge(
            "retrieve",
            "evaluate"
        )

        workflow.add_conditional_edges(
            "evaluate",
            self.route_after_evaluation,
            {
                "build_context": "build_context",
                "end": END
            }
        )

        workflow.add_edge(
            "build_context",
            "generate_answer"
        )

        workflow.add_edge(
            "generate_answer",
            END
        )

        return workflow.compile()

    def route_after_evaluation(self, state):

        if state["retrieval_success"]:

            return "build_context"

        return "end"

    def run(self, question):

        initial_state = {
            "question": question,
            "rewritten_question": "",
            "documents": [],
            "context": "",
            "answer": "",
            "retry_count": 0,
            "retrieval_success": False
        }

        return self.graph.invoke(
            initial_state
        )