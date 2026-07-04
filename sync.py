import os
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

print(data)
