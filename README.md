# Product Recommendation Engine

A small, practical product recommendation engine demonstrating how a simple ML model can be integrated into an e-commerce application.

## V1 Goal

Recommend products to a customer based on previous product interactions.

## How V1 Works

V1 uses a **content-based recommendation approach**:

1. Build a profile for each product from category, brand, and tags.
2. Convert product profiles into TF-IDF vectors.
3. Build a weighted customer preference vector from interaction history.
4. Calculate cosine similarity between the customer profile and products.
5. Return the highest-scoring products the customer has not already interacted with.
6. Use popularity as a fallback for unknown users.

Purchase interactions have a stronger weight than views in the sample data.

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

## Example Use Case

A customer who has purchased running socks and energy gels and viewed running shoes can receive recommendations for other running-related products that match those interests.

## Roadmap

- [x] V1: Content-based recommendation
- [ ] V2: Collaborative filtering
- [ ] V3: Hybrid recommendation
- [ ] V4: FastAPI recommendation API
- [ ] V5: Flutter client
- [ ] V6: React Native/Web client
