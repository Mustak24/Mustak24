import os
import requests
from urllib.parse import quote


USERNAME = "Mustak24"  # your GitHub username

headers = {"Authorization": f"token {os.getenv('GH_TOKEN')}"}
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=headers).json()

languages = {}

for repo in repos:
    repo_name = repo["name"]
    langs = requests.get(f"https://api.github.com/repos/{USERNAME}/{repo_name}/languages").json()
    for lang, lines in langs.items():
        languages[lang] = languages.get(lang, 0) + lines

total = sum(languages.values())

def fmt(num):
    if num > 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num > 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)

# Start building markdown output
output = "# 📊 **My Coding Stats**\n\n"

# Total badge
total_badge = f"https://img.shields.io/badge/Total%20Lines-{quote(fmt(total))}-brightgreen"
output += f"![Total LOC]({total_badge})\n"

# Per-language badges
for lang, lines in sorted(languages.items(), key=lambda x: x[1], reverse=True):
    badge = f"https://img.shields.io/badge/{quote(lang)}-{quote(fmt(lines))}-blue"
    output += f"![{lang}]({badge}) "

print(output)
