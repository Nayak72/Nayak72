#!/usr/bin/env python3
"""Generates every SVG card used by README.md.
Live data (contributions, repo stars) is pulled when GH_TOKEN is set; otherwise placeholders are drawn."""
import os, json, base64, textwrap, datetime as dt, urllib.request
from xml.sax.saxutils import escape as esc

USER = "Nayak72"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
TOKEN = os.environ.get("GH_TOKEN", "")

SERIF = "'Instrument Serif','Cormorant Garamond',Georgia,'Times New Roman',serif"
SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'SF Mono',Menlo,Consolas,'Courier New',monospace"
CREAM, INK, MUTED = "#faf8f3", "#0e0e0e", "#6b6b6b"
BLUE, RED, YELLOW = "#0a3cff", "#d9141f", "#ffb800"
LEVELS = ["#e4e9fb", "#bcc8f7", "#8aa0f0", "#4f6be6", "#1f3fd1"]
W = 830

# ---------- content (from resume) ----------
EYEBROW = "SOFTWARE ENGINEER INTERN AT RAASHI"
FIRST, LAST = "Koushik", "Nayaka U"
TAGLINE = ["I build secure backends, make AI agents work,", "and ship APIs that hold up in production."]
SITE = "koushiknayaka72@gmail.com"
STAT_CARDS = [
    ("BUILD", BLUE, "3", "projects", ["RakshaSetu, HireIQ and CipherGuard:", "agents, RAG and security tooling."], "projects.svg"),
    ("PLACE", RED, "2nd", "place", ["Runner-up at Ignitrix Hackathon,", "KLE Tech, among 100+ teams."], "hackathon.svg"),
    ("SHORTLIST", YELLOW, "Top", "teams", ["Round 2 of EY Techathon 6.0,", "detailed presentation stage."], "ey.svg"),
]
REPOS = [
    ("RakshaSetu", BLUE, "Multi-agent disaster response: LangGraph, YOLOv8, RAG and Ollama behind a FastAPI backend."),
    ("HireIQ", RED, "AI resume screening: a 10-step pipeline with embeddings, weighted scoring and skill-gap analysis."),
    ("CipherGuard", YELLOW, "Password storage and cracking lab: MD5 to Argon2id vs dictionary, brute-force and rainbow attacks."),
]


def save(name, body, w, h):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as f:
        f.write(svg)


def api(path, graphql=None):
    url = "https://api.github.com/graphql" if graphql else f"https://api.github.com{path}"
    data = json.dumps({"query": graphql}).encode() if graphql else None
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "profile-readme"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def card(w, h, fill=CREAM, r=18):
    return f'<rect width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'


# ---------- hero ----------
def hero():
    h = 322
    b = card(W, h)
    b += f'<rect x="40" y="38" width="7" height="7" fill="{BLUE}"/>'
    b += f'<text x="56" y="46" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="{MUTED}">{esc(EYEBROW)}</text>'
    b += f'<text x="40" y="132" font-family="{SERIF}" font-size="84" fill="{INK}">{esc(FIRST)}</text>'
    b += (f'<text x="40" y="206" font-family="{SERIF}" font-style="italic" font-size="84" fill="{INK}">'
          f'{esc(LAST[:3])}<tspan fill="{BLUE}">{esc(LAST[3:5])}</tspan>{esc(LAST[5:])}</text>')
    for i, line in enumerate(TAGLINE):
        b += f'<text x="42" y="{238 + i*21}" font-family="{SANS}" font-size="15" fill="#2a2a2a">{esc(line)}</text>'
    b += f'<text x="42" y="292" font-family="{MONO}" font-size="12" fill="{INK}">{esc(SITE)} \u2197</text>'
    portrait = os.path.join(ASSETS, "portrait.png")
    if os.path.exists(portrait):
        enc = base64.b64encode(open(portrait, "rb").read()).decode()
        b += f'<image href="data:image/png;base64,{enc}" x="{W-300}" y="10" width="280" height="280" preserveAspectRatio="xMidYMid meet"/>'
    save("hero.svg", b, W, h)


# ---------- data ----------
def fetch_days():
    if not TOKEN:
        today = dt.date.today()
        return [(today - dt.timedelta(days=370 - i), 0) for i in range(371)], False
    q = '{ user(login:"%s"){ contributionsCollection{ contributionCalendar{ weeks{ contributionDays{ date contributionCount }}}}}}' % USER
    weeks = api(None, q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [(dt.date.fromisoformat(d["date"]), d["contributionCount"]) for w in weeks for d in w["contributionDays"]]
    return days, True


def heatmap(days, live):
    h = 250
    b = card(W, h)
    b += f'<text x="32" y="58" font-family="{SERIF}" font-size="30" fill="{INK}">Every day, <tspan font-style="italic" fill="#1f3fd1">in blue</tspan></text>'
    b += f'<text x="{W-32}" y="52" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="1.4" fill="{MUTED}">REFRESHED DAILY</text>'
    first = days[0][0]
    pad = (first.weekday() + 1) % 7  # Sunday-start weeks
    cells = [None] * pad + days
    cols = [cells[i:i + 7] for i in range(0, len(cells), 7)][-53:]
    nz = sorted(c for _, c in days if c > 0)

    def lvl(c):
        if c == 0 or not nz:
            return 0
        q = nz.index(c) / len(nz)
        return 1 if q < .25 else 2 if q < .5 else 3 if q < .75 else 4

    cs, gap, x0, y0 = 11.2, 3.0, 32, 84
    last_month = None
    for ci, col in enumerate(cols):
        for ri, cell in enumerate(col):
            if cell is None:
                continue
            _, c = cell
            b += f'<rect x="{x0 + ci*(cs+gap):.1f}" y="{y0 + ri*(cs+gap):.1f}" width="{cs}" height="{cs}" rx="2.5" fill="{LEVELS[lvl(c)]}"/>'
        first_d = next((c[0] for c in col if c), None)
        if first_d and first_d.month != last_month and (first_d.day <= 14 or ci == 0):
            last_month = first_d.month
            b += f'<text x="{x0 + ci*(cs+gap):.1f}" y="{y0 + 7*(cs+gap) + 18:.1f}" font-family="{MONO}" font-size="10" fill="{MUTED}">{first_d.strftime("%b")}</text>'
    lx = W - 32 - 5 * 14 - 62
    b += f'<text x="{lx}" y="{h-16}" font-family="{MONO}" font-size="10" fill="{MUTED}">less</text>'
    for i, col in enumerate(LEVELS):
        b += f'<rect x="{lx + 30 + i*14}" y="{h-26}" width="11" height="11" rx="2.5" fill="{col}"/>'
    b += f'<text x="{lx + 30 + 5*14 + 4}" y="{h-16}" font-family="{MONO}" font-size="10" fill="{MUTED}">more</text>'
    if not live:
        b += f'<text x="32" y="{h-16}" font-family="{MONO}" font-size="10" fill="{MUTED}">waiting for first workflow run</text>'
    save("heatmap.svg", b, W, h)


def contributions(days, live):
    h = 260
    b = card(W, h)
    last = days[-365:]
    total = sum(c for _, c in last)
    b += f'<text x="32" y="50" font-family="{MONO}" font-size="10" letter-spacing="1.4" fill="{MUTED}">THE LAST 12 MONTHS ON GITHUB</text>'
    b += f'<text x="32" y="96" font-family="{SERIF}" font-size="46" fill="{INK}">{total:,} <tspan font-style="italic" font-size="30">contributions</tspan></text>'
    today = dt.date.today()
    months, y, m = [], today.year, today.month
    for _ in range(12):
        months.append((y, m))
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    months.reverse()
    totals = [sum(c for d, c in days if (d.year, d.month) == k) for k in months]
    peak = max(totals) or 1
    bw, bg, bx, base, maxh = 32, 12, 32, 222, 80
    for i, (k, t) in enumerate(zip(months, totals)):
        bh = max(6, t / peak * maxh)
        fill = "#c9c9c9" if i == 11 else BLUE if t == max(totals) and t > 0 else INK
        b += f'<rect x="{bx + i*(bw+bg)}" y="{base-bh:.1f}" width="{bw}" height="{bh:.1f}" rx="3" fill="{fill}"/>'
        b += f'<text x="{bx + i*(bw+bg) + bw/2}" y="{base+16}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{MUTED}">{dt.date(k[0], k[1], 1).strftime("%b")}</text>'
    by_date = dict(days)
    streak, d = 0, today
    if by_date.get(d, 0) == 0:
        d -= dt.timedelta(days=1)
    while by_date.get(d, 0) > 0:
        streak += 1
        d -= dt.timedelta(days=1)
    active = sum(1 for _, c in last if c > 0)
    busiest = max((c for _, c in last), default=0)
    sx = 640
    stats = [(str(streak), " days", "current streak"), (f"{active}", f" / {len(last)}", "days with a commit"), (str(busiest), "", "on the busiest day")]
    for i, (big, small, sub) in enumerate(stats):
        yy = 52 + i * 68
        b += f'<text x="{sx}" y="{yy+30}" font-family="{SERIF}" font-size="38" fill="{INK}">{big}<tspan font-style="italic" font-size="22">{small}</tspan></text>'
        b += f'<text x="{sx}" y="{yy+50}" font-family="{SANS}" font-size="12" fill="{MUTED}">{sub}</text>'
    save("contributions.svg", b, W, h)


# ---------- colored stat cards ----------
def stat_cards():
    w, h = 270, 190
    for label, color, big, word, desc, name in STAT_CARDS:
        ink = INK if color == YELLOW else "#ffffff"
        b = card(w, h, color, 16)
        b += f'<text x="22" y="34" font-family="{MONO}" font-size="10" letter-spacing="1.4" fill="{ink}">{label}</text>'
        b += f'<text x="{w-22}" y="35" text-anchor="end" font-family="{SANS}" font-size="14" fill="{ink}">\u2192</text>'
        b += f'<text x="22" y="98" font-family="{SERIF}" font-size="46" fill="{ink}">{esc(big)} <tspan font-style="italic">{esc(word)}</tspan></text>'
        for i, line in enumerate(desc):
            b += f'<text x="22" y="{138 + i*17}" font-family="{SANS}" font-size="12" fill="{ink}">{esc(line)}</text>'
        save(name, b, w, h)


# ---------- repo cards ----------
def repo_cards():
    w, h = 270, 190
    for name, color, desc in REPOS:
        lang, stars = "Python", None
        if TOKEN:
            try:
                r = api(f"/repos/{USER}/{name}")
                lang, stars = r.get("language") or lang, r.get("stargazers_count")
            except Exception:
                pass
        b = card(w, h, "#ffffff", 14) + f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="#e6e3dc"/>'
        b += f'<rect x="22" y="30" width="8" height="8" fill="{color}"/>'
        b += f'<text x="38" y="39" font-family="{SANS}" font-size="16" font-weight="600" fill="{INK}">{esc(name)}</text>'
        for i, line in enumerate(textwrap.wrap(desc, 33)[:4]):
            b += f'<text x="22" y="{70 + i*18}" font-family="{SANS}" font-size="12.5" fill="#333">{esc(line)}</text>'
        meta = lang + (f"  \u00b7  \u2605 {stars}" if stars else "")
        b += f'<text x="22" y="{h-24}" font-family="{MONO}" font-size="11" fill="{MUTED}">{esc(meta)}</text>'
        save(f"repo-{name.lower()}.svg", b, w, h)


def heading():
    b = f'<text x="2" y="34" font-family="{SERIF}" font-size="32" fill="#e8e6e1">What I\u2019m <tspan font-style="italic">coding</tspan></text>'
    save("coding-heading.svg", b, 400, 50)


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    days, live = fetch_days()
    hero(); heatmap(days, live); contributions(days, live)
    stat_cards(); repo_cards(); heading()
    print("built", "with live data" if live else "with placeholders")
