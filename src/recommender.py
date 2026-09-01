from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProductRecommender:
    """Simple content-based product recommendation engine."""

    def __init__(self, products: pd.DataFrame, interactions: pd.DataFrame) -> None:
        required_products = {"product_id", "name", "category", "brand", "tags"}
        required_interactions = {"user_id", "product_id", "weight"}

        missing_products = required_products - set(products.columns)
        missing_interactions = required_interactions - set(interactions.columns)
        if missing_products:
            raise ValueError(f"Products dataset missing columns: {sorted(missing_products)}")
        if missing_interactions:
            raise ValueError(
                f"Interactions dataset missing columns: {sorted(missing_interactions)}"
            )

        self.products = products.reset_index(drop=True).copy()
        self.interactions = interactions.copy()
        self.products["profile"] = (
            self.products["category"].fillna("")
            + " "
            + self.products["brand"].fillna("")
            + " "
            + self.products["tags"].fillna("")
        )
        self.vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
        self.product_matrix = self.vectorizer.fit_transform(self.products["profile"])

    def recommend(self, user_id: str, top_n: int = 5) -> List[dict]:
        if top_n <= 0:
            raise ValueError("top_n must be greater than 0")

        user_interactions = self.interactions[
            self.interactions["user_id"] == user_id
        ].copy()
        if user_interactions.empty:
            return self._popular_fallback(top_n)

        user_vector = None
        for row in user_interactions.itertuples():
            matches = self.products.index[self.products["product_id"] == row.product_id]
            if len(matches) == 0:
                continue
            vector = self.product_matrix[matches[0]] * float(row.weight)
            user_vector = vector if user_vector is None else user_vector + vector

        if user_vector is None:
            return self._popular_fallback(top_n)

        scores = cosine_similarity(user_vector, self.product_matrix).flatten()
        seen_ids = set(user_interactions["product_id"].tolist())
        ranked = self.products.copy()
        ranked["score"] = scores
        ranked = ranked[~ranked["product_id"].isin(seen_ids)]
        ranked = ranked.sort_values(["score", "product_id"], ascending=[False, True]).head(top_n)

        return [self._result(row.product_id, row.name, row.category, row.brand, row.price, row.score)
                for row in ranked.itertuples()]

    def _popular_fallback(self, top_n: int) -> List[dict]:
        popularity = (
            self.interactions.groupby("product_id", as_index=False)["weight"].sum()
            .rename(columns={"weight": "score"})
        )
        candidates = self.products.merge(popularity, on="product_id", how="left")
        candidates["score"] = candidates["score"].fillna(0.0)
        candidates = candidates.sort_values(["score", "product_id"], ascending=[False, True]).head(top_n)
        return [self._result(row.product_id, row.name, row.category, row.brand, row.price, row.score)
                for row in candidates.itertuples()]

    @staticmethod
    def _result(product_id, name, category, brand, price, score) -> dict:
        return {
            "product_id": product_id,
            "name": name,
            "category": category,
            "brand": brand,
            "price": float(price),
            "score": round(float(score), 4),
        }


def load_recommender(base_dir: str | Path) -> ProductRecommender:
    base_path = Path(base_dir)
    return ProductRecommender(
        pd.read_csv(base_path / "data" / "products.csv"),
        pd.read_csv(base_path / "data" / "user_interactions.csv"),
    )
