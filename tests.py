from src.reddit_api import fetch_reddit_posts
from src.kaggle_pcosdata import load_pcos_data


def test_fetch_reddit_posts():
    posts = fetch_reddit_posts(limit=3)
    assert isinstance(posts, list)

    if len(posts) > 0:
        assert "title" in posts[0]
        assert "score" in posts[0]
        assert "num_comments" in posts[0]


def test_load_pcos_data():
    df = load_pcos_data()
    assert df is not None
    assert df.shape[0] == 541


if __name__ == "__main__":
    test_fetch_reddit_posts()
    test_load_pcos_data()
    print("tests passed")