from src.kaggle_pcosdata import load_pcos_data
from src.reddit_api import fetch_reddit_posts, count_reddit_symptoms

def run_tests():
    print("Running tests...\n")

    df = load_pcos_data()
    assert df is not None
    assert len(df) > 0
    print("Kaggle data test passed")

    posts = fetch_reddit_posts(total_limit=10)
    assert isinstance(posts, list)
    assert len(posts) > 0
    print("Reddit API test passed")

    result = count_reddit_symptoms(posts)
    assert "Symptom" in result.columns
    print("Reddit processing test passed")

    print("\nAll tests passed!")

if __name__ == "__main__":
    run_tests()
