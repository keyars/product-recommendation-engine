from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from hybrid import load_hybrid_recommender


BASE_DIR = Path(__file__).resolve().parents[1]
recommender = load_hybrid_recommender(BASE_DIR)

app = FastAPI(
    title="Product Recommendation Engine",
    description="REST API for the hybrid product recommendation engine.",
    version="5.0.0",
)


@app.get("/", tags=["Health"])
def root() -> dict:
    return {
        "name": "Product Recommendation Engine",
        "version": "5.0.0",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health() -> dict:
    return {"status": "ok"}


@app.get("/recommendations/{user_id}", tags=["Recommendations"])
def recommendations(
    user_id: str,
    top_n: int = Query(default=5, ge=1, le=20),
    content_weight: float = Query(default=0.6, ge=0.0, le=1.0),
) -> dict:
    try:
        engine = recommender
        if content_weight != 0.6:
            engine = load_hybrid_recommender(BASE_DIR, content_weight=content_weight)
        items = engine.recommend(user_id, top_n=top_n)
        return {
            "user_id": user_id,
            "count": len(items),
            "recommendations": items,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
