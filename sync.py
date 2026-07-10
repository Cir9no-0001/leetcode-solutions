import os
import requests
import re
import json
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
    "content-type": "application/json"
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

        return r.json()

    except Exception as e:
        print("API error:", e)
        return {}



def clean(name):
    return (
        re.sub(r"[^a-zA-Z0-9\- ]", "", name)
        .lower()
        .replace(" ", "-")
    )



def extract_notes(content):

    lines = content.splitlines()

    start = None
    end = None


    for i,line in enumerate(lines):

        if line.strip() == "-- NOTES START":
            start = i

        if line.strip() == "-- NOTES END":
            end = i


    if start is not None and end is not None:
        return lines[start:end+1]


    return None



if os.path.exists(META_FILE):

    with open(META_FILE,"r",encoding="utf-8") as f:
        meta=json.load(f)

else:
    meta={}



recent_query = {

"query": """

query recentAcSubmissions($username:String!) {

recentAcSubmissionList(username:$username) {

title
titleSlug

}

}

""",

"variables":{
"username":username
}

}



response = post(recent_query)



subs = (
    response
    .get("data",{})
    .get("recentAcSubmissionList",[])
)



if not subs:
    raise Exception("No accepted submissions detected")



print("Detected submissions:")

for s in subs:
    print("-",s["title"])



difficulty_cache={}



def get_difficulty(slug):

    if slug in difficulty_cache:
        return difficulty_cache[slug]


    result=post({

"query":"""

query questionData($titleSlug:String!) {

question(titleSlug:$titleSlug){

difficulty

}

}

""",

"variables":{
"titleSlug":slug
}

})


    difficulty=(

result
.get("data",{})
.get("question",{})
.get("difficulty","unknown")
.lower()

)


    difficulty_cache[slug]=difficulty


    return difficulty



def get_submission_code(slug):


    history = post({

"query":"""

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

        return None,None



    details = post({

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


    result=(

    details
    .get("data",{})
    .get("submissionDetails")

    )


    if not result:

        print(
        "No details:",
        slug
        )

        return None,None



    return (
        result.get("code"),
        result.get("runtime")
    )





for submission in subs:


    title=submission["title"]
    slug=submission["titleSlug"]


    difficulty=get_difficulty(slug)


    code,runtime=get_submission_code(slug)


    if not code:

        print(
        "Skipped:",
        title
        )

        continue



    folder=f"leetcode/{difficulty}"

    os.makedirs(folder,exist_ok=True)


    filepath=f"{folder}/{clean(title)}.sql"


    old_content=""

    old_notes=None


    if os.path.exists(filepath):

        with open(filepath,"r",encoding="utf-8") as f:
            old_content=f.read()


        old_notes=extract_notes(old_content)



    if slug not in meta:

        meta[slug]={
            "first_seen":now()
        }



    content=[

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


    if old_notes:

        content.extend(old_notes)

    else:

        content.extend([

        "-- NOTES START",
        "-- write notes here",
        "-- NOTES END"

        ])


    content.append("")
    content.append(code)


    new_content="\n".join(content)


    if new_content != old_content:

        with open(filepath,"w",encoding="utf-8") as f:
            f.write(new_content)

        print("Updated:",filepath)





stats={}



for difficulty in [
    "easy",
    "medium",
    "hard"
]:


    folder=f"leetcode/{difficulty}"


    if os.path.exists(folder):

        stats[difficulty]=len([

        f for f in os.listdir(folder)
        if f.endswith(".sql")

        ])

    else:

        stats[difficulty]=0



stats["total"]=(
stats["easy"]
+
stats["medium"]
+
stats["hard"]
)


stats["last_updated"]=now()



with open(META_FILE,"w",encoding="utf-8") as f:
    json.dump(meta,f,indent=2)



readme=f"""

# LeetCode Tracker


Last synced: {stats["last_updated"]}


## Statistics


| Difficulty | Count |
|---|---:|
| Easy | {stats["easy"]} |
| Medium | {stats["medium"]} |
| Hard | {stats["hard"]} |
| Total | {stats["total"]} |


## Structure

- leetcode/easy
- leetcode/medium
- leetcode/hard


Auto-generated using GitHub Actions.

"""


with open("README.md","w",encoding="utf-8") as f:
    f.write(readme)



print("sync complete")
