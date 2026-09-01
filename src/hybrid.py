from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from collaborative import CollaborativeRecommender
from recommender import ProductRecommender


class HybridRecommender:
    """Combine content-based and collaborative recommendation signals."""

    def __init__(self, products: pd.DataFrame, interactions: pd.DataFrame, content_weight: float = 0.6):
        if not 0 <= content_weight <= 1:
            raise ValueError("content_weight must be between 0 and 1")

        self.products = products.reset_index(drop=True).copy()
        self.interactions = interactions.copy()
        self.content_weight = content_weight
        self.collaborative_weight = 1.0 - content_weight
        self.content = ProductRecommender(self.products, self.interactions)
        self.collaborative = CollaborativeRecommender(self.products, self.interactions)

    def recommend(self, user_id: str, top_n: int = 5) -> List[dict]:
        if top_n <= 0:
            raise ValueError("top_n must be greater than 0")

        candidate_count = max(top_n * 3, 10)
        content = self.content.recommend(user_id, candidate_count)
        collaborative = self.collaborative.recommend(user_id, candidate_count)

        content_scores = self._normalize(content)
        collaborative_scores = self._normalize(collaborative)

        all_ids = set(content_scores) | set(collaborative_scores)
        seen_ids = set(
            self.interactions.loc[
                self.interactions["user_id"] == user_id, "product_id"
            ].tolist()
        )

        combined = []
        for product_id in all_ids:
            if product_id in seen_ids:
                continue
            score = (
                self.content_weight * content_scores.get(product_id, 0.0)
                + self.collaborative_weight * collaborative_scores.get(product_id, 0.0)
            )
            combined.append((product_id, score))

        combined.sort(key=lambda item: (-item[1], item[0]))
        return [self._result(product_id, score, content_scores, collaborative_scores) for product_id, score in combined[:top_n]]

    @staticmethod
    def _normalize(recommendations: List[dict]) -> dict[str, float]:
        if not recommendations:
            return {}
        values = {item["product_id"]: float(item["score"]) for item in recommendations}
        maximum = max(values.values())
        if maximum <= 0:
            return {key: 0.0 for key in values}
        return {key: value / maximum for key, value in values.items()}

    def _result(self, product_id: str, score: float, content_scores: dict, collaborative_scores: dict) -> dict:
        product = self.products[self.products["product_id"] == product_id].iloc[0]
        content_score = content_scores.get(product_id, 0.0)
        collaborative_score = collaborative_scores.get(product_id, 0.0)

        if content_score > 0 and collaborative_score > 0:
            reason = "Matches your product interests and is also supported by similar customer behaviour."
        elif content_score > 0:
            reason = "Matches products and categories you have interacted with."
        else:
            reason = "Customers with similar behaviour also interacted with this product."

        return {
            "product_id": product.product_id,
            "name": product.name,
            "category": product.category,
            "brand": product.brand,
            "price": float(product.price),
            "score": round(float(score), 4),
            "content_score": round(float(content_score), 4),
            "collaborative_score": round(float(collaborative_score), 4),
            "reason": reason,
        }


def load_hybrid_recommender(base_dir: str | Path, content_weight: float = 0.6) -> HybridRecommender:
    base_path = Path(base_dir)
    products = pd.read_csv(base_path / "data" / "products.csv")
    interactions = pd.read_csv(base_path / "data" / "user_interactions.csv")
    return HybridRecommender(products, interactions, content_weight=content_weight)
