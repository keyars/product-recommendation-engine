# Product Recommendation Engine

A small, practical product recommendation engine demonstrating how ML recommendation techniques can be integrated into an e-commerce application.

## Current Version: V4

The project now combines two recommendation signals:

- **Content-based filtering** — recommends products similar to the customer's own interaction history.
- **User-based collaborative filtering** — recommends products based on behaviour from customers with similar interaction patterns.

## V1 — Content-Based Recommendation

Product category, brand, and tags are converted into TF-IDF vectors. A weighted customer profile is compared with products using cosine similarity.

## V2 — Behaviour + Explainability

- View = 1
- Wishlist = 3
- Cart = 4
- Purchase = 5
- Human-readable recommendation reasons.
- Popularity fallback for unknown customers.

## V3 — Collaborative Filtering

The engine creates a **user × product interaction matrix**, calculates cosine similarity between customers, selects similar customers, and uses their weighted interactions to rank products the target customer has not seen.

## V4 — Hybrid Recommendation

V4 combines both approaches instead of relying on one signal:

```text
                 Customer History
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
       Content-Based       Collaborative
             │                   │
             ↓                   ↓
       Content Score      Collaborative Score
             │                   │
             └─────────┬─────────┘
                       ↓
                 Weighted Blend
                       ↓
              Final Recommendation
```

The default blend is:

- Content-based signal: **60%**
- Collaborative signal: **40%**

Scores are normalized before blending so that the two algorithms contribute on the same scale.

The result exposes both component scores, the final hybrid score, and an explanation describing why the product was recommended.

### Why Hybrid?

Content-based filtering is useful when we know what a customer likes. Collaborative filtering can discover patterns that product metadata alone cannot capture. Combining them gives the application two independent recommendation signals.

The sample dataset is intentionally small. This project demonstrates the algorithmic progression rather than production-scale recommendation quality.

## Stack

- Python
- Pandas
- scikit-learn
- pytest

## Project Structure

```text
product-recommendation-engine/
├── data/
│   ├── products.csv
│   └── user_interactions.csv
├── src/
│   ├── __init__.py
│   ├── collaborative.py
│   ├── demo.py
│   ├── hybrid.py
│   ├── hybrid_demo.py
│   └── recommender.py
├── tests/
│   ├── __init__.py
│   └── test_recommender.py
├── requirements.txt
└── .gitignore
```

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/hybrid_demo.py
pytest
```

## Roadmap

- [x] V1: Content-based recommendation
- [x] V2: Interaction weighting + explainable recommendations
- [x] V3: User-based collaborative filtering
- [x] V4: Hybrid recommendation
- [ ] V5: FastAPI recommendation API
- [ ] V6: Flutter client
- [ ] V7: React Native/Web client
