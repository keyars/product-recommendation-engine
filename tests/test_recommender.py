from pathlib import Path

from src.recommender import load_recommender


BASE_DIR = Path(__file__).resolve().parents[1]


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


def test_unknown_user_uses_fallback():
    recommender = load_recommender(BASE_DIR)
    recommendations = recommender.recommend("UNKNOWN", top_n=3)

    assert len(recommendations) == 3
    assert all("product_id" in item for item in recommendations)
