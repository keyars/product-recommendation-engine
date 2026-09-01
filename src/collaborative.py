from __future__ import annotations

from typing import List

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from recommender import INTERACTION_WEIGHTS


class CollaborativeRecommender:
    """User-based collaborative filtering recommender.

    Customers are represented by weighted product-interaction vectors.
    Similar customers are identified with cosine similarity, and their
    interactions are used to rank products the target customer has not seen.
    """

    def __init__(self, products: pd.DataFrame, interactions: pd.DataFrame) -> None:
        required_products = {"product_id", "name", "category", "brand", "price"}
        required_interactions = {"user_id", "product_id", "interaction"}

        missing_products = required_products - set(products.columns)
        missing_interactions = required_interactions - set(interactions.columns)
        if missing_products:
            raise ValueError(f"Products dataset missing columns: {sorted(missing_products)}")
        if missing_interactions:
            raise ValueError(f"Interactions dataset missing columns: {sorted(missing_interactions)}")

        self.products = products.reset_index(drop=True).copy()
        self.interactions = interactions.copy()
        self.interactions["weight"] = (
            self.interactions["interaction"].map(INTERACTION_WEIGHTS).fillna(1.0)
        )

        self.matrix = self.interactions.pivot_table(
            index="user_id",
            columns="product_id",
            values="weight",
            aggfunc="sum",
            fill_value=0.0,
        )

    def recommend(self, user_id: str, top_n: int = 5, neighbor_count: int = 3) -> List[dict]:
        if top_n <= 0:
            raise ValueError("top_n must be greater than 0")
        if neighbor_count <= 0:
            raise ValueError("neighbor_count must be greater than 0")

        if user_id not in self.matrix.index:
            return self._fallback(top_n)

        user_vector = self.matrix.loc[[user_id]]
        similarities = cosine_similarity(user_vector, self.matrix).flatten()
        similarity_series = pd.Series(similarities, index=self.matrix.index)
        similarity_series = similarity_series.drop(index=user_id)
        neighbors = similarity_series[similarity_series > 0].sort_values(ascending=False).head(neighbor_count)

        if neighbors.empty:
            return self._fallback(top_n)

        scores = pd.Series(0.0, index=self.matrix.columns)
        for neighbor_id, similarity in neighbors.items():
            scores = scores.add(self.matrix.loc[neighbor_id] * float(similarity), fill_value=0.0)

        seen_ids = set(self.matrix.loc[user_id][self.matrix.loc[user_id] > 0].index)
        ranked = scores.drop(labels=list(seen_ids), errors="ignore").sort_values(ascending=False)
        ranked = ranked[ranked > 0].head(top_n)

        if ranked.empty:
            return self._fallback(top_n)

        return [
            self._result(product_id, score, neighbors.index.tolist())
            for product_id, score in ranked.items()
        ]

    def _result(self, product_id: str, score: float, neighbors: list[str]) -> dict:
        product = self.products[self.products["product_id"] == product_id].iloc[0]
        return {
            "product_id": product.product_id,
            "name": product.name,
            "category": product.category,
            "brand": product.brand,
            "price": float(product.price),
            "score": round(float(score), 4),
            "reason": f"Customers with similar behaviour also interacted with this product.",
            "similar_users": neighbors,
        }

    def _fallback(self, top_n: int) -> List[dict]:
        popularity = (
            self.interactions.groupby("product_id", as_index=False)["weight"].sum()
            .rename(columns={"weight": "score"})
            .sort_values(["score", "product_id"], ascending=[False, True])
            .head(top_n)
        )
        result = self.products.merge(popularity, on="product_id", how="inner")
        return [
            {
                "product_id": row.product_id,
                "name": row.name,
                "category": row.category,
                "brand": row.brand,
                "price": float(row.price),
                "score": round(float(row.score), 4),
                "reason": "Popular among customers.",
                "similar_users": [],
            }
            for row in result.itertuples()
        ]
