import os
import requests
import re
import json
from datetime import datetime
from zoneinfo import ZoneInfo


# =========================
# CONFIG
# =========================

LOCAL_TZ = ZoneInfo("America/Toronto")

META_FILE = "leetcode_meta.json"


username = os.environ.get("LEETCODE_USERNAME")
session = os.environ.get("LEETCODE_SESSION")


if not username or not session:
    raise Exception("Missing LeetCode credentials")


headers = {
    "cookie": f"LEETCODE_SESSION={session}",
    "referer": "https://leetcode.com",
    "content-type": "application/json"
}


# =========================
# HELPERS
# =========================


def now():
    return datetime.now(LOCAL_TZ).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )


def post(payload):

    try:

        response = requests.post(
            "https://leetcode.com/graphql",
            json=payload,
            headers=headers,
            timeout=15
        )

        return response.json()

    except Exception as e:

        print("Request error:", e)

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



# =========================
# LOAD META
# =========================


if os.path.exists(META_FILE):

    with open(
        META_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        meta = json.load(f)

else:

    meta = {}



# =========================
# GET RECENT ACCEPTED
# =========================


query = {

    "query": """

    query recentAcSubmissions($username:String!) {

        recentAcSubmissionList(username:$username) {

            id

            title

            titleSlug

        }

    }

    """,

    "variables": {

        "username": username

    }

}



response = post(query)



subs = (

    response
    .get("data", {})
    .get("recentAcSubmissionList", [])

)



if not subs:

    raise Exception(
        "No accepted submissions returned"
    )



print("\nDetected submissions:")


for s in subs:

    print(
        f"- {s['title']} ({s['id']})"
    )



# =========================
# GET DIFFICULTY
# =========================


difficulty_cache = {}



def get_difficulty(slug):


    if slug in difficulty_cache:

        return difficulty_cache[slug]



    response = post({

        "query": """

        query questionData($titleSlug:String!) {

            question(titleSlug:$titleSlug) {

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
        .get(
            "difficulty",
            "unknown"
        )
        .lower()

    )


    difficulty_cache[slug] = difficulty


    return difficulty



# =========================
# GET CODE
# =========================


def get_submission(submission_id):


    response = post({

        "query": """

        query submissionDetails($submissionId:Int!) {

            submissionDetails(submissionId:$submissionId) {

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

        response
        .get("data", {})
        .get("submissionDetails")

    )



    if not result:

        print(
            f"No submission details found: {submission_id}"
        )


        return {

            "code": None,

            "runtime": None

        }



    return {

        "code": result.get("code"),

        "runtime": result.get("runtime")

    }



# =========================
# SYNC
# =========================


for submission in subs:


    title = submission["title"]

    slug = submission["titleSlug"]

    submission_id = submission["id"]



    difficulty = get_difficulty(slug)



    data = get_submission(submission_id)



    code = data["code"]

    runtime = data["runtime"]



    if not code:

        print(
            f"Skipped {title}: no code returned"
        )

        continue



    folder = f"leetcode/{difficulty}"


    os.makedirs(
        folder,
        exist_ok=True
    )



    file_path = (

        f"{folder}/{clean(title)}.sql"

    )



    old_content = ""


    old_notes = None



    if os.path.exists(file_path):


        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            old_content = f.read()



        old_notes = extract_notes(old_content)



    if slug not in meta:


        meta[slug] = {

            "first_seen": now()

        }



    first_seen = meta[slug]["first_seen"]



    content = [

        f"-- {title}",

        f"-- https://leetcode.com/problems/{slug}",

        f"-- difficulty: {difficulty}",

        f"-- first_seen: {first_seen}"

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


        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(new_content)



        print(
            f"Updated: {title}"
        )


    else:

        print(
            f"Already synced: {title}"
        )



# =========================
# STATS
# =========================


stats = {

    "easy": 0,

    "medium": 0,

    "hard": 0,

    "total": 0,

    "last_updated": now()

}



for difficulty in [

    "easy",

    "medium",

    "hard"

]:


    folder = f"leetcode/{difficulty}"



    if os.path.exists(folder):


        stats[difficulty] = len([

            f for f in os.listdir(folder)

            if f.endswith(".sql")

        ])




stats["total"] = (

    stats["easy"]

    + stats["medium"]

    + stats["hard"]

)



# =========================
# SAVE FILES
# =========================


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


Last synced:

{stats["last_updated"]}



## Statistics


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


Auto-generated via GitHub Actions.

"""


with open(
    "README.md",
    "w",
    encoding="utf-8"
) as f:

    f.write(readme)



print("\nSync complete")
