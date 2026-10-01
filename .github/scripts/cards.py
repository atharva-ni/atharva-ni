"""Builds profile/stats-*.svg and profile/top-langs-*.svg from the GitHub API.

Only uses data that is public on the profile, so the workflow's built-in
GITHUB_TOKEN is enough. Private contributions are counted as long as
"Include private contributions on my profile" is switched on in GitHub settings.
"""

import json
import os
import sys
import urllib.request
from html import escape

USER = os.environ.get("GH_USER") or sys.argv[1]
TOKEN = os.environ["GITHUB_TOKEN"]
HIDDEN_LANGS = {"HTML"}  # static/exported HTML would drown out real code
LANG_COUNT = 6

THEMES = {
    "light": {"title": "#8A5A1C", "text": "#24292F", "icon": "#0D6B4F", "muted": "#57606A"},
    "dark": {"title": "#D9A75C", "text": "#C9D4CC", "icon": "#4FB08E", "muted": "#8B949E"},
}
FONT = "font-family=\"'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif\""


def api(url, body=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def fetch_stats():
    q = """query($login: String!) { user(login: $login) {
      name
      contributionsCollection {
        contributionCalendar { totalContributions }
        totalCommitContributions
        totalPullRequestContributions
        restrictedContributionsCount
        totalRepositoriesWithContributedCommits
      } } }"""
    data = api("https://api.github.com/graphql", {"query": q, "variables": {"login": USER}})
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]


def fetch_repos():
    repos, page = [], 1
    while True:
        batch = api(f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}")
        repos += batch
        if len(batch) < 100:
            return repos
        page += 1


def fetch_languages(repos):
    totals = {}
    for repo in repos:
        if repo["fork"]:
            continue
        for lang, size in api(repo["languages_url"]).items():
            if lang not in HIDDEN_LANGS:
                totals[lang] = totals.get(lang, 0) + size
    return sorted(totals.items(), key=lambda kv: kv[1], reverse=True)


# 16px octicons
ICONS = {
    "pulse": "M6 2c.306 0 .582.187.696.471L10 10.731l1.304-3.26A.751.751 0 0 1 12 7h3.25a.75.75 0 0 1 0 1.5h-2.742l-1.812 4.528a.751.751 0 0 1-1.392 0L6 4.77 4.696 8.03A.75.75 0 0 1 4 8.5H.75a.75.75 0 0 1 0-1.5h2.742l1.812-4.529A.751.751 0 0 1 6 2Z",
    "commit": "M11.93 8.5a4.002 4.002 0 0 1-7.86 0H.75a.75.75 0 0 1 0-1.5h3.32a4.002 4.002 0 0 1 7.86 0h3.32a.75.75 0 0 1 0 1.5Zm-1.43-.75a2.5 2.5 0 1 0-5 0 2.5 2.5 0 0 0 5 0Z",
    "lock": "M4 4a4 4 0 0 1 8 0v2h.25c.966 0 1.75.784 1.75 1.75v5.5A1.75 1.75 0 0 1 12.25 15h-8.5A1.75 1.75 0 0 1 2 13.25v-5.5C2 6.784 2.784 6 3.75 6H4Zm8.25 3.5h-8.5a.25.25 0 0 0-.25.25v5.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-5.5a.25.25 0 0 0-.25-.25ZM10.5 6V4a2.5 2.5 0 1 0-5 0v2Z",
    "pr": "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z",
    "repo": "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z",
    "star": "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z",
}


def stats_svg(rows, title, t):
    width, top, step = 360, 58, 26
    height = top + step * len(rows) + 6
    lines = []
    for i, (icon, label, value) in enumerate(rows):
        y = top + i * step
        lines.append(
            f'<g transform="translate(25,{y})">'
            f'<path fill="{t["icon"]}" transform="translate(0,-12)" d="{ICONS[icon]}"/>'
            f'<text x="26" y="0" fill="{t["text"]}" font-size="14" font-weight="600">{escape(label)}</text>'
            f'<text x="{width - 25}" y="0" fill="{t["text"]}" font-size="14" font-weight="700" text-anchor="end">{value:,}</text>'
            "</g>"
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{escape(title)}" {FONT}><title>{escape(title)}</title>'
        f'<text x="25" y="32" fill="{t["title"]}" font-size="18" font-weight="600">{escape(title)}</text>'
        + "".join(lines)
        + "</svg>"
    )


def langs_svg(langs, colors, t):
    width, bar_w = 360, 310
    langs = langs[:LANG_COUNT]
    total = sum(size for _, size in langs) or 1
    rows = (len(langs) + 1) // 2
    height = 80 + rows * 24
    bar, x = [], 25.0
    for name, size in langs:
        w = bar_w * size / total
        bar.append(f'<rect x="{x:.2f}" y="48" width="{w:.2f}" height="8" fill="{colors.get(name, "#8B949E")}"/>')
        x += w
    legend = []
    for i, (name, size) in enumerate(langs):
        lx, ly = 25 + (i % 2) * 160, 84 + (i // 2) * 24
        legend.append(
            f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5" fill="{colors.get(name, "#8B949E")}"/>'
            f'<text x="{lx + 16}" y="{ly}" fill="{t["text"]}" font-size="12">{escape(name)} '
            f'<tspan fill="{t["muted"]}">{100 * size / total:.1f}%</tspan></text>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="Most used languages" {FONT}><title>Most used languages</title>'
        f'<text x="25" y="32" fill="{t["title"]}" font-size="18" font-weight="600">Most Used Languages</text>'
        f'<clipPath id="bar"><rect x="25" y="48" width="{bar_w}" height="8" rx="4"/></clipPath>'
        f'<g clip-path="url(#bar)">{"".join(bar)}</g>'
        + "".join(legend)
        + "</svg>"
    )


LANG_COLORS = {
    "TypeScript": "#3178C6", "JavaScript": "#F1E05A", "Python": "#3572A5", "CSS": "#663399",
    "Java": "#B07219", "C++": "#F34B7D", "C": "#555555", "Shell": "#89E051", "PLpgSQL": "#336790",
    "Jupyter Notebook": "#DA5B0B", "Dockerfile": "#384D54", "SCSS": "#C6538C", "Vue": "#41B883",
    "Go": "#00ADD8", "Rust": "#DEA584", "Kotlin": "#A97BFF", "Dart": "#00B4AB", "PHP": "#4F5D95",
    "TSQL": "#E38C00", "Batchfile": "#C1F12E", "PowerShell": "#012456", "Mako": "#7E858D",
}


def main():
    user = fetch_stats()
    cc = user["contributionsCollection"]
    repos = fetch_repos()
    stars = sum(r["stargazers_count"] for r in repos if not r["fork"])
    rows = [
        ("pulse", "Contributions (last year)", cc["contributionCalendar"]["totalContributions"]),
        ("commit", "Public commits (last year)", cc["totalCommitContributions"]),
        ("lock", "Private contributions", cc["restrictedContributionsCount"]),
        ("pr", "Pull requests", cc["totalPullRequestContributions"]),
        ("repo", "Repos contributed to", cc["totalRepositoriesWithContributedCommits"]),
        ("star", "Stars earned", stars),
    ]
    rows = [r for r in rows if r[0] not in ("lock", "pr", "star") or r[2] > 0]
    title = f"{user['name'] or USER}'s GitHub Stats"
    langs = fetch_languages(repos)

    os.makedirs("profile", exist_ok=True)
    for theme, t in THEMES.items():
        with open(f"profile/stats-{theme}.svg", "w", encoding="utf-8") as f:
            f.write(stats_svg(rows, title, t))
        with open(f"profile/top-langs-{theme}.svg", "w", encoding="utf-8") as f:
            f.write(langs_svg(langs, LANG_COLORS, t))
    for _, label, value in rows:
        print(f"{label}: {value}")
    print("Languages:", ", ".join(name for name, _ in langs[:LANG_COUNT]))


if __name__ == "__main__":
    main()
