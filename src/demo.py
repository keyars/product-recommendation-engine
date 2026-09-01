from pathlib import Path

import pandas as pd

from collaborative import CollaborativeRecommender
from recommender import load_recommender


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    products = pd.read_csv(base_dir / "data" / "products.csv")
    interactions = pd.read_csv(base_dir / "data" / "user_interactions.csv")

    content_recommender = load_recommender(base_dir)
    collaborative_recommender = CollaborativeRecommender(products, interactions)

    for user_id in ["U001", "U003", "UNKNOWN"]:
        print(f"\n=== {user_id} ===")

        print("\nContent-based:")
        for index, product in enumerate(content_recommender.recommend(user_id, top_n=3), 1):
            print(f"{index}. {product['name']} - {product['score']}")
            print(f"   Why: {product['reason']}")

        print("\nCollaborative:")
        for index, product in enumerate(collaborative_recommender.recommend(user_id, top_n=3), 1):
            print(f"{index}. {product['name']} - {product['score']}")
            print(f"   Why: {product['reason']}")
