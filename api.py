from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.models import QueryRequest, QueryResponse
from src.graph_v2.build import build_graph_v2
from src.logger import logger

app = FastAPI(title="Country Information Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph_v2()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/query", response_model=QueryResponse)
def query_country(request: QueryRequest):
    logger.info("Query received", extra={"question": request.question})

    try:
        state = {
            "question": request.question,
            "chat_history": [msg.model_dump() for msg in request.chat_history],
        }
        result = graph.invoke(state)

        if result.get("error"):
            return QueryResponse(success=False, error=result["error"], country=result.get("country"))

        return QueryResponse(
            success=True,
            answer=result.get("answer"),
            country=result.get("country"),
            fields_requested=result.get("fields"),
            data=result.get("api_data"),
        )
    except Exception as e:
        logger.error(f"Query failed: {e}", exc_info=True)
        return QueryResponse(success=False, error=str(e))
