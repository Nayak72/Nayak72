#!/usr/bin/env python3
"""Generates the Matrix-themed animated SVG cards for the profile README. Run: python scripts/build.py"""
import os, random, textwrap
from xml.sax.saxutils import escape as esc

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
MONO = "'JetBrains Mono','Fira Code','SF Mono',Menlo,Consolas,'Courier New',monospace"
SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
G, GL, BG, PANEL = "#00ff41", "#b8ffc9", "#020a04", "#04120a"
ACC = ["#00ff41", "#00e5a0", "#b6ff00"]
W = 830
BLINK = "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}} .cur{animation:blink 1s steps(1) infinite}"
TWINKLE = "@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}"


def save(name, body, w, h, css=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<style>{css}</style>{body}</svg>')
    open(os.path.join(ASSETS, name), "w", encoding="utf-8").write(svg)


def rain(w, h, seed, pitch=15, cs=12, dim=1.0):
    """Falling pixel columns with a bright head and fading trail -> (svg, css)."""
    rnd = random.Random(seed)
    css = f"@keyframes fall{{from{{transform:translateY(0)}}to{{transform:translateY({h + 420}px)}}}} .c{{animation:fall linear infinite}}"
    out = ""
    for i in range(w // pitch):
        L = rnd.randint(8, 17)
        dur, delay = rnd.uniform(5, 12), -rnd.uniform(0, 12)
        px = ""
        for j in range(L):
            if j and rnd.random() < 0.18:
                continue
            y = (L - 1 - j) * pitch
            fill, op = ("#e6ffec", 1) if j == 0 else (G, round(((1 - j / L) ** 1.5) * 0.85 * dim, 2))
            px += f'<rect x="{i*pitch+1}" y="{y}" width="{cs}" height="{cs}" rx="2" fill="{fill}" opacity="{op}"/>'
        out += f'<g transform="translate(0,{-L*pitch})"><g class="c" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s">{px}</g></g>'
    return out, css


# ---------------- hero ----------------
def hero():
    h = 392
    rn, rcss = rain(W, h, 7)
    css = rcss + BLINK + TWINKLE + """
    @keyframes glitch{0%,90%,100%{transform:translate(0,0);opacity:0}91%{transform:translate(-4px,1px);opacity:.7}93%{transform:translate(5px,-1px);opacity:.7}95%{transform:translate(-2px,0);opacity:.6}97%{transform:translate(0,0);opacity:0}}
    .g1{animation:glitch 6s steps(1) infinite}.g2{animation:glitch 6s steps(1) infinite .12s}
    @keyframes glow{0%,100%{filter:drop-shadow(0 0 6px #00ff41)}50%{filter:drop-shadow(0 0 14px #00ff41)}}
    .name{animation:glow 3s ease-in-out infinite}
    @keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
    .t1{animation:rise .8s ease-out .3s both}.t2{animation:rise .8s ease-out .7s both}.t3{animation:rise .8s ease-out 1.1s both}.t4{animation:rise .8s ease-out 1.5s both}
    .d{animation:tw 1.6s ease-in-out infinite}
    """
    b = f'<defs><clipPath id="rc"><rect width="{W}" height="{h}" rx="18"/></clipPath>'
    b += f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity=".93"/><stop offset=".62" stop-color="{BG}" stop-opacity=".8"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs>'
    b += f'<rect width="{W}" height="{h}" rx="18" fill="{BG}"/><g clip-path="url(#rc)">{rn}</g><rect width="{W}" height="{h}" rx="18" fill="url(#fade)"/>'
    b += f'<rect x="40" y="38" width="9" height="9" fill="{G}"/><text x="58" y="47" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{G}">EX-INTERN @ RAASHI COGNITIVE TECHNOLOGIES</text>'
    for cls, col in (("g1", "#ff003c"), ("g2", "#00e5ff")):
        b += f'<g class="{cls}"><text x="40" y="136" font-family="{MONO}" font-weight="700" font-size="64" fill="{col}">Koushik</text><text x="40" y="208" font-family="{MONO}" font-weight="700" font-size="64" fill="{col}">Nayaka U</text></g>'
    b += f'<g class="name"><text x="40" y="136" font-family="{MONO}" font-weight="700" font-size="64" fill="{G}">Koushik</text>'
    b += f'<text x="40" y="208" font-family="{MONO}" font-weight="700" font-size="64" fill="{G}">Nayaka U<tspan class="cur">_</tspan></text></g>'
    b += f'<text class="t1" x="42" y="246" font-family="{SANS}" font-size="15" fill="{GL}">I build Android apps and FastAPI backends, with AI agents</text>'
    b += f'<text class="t2" x="42" y="268" font-family="{SANS}" font-size="15" fill="{GL}">and secure APIs working behind them.</text>'
    # role chips
    chips = ""
    for i, (label, cx) in enumerate((("ANDROID DEVELOPER", 42), ("BACKEND DEVELOPER", 262))):
        chips += (f'<rect x="{cx}" y="292" width="200" height="38" rx="8" fill="{G}" fill-opacity=".1" stroke="{G}" stroke-opacity=".8"/>'
                  f'<rect class="d" style="animation-delay:{i*.5}s" x="{cx+14}" y="307" width="8" height="8" rx="1.5" fill="{G}"/>'
                  f'<text x="{cx+32}" y="316" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1.2" fill="{G}">{label}</text>')
    b += f'<g class="t3">{chips}</g>'
    b += f'<text class="t4" x="42" y="366" font-family="{MONO}" font-size="12" fill="{G}">&gt; koushiknayaka72@gmail.com</text>'
    save("hero.svg", b, W, h, css)


# ---------------- terminal ----------------
def terminal():
    lines = [
        ("$ whoami", True), ("koushik_nayaka_u  //  Android Developer + Backend Developer", False),
        ("$ cat education.txt", True), ("RVCE  \u00b7  B.E. CS & Cyber Security Engineering  \u00b7  2027", False),
        ("$ cat stack.txt", True), ("Kotlin \u00b7 Java \u00b7 Python \u00b7 SQL \u00b7 FastAPI \u00b7 LangGraph \u00b7 RAG \u00b7 YOLOv8", False),
        ("$ cat experience.log", True), ("ex-intern @ Raashi: FastAPI, RBAC, JWT, rate limiting, audit logs", False),
        ("$ ls achievements/", True), ("ignitrix-runner-up/   ey-techathon-round2/", False),
    ]
    h = 70 + len(lines) * 26 + 40
    total, cw, x0 = 20.0, 8.7, 28
    css = BLINK
    b = f'<rect width="{W}" height="{h}" rx="14" fill="{PANEL}" stroke="#0c3a1a"/>'
    b += f'<rect width="{W}" height="38" rx="14" fill="#08200f"/><rect y="24" width="{W}" height="14" fill="#08200f"/>'
    for i, c in enumerate(("#ff5f56", "#ffbd2e", G)):
        b += f'<circle cx="{24 + i*20}" cy="19" r="6" fill="{c}"/>'
    b += f'<text x="{W/2}" y="23" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#5fae78">koushik@matrix: ~</text>'
    t = 1.0
    for k, (txt, cmd) in enumerate(lines):
        n = len(txt)
        dur = max(0.5, n * 0.045) if cmd else 0.8
        s, e = t / total * 100, (t + dur) / total * 100
        css += (f"@keyframes t{k}{{0%,{s:.2f}%{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
                f"{e:.2f}%{{transform:translateX({n*cw:.0f}px)}}{e+.05:.2f}%,100%{{transform:translateX(900px)}}}}"
                f".l{k}{{animation:t{k} {total}s linear infinite}}")
        y = 72 + k * 26
        b += f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="14" fill="{G if cmd else GL}">{esc(txt)}</text>'
        b += f'<rect class="l{k}" x="{x0-2}" y="{y-16}" width="840" height="22" fill="{PANEL}"/>'
        t += dur + 0.35
    ly = 72 + len(lines) * 26
    b += f'<text x="{x0}" y="{ly}" font-family="{MONO}" font-size="14" fill="{G}">$ <tspan class="cur">\u2588</tspan></text>'
    save("terminal.svg", b, W, h, css)


# ---------------- skills ----------------
PW = 6.9  # approx mono char width at 11.5px


def pills(items, x, y, maxw, col, solid=False):
    out, cx, cy = "", x, y
    for it in items:
        pw = len(it) * PW + 24
        if cx + pw > x + maxw:
            cx, cy = x, cy + 34
        fillop = ".16" if solid else ".07"
        out += (f'<rect x="{cx}" y="{cy}" width="{pw:.0f}" height="26" rx="6" fill="{col}" fill-opacity="{fillop}" stroke="{col}" stroke-opacity="{.75 if solid else .4}"/>'
                f'<text x="{cx+12}" y="{cy+17}" font-family="{MONO}" font-size="11.5" fill="{GL if solid else "#9fd8b0"}">{esc(it)}</text>')
        cx += pw + 8
    return out, cy + 26


def panel(title, items, x, y, w, col, primary=False):
    body, endy = pills(items, x + 20, y + 60, w - 40, col, solid=primary)
    h = endy - y + 20
    return body, h


def skills():
    android = ["Kotlin", "Android Studio", "XML Layouts", "Activity & Fragment Lifecycle", "Intents", "RecyclerView", "Material Design", "REST API Integration", "MVVM"]
    backend = ["Python", "FastAPI", "REST APIs", "SQLAlchemy", "JWT Authentication", "API Design", "Database Design", "SQL"]
    secondary = [
        ("PROGRAMMING", ["Java", "Kotlin", "Python", "SQL"]),
        ("APPLIED AI", ["LangGraph", "Multi-Agent Systems", "RAG", "LLM Inference (Ollama, OpenRouter)", "Computer Vision (YOLOv8)"]),
        ("CORE CONCEPTS", ["DSA", "System Design Basics", "Authentication & Authorization", "Android App Architecture (MVVM)"]),
        ("DEV TOOLS", ["Android Studio", "VS Code", "Git", "IntelliJ IDEA", "Postman"]),
    ]
    colw, gap, top = 405, 20, 0
    css = BLINK + TWINKLE + ".d{animation:tw 1.8s ease-in-out infinite}"
    parts = []
    # primary row
    pa, ha = panel("ANDROID DEVELOPER", android, 0, top, colw, G, True)
    pb, hb = panel("BACKEND DEVELOPER", backend, colw + gap, top, colw, G, True)
    hp = max(ha, hb)
    b = ""
    for i, (title, body, x) in enumerate((("ANDROID DEVELOPER", pa, 0), ("BACKEND DEVELOPER", pb, colw + gap))):
        b += (f'<rect x="{x+.75}" y="{top+.75}" width="{colw-1.5}" height="{hp-1.5}" rx="14" fill="{PANEL}" stroke="{G}" stroke-opacity=".7"/>'
              f'<rect class="d" style="animation-delay:{i*.6}s" x="{x+22}" y="{top+24}" width="9" height="9" rx="1.5" fill="{G}"/>'
              f'<text x="{x+40}" y="{top+33}" font-family="{MONO}" font-size="15" font-weight="700" letter-spacing="1.2" fill="{G}">{title}</text>'
              f'<text x="{x+colw-22}" y="{top+32}" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="1.4" fill="#5fae78">PRIMARY</text>{body}')
    # secondary 2x2
    y = hp + gap
    rows = []
    for idx, (title, items) in enumerate(secondary):
        x = (idx % 2) * (colw + gap)
        body, h = panel(title, items, x, y, colw, ACC[1], False)
        rows.append((idx, title, body, x, h))
    h1 = max(rows[0][4], rows[1][4])
    h2 = max(rows[2][4], rows[3][4])
    for idx, title, body, x, h in rows:
        yy = y if idx < 2 else y + h1 + gap
        hh = h1 if idx < 2 else h2
        # re-render pills at proper y (panel() assumed y)
        items = secondary[idx][1]
        body, _ = pills(items, x + 20, yy + 56, colw - 40, ACC[1])
        b += (f'<rect x="{x+.75}" y="{yy+.75}" width="{colw-1.5}" height="{hh-1.5}" rx="14" fill="{PANEL}" stroke="#0f3d1d"/>'
              f'<rect x="{x+22}" y="{yy+22}" width="8" height="8" rx="1.5" fill="{ACC[1]}"/>'
              f'<text x="{x+40}" y="{yy+30}" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1.4" fill="{ACC[1]}">{title}</text>{body}')
    total_h = y + h1 + gap + h2
    save("skills.svg", b, W, total_h, css)


# ---------------- stat cards ----------------
def stat_cards():
    cards = [
        ("[BUILD]", "6", "projects", ["Android apps, FastAPI backends", "and AI agents, end to end."], "projects.svg", ACC[0]),
        ("[PLACE]", "2nd", "place", ["Runner-up at Ignitrix Hackathon,", "KLE Tech, among 100+ teams."], "hackathon.svg", ACC[1]),
        ("[SHORTLIST]", "Top", "teams", ["Round 2 of EY Techathon 6.0,", "detailed presentation stage."], "ey.svg", ACC[2]),
    ]
    w, h = 270, 190
    for lab, big, word, desc, name, col in cards:
        css = BLINK + TWINKLE + "".join(f".p{i}{{animation:tw {2+i*.7:.1f}s ease-in-out infinite {i*.4:.1f}s}}" for i in range(4)) + \
            "@keyframes scan{from{transform:translateY(-20px)}to{transform:translateY(210px)}}.sc{animation:scan 4.5s linear infinite}"
        b = f'<defs><clipPath id="k"><rect width="{w}" height="{h}" rx="16"/></clipPath></defs>'
        b += f'<rect width="{w}" height="{h}" rx="16" fill="{PANEL}"/><g clip-path="url(#k)"><rect class="sc" width="{w}" height="14" fill="{col}" opacity=".07"/></g>'
        b += f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="15.5" fill="none" stroke="{col}" stroke-opacity=".5"/>'
        b += f'<text x="22" y="34" font-family="{MONO}" font-size="11" letter-spacing="1.6" fill="{col}">{lab}</text>'
        for i, (dx, dy) in enumerate(((0, 0), (12, 0), (0, 12), (12, 12))):
            b += f'<rect class="p{i}" x="{w-46+dx}" y="{22+dy}" width="9" height="9" rx="1.5" fill="{col}"/>'
        b += f'<text x="22" y="100" font-family="{MONO}" font-weight="700" font-size="44" fill="{col}">{esc(big)}<tspan font-size="24" font-weight="400" fill="{GL}"> {esc(word)}</tspan></text>'
        for i, line in enumerate(desc):
            b += f'<text x="22" y="{140 + i*18}" font-family="{SANS}" font-size="12" fill="#a8d9b6">{esc(line)}</text>'
        save(name, b, w, h, css)


# ---------------- project cards ----------------
PROJECTS = [
    ("RakshaSetu", "raksha-setu", ACC[0], "ANDROID + BACKEND",
     "Disaster response: a LangGraph multi-agent workflow with YOLOv8 vision and RAG on local Ollama LLMs.",
     "FastAPI \u00b7 LangGraph \u00b7 YOLOv8 \u00b7 RAG"),
    ("AgriChain", "agri-chain", ACC[1], "BACKEND",
     "Agri supply chain and freight platform: six user roles, JWT auth and a SHA-256 hash-chained audit ledger.",
     "FastAPI \u00b7 JWT \u00b7 REST APIs"),
    ("CarbonTrust", "carbontrust-blockchain", ACC[2], "ANDROID + BACKEND",
     "Carbon credit verification: IoT data checked for anomalies, credits minted on-chain, native Android app.",
     "FastAPI \u00b7 Kotlin \u00b7 Android"),
    ("HireIQ", "ai-hiring-intelligence", ACC[0], "ANDROID + BACKEND",
     "Recruitment platform with a 10-step AI screening pipeline and a native Android app for recruiters and applicants.",
     "FastAPI \u00b7 Kotlin \u00b7 MVVM \u00b7 LLM"),
    ("API Testing Platform", "ai-based-api-testing-platform", ACC[1], "BACKEND + AI",
     "Autonomous API security testing: LLM agents with RAG over the OWASP API Top 10 and live SSE tracing.",
     "FastAPI \u00b7 RAG \u00b7 SSE \u00b7 Multi-Agent"),
    ("CipherGuard", "cipherguard", ACC[2], "BACKEND + SECURITY",
     "Password security lab: MD5 to Argon2id hashing tested against simulated dictionary, brute-force and rainbow-table attacks.",
     "FastAPI \u00b7 Argon2id \u00b7 SSE \u00b7 JWT"),
]


def project_cards():
    w, h = 270, 215
    for name, slug, col, badge, desc, tags in PROJECTS:
        b = f'<rect width="{w}" height="{h}" rx="14" fill="{PANEL}"/><rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="13.5" fill="none" stroke="#0f3d1d"/>'
        b += f'<rect x="22" y="26" width="9" height="9" rx="1.5" fill="{col}"/><text x="40" y="35" font-family="{MONO}" font-size="15" font-weight="700" fill="{col}">{esc(name)}</text>'
        bw = len(badge) * 6.6 + 18
        b += f'<rect x="22" y="48" width="{bw:.0f}" height="20" rx="5" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>'
        b += f'<text x="31" y="62" font-family="{MONO}" font-size="10" letter-spacing=".8" fill="{col}">{badge}</text>'
        for i, line in enumerate(textwrap.wrap(desc, 33)[:4]):
            b += f'<text x="22" y="{92 + i*18}" font-family="{SANS}" font-size="12.5" fill="#b3dfc0">{esc(line)}</text>'
        b += f'<text x="22" y="{h-22}" font-family="{MONO}" font-size="11" fill="#5fae78">{esc(tags)}</text>'
        save(f"project-{slug}.svg", b, w, h)


def heading(name, text):
    w = 14 + len(text) * 15 + 40
    b = f'<rect width="{w}" height="44" rx="10" fill="{PANEL}" stroke="#0f3d1d"/>'
    b += f'<text x="18" y="29" font-family="{MONO}" font-size="20" font-weight="700" fill="{G}">&gt; {esc(text)}<tspan class="cur">_</tspan></text>'
    save(name, b, w, 44, BLINK)


def footer():
    lines = [("$ contact --koushik", True),
             ("koushiknayaka72@gmail.com  \u00b7  LinkedIn  \u00b7  GitHub  \u00b7  Bengaluru, India", False),
             ("$ echo \"let's build something\"", True)]
    h = 70 + len(lines) * 26 + 30
    total, cw, x0 = 12.0, 8.7, 28
    css = BLINK
    b = f'<rect width="{W}" height="{h}" rx="14" fill="{PANEL}" stroke="#0c3a1a"/>'
    b += f'<rect width="{W}" height="38" rx="14" fill="#08200f"/><rect y="24" width="{W}" height="14" fill="#08200f"/>'
    for i, c in enumerate(("#ff5f56", "#ffbd2e", G)):
        b += f'<circle cx="{24 + i*20}" cy="19" r="6" fill="{c}"/>'
    b += f'<text x="{W/2}" y="23" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#5fae78">connect.sh</text>'
    t = 0.8
    for k, (txt, cmd) in enumerate(lines):
        n = len(txt)
        dur = max(0.5, n * 0.045) if cmd else 0.8
        sp, ep = t / total * 100, (t + dur) / total * 100
        css += (f"@keyframes f{k}{{0%,{sp:.2f}%{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
                f"{ep:.2f}%{{transform:translateX({n*cw:.0f}px)}}{ep+.05:.2f}%,100%{{transform:translateX(900px)}}}}"
                f".f{k}{{animation:f{k} {total}s linear infinite}}")
        y = 72 + k * 26
        b += f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="14" fill="{G if cmd else GL}">{esc(txt)}</text>'
        b += f'<rect class="f{k}" x="{x0-2}" y="{y-16}" width="840" height="22" fill="{PANEL}"/>'
        t += dur + 0.4
    ly = 72 + len(lines) * 26
    b += f'<text x="{x0}" y="{ly}" font-family="{MONO}" font-size="14" fill="{G}">$ <tspan class="cur">\u2588</tspan></text>'
    save("footer.svg", b, W, h, css)


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    hero(); terminal(); skills(); stat_cards(); project_cards()
    heading("skills-heading.svg", "tech_stack"); heading("projects-heading.svg", "featured_projects"); footer()
    print("built")
