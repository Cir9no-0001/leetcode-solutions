import os
import requests
import re

username = os.environ["LEETCODE_USERNAME"]

HEADERS = {
    "content-type": "application/json",
    "referer": "https://leetcode.com",
}
def get_recent_submissions():
    query = {
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

    r = requests.post(
        "https://leetcode.com/graphql",
        json=query,
        headers=HEADERS
    ).json()

    return r["data"]["recentAcSubmissionList"]

def get_difficulty(slug):
    query = {
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
        json=query,
        headers=HEADERS
    ).json()

    return r["data"]["question"]["difficulty"].lower()

def get_code_fallback(slug):
    """
    IMPORTANT:
    LeetCode does NOT reliably expose full submission code via public API.
    So we use a safe placeholder approach.
    """
    return "-- SQL code not auto-retrievable from LeetCode API reliably"

def clean(name):
    return re.sub(r'[^a-zA-Z0-9\- ]', '', name).lower().replace(" ", "-")

subs = get_recent_submissions()

for s in subs:
    title = s["title"]
    slug = s["titleSlug"]

    difficulty = get_difficulty(slug)

    folder = f"leetcode/{difficulty}"
    os.makedirs(folder, exist_ok=True)

    filename = f"{folder}/{clean(title)}.sql"

    code = get_code_fallback(slug)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"-- {title}\n")
        f.write(f"-- https://leetcode.com/problems/{slug}/\n\n")
        f.write(code)

print("sync complete")
