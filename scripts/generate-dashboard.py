#!/usr/bin/env python3
import html
import json
import os
import urllib.request

USERNAME = os.environ.get("USERNAME", "AnandBinuArjun")
OUT = "security-dashboard.svg"

def get_json(url):
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "github-profile-dashboard"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def esc(value):
    return html.escape(str(value), quote=True)

user = get_json(f"https://api.github.com/users/{USERNAME}")
repos = []
for page in range(1, 11):
    batch = get_json(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}&type=owner"
    )
    if not batch:
        break
    repos.extend(batch)
    if len(batch) < 100:
        break

public_repos = user.get("public_repos", len(repos))
followers = user.get("followers", 0)
following = user.get("following", 0)

top = sorted(
    repos,
    key=lambda r: (r.get("stargazers_count", 0), r.get("forks_count", 0)),
    reverse=True,
)[:5]

max_star = max([r.get("stargazers_count", 0) for r in top] + [1])
name_map = {
    "SENTINEL-IOT": "SENTINEL-IoT",
    "threat-intelligence-cti-analysis": "CTI Analysis",
    "AI-Powered-Personal-Digital-Safety-Assistant": "AI Digital Safety",
    "TOTAL-ENTITY": "TOTAL ENTITY",
    "TOTAL-ENTITY-Exposure-Monitor": "TOTAL ENTITY",
}

def display_name(name):
    return name_map.get(name, name[:20])

ys = [294, 336, 378, 420, 462]
colors = ["#34d399", "#8b5cf6", "#8b5cf6", "#22d3ee", "#22d3ee"]
rows = []
for item, y, color in zip(top, ys, colors):
    stars = item.get("stargazers_count", 0)
    width = max(8, int(360 * stars / max_star))
    rows.append(
        f'<text x="338" y="{y}" fill="#94a3b8">{esc(display_name(item.get("name", "repo")))}</text>'
        f'<rect x="472" y="{y-11}" width="360" height="15" rx="7" fill="#171e2d"/>'
        f'<rect x="472" y="{y-11}" width="{width}" height="15" rx="7" fill="{color}"/>'
        f'<text x="846" y="{y+1}" fill="#e2e8f0">{stars}</text>'
    )
project_rows = "".join(rows)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="560" viewBox="0 0 1200 560">
<title>Anand Binu Arjun — Cybersecurity Developer Dashboard</title>
<desc>Live GitHub cybersecurity developer dashboard with identity, metrics, projects and current work.</desc>
<rect width="1200" height="560" rx="28" fill="#05070b"/>
<rect x="1" y="1" width="1198" height="558" rx="27" fill="none" stroke="#22d3ee" stroke-opacity=".65"/>
<rect x="182" y="-22" width="28" height="112" rx="8" fill="#8b5cf6"/>
<rect x="184" y="-18" width="24" height="78" fill="#22d3ee" fill-opacity=".28"/>
<text x="196" y="42" text-anchor="middle" transform="rotate(90 196 42)" fill="#f8fafc" font-family="monospace" font-size="7" letter-spacing="2">SECURITY OPERATIONS</text>
<circle cx="196" cy="87" r="10" fill="#0f172a" stroke="#94a3b8" stroke-width="3"/>
<circle cx="196" cy="87" r="3" fill="#22d3ee"/>

<g font-family="monospace">
<text x="300" y="47" fill="#a78bfa" font-size="11" letter-spacing="2">// DEVELOPER DASHBOARD</text>
<text x="300" y="81" fill="#f8fafc" font-family="Arial, sans-serif" font-size="28" font-weight="700">Profile at a glance</text>
<rect x="1034" y="34" width="132" height="25" rx="13" fill="#071b17" stroke="#34d399" stroke-opacity=".55"/>
<circle cx="1050" cy="46.5" r="4" fill="#34d399"/>
<text x="1061" y="50" fill="#34d399" font-size="8" letter-spacing="1">LIVE · GITHUB</text>
</g>

<rect x="36" y="106" width="250" height="408" rx="21" fill="#0a101a" stroke="#22d3ee" stroke-opacity=".55"/>
<rect x="52" y="122" width="218" height="34" rx="9" fill="#08131d" stroke="#1e293b"/>
<text x="67" y="144" fill="#22d3ee" font-family="monospace" font-size="9" letter-spacing="1.5">DEVELOPER ID</text>
<text x="253" y="144" text-anchor="end" fill="#64748b" font-family="monospace" font-size="8">AA · LIVE</text>
<defs><clipPath id="idPortrait"><rect x="67" y="174" width="188" height="126" rx="16"/></clipPath></defs>
<rect x="67" y="174" width="188" height="126" rx="16" fill="#0f172a" stroke="#8b5cf6" stroke-opacity=".7"/>
<image href="assets/anand-footer.jpg" x="67" y="174" width="188" height="126" preserveAspectRatio="xMidYMid slice" clip-path="url(#idPortrait)"/>
<rect x="67" y="174" width="188" height="126" rx="16" fill="none" stroke="#22d3ee" stroke-opacity=".35"/>
<rect x="78" y="267" width="166" height="22" rx="8" fill="#05070b" fill-opacity=".82"/>
<text x="161" y="281" text-anchor="middle" fill="#94a3b8" font-family="monospace" font-size="7">CYBERSECURITY ENGINEER</text>
<text x="67" y="328" fill="#f8fafc" font-family="Arial, sans-serif" font-size="17" font-weight="800">ANAND BINU ARJUN</text>
<text x="67" y="349" fill="#22d3ee" font-family="monospace" font-size="9">AI · SECURITY · IoT · FORENSICS</text>
<line x1="67" y1="367" x2="255" y2="367" stroke="#1e293b"/>
<text x="67" y="390" fill="#64748b" font-family="monospace" font-size="8">BASE</text>
<text x="67" y="407" fill="#e2e8f0" font-family="monospace" font-size="10">UNITED KINGDOM</text>
<text x="67" y="432" fill="#64748b" font-family="monospace" font-size="8">SPECIALTY</text>
<text x="67" y="449" fill="#e2e8f0" font-family="monospace" font-size="9">SECURITY SYSTEMS</text>
<text x="67" y="474" fill="#64748b" font-family="monospace" font-size="8">MODE</text>
<text x="67" y="491" fill="#34d399" font-family="monospace" font-size="9">BUILD · RESEARCH · SHIP</text>

<g font-family="monospace">
<rect x="312" y="106" width="190" height="78" rx="14" fill="#0d1220" stroke="#334155"/>
<rect x="329" y="121" width="20" height="3" rx="1" fill="#22d3ee"/>
<text x="329" y="146" fill="#64748b" font-size="8">PUBLIC REPOS</text>
<text x="329" y="173" fill="#f8fafc" font-family="Arial" font-size="25" font-weight="800">{public_repos}</text>
<rect x="514" y="106" width="190" height="78" rx="14" fill="#0d1220" stroke="#334155"/>
<rect x="531" y="121" width="20" height="3" rx="1" fill="#fbbf24"/>
<text x="531" y="146" fill="#64748b" font-size="8">TOP PROJECT</text>
<text x="531" y="173" fill="#f8fafc" font-family="Arial" font-size="25" font-weight="800">{top[0].get("stargazers_count", 0) if top else 0}★</text>
<rect x="716" y="106" width="190" height="78" rx="14" fill="#0d1220" stroke="#334155"/>
<rect x="733" y="121" width="20" height="3" rx="1" fill="#a78bfa"/>
<text x="733" y="146" fill="#64748b" font-size="8">FOLLOWERS</text>
<text x="733" y="173" fill="#f8fafc" font-family="Arial" font-size="25" font-weight="800">{followers}</text>
<rect x="918" y="106" width="248" height="78" rx="14" fill="#0d1220" stroke="#334155"/>
<rect x="935" y="121" width="20" height="3" rx="1" fill="#f472b6"/>
<text x="935" y="146" fill="#64748b" font-size="8">FOLLOWING</text>
<text x="935" y="173" fill="#f8fafc" font-family="Arial" font-size="25" font-weight="800">{following}</text>
<text x="1050" y="146" fill="#64748b" font-size="8">FOCUS</text>
<text x="1050" y="166" fill="#34d399" font-size="8">SECURITY + AI</text>
</g>

<rect x="312" y="202" width="594" height="312" rx="18" fill="#0a101a" stroke="#334155"/>
<text x="338" y="234" fill="#f8fafc" font-family="Arial, sans-serif" font-size="17" font-weight="700">MOST-STARRED SECURITY PROJECTS</text>
<text x="338" y="254" fill="#64748b" font-family="monospace" font-size="8">PUBLIC REPOSITORIES · CURRENT GITHUB SNAPSHOT</text>
<g font-family="monospace" font-size="9">{project_rows}</g>
<text x="338" y="493" fill="#475569" font-family="monospace" font-size="7">STAR COUNT · TOP PUBLIC REPOSITORIES</text>

<rect x="926" y="202" width="240" height="145" rx="18" fill="#0a101a" stroke="#334155"/>
<text x="949" y="229" fill="#f472b6" font-family="monospace" font-size="9">COMMUNITY</text>
<text x="949" y="267" fill="#f8fafc" font-family="Arial" font-size="24" font-weight="800">{followers}</text>
<text x="949" y="284" fill="#64748b" font-family="monospace" font-size="7">FOLLOWERS</text>
<text x="1040" y="267" fill="#f8fafc" font-family="Arial" font-size="24" font-weight="800">{following}</text>
<text x="1040" y="284" fill="#64748b" font-family="monospace" font-size="7">FOLLOWING</text>
<line x1="949" y1="300" x2="1143" y2="300" stroke="#1e293b"/>
<text x="949" y="321" fill="#94a3b8" font-family="monospace" font-size="8">@{esc(USERNAME)}</text>

<rect x="926" y="366" width="240" height="148" rx="18" fill="#0a101a" stroke="#334155"/>
<circle cx="950" cy="392" r="4" fill="#34d399"/>
<text x="962" y="396" fill="#34d399" font-family="monospace" font-size="9">BUILDING</text>
<text x="949" y="423" fill="#e2e8f0" font-family="monospace" font-size="9">SHIELDDESK</text>
<text x="949" y="440" fill="#94a3b8" font-family="monospace" font-size="7">AI-assisted SOC control plane</text>
<text x="949" y="467" fill="#e2e8f0" font-family="monospace" font-size="9">SENTINEL-IoT</text>
<text x="949" y="484" fill="#94a3b8" font-family="monospace" font-size="7">IoT threat intelligence</text>
<text x="949" y="505" fill="#a78bfa" font-family="monospace" font-size="7">RESEARCH · BUILD · VERIFY</text>
</svg>
'''

with open(OUT, "w", encoding="utf-8") as file:
    file.write(svg)

print(f"Generated {OUT}: {public_repos} repos, {followers} followers, {following} following, top project {top[0].get('stargazers_count', 0) if top else 0} stars.")
