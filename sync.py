```python
import os
import requests
import re
import json
from datetime import datetime
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Toronto")

username = os.environ.get("LEETCODE_USERNAME")
session = os.environ.get("LEETCODE_SESSION")

if not username or not session:
    raise Exception("Missing LEETCODE_USERNAME or LEETCODE_SESSION")


headers = {
    "cookie": f"LEETCODE_SESSION={session}",
    "referer": "https://leetcode.com",
    "content-type": "application/json"
}


META_FILE = "leetcode_meta.json"


def post(query):
    try:
        response = requests.post(
            "https://leetcode.com/graphql",
            json=query,
            headers=headers,
            timeout=10
        )
        return response.json()
    except Exception as e:
        print("Request error:", e)
        return {}


def clean(name):
    return (
        re.sub(r"[^a-zA-Z0-9\- ]", "", name)
        .lower()
        .replace(" ", "-")
    )


def now():
    return datetime.now(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def extract_notes(content):
    lines = content.splitlines()

    start = None
    end = None

    for i, line in enumerate(lines):
        if line.strip() == "-- NOTES START":
            start = i
        if line.strip() == "-- NOTES END":
            end = i

    if start is not None and end is not None:
        return lines[start:end + 1]

    return None


# -------------------------
# Load metadata
# -------------------------

if os.path.exists(META_FILE):
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    meta = {}


# -------------------------
# Get submissions
# -------------------------

query = {
    "query": """
    query recentAcSubmissions($username: String!) {
      recentAcSubmissionList(username: $username) {
        title
        titleSlug
      }
    }
    """,
    "variables": {
        "username": username
    }
}


data = post(query)

subs = (
    data.get("data", {})
        .get("recentAcSubmissionList", [])
)

if not subs:
    raise Exception("No submissions returned")


# -------------------------
# Difficulty lookup
# -------------------------

difficulty_cache = {}


def get_difficulty(slug):

    if slug in difficulty_cache:
        return difficulty_cache[slug]


    query = {
        "query": """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            difficulty
          }
        }
        """,
        "variables": {
            "titleSlug": slug
        }
    }


    data = post(query)

    difficulty = (
        data.get("data", {})
            .get("question", {})
            .get("difficulty", "unknown")
            .lower()
    )


    difficulty_cache[slug] = difficulty

    return difficulty



# -------------------------
# Submission details
# -------------------------

def get_submission(slug):

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


    data = post(query)


    try:
        submission_id = (
            data["data"]
            ["submissionList"]
            ["submissions"][0]
            ["id"]
        )

    except:
        return {
            "code": "",
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
        "variables": {
            "submissionId": int(submission_id)
        }
    })


    result = (
        detail.get("data", {})
        .get("submissionDetails", {})
    )


    return {
        "code": result.get("code", ""),
        "runtime": result.get("runtime")
    }



# -------------------------
# Stats
# -------------------------

stats = {
    "total": 0,
    "easy": 0,
    "medium": 0,
    "hard": 0,
    "last_updated": now()
}



# -------------------------
# Generate files
# -------------------------

for submission in subs:

    title = submission["title"]
    slug = submission["titleSlug"]

    difficulty = get_difficulty(slug)

    data = get_submission(slug)

    code = data["code"]
    runtime = data["runtime"]


    # FIRST SEEN FIX
    if slug not in meta:
        meta[slug] = {
            "first_seen": now()
        }


    first_seen = meta[slug]["first_seen"]



    folder = f"leetcode/{difficulty}"

    os.makedirs(folder, exist_ok=True)


    file_path = f"{folder}/{clean(title)}.sql"


    old_content = ""

    old_notes = None


    if os.path.exists(file_path):

        with open(file_path, "r", encoding="utf-8") as f:
            old_content = f.read()

        old_notes = extract_notes(old_content)



    content = [
        f"-- {title}",
        f"-- https://leetcode.com/problems/{slug}",
        f"-- difficulty: {difficulty}",
        f"-- first_seen: {first_seen}",
    ]


    if runtime:
        content.append(
            f"-- runtime: {runtime}"
        )


    content.append("")


    if old_notes:

        content.extend(old_notes)

    else:

        content.extend([
            "-- NOTES START",
            "-- write your notes here",
            "-- NOTES END"
        ])


    content.append("")
    content.append(code)


    new_content = "\n".join(content)



    if new_content != old_content:

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)



    stats["total"] += 1
    stats[difficulty] += 1



# -------------------------
# Save metadata
# -------------------------

with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)



with open("leetcode_stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)



# -------------------------
# README
# -------------------------

readme = f"""# LeetCode Tracker

Last updated: {stats["last_updated"]}

## Summary

- Total solved: {stats["total"]}
- Easy: {stats["easy"]}
- Medium: {stats["medium"]}
- Hard: {stats["hard"]}

## Structure

- leetcode/easy/
- leetcode/medium/
- leetcode/hard/

Auto-generated via GitHub Actions.
"""


with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)


print("sync complete")
```
