import os
import requests
import re

username = os.environ["LEETCODE_USERNAME"]

HEADERS = {
    "content-type": "application/json",
    "referer": "https://leetcode.com",
}

# 1. Get recent accepted submissions
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


# 2. Get difficulty (IMPORTANT FIX)
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


# 3. Get latest accepted submission code (best-effort)
def get_submission_code(slug):
    query = {
        "query": """
        query submissionList($offset: Int!, $limit: Int!, $questionSlug: String!) {
          submissionList(offset: $offset, limit: $limit, questionSlug: $questionSlug) {
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
        json=query,
        headers=HEADERS
    ).json()

    try:
        sub_id = r["data"]["submissionList"]["submissions"][0]["id"]
    except:
        return "-- code not found"

    detail = {
        "query": """
        query submissionDetails($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
          }
        }
        """,
        "variables": {"submissionId": sub_id}
    }

    r = requests.post(
        "https://leetcode.com/graphql",
        json=detail,
        headers=HEADERS
    ).json()

    return r["data"]["submissionDetails"]["code"]


# 4. clean filename
def clean(name):
    return re.sub(r'[^a-zA-Z0-9\- ]', '', name).lower().replace(" ", "-")


# 5. main
subs = get_recent_submissions()

for s in subs:
    title = s["title"]
    slug = s["titleSlug"]

    difficulty = get_difficulty(slug)

    folder = f"leetcode/{difficulty}"
    os.makedirs(folder, exist_ok=True)

    code = get_submission_code(slug)

    filename = f"{folder}/{clean(title)}.sql"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"-- {title}\n")
        f.write(f"-- https://leetcode.com/problems/{slug}/\n\n")
        f.write(code)

print("sync complete")
