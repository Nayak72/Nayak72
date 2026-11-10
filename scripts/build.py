#!/usr/bin/env python3
"""Generates the Matrix-themed animated SVG cards for the profile README. Run: python scripts/build.py"""
import os, random, textwrap
from xml.sax.saxutils import escape as esc

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
MONO = "'JetBrains Mono','Fira Code','SF Mono',Menlo,Consolas,'Courier New',monospace"
SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
G, GL, BG, PANEL = "#00ff41", "#b8ffc9", "#020a04", "#04120a"
W = 830

def save(name, body, w, h, css=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<style>{css}</style>{body}</svg>')
    open(os.path.join(ASSETS, name), "w", encoding="utf-8").write(svg)

BLINK = "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}} .cur{animation:blink 1s steps(1) infinite}"

def rain_wrapped(w, h, seed, **kw):
    rnd = random.Random(seed)
    pitch, cs, dim = kw.get("pitch", 15), kw.get("cs", 12), kw.get("dim", 1.0)
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
    h = 352
    rn, rcss = rain_wrapped(W, h, 7)
    css = rcss + BLINK + """
    @keyframes glitch{0%,90%,100%{transform:translate(0,0);opacity:0}91%{transform:translate(-4px,1px);opacity:.7}93%{transform:translate(5px,-1px);opacity:.7}95%{transform:translate(-2px,0);opacity:.6}97%{transform:translate(0,0);opacity:0}}
    .g1{animation:glitch 6s steps(1) infinite}.g2{animation:glitch 6s steps(1) infinite .12s}
    @keyframes glow{0%,100%{filter:drop-shadow(0 0 6px #00ff41)}50%{filter:drop-shadow(0 0 14px #00ff41)}}
    .name{animation:glow 3s ease-in-out infinite}
    @keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
    .t1{animation:rise .8s ease-out .3s both}.t2{animation:rise .8s ease-out .7s both}.t3{animation:rise .8s ease-out 1.1s both}
    """
    b = f'<rect width="{W}" height="{h}" rx="18" fill="{BG}"/><g>{rn}</g>'
    b += f'<defs><linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity=".92"/><stop offset=".62" stop-color="{BG}" stop-opacity=".8"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
    b += f'<clipPath id="rc"><rect width="{W}" height="{h}" rx="18"/></clipPath></defs>'
    b = b.replace(f'<g>{rn}</g>', f'<g clip-path="url(#rc)">{rn}</g>')
    b += f'<rect width="{W}" height="{h}" rx="18" fill="url(#fade)"/>'
    b += f'<rect x="40" y="38" width="9" height="9" fill="{G}"/><text x="58" y="47" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{G}">EX-INTERN @ RAASHI COGNITIVE TECHNOLOGIES</text>'
    for cls, col, dx in (("g1", "#ff003c", 0), ("g2", "#00e5ff", 0)):
        b += f'<g class="{cls}"><text x="40" y="150" font-family="{MONO}" font-weight="700" font-size="64" fill="{col}">Koushik</text><text x="40" y="222" font-family="{MONO}" font-weight="700" font-size="64" fill="{col}">Nayaka U</text></g>'
    b += f'<g class="name"><text x="40" y="150" font-family="{MONO}" font-weight="700" font-size="64" fill="{G}">Koushik</text>'
    b += f'<text x="40" y="222" font-family="{MONO}" font-weight="700" font-size="64" fill="{G}">Nayaka U<tspan class="cur" fill="{G}">_</tspan></text></g>'
    b += f'<text class="t1" x="42" y="264" font-family="{SANS}" font-size="15" fill="{GL}">I build secure backends, make AI agents work,</text>'
    b += f'<text class="t2" x="42" y="286" font-family="{SANS}" font-size="15" fill="{GL}">and ship APIs that hold up in production.</text>'
    b += f'<text class="t3" x="42" y="326" font-family="{MONO}" font-size="12" fill="{G}">&gt; koushiknayaka72@gmail.com</text>'
    save("hero.svg", b, W, h, css)

# ---------------- terminal ----------------
def terminal():
    lines = [
        ("$ whoami", True), ("koushik_nayaka_u  //  RVCE, CS & Cyber Security Engineering '27", False),
        ("$ cat stack.txt", True), ("Python \u00b7 FastAPI \u00b7 Kotlin \u00b7 Java \u00b7 SQL \u00b7 LangGraph \u00b7 RAG \u00b7 YOLOv8", False),
        ("$ cat experience.log", True), ("ex-intern @ Raashi: RBAC, JWT, rate limiting, audit logging", False),
        ("$ ls achievements/", True), ("ignitrix-runner-up/   ey-techathon-round2/", False),
    ]
    h = 70 + len(lines) * 26 + 40
    total, cw, x0 = 18.0, 8.7, 28
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
        dist = n * cw
        css += (f"@keyframes t{k}{{0%,{s:.2f}%{{transform:translateX(0);animation-timing-function:steps({n},end)}}"
                f"{e:.2f}%{{transform:translateX({dist:.0f}px)}}{e+.05:.2f}%,100%{{transform:translateX(900px)}}}}"
                f".l{k}{{animation:t{k} {total}s linear infinite}}")
        y = 72 + k * 26
        fill = G if cmd else GL
        b += f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="14" fill="{fill}">{esc(txt)}</text>'
        b += f'<rect class="l{k}" x="{x0-2}" y="{y-16}" width="820" height="22" fill="{PANEL}"/>'
        t += dur + 0.35
    ly = 72 + len(lines) * 26
    b += f'<text x="{x0}" y="{ly}" font-family="{MONO}" font-size="14" fill="{G}">$ <tspan class="cur">\u2588</tspan></text>'
    save("terminal.svg", b, W, h, css)

# ---------------- stat cards ----------------
def stat_cards():
    cards = [
        ("[BUILD]", "3", "projects", ["RakshaSetu, HireIQ and CipherGuard:", "agents, RAG and security tooling."], "projects.svg", "#00ff41"),
        ("[PLACE]", "2nd", "place", ["Runner-up at Ignitrix Hackathon,", "KLE Tech, among 100+ teams."], "hackathon.svg", "#00e5a0"),
        ("[SHORTLIST]", "Top", "teams", ["Round 2 of EY Techathon 6.0,", "detailed presentation stage."], "ey.svg", "#b6ff00"),
    ]
    w, h = 270, 190
    for n, (lab, big, word, desc, name, col) in enumerate(cards):
        css = BLINK + "@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}" + \
              "".join(f".p{i}{{animation:tw {2+i*.7:.1f}s ease-in-out infinite {i*.4:.1f}s}}" for i in range(4)) + \
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

# ---------------- repo cards ----------------
def repo_cards():
    repos = [
        ("RakshaSetu", "#00ff41", "Multi-agent disaster response: LangGraph, YOLOv8, RAG and Ollama behind a FastAPI backend.", "LangGraph \u00b7 YOLOv8 \u00b7 RAG"),
        ("HireIQ", "#00e5a0", "AI resume screening: a 10-step pipeline with embeddings, weighted scoring and skill-gap analysis.", "FastAPI \u00b7 embeddings \u00b7 LLM"),
        ("CipherGuard", "#b6ff00", "Password storage and cracking lab: MD5 to Argon2id vs dictionary, brute-force and rainbow attacks.", "FastAPI \u00b7 Argon2id \u00b7 SSE"),
    ]
    w, h = 270, 190
    for name, col, desc, tags in repos:
        b = f'<rect width="{w}" height="{h}" rx="14" fill="{PANEL}"/><rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="13.5" fill="none" stroke="#0f3d1d"/>'
        b += f'<rect x="22" y="28" width="9" height="9" rx="1.5" fill="{col}"/><text x="40" y="37" font-family="{MONO}" font-size="15" font-weight="700" fill="{col}">{esc(name)}</text>'
        for i, line in enumerate(textwrap.wrap(desc, 33)[:4]):
            b += f'<text x="22" y="{66 + i*18}" font-family="{SANS}" font-size="12.5" fill="#b3dfc0">{esc(line)}</text>'
        b += f'<text x="22" y="{h-22}" font-family="{MONO}" font-size="11" fill="#5fae78">{esc(tags)}</text>'
        save(f"repo-{name.lower()}.svg", b, w, h)

def heading(name, text):
    css = BLINK
    w = 14 + len(text) * 15 + 40
    b = f'<rect width="{w}" height="44" rx="10" fill="{PANEL}" stroke="#0f3d1d"/>'
    b += f'<text x="18" y="29" font-family="{MONO}" font-size="20" font-weight="700" fill="{G}">&gt; {esc(text)}<tspan class="cur">_</tspan></text>'
    save(name, b, w, 44, css)

def footer():
    h = 120
    rn, rcss = rain_wrapped(W, h, 21, dim=.55)
    css = rcss + BLINK
    b = f'<defs><clipPath id="f"><rect width="{W}" height="{h}" rx="14"/></clipPath></defs><rect width="{W}" height="{h}" rx="14" fill="{BG}"/>'
    b += f'<g clip-path="url(#f)">{rn}</g><rect width="{W}" height="{h}" rx="14" fill="{BG}" opacity=".55"/>'
    b += f'<text x="{W/2}" y="56" text-anchor="middle" font-family="{MONO}" font-size="20" font-weight="700" fill="{G}">Follow the white rabbit<tspan class="cur">_</tspan></text>'
    b += f'<text x="{W/2}" y="86" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{GL}">koushiknayaka72@gmail.com  \u00b7  Bengaluru, India</text>'
    save("footer.svg", b, W, h, css)

if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    hero(); terminal(); stat_cards(); repo_cards(); heading("coding-heading.svg", "what_i_am_coding"); footer()
    print("built")
