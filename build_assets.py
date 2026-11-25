#!/usr/bin/env python3
"""
Soban Ahmed - animated GitHub profile generator.
Run:  python3 build_assets.py
Writes every SVG into ./assets and README.md next to this file.
Edit the DATA section (skills levels, links, text) and re-run.
"""
import os, random, html
from urllib.parse import quote_plus

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

# ---------- theme (same as the original profile) ----------
O = "#FF7A1A"      # orange accent
AMB = "#FFB066"    # soft amber
BG = "#0B0C0F"
PANEL = "#13151A"
LINE = "#23262D"
TXT = "#E8E8EA"
MUT = "#8A8F98"
MONO = "'JetBrains Mono','SF Mono','Fira Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"

# ---------- DATA you can edit ----------
USER = "SobanAhmed96"
EMAIL = "sobanahmed9898@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/soban-ahmed-b50b30316/"
PORTFOLIO = "https://potfolio-two-weld.vercel.app/"
# self-rated levels 0-100 (edit to match reality)
SKILLS = [
    ("React.js", 85), ("Angular", 72),
    ("Node / Express", 70), ("MongoDB", 68),
    ("REST APIs", 80), ("Responsive UI", 90),
    ("Flutter", 62), ("Git / GitHub", 75),
]


def esc(s):
    return html.escape(s, quote=False)


def svg(w, h, body, defs="", style="", bg=False):
    if bg:
        body = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{BG}" stroke="{LINE}"/>\n' + body
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
<defs>{defs}<style>
text{{font-family:{SANS}}}
.m{{font-family:{MONO}}}
{style}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style></defs>
{body}
</svg>'''


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


SWEEP = f'<linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{O}" stop-opacity="0"/><stop offset=".5" stop-color="{O}"/><stop offset="1" stop-color="{O}" stop-opacity="0"/></linearGradient>'


# =====================================================================
# HERO
# =====================================================================
def hero():
    w, h = 1000, 360
    rnd = random.Random(7)
    defs = f'''
<pattern id="g" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{O}" stroke-opacity=".07"/></pattern>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{O}" stop-opacity=".38"/><stop offset="1" stop-color="{O}" stop-opacity="0"/></radialGradient>
<linearGradient id="nm" x1="0" x2="1.2" spreadMethod="reflect"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="{O}"/><stop offset="1" stop-color="{AMB}"/>
<animate attributeName="x1" values="0;1.2" dur="5s" repeatCount="indefinite"/><animate attributeName="x2" values="1.2;2.4" dur="5s" repeatCount="indefinite"/></linearGradient>
<clipPath id="card"><rect width="{w}" height="{h}" rx="16"/></clipPath>
<clipPath id="sub"><rect x="56" y="200" height="34" width="0"><animate attributeName="width" values="0;0;420;420;0" keyTimes="0;.12;.42;.93;1" dur="10s" repeatCount="indefinite"/></rect></clipPath>
{SWEEP}
'''
    style = f'''
.drift{{animation:drift 7s linear infinite}}
@keyframes drift{{to{{transform:translate(32px,32px)}}}}
.draw{{fill-opacity:0;stroke-dasharray:3000;stroke-dashoffset:3000;animation:draw 2.6s ease forwards,fin .9s 1.9s ease forwards,sf 3s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes fin{{to{{fill-opacity:1}}}}
@keyframes sf{{0%,70%{{stroke-opacity:1}}100%{{stroke-opacity:0}}}}
.ln{{opacity:0;animation:ln 11s infinite}}
@keyframes ln{{0%{{opacity:0;transform:translateX(-10px)}}5%,86%{{opacity:1;transform:none}}94%,100%{{opacity:0}}}}
.fl{{animation:fl 4s ease-in-out infinite}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-12px)}}}}
.fade{{opacity:0;animation:fo 1s 2.6s ease forwards}}
@keyframes fo{{to{{opacity:1}}}}
.pulse{{animation:pu 1.8s ease-in-out infinite}}
@keyframes pu{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
'''
    parts = [f'<g clip-path="url(#card)"><rect width="{w}" height="{h}" fill="{BG}"/>',
             f'<rect class="drift" x="-32" y="-32" width="{w+64}" height="{h+64}" fill="url(#g)"/>',
             f'<ellipse cx="760" cy="180" rx="330" ry="210" fill="url(#glow)"><animate attributeName="opacity" values=".55;1;.55" dur="5s" repeatCount="indefinite"/></ellipse>']
    # particles
    for _ in range(20):
        x = rnd.randint(10, w - 10)
        r = rnd.choice([1.2, 1.6, 2, 2.6])
        d = rnd.uniform(8, 16)
        parts.append(f'<circle cx="{x}" r="{r}" fill="{O}"><animate attributeName="cy" values="{h+10};-10" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.55;0" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>')
    # left text
    parts += [
        f'<text class="m ln" x="56" y="96" font-size="15" fill="{O}" style="animation-delay:0s">&lt;hello-world /&gt;</text>',
        f'<text class="draw" x="56" y="172" font-size="60" font-weight="800" fill="url(#nm)" stroke="{O}" stroke-width="1.4" letter-spacing="-1">Soban Ahmed</text>',
        f'<g clip-path="url(#sub)"><text class="m" x="56" y="226" font-size="22" font-weight="600" fill="{TXT}">MERN Stack · Frontend Developer</text></g>',
        f'<rect x="56" y="206" width="11" height="26" fill="{O}"><animate attributeName="x" values="56;56;474;474;56" keyTimes="0;.12;.42;.93;1" dur="10s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0;1;0;1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>',
        f'<text class="fade" x="56" y="268" font-size="15" fill="{MUT}">Frontend Developer @ Airtech Solutions · Karachi, Pakistan</text>',
        f'<g class="fade"><circle cx="62" cy="304" r="5" fill="{O}" class="pulse"/><text x="76" y="309" font-size="15" font-weight="600" fill="{O}">Open to opportunities</text></g>',
    ]
    # code card
    parts.append(f'<g class="fl" style="animation-duration:6s"><rect x="560" y="52" width="384" height="250" rx="14" fill="{PANEL}" stroke="{LINE}"/><rect x="560" y="52" width="384" height="34" rx="14" fill="#191C22"/><rect x="560" y="72" width="384" height="14" fill="#191C22"/>'
                 f'<circle cx="580" cy="69" r="5" fill="#FF5F57"/><circle cx="598" cy="69" r="5" fill="#FEBC2E"/><circle cx="616" cy="69" r="5" fill="{O}"/>'
                 f'<text class="m" x="752" y="73" font-size="12" fill="{MUT}" text-anchor="middle">soban.js</text>')
    code = [
        (f'<tspan fill="{O}">const</tspan> <tspan fill="{TXT}">soban</tspan> <tspan fill="{MUT}">= {{</tspan>'),
        (f'  <tspan fill="{MUT}">role:</tspan> <tspan fill="{AMB}">"Frontend Dev"</tspan>,'),
        (f'  <tspan fill="{MUT}">stack:</tspan> <tspan fill="{AMB}">["React","Node"]</tspan>,'),
        (f'  <tspan fill="{MUT}">systems:</tspan> <tspan fill="{AMB}">["POS","KDS","ERP"]</tspan>,'),
        (f'  <tspan fill="{MUT}">building:</tspan> <tspan fill="{AMB}">"FoodlyOS"</tspan>,'),
        (f'  <tspan fill="{MUT}">coffee:</tspan> <tspan fill="{O}">true</tspan>'),
        (f'<tspan fill="{MUT}">}};</tspan>'),
    ]
    for i, c in enumerate(code):
        parts.append(f'<text class="m ln" xml:space="preserve" x="580" y="{116+i*26}" font-size="14" style="animation-delay:{0.5+i*0.45:.2f}s">{c}</text>')
    parts.append(f'<rect x="580" y="{116+7*26-14}" width="9" height="16" fill="{O}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>')
    # floating badges
    for lab, x, y, dl in [("R", 520, 90, 0), ("A", 972, 120, 1), ("N", 530, 320, 2), ("M", 968, 320, 3)]:
        parts.append(f'<g class="fl" style="animation-delay:-{dl}s;animation-duration:{4+dl*0.7:.1f}s"><circle cx="{x}" cy="{y}" r="21" fill="{PANEL}" stroke="{O}" stroke-opacity=".6"/><text class="m" x="{x}" y="{y+5}" font-size="15" font-weight="700" fill="{O}" text-anchor="middle">{lab}</text></g>')
    # bottom scanner
    parts.append(f'<rect x="-240" y="{h-3}" width="240" height="3" fill="url(#sw)"><animate attributeName="x" values="-240;1000" dur="4s" repeatCount="indefinite"/></rect></g>')
    parts.append(f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="{LINE}"/>')
    save("hero.svg", svg(w, h, "\n".join(parts), defs, style))


# =====================================================================
# SECTION HEADERS
# =====================================================================
def section(key, title, comment):
    w, h = 1000, 56
    tx = 44
    cx = tx + int(len(title) * 12.8) + 16
    defs = SWEEP + f'<clipPath id="c"><rect width="{w}" height="{h}" rx="12"/></clipPath>'
    body = f'''<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{PANEL}" stroke="{LINE}"/>
<g clip-path="url(#c)"><rect x="-220" y="{h-3}" width="220" height="3" fill="url(#sw)"><animate attributeName="x" values="-220;1000" dur="3.4s" repeatCount="indefinite"/></rect></g>
<rect x="18" y="14" width="5" height="28" rx="2.5" fill="{O}"><animate attributeName="height" values="28;12;28" dur="2.4s" repeatCount="indefinite"/><animate attributeName="y" values="14;22;14" dur="2.4s" repeatCount="indefinite"/></rect>
<text x="{tx}" y="36" font-size="22" font-weight="700" fill="{TXT}">{esc(title)}</text>
<text class="m" x="{cx}" y="35" font-size="14" fill="{MUT}">{esc(comment)}</text>
<circle cx="930" cy="28" r="3.5" fill="{O}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>
<circle cx="946" cy="28" r="3.5" fill="{O}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" begin=".3s" repeatCount="indefinite"/></circle>
<circle cx="962" cy="28" r="3.5" fill="{O}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" begin=".6s" repeatCount="indefinite"/></circle>'''
    save(f"section-{key}.svg", svg(w, h, body, defs))


# =====================================================================
# DIVIDER (heartbeat line)
# =====================================================================
def divider():
    w, h = 1000, 44
    path = "M0 22 H250 l10 0 l8 -14 l12 30 l10 -36 l10 20 l6 0 H560 l10 0 l8 -14 l12 30 l10 -36 l10 20 l6 0 H1000"
    defs = ""
    body = f'''<path d="{path}" fill="none" stroke="{LINE}" stroke-width="2"/>
<path d="{path}" fill="none" stroke="{O}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="160 1700" pathLength="1860"><animate attributeName="stroke-dashoffset" values="160;-1700" dur="4s" repeatCount="indefinite"/></path>'''
    save("divider.svg", svg(w, h, body, defs))


# =====================================================================
# ABOUT cards
# =====================================================================
def about():
    w, h = 1000, 250
    cards = [
        ("Frontend", "</>", ["React.js & Angular", "Figma to responsive UI", "Forms, state & validation", "Loading & error states"]),
        ("Backend", "{ }", ["Node.js & Express", "REST APIs", "JWT authentication", "Role-based access"]),
        ("Business systems", "ERP", ["Admin panels & dashboards", "POS, KDS & Kiosk", "Self-Checkout screens", "Receipt & invoice printing"]),
        ("Mobile & AI", "AI", ["Flutter features & fixes", "Android device testing", "AI-assisted development", "Build & debug faster"]),
    ]
    style = f'''
.card{{opacity:0;animation:up .8s ease forwards}}
@keyframes up{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:ring 2.6s ease-out infinite}}
@keyframes ring{{0%{{transform:scale(.7);opacity:.8}}100%{{transform:scale(1.7);opacity:0}}}}
'''
    defs = SWEEP
    parts = []
    for i, (t, g, items) in enumerate(cards):
        x = i * 256
        parts.append(f'<g class="card" style="animation-delay:{i*0.15:.2f}s"><clipPath id="cc{i}"><rect x="{x}" y="8" width="232" height="234" rx="14"/></clipPath>'
                     f'<rect x="{x+.5}" y="8.5" width="231" height="233" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
                     f'<g clip-path="url(#cc{i})"><rect x="{x-160}" y="8" width="160" height="3" fill="url(#sw)"><animate attributeName="x" values="{x-160};{x+232}" dur="3.6s" begin="{i*0.5}s" repeatCount="indefinite"/></rect></g>'
                     f'<circle class="ring" cx="{x+38}" cy="56" r="20" fill="none" stroke="{O}" style="animation-delay:{i*0.4}s"/>'
                     f'<circle cx="{x+38}" cy="56" r="20" fill="{BG}" stroke="{O}"/>'
                     f'<text class="m" x="{x+38}" y="61" font-size="14" font-weight="700" fill="{O}" text-anchor="middle">{esc(g)}</text>'
                     f'<text x="{x+70}" y="62" font-size="18" font-weight="700" fill="{TXT}">{esc(t)}</text>')
        for j, it in enumerate(items):
            y = 108 + j * 30
            parts.append(f'<circle cx="{x+24}" cy="{y-4}" r="3" fill="{O}"><animate attributeName="opacity" values=".3;1;.3" dur="3s" begin="{(i+j)*.25:.2f}s" repeatCount="indefinite"/></circle>'
                         f'<text x="{x+38}" y="{y}" font-size="14" fill="{MUT}">{esc(it)}</text>')
        parts.append('</g>')
    save("about.svg", svg(w, h, "\n".join(parts), defs, style, bg=True))


# =====================================================================
# PIPELINE
# =====================================================================
def sequence(name, w, h, nodes, y=96, dur=6, label_y=(142, 164), nowlast=False):
    """Generic animated horizontal sequence (pipeline / journey)."""
    n = len(nodes)
    xs = [round(80 + i * (w - 160) / (n - 1)) for i in range(n)]
    parts = [f'<path d="M{xs[0]} {y} H{xs[-1]}" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>',
             f'<path d="M{xs[0]} {y} H{xs[-1]}" stroke="{O}" stroke-width="3" stroke-linecap="round" stroke-dasharray="{xs[-1]-xs[0]}" stroke-dashoffset="{xs[-1]-xs[0]}">'
             f'<animate attributeName="stroke-dashoffset" values="{xs[-1]-xs[0]};0;0;{xs[-1]-xs[0]}" keyTimes="0;.85;.96;1" dur="{dur}s" repeatCount="indefinite"/></path>']
    for i, (a, b, c) in enumerate(nodes):
        x = xs[i]
        t = max(i / n * .85, 0.001)
        parts.append(f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="{O}"><animate attributeName="r" values="22;22;38;38" keyTimes="0;{t:.3f};{min(t+.12,.98):.3f};1" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0;.7;0;0" keyTimes="0;{t:.3f};{min(t+.02,.97):.3f};{min(t+.12,.98):.3f};1" dur="{dur}s" repeatCount="indefinite"/></circle>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{PANEL}" stroke="{O}" stroke-width="2"><animate attributeName="fill" calcMode="discrete" values="{PANEL};{O};{PANEL};{PANEL}" keyTimes="0;{t:.3f};.96;1" dur="{dur}s" repeatCount="indefinite"/></circle>')
        parts.append(f'<text class="m" x="{x}" y="{y+5}" font-size="14" font-weight="700" text-anchor="middle" fill="{O}"><animate attributeName="fill" calcMode="discrete" values="{O};{BG};{O};{O}" keyTimes="0;{t:.3f};.96;1" dur="{dur}s" repeatCount="indefinite"/>{i+1}</text>')
        parts.append(f'<text class="m" x="{x}" y="{y-38}" font-size="12" fill="{O}" text-anchor="middle">{esc(a)}</text>' if nowlast else '')
        parts.append(f'<text x="{x}" y="{label_y[0]+ (0)}" font-size="17" font-weight="700" fill="{TXT}" text-anchor="middle">{esc(b)}</text>'
                     f'<text x="{x}" y="{label_y[1]}" font-size="13" fill="{MUT}" text-anchor="middle">{esc(c)}</text>')
    parts.append(f'<circle r="6" fill="#fff"><animateMotion path="M{xs[0]} {y} H{xs[-1]}" dur="{dur}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.85;1" calcMode="linear"/></circle>')
    return "\n".join(parts)


def pipeline():
    w, h = 1000, 200
    nodes = [("", "Design", "Figma & UI review"), ("", "Plan", "Scope & components"), ("", "Build UI", "Responsive screens"),
             ("", "Integrate", "REST APIs & states"), ("", "Test", "QA & device checks"), ("", "Deliver", "Ship & iterate")]
    save("pipeline.svg", svg(w, h, sequence("p", w, h, nodes, y=70, label_y=(130, 152)), bg=True))


def journey():
    w, h = 1000, 210
    nodes = [("2023 – 2024", "Frontend course", "Web & mobile frontend"),
             ("2025", "Flutter course", "Flutter development"),
             ("Dec 2025", "Airtech Solutions", "Joined as Frontend Developer"),
             ("Now", "FoodlyOS", "Growing as a MERN developer")]
    save("journey.svg", svg(w, h, sequence("j", w, h, nodes, y=84, label_y=(142, 164), nowlast=True, dur=7), bg=True))


# =====================================================================
# FOODLYOS ARCHITECTURE
# =====================================================================
def architecture():
    w, h = 1000, 340
    style = f'''.flow{{stroke-dasharray:6 8;animation:flow 1.2s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-14}}}}
.glow{{animation:gl 2.4s ease-in-out infinite}}
@keyframes gl{{0%,100%{{stroke-opacity:.35}}50%{{stroke-opacity:1}}}}'''
    clients = [("Super Admin", "Platform control", 30), ("Restaurant Admin", "Menu & incoming orders", 135), ("Customer Website", "Browse, order & delivery", 240)]
    parts = []
    for i, (t, s, y) in enumerate(clients):
        cy = y + 35
        p = f"M250 {cy} C 325 {cy}, 325 170, 400 170"
        parts.append(f'<path d="{p}" fill="none" stroke="{LINE}" stroke-width="2"/><path class="flow" d="{p}" fill="none" stroke="{O}" stroke-opacity=".5" stroke-width="2"/>')
        parts.append(f'<rect x="20.5" y="{y+.5}" width="229" height="69" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
                     f'<rect x="38" y="{y+22}" width="26" height="26" rx="7" fill="none" stroke="{O}" stroke-width="2"><animate attributeName="stroke-opacity" values="1;.3;1" dur="2.4s" begin="{i*.5}s" repeatCount="indefinite"/></rect>'
                     f'<text x="78" y="{y+31}" font-size="16" font-weight="700" fill="{TXT}">{esc(t)}</text><text x="78" y="{y+52}" font-size="13" fill="{MUT}">{esc(s)}</text>')
        for k in range(2):
            parts.append(f'<circle r="5" fill="{O}"><animateMotion path="{p}" dur="2.6s" begin="{i*.45 + k*1.3:.2f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="2.6s" begin="{i*.45 + k*1.3:.2f}s" repeatCount="indefinite"/></circle>')
        parts.append(f'<circle r="3.5" fill="#fff" opacity=".8"><animateMotion path="{p}" keyPoints="1;0" keyTimes="0;1" calcMode="linear" dur="2.6s" begin="{i*.45+.9:.2f}s" repeatCount="indefinite"/></circle>')
    dbp = "M640 170 H800"
    parts.append(f'<path d="{dbp}" stroke="{LINE}" stroke-width="2"/><path class="flow" d="{dbp}" stroke="{O}" stroke-opacity=".5" stroke-width="2"/>')
    for k in range(3):
        parts.append(f'<circle r="5" fill="{O}"><animateMotion path="{dbp}" dur="1.6s" begin="{k*.53:.2f}s" repeatCount="indefinite"/></circle>')
        parts.append(f'<circle r="3.5" fill="#fff" opacity=".8"><animateMotion path="{dbp}" keyPoints="1;0" keyTimes="0;1" calcMode="linear" dur="1.6s" begin="{k*.53+.26:.2f}s" repeatCount="indefinite"/></circle>')
    # API box
    parts.append(f'<rect x="400" y="80" width="240" height="180" rx="16" fill="{PANEL}" stroke="{O}" stroke-width="2" class="glow"/>'
                 f'<text x="520" y="118" font-size="18" font-weight="700" fill="{TXT}" text-anchor="middle">Node.js + Express</text>'
                 f'<text class="m" x="520" y="140" font-size="13" fill="{O}" text-anchor="middle">REST API</text>')
    for j, (c, cxp) in enumerate([("JWT auth", 440), ("Role-based access", 575)]):
        pass
    parts.append(f'<g><rect x="420" y="160" width="90" height="28" rx="14" fill="none" stroke="{O}" stroke-opacity=".7"/><text class="m" x="465" y="179" font-size="12" fill="{TXT}" text-anchor="middle">JWT auth</text>'
                 f'<rect x="522" y="160" width="100" height="28" rx="14" fill="none" stroke="{O}" stroke-opacity=".7"/><text class="m" x="572" y="179" font-size="12" fill="{TXT}" text-anchor="middle">role guard</text>'
                 f'<rect x="420" y="200" width="202" height="28" rx="14" fill="none" stroke="{LINE}"/><text class="m" x="521" y="219" font-size="12" fill="{MUT}" text-anchor="middle">Mongoose models</text></g>')
    # DB cylinder
    parts.append(f'<path d="M800 120 V220 A80 22 0 0 0 960 220 V120" fill="{PANEL}" stroke="{O}" stroke-width="2"/><ellipse cx="880" cy="120" rx="80" ry="22" fill="{BG}" stroke="{O}" stroke-width="2"/>'
                 f'<path d="M800 160 A80 22 0 0 0 960 160" fill="none" stroke="{LINE}"/><path d="M800 190 A80 22 0 0 0 960 190" fill="none" stroke="{LINE}"/>'
                 f'<ellipse cx="880" cy="120" rx="80" ry="22" fill="none" stroke="{O}" stroke-width="2"><animate attributeName="ry" values="22;26;22" dur="2.4s" repeatCount="indefinite"/></ellipse>'
                 f'<text x="880" y="285" font-size="18" font-weight="700" fill="{TXT}" text-anchor="middle">MongoDB</text><text class="m" x="880" y="306" font-size="12" fill="{MUT}" text-anchor="middle">orders · menus · users</text>')
    save("foodlyos-architecture.svg", svg(w, h, "\n".join(parts), "", style, bg=True))


# =====================================================================
# STACK (marquee)
# =====================================================================
def stack():
    w = 1000
    rows = [
        ("Frontend & Mobile", "UI that ships", ["React.js", "Angular", "JavaScript", "HTML5", "CSS3", "Responsive Design", "Flutter", "Figma"]),
        ("Backend & Data", "APIs and storage", ["Node.js", "Express.js", "REST APIs", "JWT", "MongoDB", "Mongoose", "Git", "GitHub"]),
        ("Business systems", "real-world work", ["ERP panels", "POS", "KDS", "Kiosk", "Self-Checkout", "Receipt printing", "Dashboards", "AI-assisted dev"]),
    ]
    h = 40 + len(rows) * 86
    defs = f'<clipPath id="cp"><rect x="0" y="-2" width="770" height="44"/></clipPath>' \
           f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>' \
           f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
    parts = [f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{BG}" stroke="{LINE}"/>']
    style = ""
    for ri, (lab, sub, items) in enumerate(rows):
        y = 40 + ri * 86
        chips, x, k = [], 0, 0
        while x < 820:
            t = items[k % len(items)]
            cw = int(len(t) * 8.6 + 46)
            chips.append(f'<g transform="translate({x},0)"><rect width="{cw}" height="40" rx="20" fill="{PANEL}" stroke="{LINE}"/><circle cx="20" cy="20" r="4" fill="{O}"/><text class="m" x="34" y="25" font-size="14" fill="{TXT}">{esc(t)}</text></g>')
            x += cw + 14
            k += 1
        total = x
        s1 = "".join(chips)
        style += f"@keyframes mq{ri}{{to{{transform:translateX(-{total}px)}}}}\n"
        d = "reverse" if ri % 2 else "normal"
        parts.append(f'<text x="28" y="{y+18}" font-size="17" font-weight="700" fill="{TXT}">{esc(lab)}</text><text class="m" x="28" y="{y+38}" font-size="12" fill="{MUT}">{esc(sub)}</text>')
        parts.append(f'<g transform="translate(205,{y})"><g clip-path="url(#cp)"><g style="animation:mq{ri} {total/38:.1f}s linear infinite {d}">{s1}<g transform="translate({total},0)">{s1}</g></g></g></g>')
    parts.append(f'<rect x="205" y="30" width="70" height="{h-60}" fill="url(#fl)"/><rect x="905" y="30" width="70" height="{h-60}" fill="url(#fr)"/>')
    parts.append(f'<rect x="-200" y="{h-3}" width="200" height="3" fill="url(#sw)"><animate attributeName="x" values="-200;1000" dur="4s" repeatCount="indefinite"/></rect>')
    save("stack.svg", svg(w, h, "\n".join(parts), defs + SWEEP, style))


# =====================================================================
# TERMINAL (whoami)
# =====================================================================
def terminal():
    w, h = 1000, 330
    cw = 9.0
    P = "soban@karachi:~$ "
    lines = [
        ("cmd", "whoami", ""),
        ("out", "Soban Ahmed — Frontend Developer @ Airtech Solutions", ""),
        ("cmd", "cat stack.txt", ""),
        ("out", "React · Angular · Node.js · Express · MongoDB · Flutter", ""),
        ("cmd", "git log --oneline -3", ""),
        ("log", "a1f9c2e feat(foodlyos): JWT auth + role-based access", ""),
        ("log", "7be40d1 feat(pos): billing flow + receipt printing", ""),
        ("log", "c03d8aa feat(kds): kitchen order screen", ""),
    ]
    t = 0.6
    sched = []
    for kind, txt, _ in lines:
        full = (P + txt) if kind == "cmd" else txt
        dur = max(len(full) * 0.05, .5) if kind == "cmd" else 0.5
        sched.append((t, dur, full))
        t += dur + (0.45 if kind == "cmd" else 0.12)
    final_start = t
    T = t + 5
    parts = [f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{BG}" stroke="{LINE}"/>',
             f'<path d="M.5 36 V14.5 A14 14 0 0 1 14.5 .5 H985.5 A14 14 0 0 1 999.5 14.5 V36 Z" fill="#171A20"/>',
             f'<circle cx="24" cy="18" r="6" fill="#FF5F57"/><circle cx="44" cy="18" r="6" fill="#FEBC2E"/><circle cx="64" cy="18" r="6" fill="{O}"/>',
             f'<text class="m" x="500" y="23" font-size="13" fill="{MUT}" text-anchor="middle">soban — zsh — 100×30</text>']
    defs = ""
    for i, ((kind, txt, _), (s, d, full)) in enumerate(zip(lines, sched)):
        y = 76 + i * 28
        W = len(full) * cw + 12
        a, b = s / T, (s + d) / T
        defs += f'<clipPath id="t{i}"><rect x="28" y="{y-18}" height="26" width="0"><animate attributeName="width" values="0;0;{W:.0f};{W:.0f};0" keyTimes="0;{a:.4f};{b:.4f};.97;1" dur="{T:.1f}s" repeatCount="indefinite"/></rect></clipPath>'
        if kind == "cmd":
            inner = f'<tspan fill="{O}">soban@karachi</tspan><tspan fill="{MUT}">:~$</tspan> <tspan fill="{TXT}">{esc(txt)}</tspan>'
        elif kind == "log":
            hsh, rest = txt.split(" ", 1)
            inner = f'<tspan fill="{O}">{hsh}</tspan> <tspan fill="{MUT}">{esc(rest)}</tspan>'
        else:
            inner = f'<tspan fill="{AMB}">{esc(txt)}</tspan>'
        parts.append(f'<g clip-path="url(#t{i})"><text class="m" xml:space="preserve" x="28" y="{y}" font-size="15">{inner}</text></g>')
        if kind == "cmd":
            x0 = 28
            parts.append(f'<rect y="{y-14}" width="9" height="18" fill="{O}" x="{x0}"><animate attributeName="x" values="{x0};{x0};{x0+W-12:.0f};{x0+W-12:.0f};{x0}" keyTimes="0;{a:.4f};{b:.4f};.97;1" dur="{T:.1f}s" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" calcMode="discrete" values="0;1;0;0" keyTimes="0;{a:.4f};{b:.4f};1" dur="{T:.1f}s" repeatCount="indefinite"/></rect>')
    y = 76 + len(lines) * 28
    fa = final_start / T
    parts.append(f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0;0" keyTimes="0;{fa:.4f};.97;1" dur="{T:.1f}s" repeatCount="indefinite"/>'
                 f'<text class="m" xml:space="preserve" x="28" y="{y}" font-size="15"><tspan fill="{O}">soban@karachi</tspan><tspan fill="{MUT}">:~$</tspan> </text>'
                 f'<rect x="{28+len(P)*cw-6:.0f}" y="{y-14}" width="9" height="18" fill="{O}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect></g>')
    save("terminal.svg", svg(w, h, "\n".join(parts), defs))


# =====================================================================
# SKILLS
# =====================================================================
def skills():
    w, h = 1000, 330
    defs = f'<linearGradient id="bar" x1="0" x2="1"><stop offset="0" stop-color="{O}"/><stop offset="1" stop-color="{AMB}"/></linearGradient>' \
           f'<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
    parts = [f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{BG}" stroke="{LINE}"/>',
             f'<text x="32" y="46" font-size="20" font-weight="700" fill="{TXT}">Core skills</text>',
             f'<text class="m" x="150" y="45" font-size="13" fill="{MUT}">// self-rated, always learning</text>']
    TW = 250
    for i, (name, lvl) in enumerate(SKILLS):
        col, row = i % 2, i // 2
        x = 32 + col * 490
        y = 96 + row * 56
        L = TW * lvl / 100
        d0 = .05 + i * .03
        parts.append(f'<text x="{x}" y="{y+5}" font-size="15" font-weight="600" fill="{TXT}">{esc(name)}</text>'
                     f'<rect x="{x+170}" y="{y-6}" width="{TW}" height="12" rx="6" fill="{PANEL}" stroke="{LINE}"/>'
                     f'<clipPath id="k{i}"><rect x="{x+170}" y="{y-6}" height="12" width="0"><animate attributeName="width" values="0;0;{L};{L};0" keyTimes="0;{d0:.2f};{d0+.14:.2f};.93;1" dur="10s" repeatCount="indefinite"/></rect></clipPath>'
                     f'<g clip-path="url(#k{i})"><rect x="{x+170}" y="{y-6}" width="{L}" height="12" rx="6" fill="url(#bar)"/>'
                     f'<rect x="{x+170-80}" y="{y-6}" width="80" height="12" fill="url(#sh)"><animate attributeName="x" values="{x+90};{x+170+L}" dur="2.2s" begin="{i*.2}s" repeatCount="indefinite"/></rect></g>'
                     f'<circle cy="{y}" r="5" fill="#fff"><animate attributeName="cx" values="{x+170};{x+170};{x+170+L};{x+170+L};{x+170}" keyTimes="0;{d0:.2f};{d0+.14:.2f};.93;1" dur="10s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;1;1;1;0" keyTimes="0;{d0:.2f};{d0+.14:.2f};.93;1" dur="10s" repeatCount="indefinite"/></circle>')
    save("skills.svg", svg(w, h, "\n".join(parts), defs))


# =====================================================================
# POS DEMO  (KDS board + receipt printer)
# =====================================================================
def pos_demo():
    w, h = 1000, 410
    T = 12
    cols = [("New", 28), ("Cooking", 228), ("Ready", 428)]
    parts = [f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{BG}" stroke="{LINE}"/>',
             f'<rect x="12.5" y="12.5" width="625" height="385" rx="14" fill="{PANEL}" stroke="{LINE}"/>',
             f'<text x="30" y="44" font-size="18" font-weight="700" fill="{TXT}">Kitchen display</text>',
             f'<text class="m" x="190" y="43" font-size="12" fill="{MUT}">// order flow: New → Cooking → Ready</text>',
             f'<circle cx="590" cy="38" r="5" fill="{O}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle><text class="m" x="602" y="42" font-size="11" fill="{O}">live</text>']
    for name, x in cols:
        parts.append(f'<rect x="{x+4}" y="66" width="190" height="318" rx="12" fill="{BG}" stroke="{LINE}"/><text class="m" x="{x+20}" y="92" font-size="13" fill="{MUT}">{name}</text>')
    tickets = [("#101", "2× Burger", "1× Fries"), ("#102", "1× Wrap", "2× Drink"), ("#103", "3× Fries", "1× Nuggets")]
    for i, (num, l1, l2) in enumerate(tickets):
        begin = f"-{i*T/3:.1f}s"
        parts.append(f'''<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;200 0;200 0;400 0;400 0;0 0" keyTimes="0;.30;.35;.62;.67;.99;1" dur="{T}s" begin="{begin}" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;1;1;1;0;0" keyTimes="0;.05;.30;.93;.98;1" dur="{T}s" begin="{begin}" repeatCount="indefinite"/>
<rect x="38" y="108" width="162" height="92" rx="10" fill="{PANEL}" stroke="{LINE}"/>
<rect x="38" y="108" width="6" height="92" rx="3" fill="{MUT}"><animate attributeName="fill" calcMode="discrete" values="{MUT};{O};{AMB};{MUT}" keyTimes="0;.35;.67;.99" dur="{T}s" begin="{begin}" repeatCount="indefinite"/></rect>
<text class="m" x="58" y="134" font-size="16" font-weight="700" fill="{TXT}">{num}</text>
<text class="m" x="58" y="160" font-size="13" fill="{MUT}">{l1}</text><text class="m" x="58" y="180" font-size="13" fill="{MUT}">{l2}</text>
<text class="m" x="186" y="134" font-size="11" fill="{O}" text-anchor="end">dine-in</text></g>''')
    # printer
    px = 700
    defs = f'<clipPath id="slot"><rect x="{px}" y="106" width="250" height="300"/></clipPath>'
    parts.append(f'<text x="{px}" y="40" font-size="18" font-weight="700" fill="{TXT}">Receipt printing</text>')
    # paper
    paper_x, paper_w, top, bot = px + 25, 200, 106, 366
    zig = "".join(f"l-10 10 l-10 -10 " for _ in range(paper_w // 20))
    paper = f'<path d="M{paper_x} {top} H{paper_x+paper_w} V{bot} {zig}Z" fill="#EDEDEF"/>'
    cx = paper_x + paper_w / 2
    rows = [("1,300", "2x Burger", 176), ("350", "1x Fries", 198), ("300", "2x Drink", 220)]
    content = f'<text class="m" x="{cx}" y="140" font-size="16" font-weight="800" fill="{BG}" text-anchor="middle">FOODLYOS</text>' \
              f'<text class="m" x="{cx}" y="158" font-size="11" fill="#555" text-anchor="middle">Order #102 · Dine-in</text>' \
              f'<path d="M{paper_x+14} 168 H{paper_x+paper_w-14}" stroke="#999" stroke-dasharray="4 4"/>'
    for pr, nm, yy in rows:
        content += f'<text class="m" x="{paper_x+16}" y="{yy+6}" font-size="12" fill="{BG}">{nm}</text><text class="m" x="{paper_x+paper_w-16}" y="{yy+6}" font-size="12" fill="{BG}" text-anchor="end">{pr}</text>'
    content += f'<path d="M{paper_x+14} 238 H{paper_x+paper_w-14}" stroke="#999" stroke-dasharray="4 4"/>' \
               f'<text class="m" x="{paper_x+16}" y="262" font-size="14" font-weight="800" fill="{BG}">TOTAL Rs</text><text class="m" x="{paper_x+paper_w-16}" y="262" font-size="14" font-weight="800" fill="{BG}" text-anchor="end">1,950</text>'
    bars = "".join(f'<rect x="{paper_x+30+k*4.6:.1f}" y="284" width="{1.4+(k%3)}" height="34" fill="{BG}"/>' for k in range(32))
    content += bars + f'<text class="m" x="{cx}" y="342" font-size="11" fill="#555" text-anchor="middle">Thank you!</text>'
    parts.append(f'<g clip-path="url(#slot)"><g><animateTransform attributeName="transform" type="translate" values="0 -270;0 0;0 0;0 -270" keyTimes="0;.38;.9;1" dur="{T}s" repeatCount="indefinite"/>{paper}{content}</g></g>')
    parts.append(f'<rect x="{px+.5}" y="56.5" width="249" height="52" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
                 f'<rect x="{px+18}" y="98" width="214" height="5" rx="2.5" fill="{BG}" stroke="{O}" stroke-opacity=".8"><animate attributeName="stroke-opacity" values=".3;1;.3" dur="1.2s" repeatCount="indefinite"/></rect>'
                 f'<circle cx="{px+26}" cy="76" r="4" fill="{O}"><animate attributeName="opacity" values="1;.2;1" dur=".9s" repeatCount="indefinite"/></circle>'
                 f'<text class="m" x="{px+40}" y="80" font-size="12" fill="{MUT}">printing…</text>')
    parts.append(f'<text class="m" x="{px+125}" y="396" font-size="11" fill="{MUT}" text-anchor="middle">// printer integration</text>')
    save("pos-demo.svg", svg(w, h, "\n".join(parts), defs))


# =====================================================================
# CONTACT + FOOTER
# =====================================================================
def contact():
    w, h = 1000, 250
    defs = f'<linearGradient id="nm" x1="0" x2="1.2" spreadMethod="reflect"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="{O}"/><stop offset="1" stop-color="{AMB}"/><animate attributeName="x1" values="0;1.2" dur="5s" repeatCount="indefinite"/><animate attributeName="x2" values="1.2;2.4" dur="5s" repeatCount="indefinite"/></linearGradient>'
    style = f'''.fl{{animation:fl 3.2s ease-in-out infinite}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:ring 2.6s ease-out infinite}}
@keyframes ring{{0%{{transform:scale(.6);opacity:.8}}100%{{transform:scale(1.8);opacity:0}}}}
.dash{{stroke-dasharray:14 10;animation:dash 1.6s linear infinite}}
@keyframes dash{{to{{stroke-dashoffset:-24}}}}'''
    body = f'''<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{BG}"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="none" stroke="{O}" stroke-opacity=".7" class="dash"/>
<ellipse cx="170" cy="125" rx="200" ry="150" fill="{O}" opacity=".09"><animate attributeName="opacity" values=".05;.14;.05" dur="4s" repeatCount="indefinite"/></ellipse>
<circle class="ring" cx="150" cy="118" r="52" fill="none" stroke="{O}"/><circle class="ring" cx="150" cy="118" r="52" fill="none" stroke="{O}" style="animation-delay:1.3s"/>
<g class="fl"><rect x="106" y="90" width="88" height="62" rx="10" fill="{PANEL}" stroke="{O}" stroke-width="2.5"/><path d="M106 98 L150 128 L194 98" fill="none" stroke="{O}" stroke-width="2.5" stroke-linejoin="round"/></g>
<text x="270" y="108" font-size="44" font-weight="800" fill="url(#nm)">Let's build something great.</text>
<text class="m" x="270" y="150" font-size="20" fill="{TXT}">{EMAIL}</text>
<text class="m" x="270" y="184" font-size="14" fill="{MUT}">// web apps · admin panels · POS / KDS · MERN products</text>
<circle cx="276" cy="216" r="5" fill="{O}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>
<text x="292" y="221" font-size="15" font-weight="600" fill="{O}">Open to opportunities</text>'''
    save("contact.svg", svg(w, h, body, defs, style))


def footer():
    w, h = 1000, 130
    import math

    def wave(amp, phase, y0):
        pts = []
        for x in range(0, 2001, 20):
            pts.append(f"{x},{y0 + amp * math.sin((x / 250) * 2 * math.pi + phase):.1f}")
        return "M" + " L".join(pts) + f" V{h} H0 Z"
    body = f'''<clipPath id="c"><rect width="{w}" height="{h}" rx="14"/></clipPath>
<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="{BG}"/>
<path d="{wave(8,0,84)}" fill="{O}" fill-opacity=".10"><animateTransform attributeName="transform" type="translate" from="0 0" to="-1000 0" dur="14s" repeatCount="indefinite"/></path>
<path d="{wave(10,1.6,92)}" fill="{O}" fill-opacity=".16"><animateTransform attributeName="transform" type="translate" from="-1000 0" to="0 0" dur="10s" repeatCount="indefinite"/></path>
<path d="{wave(6,3.2,102)}" fill="{O}" fill-opacity=".28"><animateTransform attributeName="transform" type="translate" from="0 0" to="-1000 0" dur="7s" repeatCount="indefinite"/></path>
<text x="500" y="48" font-size="20" font-weight="700" fill="{TXT}" text-anchor="middle">Thanks for stopping by</text>
<text class="m" x="500" y="72" font-size="13" fill="{MUT}" text-anchor="middle">© 2026 Soban Ahmed · built with React, Node and a lot of coffee</text></g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/>'''
    save("footer.svg", svg(w, h, body))


# =====================================================================
# README
# =====================================================================
def readme():
    lines = ["Frontend Developer @ Airtech Solutions", "MERN Stack · React · Angular · Node.js · MongoDB",
             "Building FoodlyOS — multi-role food delivery", "POS · KDS · Kiosk · ERP · Receipt printing",
             "From Figma designs to production-ready UIs"]
    typing = "https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=17&duration=3200&pause=1100&color=FF7A1A&center=true&vCenter=true&width=820&lines=" + ";".join(quote_plus(l) for l in lines)
    S = "./assets/"
    def img(alt, f):
        return f"[![{alt}]({S}{f})]({S}{f})"
    md = f'''<a name="top"></a>
<div align="center">

{img("Soban Ahmed — MERN Stack Developer and Frontend Developer", "hero.svg")}

[![Typing animation]({typing})](https://github.com/{USER})

[![Email](https://img.shields.io/badge/EMAIL-sobanahmed9898%40gmail.com-FF7A1A?style=for-the-badge&logo=gmail&logoColor=0B0C0F&labelColor=0B0C0F)](mailto:{EMAIL}) [![LinkedIn](https://img.shields.io/badge/LINKEDIN-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LINKEDIN}) [![GitHub](https://img.shields.io/badge/GITHUB-{USER}-FF7A1A?style=for-the-badge&logo=github&logoColor=0B0C0F&labelColor=0B0C0F)](https://github.com/{USER}) [![Portfolio](https://img.shields.io/badge/PORTFOLIO-LIVE-FF7A1A?style=for-the-badge&logo=vercel&logoColor=0B0C0F&labelColor=0B0C0F)]({PORTFOLIO})

[![Open to](https://img.shields.io/badge/OPEN_TO-OPPORTUNITIES-FF7A1A?style=flat-square&logo=rocket&logoColor=0B0C0F&labelColor=0B0C0F)](mailto:{EMAIL}) [![Location](https://img.shields.io/badge/BASED_IN-KARACHI,_PAKISTAN-FF7A1A?style=flat-square&logo=googlemaps&logoColor=0B0C0F&labelColor=0B0C0F)](#contact) [![Work](https://img.shields.io/badge/WORKING_AT-AIRTECH_SOLUTIONS-FF7A1A?style=flat-square&logo=briefcase&logoColor=0B0C0F&labelColor=0B0C0F)](#experience) [![Followers](https://img.shields.io/github/followers/{USER}?style=flat-square&label=followers&color=FF7A1A&labelColor=0B0C0F)](https://github.com/{USER}?tab=followers) [![Profile views](https://komarev.com/ghpvc/?username={USER}&label=profile%20views&style=flat-square&color=FF7A1A&labelColor=0B0C0F)](https://github.com/{USER})

**[About](#about) · [Skills](#skills) · [How I Build](#how-i-build) · [Projects](#projects) · [Experience](#experience) · [Services](#services) · [Stack](#stack) · [Activity](#activity) · [Contact](#contact)**

![divider]({S}divider.svg)

</div>

<a name="about"></a>

{img("About", "section-about.svg")}

I build web products across the whole stack: **React and Angular frontends**, **Node/Express REST APIs with JWT auth**, and **MongoDB** data layers. At work I ship **ERP, POS, KDS, Kiosk and Self-Checkout** interfaces with printer integration, and I use **AI-assisted development** to build and debug faster.

{img("Frontend, Backend, Business Systems and Mobile & AI capabilities", "about.svg")}

{img("Terminal: whoami, stack and recent commits", "terminal.svg")}

| 🔭 Working on | 🌱 Improving | 🎓 Next goal |
|---|---|---|
| FoodlyOS, a full MERN food delivery product | Full-stack skills, clean architecture & reusable components | University studies in Computer Science |

<a name="skills"></a>

{img("Skills", "section-skills.svg")}

{img("Animated skill bars", "skills.svg")}

<a name="how-i-build"></a>

{img("How I Build", "section-workflow.svg")}

One workflow, six stages. Every project goes through the same path.

{img("Pipeline: Design, Plan, Build UI, Integrate, Test, Deliver", "pipeline.svg")}

<a name="projects"></a>

{img("Featured Projects", "section-projects.svg")}

#### 🍔 FoodlyOS &nbsp;`In Development`

**Multi-role food delivery platform** built on the full MERN stack with JWT authentication and role-based access.

{img("FoodlyOS architecture: Super Admin, Restaurant Admin and Customer Website to a Node.js Express REST API, then MongoDB", "foodlyos-architecture.svg")}

| Role | What it does |
|---|---|
| 👑 **Super Admin** | Platform control and restaurant oversight |
| 🏪 **Restaurant Admin** | Menu management and incoming orders |
| 🛒 **Customer Website** | Browse, order and delivery |

`MongoDB` `Express.js` `React.js` `Node.js` `Mongoose` `JWT`

#### More projects

| Project | Description | Stack |
|---|---|---|
| **🚚 FoodCarrier** | Food delivery platform: customer frontend with menu browsing & order flow, reusable components, responsive layouts, REST API integration with error handling, admin interfaces & configurable delivery options | `React.js` `JavaScript` `REST APIs` `Git` |
| **📋 Digital Menu** | Digital menu application with a clean interface and responsive layout across all screen sizes | `React.js` `Responsive Design` |
| **💼 Airtech Solutions** | Real business projects: ERP admin panels & dashboards, Angular POS system (billing & orders), KDS, Kiosk & Self-Checkout screens, printer integration for receipts & invoices | `React` `Angular` `Flutter` |

<div align="center">

[![ChatGPT-Auto-Prompt](https://github-readme-stats.vercel.app/api/pin/?username={USER}&repo=ChatGPT-Auto-Prompt&bg_color=0B0C0F&title_color=FF7A1A&text_color=E8E8EA&icon_color=FF7A1A&border_color=23262D)](https://github.com/{USER}/ChatGPT-Auto-Prompt)

</div>

<a name="experience"></a>

{img("Experience", "section-experience.svg")}

#### 🏢 Frontend Developer — Airtech Solutions

`Dec 2025 – Present` · Karachi, Pakistan

<details open>
<summary><b>What I do day to day</b> (click to collapse)</summary>
<br>

- React.js apps from scratch: planning → components → implementation
- Figma/UI designs → responsive interfaces for desktop, tablet and mobile
- REST API integration with loading & error states
- Forms with controlled inputs & validation (`useState`, `useEffect`)
- ERP admin panels, dashboards & business workflows
- Angular POS system for billing & day-to-day order operations
- KDS, Kiosk & Self-Checkout projects
- Printer integration for receipts, invoices & reports
- Flutter features, bug fixes & Android device/emulator testing
- Git/GitHub collaboration with backend developers, designers & QA

</details>

{img("Journey", "section-journey.svg")}

{img("Journey: 2023-2024 frontend course, 2025 Flutter course, Dec 2025 joined Airtech Solutions, now building FoodlyOS", "journey.svg")}

<a name="services"></a>

{img("What I Build", "section-services.svg")}

{img("Animated demo: kitchen display order flow and receipt printing", "pos-demo.svg")}

| 🌐 Web Apps | 📊 Admin Panels | 🧾 POS / KDS / Kiosk | ⚙️ MERN Products |
|---|---|---|---|
| React.js & Angular applications built from scratch | Dashboards, ERP screens & business workflows | Order, billing, checkout & receipt printing UIs | Full-stack apps with REST APIs, JWT & role-based access |

<div align="center">

[![Let's Work Together](https://img.shields.io/badge/%F0%9F%93%A9%20LET'S%20WORK%20TOGETHER-FF7A1A?style=for-the-badge&labelColor=0B0C0F)](mailto:{EMAIL}?subject=Project%20Inquiry)

</div>

<a name="stack"></a>

{img("Tech Stack", "section-stack.svg")}

{img("Technology stack: frontend, backend, database, mobile, business systems and AI tools", "stack.svg")}

<a name="activity"></a>

{img("GitHub Activity", "section-activity.svg")}

<div align="center">

[![GitHub stats](https://github-readme-stats.vercel.app/api?username={USER}&show_icons=true&hide_border=true&count_private=true&bg_color=0B0C0F&title_color=FF7A1A&icon_color=FF7A1A&text_color=E8E8EA&ring_color=FF7A1A)](https://github.com/{USER}) [![Top languages](https://github-readme-stats.vercel.app/api/top-langs/?username={USER}&layout=compact&hide_border=true&bg_color=0B0C0F&title_color=FF7A1A&text_color=E8E8EA)](https://github.com/{USER})

[![GitHub streak](https://streak-stats.demolab.com?user={USER}&hide_border=true&background=0B0C0F&ring=FF7A1A&fire=FF7A1A&currStreakLabel=FF7A1A&currStreakNum=E8E8EA&sideLabels=E8E8EA&sideNums=E8E8EA&dates=8A8F98&stroke=23262D)](https://github.com/{USER})

[![Contribution activity graph](https://github-readme-activity-graph.vercel.app/graph?username={USER}&bg_color=0B0C0F&color=FF7A1A&line=FF7A1A&point=FFFFFF&area=true&area_color=FF7A1A&hide_border=true)](https://github.com/{USER})

[![Contribution graph snake animation](https://raw.githubusercontent.com/{USER}/{USER}/output/github-snake-dark.svg)](https://github.com/{USER})

</div>

<a name="contact"></a>

{img("Contact", "section-contact.svg")}

[![Let's build something great. {EMAIL}]({S}contact.svg)](mailto:{EMAIL})

<div align="center">

[![Email](https://img.shields.io/badge/EMAIL-sobanahmed9898%40gmail.com-FF7A1A?style=for-the-badge&logo=gmail&logoColor=0B0C0F&labelColor=0B0C0F)](mailto:{EMAIL}) [![LinkedIn](https://img.shields.io/badge/LINKEDIN-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LINKEDIN}) [![GitHub](https://img.shields.io/badge/GITHUB-{USER}-FF7A1A?style=for-the-badge&logo=github&logoColor=0B0C0F&labelColor=0B0C0F)](https://github.com/{USER}) [![Portfolio](https://img.shields.io/badge/PORTFOLIO-LIVE-FF7A1A?style=for-the-badge&logo=vercel&logoColor=0B0C0F&labelColor=0B0C0F)]({PORTFOLIO})

{img("footer", "footer.svg")}

<a href="#top">⬆️ Back to top</a>

</div>
'''
    with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print("wrote README.md")


if __name__ == "__main__":
    hero(); divider(); about(); pipeline(); journey(); architecture(); stack()
    terminal(); skills(); pos_demo(); contact(); footer()
    for k, t, c in [("about", "About", "// who I am"), ("skills", "Skills", "// what I work with"),
                    ("workflow", "How I Build", "// one workflow, six stages"), ("projects", "Featured Projects", "// things I've shipped"),
                    ("experience", "Experience", "// where I work"), ("journey", "Journey", "// how I got here"),
                    ("services", "What I Build", "// POS · KDS · Kiosk · ERP"), ("stack", "Tech Stack", "// tools of the trade"),
                    ("activity", "GitHub Activity", "// commits & streaks"), ("contact", "Contact", "// say hello")]:
        section(k, t, c)
    readme()
