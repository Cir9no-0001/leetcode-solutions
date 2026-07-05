import os
import requests
import re
from collections import defaultdict
from datetime import datetime

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

subs = (
    data.get("data", {})
        .get("recentAcSubmissionList", [])
)

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


def get_sql(slug):
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
        return "-- SQL not found"

    detail = post({
        "query": """
        query submissionDetails($submissionId: Int!) {
          submissionDetails(submissionId: $submissionId) {
            code
          }
        }
        """,
        "variables": {"submissionId": sub_id}
    })

    return (
        detail.get("data", {})
              .get("submissionDetails", {})
              .get("code", "-- SQL not found")
    )


for s in subs:
    title = s["title"]
    slug = s["titleSlug"]

    difficulty = get_difficulty(slug).lower()
    folder = f"leetcode/{difficulty}"

    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/{clean(title)}.sql"

    sql = get_sql(slug)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"-- {title}\n")
        f.write(f"-- https://leetcode.com/problems/{slug}\n")
        f.write(f"-- solved: {timestamp}\n\n")
        f.write(sql)


def update_readme():
    base_dir = "leetcode"

    stats = defaultdict(int)
    total = 0

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".sql"):
                total += 1
                difficulty = os.path.basename(root).lower()

                if difficulty in ["easy", "medium", "hard"]:
                    stats[difficulty] += 1

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    content = f"""# LeetCode Sync

## Stats

- Total Solved: {total}
- Easy: {stats['easy']}
- Medium: {stats['medium']}
- Hard: {stats['hard']}

## Last Updated

{timestamp}

## Structure

leetcode/
- easy/
- medium/
- hard/
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)


update_readme()
print("sync complete")
