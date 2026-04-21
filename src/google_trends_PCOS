from pytrends.request import TrendReq
import pandas as pd


def fetch_google_trends_data():
    keywords = [
        "PCOS",
        "polycystic ovary syndrome",
        "PCOS symptoms",
        "irregular periods",
        "hormonal imbalance",
        "ovarian cysts",
        "PCOS diagnosis"
    ]

    pytrends = TrendReq(hl="en-US", tz=360)
    all_data = []

    for keyword in keywords:
        pytrends.build_payload([keyword], cat=0, timeframe="today 5-y", geo="", gprop="")
        data = pytrends.interest_over_time()

        if not data.empty:
            data = data.reset_index()
            data["keyword"] = keyword
            data = data.rename(columns={keyword: "interest_score"})

            if "isPartial" in data.columns:
                data = data.drop(columns=["isPartial"])

            all_data.append(data)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        return final_df
    else:
        return pd.DataFrame(columns=["date", "interest_score", "keyword"])


def fetch_related_queries(top_n=5):
    keywords = [
        "PCOS",
        "polycystic ovary syndrome",
        "PCOS symptoms",
        "irregular periods",
        "hormonal imbalance",
        "ovarian cysts",
        "PCOS diagnosis"
    ]

    pytrends = TrendReq(hl="en-US", tz=360)
    related_queries_data = []

    for keyword in keywords:
        pytrends.build_payload([keyword], cat=0, timeframe="today 5-y", geo="", gprop="")
        related = pytrends.related_queries()

        if keyword in related and related[keyword] is not None:
            top_queries = related[keyword].get("top")

            if top_queries is not None and not top_queries.empty:
                top_queries = top_queries.copy()
                top_queries = top_queries.head(top_n)
                top_queries = top_queries[["query", "value"]]
                top_queries = top_queries.rename(columns={"value": "related_query_score"})
                top_queries["source_keyword"] = keyword
                related_queries_data.append(top_queries)

    if related_queries_data:
        return pd.concat(related_queries_data, ignore_index=True)
    else:
        return pd.DataFrame(columns=["query", "related_query_score", "source_keyword"])


if __name__ == "__main__":
    df = fetch_google_trends_data()
    print("Google Trends data loaded successfully.")
    print(f"Shape: {df.shape}")
    print(df.head())

    related_df = fetch_related_queries(top_n=5)
    print("\nRelated queries loaded successfully.")
    print(f"Shape: {related_df.shape}")
    print(related_df.head(10))