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

# 1. Get recent accepted submissions
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

# 2. For each problem, fetch latest submission detail
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
              submissionDetails(submissionId: $submissionId) {
                code
              }
            }
            """,
            "variables": {"submissionId": sub_id}
        },
        headers=headers
    ).json()

    return detail["data"]["submissionDetails"]["code"]

# 3. Save files
for s in subs:
    title = s["title"]
    slug = s["titleSlug"]

    sql = get_sql(slug)

    folder = "leetcode/medium"  # default; can be improved later

    filename = f"{folder}/{clean(title)}.sql"

    os.makedirs(folder, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"-- {title}\n-- https://leetcode.com/problems/{slug}/\n\n")
        f.write(sql)

print("sync complete")
