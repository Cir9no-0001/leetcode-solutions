import os
import requests

username = os.environ["LEETCODE_USERNAME"]

url = "https://leetcode.com/graphql"

query = {
    "query": """
    query recentAcSubmissions($username: String!) {
      recentAcSubmissionList(username: $username) {
        title
        titleSlug
        timestamp
      }
    }
    """,
    "variables": {"username": username}
}

r = requests.post(url, json=query)
data = r.json()

print(data)
