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

if os.path.exists(META_FILE):
    with open(META_FILE, "r", encoding="utf-8") as f:
        meta = json.load(f)
else:
    meta = {}

if os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        notes = json.load(f)
else:
    notes = {}

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

def update_notes_in_files():

    for root, _, files in os.walk("leetcode"):

        for file in files:

            if not file.endswith(".sql"):
                continue

            path = os.path.join(root, file)
            slug = file[:-4]

            if slug not in notes:
                continue

            note_text = notes[slug].get("notes", "")

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            if "-- Notes:" not in content:
                continue

            before_notes = content.split("-- Notes:")[0]

            notes_position = content.find("-- Notes:")

            code_position = content.find("\n\n", notes_position)

            if code_position != -1:
                code = content[code_position:]
            else:
                code = ""

            new_content = before_notes + "-- Notes:\n"

            if note_text:
                for line in note_text.split("\n"):
                    new_content += f"-- {line}\n"
            else:
                new_content += "--\n"

            new_content += code

            if new_content != content:

                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print("Updated notes:", file)

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
            f"-- runtime: {runtime}ms"
        )

    content.extend([
        "-- Notes:"
    ])
    if notes[slug]["notes"]:
        for line in notes[slug]["notes"].split("\n"):
            content.append(f"-- {line}")
    else:
        content.append("--")

    content.extend([
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

update_notes_in_files()

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

with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

with open(NOTES_FILE, "w", encoding="utf-8") as f:
    json.dump(notes, f, indent=2)

with open("leetcode_stats.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)

readme = f"""# LeetCode Tracker

Last updated: {stats["last_updated"]}

| Difficulty | Count |
|---|---:|
| Easy | {stats["easy"]} |
| Medium | {stats["medium"]} |
| Hard | {stats["hard"]} |
| Total | {stats["total"]} |

## Folder Structure

- leetcode/easy/
- leetcode/medium/
- leetcode/hard/
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("\nSync complete")
