import os
import requests
import re

username = os.environ["LEETCODE_USERNAME"]

HEADERS = {
    "content-type": "application/json",
    "referer": "https://leetcode.com",
}

def get_subs():
    q = {
        "query": """
        query recentAcSubmissions($username: String!) {
          recentAcSubmissionList(username: $username) {
            title
            titleSlug
          }
        }
        """,
        "variables": {"username": username}
    }

    return requests.post(
        "https://leetcode.com/graphql",
        json=q,
        headers=HEADERS
    ).json()["data"]["recentAcSubmissionList"]

def get_difficulty(slug):
    q = {
        "query": """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            difficulty
          }
        }
        """,
        "variables": {"titleSlug": slug}
    }

    r = requests.post(
        "https://leetcode.com/graphql",
        json=q,
        headers=HEADERS
    ).json()

    return r["data"]["question"]["difficulty"].lower()

def clean(s):
    return re.sub(r'[^a-zA-Z0-9\- ]', '', s).lower().replace(" ", "-")

subs = get_subs()

for s in subs:
    title = s["title"]
    slug = s["titleSlug"]

    difficulty = get_difficulty(slug)
    folder = f"leetcode/{difficulty}"

    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/{clean(title)}.sql"

    code = "-- SQL code not available via public LeetCode API"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"-- {title}\n")
        f.write(f"-- https://leetcode.com/problems/{slug}/\n\n")
        f.write(code)

print("sync complete")
