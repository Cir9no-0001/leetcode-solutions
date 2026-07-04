import os
import requests
import re

username = os.environ["LEETCODE_USERNAME"]
session = os.environ["LEETCODE_SESSION"]

headers = {
    "cookie": f"LEETCODE_SESSION={session}",
    "referer": "https://leetcode.com",
    "content-type": "application/json"
}

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

subs = requests.post(
    "https://leetcode.com/graphql",
    json=query,
    headers=headers
).json()["data"]["recentAcSubmissionList"]


def clean(name):
    return re.sub(r'[^a-zA-Z0-9\- ]', '', name).lower().replace(" ", "-")

difficulty_cache = {}

def get_difficulty(slug):
    if slug in difficulty_cache:
        return difficulty_cache[slug]

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

    try:
        r = requests.post(
            "https://leetcode.com/graphql",
            json=q,
            headers=headers,
            timeout=5
        ).json()

        diff = r["data"]["question"]["difficulty"].lower()
    except:
        diff = "unknown"

    difficulty_cache[slug] = diff
    return diff
    
def get_sql(slug):
    q = {
        "query": """
        query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!) {
          submissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug) {
            submissions {
              id
            }
          }
        }
        """,
        "variables": {
            "offset": 0,
            "limit": 1,
            "questionSlug": slug
        }
    }

    r = requests.post(
        "https://leetcode.com/graphql",
        json=q,
        headers=headers
    ).json()

    try:
        sub_id = r["data"]["submissionList"]["submissions"][0]["id"]
    except:
        return "-- SQL not found"

    detail = requests.post(
        "https://leetcode.com/graphql",
        json={
            "query": """
            query submissionDetails($submissionId: Int!) {
             
