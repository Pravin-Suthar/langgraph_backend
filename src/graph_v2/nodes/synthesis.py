import json

from langchain_core.messages import HumanMessage, SystemMessage

from src.llm import llm
from src.models import AgentState
from src.prompts.synthesis import SYNTHESIS_SYSTEM_PROMPT
from src.logger import logger


def synthesis_node(state: AgentState) -> AgentState:
    """Synthesize answer from the rewritten question and fetched data. No history needed."""
    question = state.get("rewritten_question", state["question"])
    api_data = state.get("api_data", {})

    logger.info("[v2] Synthesis node: generating answer")

    try:
        prompt = f"""Question: {question}

Country data:
{json.dumps(api_data, indent=2, default=str)}

Answer the question using only the data above."""

        response = llm.invoke([
            SystemMessage(content=SYNTHESIS_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ])

        answer = response.content.strip()
        logger.info("[v2] Synthesis node: answer generated")
        return {**state, "answer": answer}

    except Exception as e:
        logger.error(f"[v2] Synthesis node error: {e}", exc_info=True)
        return {**state, "error": f"Failed to generate answer: {str(e)}"}
