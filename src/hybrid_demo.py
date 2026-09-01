from pathlib import Path

from hybrid import load_hybrid_recommender


if __name__ == "__main__":
    recommender = load_hybrid_recommender(Path(__file__).resolve().parents[1])

    for user_id in ["U001", "U003", "UNKNOWN"]:
        print(f"\nHybrid recommendations for {user_id}:")
        for index, product in enumerate(recommender.recommend(user_id, top_n=3), 1):
            print(f"{index}. {product['name']} ({product['category']})")
            print(f"   Hybrid score: {product['score']}")
            print(f"   Content score: {product['content_score']}")
            print(f"   Collaborative score: {product['collaborative_score']}")
            print(f"   Why: {product['reason']}")
