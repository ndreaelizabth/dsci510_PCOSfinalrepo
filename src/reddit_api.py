import requests
import time
import pandas as pd
import matplotlib.pyplot as plt


def fetch_reddit_posts(subreddit="PCOS", total_limit=300, batch_size=100):
    headers = {"User-Agent": "dsci510-project"}
    posts = []
    after = None

    while len(posts) < total_limit:
        remaining = total_limit - len(posts)
        current_batch_size = min(batch_size, remaining)

        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={current_batch_size}"
        if after:
            url += f"&after={after}"

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        children = data["data"]["children"]

        if not children:
            break

        for post in children:
            post_data = post["data"]
            posts.append({
                "title": post_data.get("title", ""),
                "selftext": post_data.get("selftext", ""),
                "score": post_data.get("score"),
                "num_comments": post_data.get("num_comments"),
                "created_utc": post_data.get("created_utc")
            })

        after = data["data"].get("after")
        if not after:
            break

        time.sleep(1)

    return posts


def count_reddit_symptoms(posts):
    
    symptom_keywords = {

    "Cycle irregularity": [
        "irregular period", "irregular periods", "missed period",
        "late period", "no period", "skipped period",
        "cycle is off", "cycle irregular", "cycle problems",
        "period hasn't come", "amenorrhea"
    ],

    "Weight gain": [
        "weight gain", "gained weight", "put on weight",
        "can't lose weight", "hard to lose weight",
        "weight won't budge", "struggling to lose weight",
        "gaining weight", "losing weight is hard"
    ],

    "Hair growth": [
        "facial hair", "chin hair", "upper lip hair",
        "body hair", "excess hair", "hair growth",
        "hirsutism", "thick hair on face"
    ],

    "Skin darkening": [
        "dark skin", "dark patches", "skin darkening",
        "dark neck", "neck darkening", "acanthosis",
        "dark underarms"
    ],

    "Hair loss": [
        "hair loss", "losing hair", "hair falling out",
        "thinning hair", "bald spots", "hair shedding",
        "losing so much hair"
    ],

    "Pimples / acne": [
        "acne", "pimples", "breakouts",
        "cystic acne", "bad acne", "skin breaking out"
    ],

    "Fast food / diet": [
        "fast food", "junk food", "bad diet",
        "eating unhealthy", "diet issues", "sugar cravings",
        "craving sugar", "carbs", "processed food"
    ],

    "Exercise / lifestyle": [
        "exercise", "working out", "workout",
        "gym", "walking", "walk",
        "sedentary", "not active"
    ]
}

    counts = {symptom: 0 for symptom in symptom_keywords}

    for post in posts:
        text = f"{post.get('title', '')} {post.get('selftext', '')}".lower()

        for symptom, keywords in symptom_keywords.items():
            if any(keyword in text for keyword in keywords):
                counts[symptom] += 1

    result_df = pd.DataFrame(list(counts.items()), columns=["Symptom", "Count"])
    result_df["Percentage_of_Posts"] = (result_df["Count"] / len(posts)) * 100
    result_df = result_df.sort_values(by="Count", ascending=False)

    return result_df


def plot_reddit_symptoms(result_df):
    plt.figure(figsize=(10, 6))
    plt.barh(result_df["Symptom"], result_df["Count"])
    plt.xlabel("Number of Reddit Posts Mentioning Symptom")
    plt.ylabel("Symptom")
    plt.title("Most Common Symptoms Mentioned in r/PCOS Posts")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig("reddit_symptom_prevalence.png")
    plt.show()


if __name__ == "__main__":
    posts = fetch_reddit_posts(total_limit=300)

    print(f"Fetched {len(posts)} Reddit posts.\n")

    print("Sample posts:")
    for i, post in enumerate(posts[:5]):
        print(f"Post {i+1}")
        print(f"Title: {post['title']}")
        print(f"Body: {post['selftext'][:150] if post['selftext'] else ''}...")
        print(f"Comments count: {post['num_comments']}")
        print("-" * 40)

    result = count_reddit_symptoms(posts)

    print("\nReddit symptom ranking:")
    print(result)

    plot_reddit_symptoms(result)