from pathlib import Path

from recommender import load_recommender


if __name__ == "__main__":
    recommender = load_recommender(Path(__file__).resolve().parents[1])

    for user_id in ["U001", "U003", "UNKNOWN"]:
        print(f"\nRecommendations for {user_id}:")
        for index, product in enumerate(recommender.recommend(user_id, top_n=3), 1):
            print(f"{index}. {product['name']} ({product['category']})")
            print(f"   Score: {product['score']}")
            print(f"   Why: {product['reason']}")
