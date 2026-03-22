from langgraph.graph import StateGraph, END

from src.models import AgentState
from src.graph_v2.nodes.rewrite import rewrite_node
from src.graph_v2.nodes.intent import intent_node
from src.graph_v2.nodes.fetch import fetch_node
from src.graph_v2.nodes.synthesis import synthesis_node


def after_intent(state: AgentState) -> str:
    if state.get("error"):
        return "error"
    if state.get("answer"):
        return "done"
    return "continue"


def should_continue(state: AgentState) -> str:
    if state.get("error"):
        return "error"
    return "continue"


def build_graph_v2():
    """
    V2 — Advanced context preservation via question rewriting.

    Flow: question → rewrite → intent → fetch → synthesis → END

    The rewrite node reformulates the user's question into a clean,
    self-contained query. Downstream nodes never see raw chat history.
    """
    graph = StateGraph(AgentState)

    graph.add_node("rewrite", rewrite_node)
    graph.add_node("intent", intent_node)
    graph.add_node("fetch", fetch_node)
    graph.add_node("synthesis", synthesis_node)

    graph.set_entry_point("rewrite")
    graph.add_edge("rewrite", "intent")

    graph.add_conditional_edges(
        "intent",
        after_intent,
        {"continue": "fetch", "error": END, "done": END},
    )

    graph.add_conditional_edges(
        "fetch",
        should_continue,
        {"continue": "synthesis", "error": END},
    )

    graph.add_edge("synthesis", END)

    return graph.compile()
