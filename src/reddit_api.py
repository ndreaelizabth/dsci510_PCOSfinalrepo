import requests

def fetch_reddit_posts(subreddit="PCOS", limit=100):
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    headers = {"User-Agent": "dsci510-project"}

    response = requests.get(url, headers=headers)
    data = response.json()

    posts = []

    for post in data["data"]["children"]:
        post_data = post["data"]
        posts.append({
            "title": post_data.get("title"),
            "selftext": post_data.get("selftext"),
            "score": post_data.get("score"),
            "num_comments": post_data.get("num_comments")
        })

    return posts


if __name__ == "__main__":
    posts = fetch_reddit_posts(limit=5)

    print(f"Fetched {len(posts)} posts\n")

    for i, post in enumerate(posts[:5]):
        print(f"Post {i+1}")
        print(f"Title: {post['title']}")
        print(f"Score: {post['score']}")
        print(f"Selftext: {post['selftext']}...")  # Print first 100 characters of selftext
        print(f"Comments: {post['num_comments']}")
        print("-" * 30)