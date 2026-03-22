import json

from langchain_core.messages import HumanMessage, SystemMessage

from src.llm import llm
from src.models import AgentState
from src.prompts.intent import INTENT_SYSTEM_PROMPT
from src.logger import logger


def intent_node(state: AgentState) -> AgentState:
    """Extract country and fields from the rewritten (self-contained) question."""
    question = state.get("rewritten_question", state["question"])
    logger.info(f"[v2] Intent node processing: {question}")

    try:
        response = llm.invoke([
            SystemMessage(content=INTENT_SYSTEM_PROMPT),
            HumanMessage(content=question),
        ])

        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        parsed = json.loads(content)

        country = parsed.get("country")
        fields = parsed.get("fields", [])
        clarify = parsed.get("clarify")
        error = parsed.get("error")

        # Clarification needed — return as answer, skip fetch/synthesis
        if clarify:
            logger.info(f"[v2] Intent node: needs clarification — {clarify}")
            return {**state, "answer": clarify}

        if error or not country:
            logger.info(f"[v2] Intent node: not a country question — {error}")
            return {**state, "error": error or "Could not identify a country in the question."}

        logger.info(f"[v2] Intent node: country={country}, fields={fields}")
        return {**state, "country": country, "fields": fields}

    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"[v2] Intent parsing failed: {e}")
        return {**state, "error": "Failed to understand the question. Please ask about a specific country."}
    except Exception as e:
        logger.error(f"[v2] Intent node error: {e}", exc_info=True)
        return {**state, "error": f"Intent analysis failed: {str(e)}"}
