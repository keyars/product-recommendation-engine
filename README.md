# Product Recommendation Engine

A small, practical product recommendation engine demonstrating how a simple ML model can be integrated into an e-commerce application.

## Current Version: V2

V2 keeps the V1 content-based model and makes the recommendation output more practical and explainable.

### V2 Improvements

- Interaction-aware weighting: view, wishlist, cart, and purchase have different strengths.
- Customer preferences are built from the weighted interaction history.
- Recommendations exclude products the customer has already interacted with.
- Each recommendation includes a human-readable reason.
- Unknown customers receive a popularity-based fallback.

## How It Works

1. Build a profile for each product from category, brand, and tags.
2. Convert product profiles into TF-IDF vectors.
3. Translate each customer interaction into a behavioural weight.
4. Build a weighted customer preference vector.
5. Calculate cosine similarity between the customer profile and available products.
6. Remove products the customer has already interacted with.
7. Rank the remaining products by similarity.
8. Generate an explanation based on category and brand preferences.
9. Fall back to popularity when there is not enough customer history.

### Interaction Weights

| Interaction | Weight |
|---|---:|
| View | 1 |
| Wishlist | 3 |
| Cart | 4 |
| Purchase | 5 |

These values are intentionally simple and transparent for V2. A future version can learn weights from real behavioural data.

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

## Example

```text
Recommendations for U001:
1. Running Shoes Pro (Running)
   Score: ...
   Why: Matches your interest in running products.
```

The exact ranking depends on the product feature representation and customer interaction history.

## Why This Project Matters

The objective is not to build a research-grade recommender. It is to demonstrate a complete progression from a simple ML algorithm to an application-ready recommendation feature.

## Roadmap

- [x] V1: Content-based recommendation
- [x] V2: Interaction weighting + explainable recommendations
- [ ] V3: Collaborative filtering
- [ ] V4: Hybrid recommendation
- [ ] V5: FastAPI recommendation API
- [ ] V6: Flutter client
- [ ] V7: React Native/Web client
