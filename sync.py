import os
import requests
import re
import json
from datetime import datetime, timezone, timedelta

EST = timezone(timedelta(hours=-4))

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
    except Exception:
        return {}


def clean(name):
    return re.sub(r'[^a-zA-Z0-9\- ]', '', name).lower().replace(" ", "-")

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
    raise Exception("No submissions returned")


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
    diff = r.get("data", {}).get("question", {}).get("difficulty", "unknown").lower()

    difficulty_cache[slug] = diff
    return diff


def get_submission(slug):
    q = {
        "query": """
        query submissionList($offset: Int!, $limit: Int!, $questionSlug: String!) {
          submissionList(offset: $offset, limit: $limit, questionSlug: $questionSlug) {
            submissions { id }
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
    except Exception:
        return {"code": "", "runtime": None}

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

    d = detail.get("data", {}).get("submissionDetails", {})

    return {
        "code": d.get("code", ""),
        "runtime": d.get("runtime")
    }


def load_first_seen(file_path):
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("-- first_seen:"):
                return line.replace("-- first_seen:", "").strip()
    return None


def normalize_runtime(rt):
    if not rt:
        return None
    return str(rt).replace(" ", "")

stats = {
    "total": 0,
    "easy": 0,
    "medium": 0,
    "hard": 0,
    "last_updated": datetime.now(EST).strftime("%Y-%m-%d %H:%M:%S"),
}

for s in subs:
    title = s["title"]
    slug = s["titleSlug"]

    difficulty = get_difficulty(slug)
    submission = get_submission(slug)

    code = submission["code"]
    runtime = normalize_runtime(submission["runtime"])

    folder = f"leetcode/{difficulty}"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/{clean(title)}.sql"

    first_seen = load_first_seen(file_path)
    if first_seen is None:
        first_seen = stats["last_updated"]

    lines = [
        f"-- {title}",
        f"-- https://leetcode.com/problems/{slug}",
        f"-- difficulty: {difficulty}",
        f"-- first_seen: {first_seen}"
    ]

    if runtime:
        lines.append(f"-- runtime: {runtime}")

    lines.append("")
    lines.append(code)

    new_content = "\n".join(lines)

    old_content = ""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            old_content = f.read()

    if new_content != old_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

    stats["total"] += 1
    stats[difficulty] += 1


with open("leetcode_stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)


with open("README.md", "w", encoding="utf-8") as f:
    f.write(
f"""# LeetCode Tracker

Last updated (EST): {stats['last_updated']}

## Summary
- Total solved: {stats['total']}
- Easy: {stats['easy']}
- Medium: {stats['medium']}
- Hard: {stats['hard']}

Auto-generated via GitHub Actions.
"""
    )

print("sync complete")
