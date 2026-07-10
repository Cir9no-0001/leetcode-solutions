import os,json,re,requests
from datetime import datetime
from zoneinfo import ZoneInfo

TZ=ZoneInfo("America/Toronto")
META="leetcode_meta.json"

username=os.getenv("LEETCODE_USERNAME")
session=os.getenv("LEETCODE_SESSION")

if not username or not session:
    raise Exception("Missing LeetCode secrets")

headers={
    "cookie":f"LEETCODE_SESSION={session}",
    "referer":"https://leetcode.com",
    "content-type":"application/json",
    "user-agent":"Mozilla/5.0"
}

def now():
    return datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

def post(query):
    r=requests.post(
        "https://leetcode.com/graphql",
        json=query,
        headers=headers,
        timeout=20
    )

    try:
        data=r.json()
    except:
        print(r.text)
        return {}

    if "errors" in data:
        print("GRAPHQL:",data["errors"])

    return data

def clean(x):
    return re.sub(
        r"[^a-zA-Z0-9\-]",
        "",
        x.lower().replace(" ","-")
    )

if os.path.exists(META):
    meta=json.load(open(META))
else:
    meta={}


# GET ACCEPTED SUBMISSIONS

q={
"query":"""
query($username:String!){
 recentAcSubmissionList(username:$username){
  id
  title
  titleSlug
 }
}
""",
"variables":{
"username":username
}
}

subs=post(q).get(
"data",
{}
).get(
"recentAcSubmissionList",
[])

if not subs:
    raise Exception("No accepted submissions")

print("\nAccepted submissions:")


seen=set()
unique=[]

for s in subs:

    if s["id"] not in seen:
        seen.add(s["id"])
        unique.append(s)

    print("-",s["title"],s["id"])


# DIFFICULTY

def difficulty(slug):

    q={
    "query":"""
    query($slug:String!){
     question(titleSlug:$slug){
      difficulty
     }
    }
    """,
    "variables":{
    "slug":slug
    }
    }

    return post(q).get(
    "data",
    {}
    ).get(
    "question",
    {}
    ).get(
    "difficulty",
    "unknown"
    ).lower()


# GET CODE DIRECTLY FROM ID

def get_code(id):

    q={
    "query":"""
    query($id:Int!){
      submissionDetails(submissionId:$id){
        code
        runtime
      }
    }
    """,
    "variables":{
    "id":int(id)
    }
    }

    result=post(q).get(
    "data",
    {}
    ).get(
    "submissionDetails"
    )

    if not result:
        print(
        "FAILED CODE FETCH:",
        id
        )
        return None,None

    return (
    result.get("code"),
    result.get("runtime")
    )


for s in unique:

    title=s["title"]
    slug=s["titleSlug"]
    sid=s["id"]

    code,runtime=get_code(sid)

    if not code:
        print(
        "Skipped:",
        title
        )
        continue


    diff=difficulty(slug)

    folder=f"leetcode/{diff}"
    os.makedirs(folder,exist_ok=True)

    path=f"{folder}/{clean(title)}.sql"


    if slug not in meta:
        meta[slug]={
        "first_seen":now()
        }


    content=[
    f"-- {title}",
    f"-- https://leetcode.com/problems/{slug}",
    f"-- difficulty: {diff}",
    f"-- first_seen: {meta[slug]['first_seen']}"
    ]

    if runtime:
        content.append(
        f"-- runtime: {runtime}"
        )

    content.append("")
    content.append(code)

    new="\n".join(content)


    old=""

    if os.path.exists(path):
        old=open(path,encoding="utf8").read()


    if old!=new:
        open(
        path,
        "w",
        encoding="utf8"
        ).write(new)

        print(
        "Updated:",
        title
        )


# COUNT FILES

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
        x for x in os.listdir(folder)
        if x.endswith(".sql")
        ]
        )


stats["total"]=sum(stats.values())
stats["last_updated"]=now()


json.dump(
meta,
open(META,"w"),
indent=2
)

json.dump(
stats,
open("leetcode_stats.json","w"),
indent=2
)


print("\nSync complete")
