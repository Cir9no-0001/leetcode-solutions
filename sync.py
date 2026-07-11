import os
import requests
import re
import json
from datetime import datetime
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Toronto")

META_FILE = "leetcode_meta.json"
NOTES_FILE = "leetcode_notes.json"

username = os.environ.get("LEETCODE_USERNAME")
session = os.environ.get("LEETCODE_SESSION")

if not username or not session:
    raise Exception("Missing LEETCODE_USERNAME or LEETCODE_SESSION")

headers = {
    "cookie": f"LEETCODE_SESSION={session}",
    "referer": "https://leetcode.com",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0"
}


def now():
    return datetime.now(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S %Z")


def post(query):
    try:
        r = requests.post(
            "https://leetcode.com/graphql",
            json=query,
            headers=headers,
            timeout=15
        )
        data = r.json()

        if "errors" in data:
            print("GRAPHQL ERROR:", data["errors"])

        return data

    except Exception as e:
        print("REQUEST ERROR:", e)
        return {}


def clean(name):
    return (
        re.sub(
            r"[^a-zA-Z0-9\- ]",
            "",
            name
        )
        .lower()
        .replace(" ", "-")
    )


# Load metadata

if os.path.exists(META_FILE):
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    meta = {}


# Load notes

if os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        notes = json.load(f)
else:
    notes = {}


# Get recent accepted submissions

response = post({
    "query": """
    query recentAcSubmissions($username:String!){
        recentAcSubmissionList(username:$username){
            title
            titleSlug
        }
    }
    """,
    "variables": {
        "username": username
    }
})


subs = (
    response
    .get("data", {})
    .get("recentAcSubmissionList", [])
)


if not subs:
    raise Exception("No submissions returned")


print("\nAccepted submissions:")

for s in subs:
    print("-", s["title"])


# Difficulty lookup

difficulty_cache = {}


def get_difficulty(slug):

    if slug in difficulty_cache:
        return difficulty_cache[slug]

    response = post({
        "query": """
        query questionData($titleSlug:String!){
            question(titleSlug:$titleSlug){
                difficulty
            }
        }
        """,
        "variables": {
            "titleSlug": slug
        }
    })

    difficulty = (
        response
        .get("data", {})
        .get("question", {})
        .get("difficulty", "unknown")
        .lower()
    )

    difficulty_cache[slug] = difficulty

    return difficulty


# Submission code lookup

def get_submission(slug):

    history = post({
        "query": """
        query submissionList(
            $offset:Int!,
            $limit:Int!,
            $questionSlug:String!
        ){
            submissionList(
                offset:$offset,
                limit:$limit,
                questionSlug:$questionSlug
            ){
                submissions{
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
    })

    try:
        submission_id = (
            history["data"]
            ["submissionList"]
            ["submissions"][0]
            ["id"]
        )

    except Exception:
        print("No submission history:", slug)
        return {
            "code": "",
            "runtime": None
        }


    detail = post({
        "query": """
        query submissionDetails($submissionId:Int!){
            submissionDetails(
                submissionId:$submissionId
            ){
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
        detail
        .get("data", {})
        .get("submissionDetails")
    )


    if not result:
        print("No code returned:", slug)
        return {
            "code": "",
            "runtime": None
        }


    return {
        "code": result.get("code", ""),
        "runtime": result.get("runtime")
    }


# Sync solutions

for submission in subs:

    title = submission["title"]
    slug = submission["titleSlug"]

    difficulty = get_difficulty(slug)

    if difficulty not in ["easy", "medium", "hard"]:
        print("Unknown difficulty:", title)
        continue


    data = get_submission(slug)

    code = data["code"]
    runtime = data["runtime"]


    if not code:
        print("Skipped:", title)
        continue


    if slug not in meta:
        meta[slug] = {
            "first_seen": now()
        }


    if slug not in notes:
        notes[slug] = {
            "notes": ""
        }


    folder = f"leetcode/{difficulty}"

    os.makedirs(
        folder,
        exist_ok=True
    )


    path = f"{folder}/{clean(title)}.sql"


    content = [
        f"-- {title}",
        f"-- https://leetcode.com/problems/{slug}",
        f"-- difficulty: {difficulty}",
        f"-- first_seen: {meta[slug]['first_seen']}"
    ]


    if runtime:
        content.append(
            f"-- runtime: {runtime}"
        )


    content.extend([
        "--",
        "-- Notes stored in leetcode_notes.json",
        "",
        code
    ])


    new_content = "\n".join(content)


    old_content = ""

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            old_content = f.read()


    if new_content != old_content:

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print("Updated:", title)



# Count actual files

stats = {
    "easy": 0,
    "medium": 0,
    "hard": 0,
    "total": 0,
    "last_updated": now()
}


for difficulty in ["easy", "medium", "hard"]:

    folder = f"leetcode/{difficulty}"

    if os.path.exists(folder):

        stats[difficulty] = len([
            file
            for file in os.listdir(folder)
            if file.endswith(".sql")
        ])


stats["total"] = (
    stats["easy"]
    +
    stats["medium"]
    +
    stats["hard"]
)



# Save metadata

with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)


with open(NOTES_FILE, "w", encoding="utf-8") as f:
    json.dump(notes, f, indent=2)


with open("leetcode_stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)



# README

readme = f"""# LeetCode Tracker

Last updated: {stats["last_updated"]}

| Difficulty | Count |
|---|---:|
| Easy | {stats["easy"]} |
| Medium | {stats["medium"]} |
| Hard | {stats["hard"]} |
| Total | {stats["total"]} |

## Structure

- leetcode/easy/
- leetcode/medium/
- leetcode/hard/

Notes feature currently down :<

Automatically synced using GitHub Actions.
"""


with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)


print("\nSync complete")
