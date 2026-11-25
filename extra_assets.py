"""
Extra animated assets (v2): stats, ticker, orbit, responsive, jwt-flow,
dashboard, kiosk + the v2 README. Imported by build_assets.py.
"""
import os, math
from urllib.parse import quote_plus
import build_assets as B
from build_assets import O, AMB, BG, PANEL, LINE, TXT, MUT, SANS, MONO, SWEEP, esc, svg, save

DEBUG = bool(os.environ.get("DEBUG_STATIC"))
REV = "1" if DEBUG else "0"


def win(a, b, T):
    """(base_opacity, <animate>) element visible only for fractions a..b of the loop."""
    if a <= 0:
        return "1", f'<animate attributeName="opacity" calcMode="discrete" values="1;0;0" keyTimes="0;{b:.4f};1" dur="{T}s" repeatCount="indefinite"/>'
    if b >= 1:
        return REV, f'<animate attributeName="opacity" calcMode="discrete" values="0;1" keyTimes="0;{a:.4f}" dur="{T}s" repeatCount="indefinite"/>'
    return REV, f'<animate attributeName="opacity" calcMode="discrete" values="0;1;0;0" keyTimes="0;{a:.4f};{b:.4f};1" dur="{T}s" repeatCount="indefinite"/>'


def wg(a, b, T, inner, extra=""):
    base, an = win(a, b, T)
    return f'<g opacity="{base}" {extra}>{an}{inner}</g>'


def count_texts(x, y, vals, T, t0, t1, attrs):
    """Count-up effect: stacked texts, exactly one visible at a time."""
    n = len(vals)
    step = (t1 - t0) / max(n - 1, 1)
    cuts = [t0 + i * step for i in range(n - 1)]          # moments the value changes
    out = []
    for i, v in enumerate(vals):
        a = 0 if i == 0 else cuts[i - 1]
        b = 0.95 if i == n - 1 else cuts[i]
        out.append(wg(a, b, T, f'<text x="{x}" y="{y}" {attrs}>{esc(v)}</text>'))
    out.append(wg(0.95, 1.0, T, f'<text x="{x}" y="{y}" {attrs}>{esc(vals[0])}</text>'))
    return "".join(out)


def frame(w, h, r=16):
    return f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="{BG}" stroke="{LINE}"/>'


# =====================================================================
# STATS strip (counters)
# =====================================================================
def stats():
    w, h, T = 1000, 140, 9
    cells = [(3, "user roles", "Admin · Restaurant · Customer"),
             (5, "business systems", "ERP · POS · KDS · Kiosk · Checkout"),
             (3, "frameworks", "React · Angular · Flutter"),
             (6, "stage workflow", "Design to Deliver")]
    defs = SWEEP + "".join(f'<clipPath id="s{i}"><rect x="{i*256}" y="6" width="232" height="128" rx="14"/></clipPath>' for i in range(4))
    style = ".ring{transform-box:fill-box;transform-origin:center;animation:ring 2.8s ease-out infinite}@keyframes ring{0%{transform:scale(.6);opacity:.7}100%{transform:scale(1.8);opacity:0}}"
    parts = []
    for i, (n, lab, sub) in enumerate(cells):
        x = i * 256
        parts.append(f'<rect x="{x+.5}" y="6.5" width="231" height="127" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
                     f'<g clip-path="url(#s{i})"><rect x="{x-160}" y="6" width="160" height="3" fill="url(#sw)"><animate attributeName="x" values="{x-160};{x+232}" dur="3.6s" begin="{i*.6}s" repeatCount="indefinite"/></rect></g>')
        vals = [str(k) for k in range(n + 1)]
        parts.append(count_texts(x + 24, 78, vals, T, 0.05, 0.35, f'font-size="54" font-weight="800" fill="{O}"'))
        parts.append(f'<text x="{x+70}" y="62" font-size="15" font-weight="700" fill="{TXT}">{esc(lab)}</text>')
        parts.append(f'<text x="{x+24}" y="112" font-size="12" fill="{MUT}">{esc(sub)}</text>')
    save("stats.svg", svg(w, h, "\n".join(parts), defs, style))


# =====================================================================
# TICKER
# =====================================================================
def ticker():
    w, h = 1000, 56
    phrases = ["Clean code", "Reusable components", "Responsive by default", "REST + JWT", "Figma to production", "Ship and iterate", "Loading & error states handled"]
    x, k, items = 0, 0, []
    while x < 1300:
        t = phrases[k % len(phrases)]
        tw = len(t) * 9.2
        items.append(f'<text class="m" x="{x}" y="34" font-size="15" fill="{TXT}">{esc(t)}</text><rect x="{x+tw+22:.0f}" y="25" width="8" height="8" fill="{O}" transform="rotate(45 {x+tw+26:.0f} 29)"/>')
        x += tw + 56
        k += 1
    total = x
    s1 = "".join(items)
    defs = (f'<clipPath id="tk"><rect width="{w}" height="{h}" rx="12"/></clipPath>'
            f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{PANEL}"/><stop offset="1" stop-color="{PANEL}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{PANEL}"/><stop offset="1" stop-color="{PANEL}" stop-opacity="0"/></linearGradient>')
    style = f"@keyframes tk{{to{{transform:translateX(-{total}px)}}}}"
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{PANEL}" stroke="{LINE}"/><g clip-path="url(#tk)">'
            f'<g style="animation:tk {total/45:.1f}s linear infinite">{s1}<g transform="translate({total},0)">{s1}</g></g>'
            f'<rect width="90" height="{h}" fill="url(#fl)"/><rect x="{w-90}" width="90" height="{h}" fill="url(#fr)"/></g>')
    save("ticker.svg", svg(w, h, body, defs, style))


# =====================================================================
# ORBIT
# =====================================================================
def orbit():
    w, h = 1000, 460
    cx, cy = 720, 230
    rings = [(82, ["React", "Angular", "JS"], 30, 1, 90), (146, ["Node.js", "Express", "MongoDB", "JWT"], 44, -1, 45),
             (208, ["Flutter", "Git", "Figma", "ERP", "POS", "KDS"], 60, 1, 20)]
    parts = [f'<ellipse cx="{cx}" cy="{cy}" rx="260" ry="210" fill="{O}" opacity=".07"><animate attributeName="opacity" values=".04;.12;.04" dur="5s" repeatCount="indefinite"/></ellipse>']
    for r, _, _, _, _ in rings:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{O}" stroke-opacity=".28" stroke-dasharray="4 8"/>')
    for r, names, dur, s, off in rings:
        n = len(names)
        spin_to = 360 * s
        chips = ""
        for i, nm in enumerate(names):
            a = i * 360 / n + off
            cw = len(nm) * 7.2 + 24
            chips += (f'<g transform="rotate({a:.1f})"><g transform="translate({r},0)"><g>'
                      f'<animateTransform attributeName="transform" type="rotate" from="{-a:.1f}" to="{-a-spin_to:.1f}" dur="{dur}s" repeatCount="indefinite"/>'
                      f'<rect x="{-cw/2:.0f}" y="-14" width="{cw:.0f}" height="28" rx="14" fill="{PANEL}" stroke="{O}" stroke-opacity=".75"/>'
                      f'<text class="m" y="4" font-size="12" fill="{TXT}" text-anchor="middle">{esc(nm)}</text></g></g></g>')
        parts.append(f'<g transform="translate({cx},{cy})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{spin_to}" dur="{dur}s" repeatCount="indefinite"/>{chips}</g></g>')
    parts.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="38" fill="none" stroke="{O}"/><circle cx="{cx}" cy="{cy}" r="38" fill="{BG}" stroke="{O}" stroke-width="2.5"/>'
                 f'<text x="{cx}" y="{cy+7}" font-size="20" font-weight="800" fill="{O}" text-anchor="middle">SA</text>')
    parts.append(f'<text x="40" y="150" font-size="34" font-weight="800" fill="{TXT}">My tech orbit</text>'
                 f'<text class="m" x="40" y="180" font-size="14" fill="{MUT}">// everything I use, in motion</text>')
    for i, (lab, sub) in enumerate([("Inner ring", "front-end core"), ("Middle ring", "backend & data"), ("Outer ring", "tools & business systems")]):
        y = 240 + i * 46
        parts.append(f'<circle cx="52" cy="{y}" r="9" fill="none" stroke="{O}" stroke-dasharray="3 4"><animateTransform attributeName="transform" type="rotate" from="0 52 {y}" to="360 52 {y}" dur="6s" repeatCount="indefinite"/></circle>'
                     f'<text x="76" y="{y-2}" font-size="16" font-weight="700" fill="{TXT}">{esc(lab)}</text><text x="76" y="{y+17}" font-size="13" fill="{MUT}">{esc(sub)}</text>')
    style = ".ring{transform-box:fill-box;transform-origin:center;animation:ring 2.6s ease-out infinite}@keyframes ring{0%{transform:scale(.8);opacity:.8}100%{transform:scale(1.9);opacity:0}}"
    save("orbit.svg", svg(w, h, "\n".join(parts), "", style, bg=True))


# =====================================================================
# RESPONSIVE morph
# =====================================================================
def responsive():
    w, h, T = 1000, 450, 12
    cx, top, FH = 660, 40, 340
    KT = "0;.2;.3;.5;.6;.85;.95;1"
    Ws = [560, 400, 220]

    def A(attr, d, t, m):
        v = [d, d, t, t, m, m, d, d]
        return f'<animate attributeName="{attr}" values="{";".join(f"{x:.1f}" for x in v)}" keyTimes="{KT}" dur="{T}s" repeatCount="indefinite"/>'

    def R(attrs, **fn):
        """rect whose x,y,width,height are functions of state index (0,1,2)."""
        vals = {k: [f(s) for s in range(3)] for k, f in fn.items()}
        base = " ".join(f'{k}="{v[0]:.1f}"' for k, v in vals.items())
        anims = "".join(A(k, *v) for k, v in vals.items())
        return f'<rect {base} {attrs}>{anims}</rect>'

    W = lambda s: Ws[s]
    fx = lambda s: cx - Ws[s] / 2
    parts = [R(f'rx="14" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"', x=fx, y=lambda s: top, width=W, height=lambda s: FH)]
    parts.append(R('rx="9" fill="#191C22"', x=lambda s: fx(s) + 5, y=lambda s: top + 5, width=lambda s: W(s) - 10, height=lambda s: 30))
    parts.append(R(f'rx="6" fill="{O}"', x=lambda s: fx(s) + 18, y=lambda s: top + 14, width=lambda s: 44, height=lambda s: 12))
    for k in range(3):
        parts.append(f'<g opacity="1"><animate attributeName="opacity" calcMode="discrete" values="1;1;0;1" keyTimes="0;.5;.6;.95" dur="{T}s" repeatCount="indefinite"/>' +
                     R(f'rx="4" fill="{MUT}" fill-opacity=".5"', x=lambda s, k=k: fx(s) + W(s) - 18 - 38 - (2 - k) * 46, y=lambda s: top + 17, width=lambda s: 36, height=lambda s: 6) + '</g>')
    ham = "".join(R(f'rx="1" fill="{TXT}"', x=lambda s: fx(s) + W(s) - 38, y=lambda s, k=k: top + 14 + k * 6, width=lambda s: 18, height=lambda s: 2) for k in range(3))
    parts.append(f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0;0" keyTimes="0;.6;.95;1" dur="{T}s" repeatCount="indefinite"/>{ham}</g>')
    parts.append(R(f'rx="10" fill="{BG}" stroke="{O}" stroke-opacity=".55"', x=lambda s: fx(s) + 14, y=lambda s: top + 46, width=lambda s: W(s) - 28, height=lambda s: 72))
    parts.append(R(f'rx="5" fill="{TXT}"', x=lambda s: fx(s) + 28, y=lambda s: top + 62, width=lambda s: (W(s) - 28) * .5, height=lambda s: 10))
    parts.append(R(f'rx="3" fill="{MUT}"', x=lambda s: fx(s) + 28, y=lambda s: top + 82, width=lambda s: (W(s) - 28) * .34, height=lambda s: 6))
    parts.append(R(f'rx="8" fill="{O}"', x=lambda s: fx(s) + 28, y=lambda s: top + 98, width=lambda s: 56, height=lambda s: 10))

    def cardgeom(s, k):
        Wd = Ws[s]
        if s == 0:
            cw = (Wd - 28 - 24) / 3
            return fx(s) + 14 + k * (cw + 12), top + 130, cw, 110
        if s == 1:
            cw = (Wd - 28 - 12) / 2
            return (fx(s) + 14 + k * (cw + 12), top + 130, cw, 90) if k < 2 else (fx(s) + 14, top + 232, Wd - 28, 90)
        return fx(s) + 14, top + 130 + k * 70, Wd - 28, 60

    for k in range(3):
        g = lambda s, k=k: cardgeom(s, k)
        parts.append(R(f'rx="10" fill="{PANEL}" stroke="{LINE}"', x=lambda s, g=g: g(s)[0], y=lambda s, g=g: g(s)[1], width=lambda s, g=g: g(s)[2], height=lambda s, g=g: g(s)[3]))
        parts.append(R(f'rx="4" fill="{O}" fill-opacity="{.9 - k*.2:.1f}"', x=lambda s, g=g: g(s)[0] + 12, y=lambda s, g=g: g(s)[1] + 12, width=lambda s: 16, height=lambda s: 16))
        parts.append(R(f'rx="3" fill="{TXT}" fill-opacity=".8"', x=lambda s, g=g: g(s)[0] + 12, y=lambda s, g=g: g(s)[1] + 38, width=lambda s, g=g: g(s)[2] * .6, height=lambda s: 6))
        parts.append(R(f'rx="3" fill="{MUT}" fill-opacity=".6"', x=lambda s, g=g: g(s)[0] + 12, y=lambda s, g=g: g(s)[1] + 52, width=lambda s, g=g: g(s)[2] * .4, height=lambda s: 6))
    ry = top + FH + 26
    parts.append(f'<g stroke="{O}" stroke-width="2" stroke-linecap="round">' +
                 f'<line y1="{ry}" y2="{ry}" x1="{fx(0)}" x2="{fx(0)+Ws[0]}">{A("x1", fx(0), fx(1), fx(2))}{A("x2", fx(0)+Ws[0], fx(1)+Ws[1], fx(2)+Ws[2])}</line></g>')
    labels = [("Desktop · 1440px", 0, .25), ("Tablet · 768px", .25, .55), ("Mobile · 375px", .55, .9), ("Desktop · 1440px", .9, 1.0)]
    for t, a, b in labels:
        parts.append(wg(a, b, T, f'<text class="m" x="{cx}" y="{ry+24}" font-size="14" fill="{O}" text-anchor="middle">{t}</text>'))
    parts.append(f'<text x="40" y="130" font-size="34" font-weight="800" fill="{TXT}">One design,</text><text x="40" y="170" font-size="34" font-weight="800" fill="{O}">every screen.</text>'
                 f'<text class="m" x="40" y="204" font-size="14" fill="{MUT}">// desktop → tablet → mobile</text>')
    for i, t in enumerate(["Figma designs to responsive interfaces", "Layouts that reflow, not just shrink", "Checked on desktop, tablet and mobile"]):
        y = 258 + i * 36
        parts.append(f'<circle cx="48" cy="{y-5}" r="4" fill="{O}"><animate attributeName="opacity" values=".3;1;.3" dur="3s" begin="{i*.4}s" repeatCount="indefinite"/></circle><text x="64" y="{y}" font-size="15" fill="{TXT}">{esc(t)}</text>')
    save("responsive.svg", svg(w, h, "\n".join(parts), "", "", bg=True))


# =====================================================================
# JWT FLOW (sequence diagram)
# =====================================================================
def jwt_flow():
    w, h, T = 1000, 440, 14
    X = {"c": 140, "a": 500, "d": 860}
    parts = []
    heads = [("c", "Client", "React app"), ("a", "API", "Express + JWT"), ("d", "MongoDB", "Mongoose models")]
    for k, t, s in heads:
        x = X[k]
        parts.append(f'<rect x="{x-90}" y="18.5" width="180" height="52" rx="12" fill="{PANEL}" stroke="{O}" stroke-opacity=".8"/>'
                     f'<text x="{x}" y="42" font-size="16" font-weight="700" fill="{TXT}" text-anchor="middle">{t}</text><text class="m" x="{x}" y="60" font-size="11" fill="{MUT}" text-anchor="middle">{s}</text>'
                     f'<line x1="{x}" y1="74" x2="{x}" y2="424" stroke="{LINE}" stroke-width="2" stroke-dasharray="5 7"/>')
    steps = [("c", "a", "POST /login  { email, password }", False), ("a", "d", "find user by email", False), ("d", "a", "user + role", True),
             ("a", "c", "JWT  (signed token)", True), ("c", "a", "GET /orders  ·  Bearer token", False), ("a", "c", "200 OK  ·  role: restaurant admin", True)]
    for i, (f, t, label, ret) in enumerate(steps):
        y = 124 + i * 54
        a = .04 + i * .14
        b = a + .08
        x1, x2 = X[f], X[t]
        d = 1 if x2 > x1 else -1
        col = AMB if ret else O
        dash = 'stroke-dasharray="7 6"' if ret else ""
        # solid lines use dasharray 100 for draw effect; dashed returns fade in instead
        parts.append((f'<path d="M{x1} {y} H{x2}" stroke="{col}" stroke-width="2.4" fill="none" opacity="{REV}" {dash}>' + win(a, .95, T)[1] + '</path>') if ret else
                    (f'<path d="M{x1} {y} H{x2}" stroke="{col}" stroke-width="2.4" fill="none" stroke-dasharray="{abs(x2-x1)}" stroke-dashoffset="{0 if DEBUG else abs(x2-x1)}">'
                     f'<animate attributeName="stroke-dashoffset" values="{abs(x2-x1)};{abs(x2-x1)};0;0;{abs(x2-x1)}" keyTimes="0;{a:.3f};{b:.3f};.95;1" dur="{T}s" repeatCount="indefinite"/></path>'))
        parts.append(wg(b, .95, T, f'<polygon points="{x2-d*11},{y-6} {x2},{y} {x2-d*11},{y+6}" fill="{col}"/>'))
        parts.append(wg(a + .01, .95, T, f'<text class="m" x="{(x1+x2)/2}" y="{y-10}" font-size="13" fill="{TXT}" text-anchor="middle">{esc(label)}</text>'))
        base, an = win(a, b, T)
        parts.append(f'<circle r="6" fill="#fff" opacity="{base if not DEBUG else 0}">{an}<animateMotion path="M{x1} {y} H{x2}" dur="{T}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" keyTimes="0;{a:.3f};{b:.3f};1"/></circle>')
    parts.append(wg(.04 + 3 * .14 + .09, .95, T, f'<rect x="{X["c"]+14}" y="{124+3*54+6}" width="128" height="24" rx="12" fill="none" stroke="{AMB}"/><text class="m" x="{X["c"]+78}" y="{124+3*54+22}" font-size="12" fill="{AMB}" text-anchor="middle">token stored</text>'))
    parts.append(wg(.04 + 4 * .14 + .09, .95, T, f'<rect x="{X["a"]+14}" y="{124+4*54+14}" width="120" height="26" rx="13" fill="{O}"/><text class="m" x="{X["a"]+74}" y="{124+4*54+31}" font-size="12" font-weight="700" fill="{BG}" text-anchor="middle">role guard ✓</text>'))
    save("jwt-flow.svg", svg(w, h, "\n".join(parts), "", "", bg=True))


# =====================================================================
# ERP DASHBOARD (sample UI)
# =====================================================================
def dashboard():
    w, h, T = 1000, 440, 9
    parts = [frame(w, h)]
    parts.append(f'<rect x="14.5" y="14.5" width="170" height="411" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
                 f'<circle cx="40" cy="42" r="12" fill="{O}"><animate attributeName="r" values="12;14;12" dur="2.4s" repeatCount="indefinite"/></circle>'
                 f'<text x="60" y="48" font-size="16" font-weight="800" fill="{TXT}">ERP Admin</text>')
    menu = ["Dashboard", "Orders", "Menu items", "Inventory", "Customers", "Reports"]
    ys = [80 + i * 40 for i in range(6)]
    vals = ";".join(str(y) for y in ys + [ys[0]])
    kt = ";".join(f"{i/6:.3f}" for i in range(7))
    parts.append(f'<rect x="24" y="80" width="150" height="32" rx="8" fill="{O}" fill-opacity=".16" stroke="{O}" stroke-opacity=".6"><animate attributeName="y" values="{vals}" keyTimes="{kt}" dur="{T*1.5}s" repeatCount="indefinite" calcMode="discrete"/></rect>')
    for i, m in enumerate(menu):
        parts.append(f'<rect x="36" y="{ys[i]+11}" width="10" height="10" rx="3" fill="{MUT}" fill-opacity=".7"/><text x="56" y="{ys[i]+21}" font-size="14" fill="{TXT}">{m}</text>')
    parts.append(f'<text x="206" y="48" font-size="22" font-weight="700" fill="{TXT}">Overview</text><text class="m" x="318" y="47" font-size="12" fill="{MUT}">// sample data</text>'
                 f'<rect x="800" y="26" width="140" height="28" rx="14" fill="{PANEL}" stroke="{LINE}"/><circle cx="962" cy="40" r="14" fill="{O}" fill-opacity=".85"/>')
    kpis = [("Orders today", ["0", "320", "640", "960", "1,284"]), ("Revenue", ["Rs 0", "Rs 90K", "Rs 210K", "Rs 340K", "Rs 482K"]), ("Customers", ["0", "120", "260", "410", "536"])]
    for i, (lab, vs) in enumerate(kpis):
        x = 200 + i * 262
        parts.append(f'<rect x="{x+.5}" y="70.5" width="244" height="86" rx="12" fill="{PANEL}" stroke="{LINE}"/><text x="{x+18}" y="98" font-size="13" fill="{MUT}">{lab}</text>')
        parts.append(count_texts(x + 18, 138, vs, T, 0.05, 0.4, f'font-size="30" font-weight="800" fill="{TXT}"'))
        sp = f"M{x+150} 130 L{x+170} 118 L{x+188} 124 L{x+208} 102 L{x+226} 96"
        parts.append(f'<path d="{sp}" pathLength="100" fill="none" stroke="{O}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="100" stroke-dashoffset="{0 if DEBUG else 100}"><animate attributeName="stroke-dashoffset" values="100;100;0;0;100" keyTimes="0;.1;.4;.92;1" dur="{T}s" begin="{i*.3}s" repeatCount="indefinite"/></path>')
    # bar chart
    parts.append(f'<rect x="200.5" y="172.5" width="484" height="252" rx="12" fill="{PANEL}" stroke="{LINE}"/><text x="220" y="202" font-size="15" font-weight="700" fill="{TXT}">Orders this week</text>')
    base = 396
    hs = [80, 118, 96, 150, 128, 168, 138]
    for i, (d, hv) in enumerate(zip(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], hs)):
        x = 226 + i * 63
        a = .06 + i * .03
        parts.append(f'<rect x="{x}" y="{base-hv if DEBUG else base}" width="34" height="{hv if DEBUG else 0}" rx="6" fill="{O}" fill-opacity="{.5+i*.07:.2f}">'
                     f'<animate attributeName="y" values="{base};{base};{base-hv};{base-hv};{base}" keyTimes="0;{a:.2f};{a+.18:.2f};.92;1" dur="{T}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="height" values="0;0;{hv};{hv};0" keyTimes="0;{a:.2f};{a+.18:.2f};.92;1" dur="{T}s" repeatCount="indefinite"/></rect>'
                     f'<text class="m" x="{x+17}" y="416" font-size="11" fill="{MUT}" text-anchor="middle">{d}</text>')
    # donut
    dcx, dcy, r = 842, 290, 52
    parts.append(f'<rect x="698.5" y="172.5" width="288" height="252" rx="12" fill="{PANEL}" stroke="{LINE}"/><text x="718" y="202" font-size="15" font-weight="700" fill="{TXT}">Top categories</text>'
                 f'<circle cx="{dcx}" cy="{dcy}" r="{r}" fill="none" stroke="{BG}" stroke-width="18"/>')
    C = 2 * math.pi * r
    for col, off, ln, a in [(O, 0, 52, .05), (AMB, 52, 30, .2), ("#FFD9B3", 82, 18, .35)]:
        L = C * ln / 100
        parts.append(f'<circle cx="{dcx}" cy="{dcy}" r="{r}" fill="none" stroke="{col}" stroke-width="18" stroke-dasharray="{(L if DEBUG else 0):.1f} {C:.1f}" stroke-dashoffset="{-C*off/100:.1f}" transform="rotate(-90 {dcx} {dcy})">'
                     f'<animate attributeName="stroke-dasharray" values="0 {C:.1f};0 {C:.1f};{L:.1f} {C-L:.1f};{L:.1f} {C-L:.1f};0 {C:.1f}" keyTimes="0;{a};{a+.2:.2f};.92;1" dur="{T}s" repeatCount="indefinite"/></circle>')
    parts.append(f'<text class="m" x="{dcx}" y="{dcy+5}" font-size="13" fill="{TXT}" text-anchor="middle">mix</text>')
    for i, (c, t) in enumerate([(O, "Burgers"), (AMB, "Sides"), ("#FFD9B3", "Drinks")]):
        parts.append(f'<circle cx="{728+i*88}" cy="372" r="5" fill="{c}"/><text x="{738+i*88}" y="376" font-size="12" fill="{MUT}">{t}</text>')
        pass
    save("dashboard.svg", svg(w, h, "\n".join(parts)))


# =====================================================================
# KIOSK
# =====================================================================
def kiosk():
    w, h, T = 1000, 470, 14
    parts = [frame(w, h)]
    parts.append(f'<rect x="40.5" y="16.5" width="340" height="438" rx="28" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/><rect x="56" y="32" width="308" height="380" rx="16" fill="{BG}" stroke="{LINE}"/>'
                 f'<rect x="150" y="430" width="120" height="8" rx="4" fill="{BG}" stroke="{O}" stroke-opacity=".7"><animate attributeName="stroke-opacity" values=".3;1;.3" dur="1.6s" repeatCount="indefinite"/></rect>'
                 f'<text x="74" y="62" font-size="18" font-weight="800" fill="{TXT}">Order here</text><text class="m" x="350" y="60" font-size="11" fill="{O}" text-anchor="end">self-checkout</text>')
    tiles = [("Burger", "Rs 650", 72, 80, .12), ("Fries", "Rs 350", 218, 80, .24), ("Drink", "Rs 150", 72, 172, .36), ("Wrap", "Rs 500", 218, 172, None)]
    for nm, pr, x, y, t in tiles:
        parts.append(f'<rect x="{x}" y="{y}" width="130" height="80" rx="12" fill="{PANEL}" stroke="{LINE}"/><circle cx="{x+24}" cy="{y+26}" r="10" fill="{O}" fill-opacity=".85"/>'
                     f'<text x="{x+44}" y="{y+31}" font-size="16" font-weight="700" fill="{TXT}">{nm}</text><text class="m" x="{x+16}" y="{y+64}" font-size="13" fill="{MUT}">{pr}</text>')
        if t:
            parts.append(wg(t, t + .06, T, f'<rect x="{x}" y="{y}" width="130" height="80" rx="12" fill="{O}" fill-opacity=".18" stroke="{O}" stroke-width="2"/>'))
            parts.append(f'<circle cx="{x+65}" cy="{y+40}" r="0" fill="none" stroke="{O}" stroke-width="2"><animate attributeName="r" values="0;0;38;38" keyTimes="0;{t:.3f};{t+.06:.3f};1" dur="{T}s" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="0;.9;0;0" keyTimes="0;{t:.3f};{t+.06:.3f};1" dur="{T}s" repeatCount="indefinite"/></circle>')
    parts.append(f'<rect x="72" y="262" width="276" height="86" rx="12" fill="{PANEL}" stroke="{LINE}"/>')
    for i, (nm, pr, t) in enumerate([("1× Burger", "650", .12), ("1× Fries", "350", .24), ("1× Drink", "150", .36)]):
        y = 282 + i * 17
        parts.append(wg(t, .93, T, f'<text class="m" x="86" y="{y}" font-size="12" fill="{TXT}">{nm}</text><text class="m" x="334" y="{y}" font-size="12" fill="{MUT}" text-anchor="end">{pr}</text>'))
    parts.append(f'<path d="M86 330 H334" stroke="{LINE}" stroke-dasharray="3 4"/><text class="m" x="86" y="343" font-size="12" fill="{MUT}">Total</text>')
    for txt, a, b in [("Rs 0", 0, .12), ("Rs 650", .12, .24), ("Rs 1,000", .24, .36), ("Rs 1,150", .36, .93), ("Rs 0", .93, 1.0)]:
        parts.append(wg(a, b, T, f'<text class="m" x="334" y="343" font-size="13" font-weight="700" fill="{O}" text-anchor="end">{txt}</text>'))
    base, an = win(.36, .93, T)
    parts.append(f'<g opacity="{"1" if DEBUG else ".35"}"><animate attributeName="opacity" calcMode="discrete" values=".35;1;.35;.35" keyTimes="0;.36;.93;1" dur="{T}s" repeatCount="indefinite"/><rect x="72" y="358" width="276" height="42" rx="10" fill="{O}"/><text x="210" y="385" font-size="16" font-weight="800" fill="{BG}" text-anchor="middle">Pay now</text></g>')
    parts.append(wg(.42, .5, T, f'<rect x="68" y="354" width="284" height="50" rx="13" fill="none" stroke="{O}" stroke-width="2"/>'))
    parts.append(wg(.5, .56, T, f'<rect x="72" y="358" width="276" height="42" rx="10" fill="{BG}" fill-opacity=".35"/>'))
    # success overlay
    ov = (f'<rect x="56" y="32" width="308" height="380" rx="16" fill="{BG}"/><circle cx="210" cy="170" r="44" fill="none" stroke="{O}" stroke-width="3"/>'
          f'<path d="M188 172 L205 189 L234 154" fill="none" stroke="{O}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="{0 if DEBUG else 100}"><animate attributeName="stroke-dashoffset" values="100;100;0;0;100" keyTimes="0;.6;.66;.92;1" dur="{T}s" repeatCount="indefinite"/></path>'
          f'<text x="210" y="256" font-size="22" font-weight="800" fill="{TXT}" text-anchor="middle">Order placed</text><text class="m" x="210" y="282" font-size="13" fill="{MUT}" text-anchor="middle">#104 · sent to the kitchen</text><text class="m" x="210" y="306" font-size="13" fill="{O}" text-anchor="middle">printing receipt…</text>')
    parts.append(wg(.58, .93, T, ov))
    # flow list
    parts.append(f'<text x="450" y="76" font-size="32" font-weight="800" fill="{TXT}">Self-checkout flow</text><text class="m" x="450" y="104" font-size="14" fill="{MUT}">// touch UI built for the counter-less order</text>')
    steps = [("Browse the menu", "Touch-friendly tiles", 0, .09), ("Add items", "Cart and total update instantly", .09, .45), ("Pay at the kiosk", "Clear checkout confirmation", .45, .58), ("Order sent", "Receipt prints, ticket lands on the KDS", .58, .93)]
    for i, (t, s, a, b) in enumerate(steps):
        y = 134 + i * 80
        parts.append(f'<rect x="450.5" y="{y+.5}" width="500" height="64" rx="12" fill="{PANEL}" stroke="{LINE}"/><circle cx="486" cy="{y+32}" r="16" fill="none" stroke="{O}"/><text class="m" x="486" y="{y+37}" font-size="14" font-weight="700" fill="{O}" text-anchor="middle">{i+1}</text>'
                     f'<text x="520" y="{y+28}" font-size="17" font-weight="700" fill="{TXT}">{t}</text><text x="520" y="{y+48}" font-size="13" fill="{MUT}">{s}</text>')
        parts.append(wg(a, b, T, f'<rect x="450" y="{y}" width="500" height="64" rx="12" fill="{O}" fill-opacity=".12" stroke="{O}" stroke-width="2"/><circle cx="486" cy="{y+32}" r="16" fill="{O}"/><text class="m" x="486" y="{y+37}" font-size="14" font-weight="800" fill="{BG}" text-anchor="middle">{i+1}</text>'))
    save("kiosk.svg", svg(w, h, "\n".join(parts)))


# =====================================================================
# README v2
# =====================================================================
def readme2():
    U, EM, LI, PF = B.USER, B.EMAIL, B.LINKEDIN, B.PORTFOLIO
    lines = ["Frontend Developer @ Airtech Solutions", "MERN Stack · React · Angular · Node.js · MongoDB",
             "Building FoodlyOS — multi-role food delivery", "POS · KDS · Kiosk · ERP · Receipt printing",
             "From Figma designs to production-ready UIs"]
    typing = "https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=17&duration=3200&pause=1100&color=FF7A1A&center=true&vCenter=true&width=820&lines=" + ";".join(quote_plus(l) for l in lines)
    S = "./assets/"
    img = lambda alt, f: f"[![{alt}]({S}{f})]({S}{f})"
    badges = (f"[![Email](https://img.shields.io/badge/EMAIL-sobanahmed9898%40gmail.com-FF7A1A?style=for-the-badge&logo=gmail&logoColor=0B0C0F&labelColor=0B0C0F)](mailto:{EM}) "
              f"[![LinkedIn](https://img.shields.io/badge/LINKEDIN-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LI}) "
              f"[![GitHub](https://img.shields.io/badge/GITHUB-{U}-FF7A1A?style=for-the-badge&logo=github&logoColor=0B0C0F&labelColor=0B0C0F)](https://github.com/{U}) "
              f"[![Portfolio](https://img.shields.io/badge/PORTFOLIO-LIVE-FF7A1A?style=for-the-badge&logo=vercel&logoColor=0B0C0F&labelColor=0B0C0F)]({PF})")
    md = f'''<a name="top"></a>
<div align="center">

{img("Soban Ahmed — MERN Stack Developer and Frontend Developer", "hero.svg")}

[![Typing animation]({typing})](https://github.com/{U})

{badges}

[![Open to](https://img.shields.io/badge/OPEN_TO-OPPORTUNITIES-FF7A1A?style=flat-square&logo=rocket&logoColor=0B0C0F&labelColor=0B0C0F)](mailto:{EM}) [![Location](https://img.shields.io/badge/BASED_IN-KARACHI,_PAKISTAN-FF7A1A?style=flat-square&logo=googlemaps&logoColor=0B0C0F&labelColor=0B0C0F)](#contact) [![Work](https://img.shields.io/badge/WORKING_AT-AIRTECH_SOLUTIONS-FF7A1A?style=flat-square&logo=briefcase&logoColor=0B0C0F&labelColor=0B0C0F)](#experience) [![Followers](https://img.shields.io/github/followers/{U}?style=flat-square&label=followers&color=FF7A1A&labelColor=0B0C0F)](https://github.com/{U}?tab=followers) [![Profile views](https://komarev.com/ghpvc/?username={U}&label=profile%20views&style=flat-square&color=FF7A1A&labelColor=0B0C0F)](https://github.com/{U})

**[About](#about) · [Skills](#skills) · [How I Build](#how-i-build) · [Projects](#projects) · [Experience](#experience) · [Services](#services) · [UI Demos](#demos) · [Stack](#stack) · [Activity](#activity) · [Contact](#contact)**

![divider]({S}divider.svg)

</div>

<a name="about"></a>

{img("About", "section-about.svg")}

I build web products across the whole stack: **React and Angular frontends**, **Node/Express REST APIs with JWT auth**, and **MongoDB** data layers. At work I ship **ERP, POS, KDS, Kiosk and Self-Checkout** interfaces with printer integration, and I use **AI-assisted development** to build and debug faster.

{img("Frontend, Backend, Business Systems and Mobile & AI capabilities", "about.svg")}

{img("Counters: 3 user roles, 5 business systems, 3 frameworks, 6 stage workflow", "stats.svg")}

{img("Terminal: whoami, stack and recent commits", "terminal.svg")}

| 🔭 Working on | 🌱 Improving | 🎓 Next goal |
|---|---|---|
| FoodlyOS, a full MERN food delivery product | Full-stack skills, clean architecture & reusable components | University studies in Computer Science |

<details>
<summary><b>⚡ Quick facts</b> (click to expand)</summary>
<br>

| | |
|---|---|
| 📍 **Based in** | Karachi, Pakistan |
| 🏢 **Working at** | Airtech Solutions (Frontend Developer, since Dec 2025) |
| 🧰 **Focus** | MERN stack, React, Angular, POS / KDS / Kiosk / ERP interfaces |
| 🚀 **Building** | FoodlyOS, a multi-role food delivery platform |
| 📫 **Reach me** | [{EM}](mailto:{EM}) · [Portfolio]({PF}) |

</details>

![ticker]({S}ticker.svg)

<a name="skills"></a>

{img("Skills", "section-skills.svg")}

{img("Animated skill bars", "skills.svg")}

{img("Rotating tech orbit: React, Angular, Node.js, Express, MongoDB, Flutter, Git and more", "orbit.svg")}

<a name="how-i-build"></a>

{img("How I Build", "section-workflow.svg")}

One workflow, six stages. Every project goes through the same path.

{img("Pipeline: Design, Plan, Build UI, Integrate, Test, Deliver", "pipeline.svg")}

{img("Responsive demo: one layout reflowing from desktop to tablet to mobile", "responsive.svg")}

<a name="projects"></a>

{img("Featured Projects", "section-projects.svg")}

#### 🍔 FoodlyOS &nbsp;`In Development`

**Multi-role food delivery platform** built on the full MERN stack with JWT authentication and role-based access.

{img("FoodlyOS architecture: Super Admin, Restaurant Admin and Customer Website to a Node.js Express REST API, then MongoDB", "foodlyos-architecture.svg")}

**How a request is authenticated:** login, signed token, then a role check on every protected route.

{img("Sequence: login, JWT issued, protected request with role guard", "jwt-flow.svg")}

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

[![ChatGPT-Auto-Prompt](https://github-readme-stats.vercel.app/api/pin/?username={U}&repo=ChatGPT-Auto-Prompt&bg_color=0B0C0F&title_color=FF7A1A&text_color=E8E8EA&icon_color=FF7A1A&border_color=23262D)](https://github.com/{U}/ChatGPT-Auto-Prompt)

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

| 🌐 Web Apps | 📊 Admin Panels | 🧾 POS / KDS / Kiosk | ⚙️ MERN Products |
|---|---|---|---|
| React.js & Angular applications built from scratch | Dashboards, ERP screens & business workflows | Order, billing, checkout & receipt printing UIs | Full-stack apps with REST APIs, JWT & role-based access |

{img("Animated demo: kitchen display order flow and receipt printing", "pos-demo.svg")}

<div align="center">

[![Let's Work Together](https://img.shields.io/badge/%F0%9F%93%A9%20LET'S%20WORK%20TOGETHER-FF7A1A?style=for-the-badge&labelColor=0B0C0F)](mailto:{EM}?subject=Project%20Inquiry)

</div>

<a name="demos"></a>

{img("UI Demos", "section-demos.svg")}

Animated mockups of the kind of interfaces I build. The numbers inside are sample data.

{img("ERP dashboard mockup with animated charts and counters", "dashboard.svg")}

{img("Self-checkout kiosk mockup: browse, add to cart, pay, order sent", "kiosk.svg")}

<a name="stack"></a>

{img("Tech Stack", "section-stack.svg")}

{img("Technology stack: frontend, backend, database, mobile, business systems and AI tools", "stack.svg")}

<a name="activity"></a>

{img("GitHub Activity", "section-activity.svg")}

<div align="center">

[![GitHub stats](https://github-readme-stats.vercel.app/api?username={U}&show_icons=true&hide_border=true&count_private=true&bg_color=0B0C0F&title_color=FF7A1A&icon_color=FF7A1A&text_color=E8E8EA&ring_color=FF7A1A)](https://github.com/{U}) [![Top languages](https://github-readme-stats.vercel.app/api/top-langs/?username={U}&layout=compact&hide_border=true&bg_color=0B0C0F&title_color=FF7A1A&text_color=E8E8EA)](https://github.com/{U})

[![GitHub streak](https://streak-stats.demolab.com?user={U}&hide_border=true&background=0B0C0F&ring=FF7A1A&fire=FF7A1A&currStreakLabel=FF7A1A&currStreakNum=E8E8EA&sideLabels=E8E8EA&sideNums=E8E8EA&dates=8A8F98&stroke=23262D)](https://github.com/{U})

[![Contribution activity graph](https://github-readme-activity-graph.vercel.app/graph?username={U}&bg_color=0B0C0F&color=FF7A1A&line=FF7A1A&point=FFFFFF&area=true&area_color=FF7A1A&hide_border=true)](https://github.com/{U})

[![Contribution graph snake animation](https://raw.githubusercontent.com/{U}/{U}/output/github-snake-dark.svg)](https://github.com/{U})

</div>

<a name="contact"></a>

{img("Contact", "section-contact.svg")}

[![Let's build something great. {EM}]({S}contact.svg)](mailto:{EM})

<div align="center">

{badges}

{img("footer", "footer.svg")}

<a href="#top">⬆️ Back to top</a>

</div>
'''
    with open(os.path.join(B.HERE, "README.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print("wrote README.md (v2)")


def build_extra():
    stats(); ticker(); orbit(); responsive(); jwt_flow(); dashboard(); kiosk()
    B.section("demos", "UI Demos", "// animated mockups")
    readme2()
