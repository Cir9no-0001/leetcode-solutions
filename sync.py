import os
import json
import requests

username = os.environ["LEETCODE_USERNAME"]

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

r = requests.post("https://leetcode.com/graphql", json=query)
data = r.json()

# THIS is the missing part:
with open("leetcode.json", "w") as f:
    json.dump(data, f, indent=2)

print("saved leetcode.json")
