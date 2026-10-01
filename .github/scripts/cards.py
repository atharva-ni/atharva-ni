"""Builds profile/recent-*.svg and profile/top-langs-*.svg from the GitHub API.

Only uses public repo data, so the workflow's built-in GITHUB_TOKEN is enough.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from html import escape

USER = os.environ.get("GH_USER") or sys.argv[1]
TOKEN = os.environ["GITHUB_TOKEN"]
HIDDEN_LANGS = {"HTML"}  # static/exported HTML would drown out real code
LANG_COUNT = 6
RECENT_COUNT = 4

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


# 16px octicon
REPO_ICON = "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"


def ago(stamp):
    days = (datetime.now(timezone.utc) - datetime.fromisoformat(stamp.replace("Z", "+00:00"))).days
    if days < 1:
        return "today"
    if days < 14:
        return f"{days}d ago"
    if days < 60:
        return f"{days // 7}w ago"
    if days < 365:
        return f"{days // 30}mo ago"
    return f"{days // 365}y ago"


def recent_svg(repos, colors, t):
    width, top, step = 360, 62, 24
    height = top + step * (len(repos) - 1) + 18
    lines = []
    for i, repo in enumerate(repos):
        y = top + i * step
        name = repo["name"] if len(repo["name"]) <= 19 else repo["name"][:18] + "…"
        lang = repo["language"]
        lang_col = (
            f'<circle cx="222" cy="-4" r="5" fill="{colors.get(lang, "#8B949E")}"/>'
            f'<text x="232" y="0" fill="{t["muted"]}" font-size="12">{escape(lang)}</text>'
            if lang else ""
        )
        lines.append(
            f'<g transform="translate(0,{y})">'
            f'<path fill="{t["icon"]}" transform="translate(25,-12)" d="{REPO_ICON}"/>'
            f'<text x="51" y="0" fill="{t["text"]}" font-size="14" font-weight="600">{escape(name)}</text>'
            f'{lang_col}<text x="{width - 25}" y="0" fill="{t["muted"]}" font-size="12" text-anchor="end">{ago(repo["pushed_at"])}</text>'
            "</g>"
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="Recently pushed repositories" {FONT}><title>Recently pushed repositories</title>'
        f'<text x="25" y="32" fill="{t["title"]}" font-size="18" font-weight="600">Recently Pushed</text>'
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
    "HTML": "#E34C26", "Ruby": "#701516",
}


def main():
    repos = fetch_repos()
    recent = sorted(
        (r for r in repos if not r["fork"] and r["name"].lower() != USER.lower()),
        key=lambda r: r["pushed_at"],
        reverse=True,
    )[:RECENT_COUNT]
    langs = fetch_languages(repos)

    os.makedirs("profile", exist_ok=True)
    for theme, t in THEMES.items():
        with open(f"profile/recent-{theme}.svg", "w", encoding="utf-8") as f:
            f.write(recent_svg(recent, LANG_COLORS, t))
        with open(f"profile/top-langs-{theme}.svg", "w", encoding="utf-8") as f:
            f.write(langs_svg(langs, LANG_COLORS, t))
    print("Recent:", ", ".join(f"{r['name']} ({ago(r['pushed_at'])})" for r in recent))
    print("Languages:", ", ".join(name for name, _ in langs[:LANG_COUNT]))


if __name__ == "__main__":
    main()
