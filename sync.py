import os
import json
import re
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Toronto")

USERNAME = os.environ.get("LEETCODE_USERNAME")
SESSION = os.environ.get("LEETCODE_SESSION")

if not USERNAME or not SESSION:
    raise Exception("Missing LeetCode credentials")


HEADERS = {
    "cookie": f"LEETCODE_SESSION={SESSION}",
    "content-type": "application/json",
    "referer": "https://leetcode.com",
    "user-agent": "Mozilla/5.0"
}


def now():
    return datetime.now(TZ).strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )


def graphql(query, variables=None):

    r = requests.post(
        "https://leetcode.com/graphql",
        headers=HEADERS,
        json={
            "query": query,
            "variables": variables or {}
        },
        timeout=20
    )

    data = r.json()

    if "errors" in data:
        print(data["errors"])

    return data



def clean(name):
    return re.sub(
        r"[^a-zA-Z0-9 ]",
        "",
        name
    ).lower().replace(" ","-")


# ----------------------------
# GET RECENT ACCEPTED SUBMISSIONS
# ----------------------------

query = """
query recentSubmissionList($username:String!){
 matchedUser(username:$username){
  submitStatsGlobal{
   acSubmissionNum{
    difficulty
    count
   }
  }
 }
}
"""



# ----------------------------
# GET RECENT SUBMISSIONS WITH IDS
# ----------------------------


subs = graphql(
"""
query recentSubmissionList($username:String!){
 recentSubmissionList(username:$username,limit:20){
   id
   title
   titleSlug
   statusDisplay
 }
}
""",
{
"username":USERNAME
}
)



submissions = (
    subs
    .get("data",{})
    .get("recentSubmissionList",[])
)


if not submissions:
    raise Exception("Could not get submissions")


accepted=[]


for s in submissions:

    if s["statusDisplay"]=="Accepted":

        accepted.append(s)



print("\nAccepted submissions:")

for s in accepted:
    print(
        "-",
        s["title"]
    )



# ----------------------------
# SUBMISSION DETAILS
# ----------------------------


def get_code(submission_id):

    result = graphql(
"""
query submissionDetails($id:Int!){
 submissionDetails(submissionId:$id){
  code
  runtime
 }
}
""",
{
"id":int(submission_id)
}
)


    details = (
        result
        .get("data",{})
        .get("submissionDetails")
    )


    if not details:
        return None,None


    return (
        details.get("code"),
        details.get("runtime")
    )



# ----------------------------
# DIFFICULTY
# ----------------------------


def get_difficulty(slug):

    result = graphql(
"""
query questionData($slug:String!){
 question(titleSlug:$slug){
  difficulty
 }
}
""",
{
"slug":slug
}
)


    return (
        result
        .get("data",{})
        .get("question",{})
        .get("difficulty","unknown")
        .lower()
    )



# ----------------------------
# WRITE FILES
# ----------------------------


for sub in accepted:


    title=sub["title"]
    slug=sub["titleSlug"]
    sid=sub["id"]


    code,runtime=get_code(sid)


    if not code:

        print(
            "No code:",
            title
        )

        continue



    difficulty=get_difficulty(slug)


    folder=f"leetcode/{difficulty}"

    os.makedirs(
        folder,
        exist_ok=True
    )


    filepath=f"{folder}/{clean(title)}.sql"


    content=f"""-- {title}
-- https://leetcode.com/problems/{slug}
-- difficulty: {difficulty}
-- synced: {now()}
-- runtime: {runtime}


{code}
"""


    old=""

    if os.path.exists(filepath):

        with open(filepath,"r",encoding="utf8") as f:
            old=f.read()



    if old != content:

        with open(filepath,"w",encoding="utf8") as f:
            f.write(content)


        print(
            "Updated:",
            title
        )



# ----------------------------
# COUNT FILES
# ----------------------------


stats={
"easy":0,
"medium":0,
"hard":0
}



for d in stats:

    folder=f"leetcode/{d}"

    if os.path.exists(folder):

        stats[d]=len(
            [
            f for f in os.listdir(folder)
            if f.endswith(".sql")
            ]
        )


stats["total"]=sum(stats.values())

stats["last_updated"]=now()



with open(
"leetcode_stats.json",
"w"
) as f:

    json.dump(
        stats,
        f,
        indent=2
    )


print("\nSync complete")
