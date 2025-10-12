import os
import requests
from urllib.parse import quote

USERNAME = "Mustak24"  # your GitHub username
TOKEN = os.getenv("GH_TOKEN")  # optional, for private repos or API limits

headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# ✅ safer request with headers + error handling
repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
response = requests.get(repos_url, headers=headers)

if response.status_code != 200:
    print(f"Error fetching repos: {response.status_code} - {response.text}")
    exit(1)

repos = response.json()
if not isinstance(repos, list):
    print("Unexpected response from GitHub API:")
    print(repos)
    exit(1)

languages = {}

for repo in repos:
    repo_name = repo["name"]
    lang_url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/languages"
    langs = requests.get(lang_url, headers=headers).json()
    for lang, lines in langs.items():
        languages[lang] = languages.get(lang, 0) + lines

total = sum(languages.values())

def fmt(num):
    if num > 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num > 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

output = "📊 **My Coding Stats**\n\n"
total_badge = f"https://img.shields.io/badge/Total%20Lines-{quote(fmt(total))}-brightgreen"
output += f"![Total LOC]({total_badge})\n"

for lang, lines in sorted(languages.items(), key=lambda x: x[1], reverse=True):
    badge = f"https://img.shields.io/badge/{quote(lang)}-{quote(fmt(lines))}-blue"
    output += f"![{lang}]({badge}) "

print(output)
