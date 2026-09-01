from pathlib import Path

import pandas as pd
import pytest

from src.recommender import INTERACTION_WEIGHTS, ProductRecommender, load_recommender


BASE_DIR = Path(__file__).resolve().parents[1]


def test_interaction_weights_are_defined():
    assert INTERACTION_WEIGHTS["view"] < INTERACTION_WEIGHTS["wishlist"]
    assert INTERACTION_WEIGHTS["wishlist"] < INTERACTION_WEIGHTS["cart"]
    assert INTERACTION_WEIGHTS["cart"] < INTERACTION_WEIGHTS["purchase"]


def test_recommendations_exclude_seen_products():
    recommender = load_recommender(BASE_DIR)
    recommendations = recommender.recommend("U001", top_n=5)
    ids = {item["product_id"] for item in recommendations}

    assert not {"P001", "P004", "P007", "P008"}.intersection(ids)


def test_recommendations_are_ranked():
    recommender = load_recommender(BASE_DIR)
    recommendations = recommender.recommend("U003", top_n=5)
    scores = [item["score"] for item in recommendations]

    assert scores == sorted(scores, reverse=True)


def test_recommendations_include_explanation():
    recommender = load_recommender(BASE_DIR)
    recommendations = recommender.recommend("U001", top_n=3)

    assert recommendations
    assert all(item["reason"] for item in recommendations)


def test_unknown_user_uses_popularity_fallback():
    recommender = load_recommender(BASE_DIR)
    recommendations = recommender.recommend("UNKNOWN", top_n=3)

    assert len(recommendations) == 3
    assert all("product_id" in item for item in recommendations)
    assert all(item["reason"] == "Popular among customers." for item in recommendations)


def test_invalid_top_n_is_rejected():
    recommender = load_recommender(BASE_DIR)

    with pytest.raises(ValueError):
        recommender.recommend("U001", top_n=0)


def test_missing_required_column_is_rejected():
    products = pd.DataFrame(
        [{"product_id": "P1", "name": "Test", "category": "Running", "brand": "Test", "tags": "run"}]
    )
    interactions = pd.DataFrame(
        [{"user_id": "U1", "product_id": "P1", "interaction": "view"}]
    )

    with pytest.raises(ValueError):
        ProductRecommender(products, interactions)
