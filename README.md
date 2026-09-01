# Product Recommendation Engine

A small, practical product recommendation engine demonstrating how ML recommendation techniques can be integrated into an e-commerce application.

## Current Version: V5

The project now exposes the hybrid recommendation engine through a lightweight REST API.

## Recommendation Engine

The engine combines:

- **Content-based filtering** — recommends products similar to the customer's own interaction history.
- **User-based collaborative filtering** — recommends products based on behaviour from customers with similar interaction patterns.

The default hybrid blend is:

- Content-based: **60%**
- Collaborative: **40%**

Scores are normalized before blending.

## V5 — FastAPI

The Python recommendation engine is now accessible to mobile, web, or other clients through REST.

### Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health check |
| GET | `/recommendations/{user_id}` | Get product recommendations |

### Recommendation Parameters

`top_n` controls the number of recommendations and defaults to 5.

`content_weight` controls the hybrid balance and defaults to 0.6. The collaborative weight is automatically calculated as `1 - content_weight`.

Example:

```text
GET /recommendations/U001?top_n=5
```

The response contains the user ID, recommendation count, product information, hybrid score, component scores, and explanation.

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.api:app --reload
```

Then open the interactive API documentation at `/docs`.

Run tests with:

```bash
pytest
```

## Stack

- Python
- Pandas
- scikit-learn
- FastAPI
- Uvicorn
- pytest

## Project Structure

```text
product-recommendation-engine/
├── data/
│   ├── products.csv
│   └── user_interactions.csv
├── src/
│   ├── __init__.py
│   ├── api.py
│   ├── collaborative.py
│   ├── demo.py
│   ├── hybrid.py
│   ├── hybrid_demo.py
│   └── recommender.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_recommender.py
├── requirements.txt
└── .gitignore
```

## Roadmap

- [x] V1: Content-based recommendation
- [x] V2: Interaction weighting + explainable recommendations
- [x] V3: User-based collaborative filtering
- [x] V4: Hybrid recommendation
- [x] V5: FastAPI recommendation API
- [ ] V6: Flutter client
- [ ] V7: React Native/Web client
