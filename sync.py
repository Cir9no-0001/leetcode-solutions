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
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0"
}

META_FILE = "leetcode_meta.json"


def now():
    return datetime.now(LOCAL_TZ).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )


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
            print("GRAPHQL ERROR:")
            print(data["errors"])

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


if os.path.exists(META_FILE):
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    meta = {}


# ==========================
# GET RECENT ACCEPTED SOLUTIONS
# ==========================

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


# ==========================
# GET DIFFICULTY
# ==========================

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



# ==========================
# GET SUBMISSION CODE
# ==========================

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
            "offset":0,
            "limit":1,
            "questionSlug":slug
        }
    })


    try:

        submission_id = (
            history
            ["data"]
            ["submissionList"]
            ["submissions"][0]
            ["id"]
        )

    except Exception:

        print(
            "No submission history:",
            slug
        )

        return {
            "code":"",
            "runtime":None
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

        print(
            "No code returned:",
            slug
        )

        return {
            "code":"",
            "runtime":None
        }


    return {
        "code": result.get("code",""),
        "runtime": result.get("runtime")
    }



# ==========================
# SYNC SOLUTION FILES
# ==========================

for submission in subs:

    title = submission["title"]
    slug = submission["titleSlug"]

    difficulty = get_difficulty(slug)

    if difficulty not in [
        "easy",
        "medium",
        "hard"
    ]:
        print(
            "Unknown difficulty:",
            title
        )
        continue


    submission_data = get_submission(slug)

    code = submission_data["code"]
    runtime = submission_data["runtime"]


    if not code:

        print(
            "Skipped:",
            title
        )

        continue



    if slug not in meta:

        meta[slug] = {
            "first_seen": now()
        }


    folder = (
        f"leetcode/{difficulty}"
    )

    os.makedirs(
        folder,
        exist_ok=True
    )


    file_path = (
        f"{folder}/{clean(title)}.sql"
    )


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


    content.append("")
    content.append(code)


    new_content = "\n".join(content)


    old_content = ""

    if os.path.exists(file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            old_content = f.read()



    if new_content != old_content:

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(new_content)


        print(
            "Updated:",
            title
        )



# ==========================
# COUNT EXISTING FILES
# ==========================

stats = {
    "easy":0,
    "medium":0,
    "hard":0,
    "total":0,
    "last_updated":now()
}


for difficulty in [
    "easy",
    "medium",
    "hard"
]:

    folder = (
        f"leetcode/{difficulty}"
    )


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



# ==========================
# SAVE DATA
# ==========================

with open(
    META_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        meta,
        f,
        indent=2
    )


with open(
    "leetcode_stats.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        stats,
        f,
        indent=2
    )



readme = f"""
# LeetCode Tracker

Last updated: {stats["last_updated"]}

## Summary

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

Automatically synced using GitHub Actions.
"""


with open(
    "README.md",
    "w",
    encoding="utf-8"
) as f:

    f.write(readme)


print("\nSync complete")
