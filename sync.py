import os
import requests
import re

username = os.environ.get("LEETCODE_USERNAME")
session = os.environ.get("LEETCODE_SESSION")

if not username or not session:
    raise Exception("Missing LEETCODE_USERNAME or LEETCODE_SESSION")

headers = {
    "cookie": f"LEETCODE_SESSION={session}",
    "referer": "https://leetcode.com",
    "content-type": "application/json"
}


def post(query):
    try:
        r = requests.post(
            "https://leetcode.com/graphql",
            json=query,
            headers=headers,
            timeout=10
        )
        return r.json()
    except Exception as e:
        print("Request failed:", e)
        return {}


# Get recent accepted submissions
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

data = post(query)

subs = data.get("data", {}).get("recentAcSubmissionList", [])

if not subs:
    raise Exception("No submissions returned from LeetCode API")


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

    r = post(q)

    diff = (
        r.get("data", {})
         .get("question", {})
         .get("difficulty", "unknown")
         .lower()
    )

    difficulty_cache[slug] = diff
    return diff


def get_submission(slug):
    q = {
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

    r = post(q)

    try:
        sub_id = r["data"]["submissionList"]["submissions"][0]["id"]
    except:
        return {
            "code": "-- SQL not found",
            "runtime": None
        }

    detail = post({
        "query": """
        query submissionDetails($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
            runtime
          }
        }
        """,
        "variables": {"submissionId": sub_id}
    })

    data = detail.get("data", {}).get("submissionDetails", {})

    return {
        "code": data.get("code", "-- SQL not found"),
        "runtime": data.get("runtime")
    }


for s in subs:
    title = s["title"]
    slug = s["titleSlug"]

    difficulty = get_difficulty(slug)

    folder = f"leetcode/{difficulty}"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/{clean(title)}.sql"

    submission = get_submission(slug)
    sql = submission["code"]
    runtime = submission["runtime"]

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"-- {title}\n")
        f.write(f"-- https://leetcode.com/problems/{slug}\n")
        f.write(f"-- difficulty: {difficulty}\n")

        if runtime:
            f.write(f"-- runtime: {runtime}\n")

        f.write("\n")
        f.write(sql)

print("sync complete")
