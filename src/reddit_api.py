# AI generated: portions of this file were created with assistance of ChatGPT

import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

from config import (
    REDDIT_SUBREDDIT,
    REDDIT_TOTAL_LIMIT,
    REDDIT_BATCH_SIZE,
    REDDIT_USER_AGENT,
    REDDIT_SYMPTOM_CHART,
)

PLOT_SIZE = (10, 6)
BAR_COLOR = "lavender"
REQUEST_DELAY = 1


def fetch_reddit_posts(
    subreddit=REDDIT_SUBREDDIT,
    total_limit=REDDIT_TOTAL_LIMIT,
    batch_size=REDDIT_BATCH_SIZE
):
    headers = {"User-Agent": REDDIT_USER_AGENT}
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

        time.sleep(REQUEST_DELAY)

    return posts


def count_reddit_symptoms(posts):
    symptom_keywords = {
        "Menstrual irregularity": [
            "irregular period",
            "irregular periods",
            "missed period",
            "missed periods",
            "late period",
            "late periods",
            "no period",
            "no periods",
            "period stopped",
            "periods stopped",
            "long cycle",
            "long cycles",
            "short cycle",
            "short cycles",
            "cycle length",
            "irregular cycle",
            "irregular cycles",
            "menstrual irregularity",
            "menstrual cycle",
            "period cycle"
        ],
        "Weight gain": [
            "weight gain",
            "gained weight",
            "gaining weight",
            "put on weight",
            "can't lose weight",
            "cant lose weight",
            "cannot lose weight",
            "hard to lose weight",
            "weight won't budge",
            "weight wont budge",
            "struggling to lose weight",
            "losing weight is hard"
        ],
        "Hair growth": [
            "facial hair",
            "chin hair",
            "upper lip hair",
            "body hair",
            "excess hair",
            "hair growth",
            "hirsutism",
            "thick hair on face"
        ],
        "Skin darkening": [
            "dark skin",
            "dark patches",
            "skin darkening",
            "dark neck",
            "neck darkening",
            "dark underarms",
            "acanthosis",
            "acanthosis nigricans"
        ],
        "Hair loss": [
            "hair loss",
            "losing hair",
            "hair falling out",
            "thinning hair",
            "bald spots",
            "hair shedding",
            "losing so much hair"
        ],
        "Pimples": [
            "acne",
            "pimples",
            "breakout",
            "breakouts",
            "cystic acne",
            "bad acne",
            "skin breaking out"
        ],
    }

    counts = {symptom: 0 for symptom in symptom_keywords}

    for post in posts:
        text = f"{post.get('title', '')} {post.get('selftext', '')}".lower()

        for symptom, keywords in symptom_keywords.items():
            if any(keyword in text for keyword in keywords):
                counts[symptom] += 1

    result_df = pd.DataFrame(
        list(counts.items()),
        columns=["Symptom", "Count"]
    )

    if len(posts) > 0:
        result_df["Percentage_of_Posts"] = (result_df["Count"] / len(posts)) * 100
    else:
        result_df["Percentage_of_Posts"] = 0

    result_df = result_df.sort_values(
        by="Percentage_of_Posts",
        ascending=False
    )

    return result_df


def plot_reddit_symptoms(result_df):
    plt.figure(figsize=PLOT_SIZE)

    plt.barh(
        result_df["Symptom"],
        result_df["Percentage_of_Posts"],
        color=BAR_COLOR
    )

    plt.xlabel("Percentage of r/PCOS posts mentioning symptom (%)")
    plt.ylabel("Patient-reported observable symptom category")
    plt.title("Reddit r/PCOS: Most Discussed Observable PCOS Symptoms")

    for i, value in enumerate(result_df["Percentage_of_Posts"]):
        plt.text(value + 0.3, i, f"{value:.1f}%", va="center")

    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(REDDIT_SYMPTOM_CHART)
    plt.close()


if __name__ == "__main__":
    posts = fetch_reddit_posts()

    print(f"Fetched {len(posts)} Reddit posts.\n")

    print("Sample posts:")
    for i, post in enumerate(posts[:5]):
        print(f"Post {i + 1}")
        print(f"Title: {post['title']}")
        print(f"Body: {post['selftext'][:150] if post['selftext'] else ''}...")
        print(f"Comments count: {post['num_comments']}")
        print("-" * 40)

    result = count_reddit_symptoms(posts)

    print("\nReddit symptom ranking:")
    print(result)

    plot_reddit_symptoms(result)