from src.models import AgentState
from src.tools.countries import fetch_country
from src.logger import logger


def fetch_node(state: AgentState) -> AgentState:
    """Fetch country data from the REST Countries API."""
    country = state.get("country")

    if not country:
        return {**state, "error": "No country identified to fetch data for."}

    logger.info(f"[v2] Fetch node: looking up '{country}'")

    data = fetch_country(country)

    if "error" in data:
        logger.info(f"[v2] Fetch node: API error — {data['error']}")
        return {**state, "error": data["error"]}

    fields = state.get("fields", [])
    if fields:
        filtered = {k: v for k, v in data.items() if k in fields or k == "name"}
    else:
        filtered = data

    logger.info(f"[v2] Fetch node: got data with {len(filtered)} fields")
    return {**state, "api_data": filtered}
