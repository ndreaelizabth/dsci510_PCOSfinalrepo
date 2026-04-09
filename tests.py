from src.reddit_api import fetch_reddit_posts


def test_fetch_reddit_posts():
    posts = fetch_reddit_posts(limit=3)
    assert isinstance(posts, list)

    if len(posts) > 0:
        assert "title" in posts[0]
        assert "score" in posts[0]
        assert "num_comments" in posts[0]


if __name__ == "__main__":
    test_fetch_reddit_posts()
    print("tests passed")
