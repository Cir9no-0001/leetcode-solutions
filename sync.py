import os
import json
import re
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Toronto")

META_FILE = "leetcode_meta.json"

username = os.environ.get("LEETCODE_USERNAME")
session = os.environ.get("LEETCODE_SESSION")

if not username or not session:
    raise Exception("Missing LeetCode credentials")

headers = {
    "cookie": f"LEETCODE_SESSION={session}",
    "referer": "https://leetcode.com",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0"
}


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
        print("Request failed:", e)
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


if os.path.exists(META_FILE):
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    meta = {}


# -----------------------------
# GET RECENT ACCEPTED SUBMISSIONS
# -----------------------------

response = post({
    "query": """
    query recentAcSubmissions($username:String!){
        recentAcSubmissionList(username:$username){
            title
            titleSlug
        }
    }
    """,
    "variables":{
        "username":username
    }
})


subs = (
    response
    .get("data", {})
    .get("recentAcSubmissionList", [])
)


if not subs:
    raise Exception("No submissions found")


print("\nDetected submissions:")

for s in subs:
    print("-", s["title"])


# -----------------------------
# DIFFICULTY
# -----------------------------

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
        "variables":{
            "titleSlug":slug
        }
    })


    difficulty = (
        response
        .get("data", {})
        .get("question", {})
        .get("difficulty","unknown")
        .lower()
    )


    difficulty_cache[slug] = difficulty

    return difficulty



# -----------------------------
# GET ACTUAL SUBMISSION CODE
# -----------------------------

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
        "variables":{
            "offset":0,
            "limit":5,
            "questionSlug":slug
        }
    })


    try:

        submissions = (
            history
            ["data"]
            ["submissionList"]
            ["submissions"]
        )

    except Exception:

        print(
            "No submission history:",
            slug
        )

        return {
            "code":None,
            "runtime":None
        }


    if not submissions:

        print(
            "Empty submission history:",
            slug
        )

        return {
            "code":None,
            "runtime":None
        }


    submission_id = submissions[0]["id"]


    detail = post({
        "query":"""
        query submissionDetails($submissionId:Int!){
            submissionDetails(
                submissionId:$submissionId
            ){
                code
                runtime
            }
        }
        """,
        "variables":{
            "submissionId":int(submission_id)
        }
    })


    result = (
        detail
        .get("data", {})
        .get("submissionDetails")
    )


    if not result:

        print(
            "No details returned:",
            submission_id
        )

        return {
            "code":None,
            "runtime":None
        }


    return {
        "code":result.get("code"),
        "runtime":result.get("runtime")
    }



# -----------------------------
# SYNC FILES
# -----------------------------

for submission in subs:

    title = submission["title"]
    slug = submission["titleSlug"]

    difficulty = get_difficulty(slug)

    data = get_submission(slug)

    code = data["code"]
    runtime = data["runtime"]


    if not code:

        print(
            "Skipped:",
            title
        )

        continue


    folder = f"leetcode/{difficulty}"

    os.makedirs(
        folder,
        exist_ok=True
    )


    path = (
        f"{folder}/{clean(title)}.sql"
    )


    old_content = ""

    notes = None


    if os.path.exists(path):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            old_content = f.read()

        notes = extract_notes(old_content)



    if slug not in meta:

        meta[slug] = {
            "first_seen":now()
        }


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


    if notes:

        content.extend(notes)

    else:

        content.extend([
            "-- NOTES START",
            "-- write notes here",
            "-- NOTES END"
        ])


    content.append("")
    content.append(code)


    new_content = "\n".join(content)


    if new_content != old_content:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(new_content)


        print(
            "Updated:",
            title
        )



# -----------------------------
# STATS
# -----------------------------

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

    folder = f"leetcode/{difficulty}"

    if os.path.exists(folder):

        stats[difficulty] = len([
            f
            for f in os.listdir(folder)
            if f.endswith(".sql")
        ])


stats["total"] = (
    stats["easy"]
    +
    stats["medium"]
    +
    stats["hard"]
)



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

Last synced: {stats["last_updated"]}

| Difficulty | Count |
|---|---:|
| Easy | {stats["easy"]} |
| Medium | {stats["medium"]} |
| Hard | {stats["hard"]} |
| Total | {stats["total"]} |

Structure:

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
