from langchain_core.messages import HumanMessage, SystemMessage

from src.llm import llm
from src.models import AgentState
from src.prompts.rewrite import REWRITE_SYSTEM_PROMPT
from src.logger import logger


def rewrite_node(state: AgentState) -> AgentState:
    """Reformulate the question into a self-contained query using chat history."""
    question = state["question"]
    chat_history = state.get("chat_history", [])

    if not chat_history:
        logger.info("[v2] Rewrite node: no history, using original question")
        return {**state, "rewritten_question": question}

    logger.info(f"[v2] Rewrite node: resolving context from {len(chat_history)} msgs")

    try:
        history_text = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in chat_history
        )

        prompt = f"""Chat history:
{history_text}

Current question: {question}

Rewrite the current question to be fully self-contained:"""

        response = llm.invoke([
            SystemMessage(content=REWRITE_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ])

        rewritten = response.content.strip()
        logger.info(f"[v2] Rewrite node: '{question}' → '{rewritten}'")
        return {**state, "rewritten_question": rewritten}

    except Exception as e:
        logger.error(f"[v2] Rewrite node error: {e}", exc_info=True)
        return {**state, "rewritten_question": question}
