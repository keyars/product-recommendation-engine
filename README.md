# Product Recommendation Engine

A small, practical product recommendation engine demonstrating how ML recommendation techniques can be integrated into an e-commerce application.

## Current Version: V3

The project now contains two recommendation strategies:

- **Content-based filtering** — recommends products similar to the customer's own interaction history.
- **User-based collaborative filtering** — recommends products based on behaviour from customers with similar interaction patterns.

## V1 — Content-Based Recommendation

1. Build a profile for each product from category, brand, and tags.
2. Convert product profiles into TF-IDF vectors.
3. Build a weighted customer preference vector.
4. Calculate cosine similarity.
5. Remove products already seen by the customer.
6. Rank the remaining products.

## V2 — Behaviour + Explainability

- View = 1
- Wishlist = 3
- Cart = 4
- Purchase = 5
- Human-readable recommendation reasons.
- Popularity fallback for unknown customers.

## V3 — Collaborative Filtering

V3 changes the question from:

> "Which products are similar to what this customer liked?"

to:

> "What did customers with similar behaviour interact with?"

The engine creates a **user × product interaction matrix**, calculates cosine similarity between customers, selects the most similar customers, and uses their weighted interactions to rank products the target customer has not seen.

This is **user-based collaborative filtering**.

### Example

```text
Customer A
 ├── Running Shoes
 ├── Running Socks
 └── Energy Gel

        ↓ similar behaviour

Customer B
 ├── Running Shoes
 ├── Running Socks
 ├── Running Watch
 └── Hydration Bottle

        ↓

Recommend to Customer A:
Running Watch
Hydration Bottle
```

The sample dataset is intentionally small. The goal is to understand the algorithm and application flow, not to claim production-level recommendation quality.

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
python src/demo.py
pytest
```

## Roadmap

- [x] V1: Content-based recommendation
- [x] V2: Interaction weighting + explainable recommendations
- [x] V3: User-based collaborative filtering
- [ ] V4: Hybrid recommendation
- [ ] V5: FastAPI recommendation API
- [ ] V6: Flutter client
- [ ] V7: React Native/Web client
