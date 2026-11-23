"""Corrigés détaillés du TD5 (magnétostatique : Biot et Savart, théorème d'Ampère) : schémas SVG et insertion
idempotente dans corriges.html (section #td5 entre <!-- TD5:DEBUT --> et <!-- TD5:FIN -->, carte d'index
<!-- TD5CARD:DEBUT/FIN -->, titre h1).
Usage : python tools/gen_td5.py   (relançable). Les résultats sont vérifiés par tools/verif_td5.py."""
import math
import os
import re

from scipy.special import ellipe, ellipk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CRLF = {}


def lire(p):
    t = open(os.path.join(ROOT, p), encoding='utf-8', newline='').read()
    _CRLF[p] = chr(13) + chr(10) in t
    return t.replace(chr(13) + chr(10), chr(10))


def ecrire(p, s):
    if _CRLF.get(p):
        s = s.replace(chr(10), chr(13) + chr(10))
    open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)


# =============================================================== outils SVG
def sb(s):
    """X[Y] -> indice SVG"""
    n = len(re.findall(r'\[([^\]]*)\]', s))
    s = re.sub(r'\[([^\]]*)\]', r'<tspan dy="3.2" font-size="72%">\1</tspan><tspan dy="-3.2">', s)
    return s + '</tspan>' * n


def cap(s):
    return re.sub(r'\[([^\]]*)\]', r'<sub>\1</sub>', s)


class Fig:
    def __init__(self, w, h):
        self.w, self.h, self.p = w, h, []

    def add(self, s):
        self.p.append(s)

    def line(self, x1, y1, x2, y2, c='ob', style=''):
        self.add('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"%s/>' % (c, x1, y1, x2, y2, (' style="%s"' % style) if style else ''))

    def head(self, x, y, dx, dy, hc='efh', size=7):
        a = math.atan2(dy, dx)
        bx, by = x - size * math.cos(a), y - size * math.sin(a)
        px, py = -math.sin(a) * size * 0.45, math.cos(a) * size * 0.45
        self.add('<polygon class="%s" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>' % (hc, x, y, bx + px, by + py, bx - px, by - py))

    def arrow(self, x1, y1, x2, y2, c='ef', hc='efh', size=7):
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - size * math.cos(a), y2 - size * math.sin(a)
        self.line(x1, y1, bx, by, c)
        self.head(x2, y2, x2 - x1, y2 - y1, hc, size)

    def circ(self, cx, cy, r, c='ob', style=''):
        self.add('<circle class="%s" cx="%.1f" cy="%.1f" r="%.1f"%s/>' % (c, cx, cy, r, (' style="%s"' % style) if style else ''))

    def rect(self, x, y, w, h, c='ob'):
        self.add('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (c, x, y, w, h))

    def path(self, d, c='ob'):
        self.add('<path class="%s" d="%s"/>' % (c, d))

    def poly(self, pts, c='box'):
        self.add('<polygon class="%s" points="%s"/>' % (c, ' '.join('%.1f,%.1f' % p for p in pts)))

    def polyline(self, pts, c='fl'):
        self.add('<path class="%s" d="M%s"/>' % (c, ' L'.join('%.1f %.1f' % p for p in pts)))

    def text(self, x, y, s, c='tx', anchor='middle', size=None, halo=False):
        st = ''
        if size or halo:
            st = ' style="%s%s"' % (('font-size:%spx;' % size) if size else '', 'stroke:var(--surface2);stroke-width:3.6px;paint-order:stroke;stroke-linejoin:round' if halo else '')
        self.add('<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' % (c, x, y, anchor, st, sb(s)))

    def wire(self, x, y, sortant=True, r=8.5, c='ob'):
        """fil perpendiculaire à la page : point (sortant) ou croix (entrant)"""
        self.circ(x, y, r, c, 'fill:var(--surface)')
        if sortant:
            self.add('<circle class="pt" cx="%.1f" cy="%.1f" r="2.4"/>' % (x, y))
        else:
            d = r * 0.58
            self.line(x - d, y - d, x + d, y + d, c, 'stroke-width:1.5')
            self.line(x - d, y + d, x + d, y - d, c, 'stroke-width:1.5')

    def svg(self, aria, caption, maxw=None):
        mw = int((maxw or self.w) * 1.3)
        return ('<figure class="fgbox"><svg class="fg" viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:%dpx">%s</svg>'
                '<figcaption>%s</figcaption></figure>' % (self.w, self.h, aria, mw, ''.join(self.p), caption))


def arc(cx, cy, r, a1, a2, c='ac', n=24):
    """arc de cercle (angles en degrés, repère mathématique y vers le haut), tracé en polyligne"""
    pts = []
    for k in range(n + 1):
        a = math.radians(a1 + (a2 - a1) * k / n)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    return pts


def circle_arrows(f, cx, cy, r, angs, sens=+1, c='flh', size=7):
    """pointes de flèches sur un cercle (angle mathématique en degrés ; sens=+1 : trigonométrique à l'écran)"""
    for a in angs:
        t = math.radians(a)
        x, y = cx + r * math.cos(t), cy - r * math.sin(t)
        dx, dy = -math.sin(t) * sens, -math.cos(t) * sens
        f.head(x + dx * size * 0.5, y + dy * size * 0.5, dx, dy, c, size)


FIG = {}

# ---------------------------------------------------------------- Ex 1 : fil coudé
f = Fig(480, 235)
ox, oy = 170, 100
mx = 330
f.line(40, oy, ox, oy, 'ob')
f.line(ox, oy, ox, 225, 'ob')
f.arrow(128, oy, 84, oy, 'ef', 'efh', 8)
f.arrow(ox, 222, ox, 196, 'ef', 'efh', 8)
f.text(ox - 12, 212, 'I', 'te', 'end', 14)
f.text(106, oy - 9, 'I', 'te', 'middle', 14)
f.line(ox, oy, mx, oy, 'dsh')
f.circ(mx, oy, 4, 'ptM')
f.text(mx + 10, oy - 9, 'M', 'tx', 'start', 14)
f.text(ox - 10, oy - 9, 'O', 'tx', 'end', 14)
f.text((ox + mx) / 2, oy - 9, 'a', 'tx', 'middle', 14)
py = 165
f.circ(ox, py, 3.2, 'pt')
f.text(ox - 9, py + 4, 'P', 'tx', 'end', 13)
f.arrow(ox + 12, py + 12, ox + 12, py - 14, 'ef', 'efh', 6)
f.text(ox + 20, py + 4, 'dl', 'te', 'start', 13)
f.line(ox, py, mx, oy, 'dsh')
a_ = math.atan2(py - oy, mx - ox)
f.polyline(arc(mx, oy, 48, 180, 180 + math.degrees(a_)), 'ac')
f.text(mx - 66, oy + 17, 'α', 'tc', 'middle', 14)
# champ en M : croix (entrant)
f.wire(mx, oy, False, 9)
f.text(mx, oy - 28, 'B(M) entrant', 'tc', 'middle', 13)
# repère
f.circ(52, 190, 7, 'ob', 'fill:var(--surface)')
f.add('<circle class="pt" cx="52.0" cy="190.0" r="2.2"/>')
f.text(40, 206, 'z (sortant)', 'tm', 'start', 12)
f.arrow(52, 190, 100, 190, 'ax', 'axh', 6)
f.text(106, 194, 'x', 'tm', 'start', 13)
f.arrow(52, 190, 52, 140, 'ax', 'axh', 6)
f.text(60, 142, 'y', 'tm', 'start', 13)
f.text(208, 202, 'branche horizontale : dl ∥ PM, donc dB = 0', 'tm', 'start', 12)
f.text(208, 222, 'branche verticale : B = μ[0] I /(4π a)', 'tm', 'start', 12)
FIG['ex1'] = f.svg('Fil infini coudé à angle droit et point M sur le prolongement de la branche horizontale',
                   cap('Fil coudé en O. M est sur le prolongement de la branche horizontale (dl ∥ PM, aucune contribution) ; la branche verticale est un fil semi-infini dont le pied de la perpendiculaire est O : B = μ[0]I/(4πa), entrant dans la page.'), 480)

# ---------------------------------------------------------------- Ex 2 : quatre fils
f = Fig(540, 265)
cx, cy, h = 150, 135, 85
corn = {1: (cx + h, cy - h), 2: (cx - h, cy - h), 3: (cx - h, cy + h), 4: (cx + h, cy + h)}
for a_, b_ in ((1, 2), (2, 3), (3, 4), (4, 1)):
    f.line(corn[a_][0], corn[a_][1], corn[b_][0], corn[b_][1], 'dsh')
for k, (x, y) in corn.items():
    f.wire(x, y, False, 8.5)
lab = {1: (corn[1][0] + 14, corn[1][1] - 10), 2: (corn[2][0] - 14, corn[2][1] - 10), 3: (corn[3][0] - 14, corn[3][1] + 20), 4: (corn[4][0] + 14, corn[4][1] + 20)}
for k, (x, y) in lab.items():
    f.text(x, y, str(k), 'tm', 'middle', 13)
dirs = {1: (-1, -1), 2: (-1, 1), 3: (1, 1), 4: (1, -1)}  # coordonnées écran des B_k en O
for k, (sx, sy) in dirs.items():
    L = 52 / math.sqrt(2)
    f.arrow(cx, cy, cx + sx * L, cy + sy * L, 'bl', 'blh', 8)
    f.text(cx + sx * (L + 9), cy + sy * (L + 5) + (4 if sy > 0 else 0), 'B[%d]' % k, 'tc', 'end' if sx < 0 else 'start', 13)
f.circ(cx, cy, 3, 'pt')
f.text(cx + 7, cy + 4, 'O', 'tx', 'start', 12)
f.text(cx, cy - h - 24, '2b', 'tx', 'middle', 13)
f.text(cx - h - 24, cy + 4, '2b', 'tx', 'end', 13)
f.text(300, 62, 'un fil : B[k] = μ[0]I /(2π b√2)', 'tc', 'start', 13)
f.text(300, 82, 'perpendiculaire à Ok, sens horaire', 'tm', 'start', 12)
f.text(300, 100, '(courants entrants)', 'tm', 'start', 12)
f.text(300, 140, 'B[1] + B[3] = 0', 'tx', 'start', 14)
f.text(300, 162, 'B[2] + B[4] = 0', 'tx', 'start', 14)
f.text(300, 196, 'B(O) = 0', 'te', 'start', 16)
f.text(300, 226, 'plans x = 0 et y = 0 : symétrie des courants', 'tm', 'start', 12)
f.text(300, 244, 'donc B ∥ e[y] et B ∥ e[x] en O', 'tm', 'start', 12)
FIG['ex2'] = f.svg('Quatre fils au sommet d\'un carré et champ de chaque fil au centre', cap('Quatre fils entrants aux sommets d\'un carré de côté 2b. Chaque fil crée en O un champ de même module, perpendiculaire à la diagonale correspondante ; les champs des fils diagonalement opposés se compensent : B(O) = 0.'), 540)

# ---------------------------------------------------------------- champ d'une spire (éléments elliptiques), unités mu0 I /(2π) = 1
def loop_field(r, z, R=1.0):
    r = max(abs(r), 1e-9)
    d1 = (R + r) ** 2 + z ** 2
    d2 = (R - r) ** 2 + z ** 2
    m = 4 * R * r / d1
    K, E = ellipk(m), ellipe(m)
    Bz = (K + (R * R - r * r - z * z) / d2 * E) / math.sqrt(d1)
    Br = (z / (r * math.sqrt(d1))) * (-K + (R * R + r * r + z * z) / d2 * E)
    return Br, Bz


def loop_xz(x, z):
    br, bz = loop_field(abs(x), z)
    return (math.copysign(1.0, x) * br if abs(x) > 1e-9 else 0.0), bz


def rk4(Bf, x, y, h):
    def u(x_, y_):
        bx, by = Bf(x_, y_)
        n = math.hypot(bx, by)
        return (bx / n, by / n) if n > 1e-12 else (0.0, 0.0)
    k1 = u(x, y)
    k2 = u(x + h / 2 * k1[0], y + h / 2 * k1[1])
    k3 = u(x + h / 2 * k2[0], y + h / 2 * k2[1])
    k4 = u(x + h * k3[0], y + h * k3[1])
    return x + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]), y + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])


def trace(Bf, p0, h, inbox, nmax=5000, sgn=1):
    pts = [p0]
    x, y = p0
    for i in range(nmax):
        x, y = rk4(Bf, x, y, sgn * h)
        if not inbox(x, y):
            break
        pts.append((x, y))
        if i > 12 and math.hypot(x - p0[0], y - p0[1]) < 0.8 * h:
            pts.append(p0)
            return pts, True
    return pts, False


def fline(Bf, p0, h, inbox):
    fw, closed = trace(Bf, p0, h, inbox)
    if closed:
        return fw
    bw, _ = trace(Bf, p0, h, inbox, sgn=-1)
    return bw[::-1][:-1] + fw


def draw_lines(f, lines, tr, fracs=(0.5,), cls='fl', hcls='flh', hs=7):
    """lines : listes de points en unités du modèle ; tr : fonction -> écran. Place une pointe aux fractions de longueur indiquées
    (fracs : un tuple de fractions, ou une liste de tuples utilisés tour à tour pour répartir les pointes)"""
    for i_ln, pts in enumerate(lines):
        frs = fracs[i_ln % len(fracs)] if isinstance(fracs[0], (tuple, list)) else fracs
        sp = [tr(*p) for p in pts]
        if len(sp) < 3:
            continue
        f.polyline(sp, cls)
        L = [0.0]
        for a_, b_ in zip(sp, sp[1:]):
            L.append(L[-1] + math.hypot(b_[0] - a_[0], b_[1] - a_[1]))
        for fr in frs:
            tgt = fr * L[-1]
            k = next((i for i, v in enumerate(L) if v >= tgt), len(L) - 1)
            k = min(max(k, 1), len(sp) - 2)
            dx, dy = sp[k + 1][0] - sp[k - 1][0], sp[k + 1][1] - sp[k - 1][1]
            f.head(sp[k][0] + dx / math.hypot(dx, dy) * hs * 0.5, sp[k][1] + dy / math.hypot(dx, dy) * hs * 0.5, dx, dy, hcls, hs)


# ---------------------------------------------------------------- Ex 3 : spire (3D) et lignes de champ
f = Fig(500, 285)
ox, oy = 110, 140
f.arrow(25, oy, 470, oy, 'ax', 'axh', 7)
f.text(478, oy + 16, 'z', 'tm', 'end', 14)
f.arrow(ox, oy, ox, 18, 'ax', 'axh', 7)
f.text(ox + 12, 24, 'x', 'tm', 'start', 14)
f.arrow(ox, oy, 62, oy + 52, 'ax', 'axh', 7)
f.text(54, oy + 66, 'y', 'tm', 'end', 14)
rx, ry = 24, 82
ell = [(ox + rx * math.sin(t / 60 * 2 * math.pi), oy - ry * math.cos(t / 60 * 2 * math.pi)) for t in range(61)]
f.polyline(ell, 'ob')
# courant : vers +y au point haut (côté gauche de l'ellipse à l'écran)
cur = [(ox - rx * math.sin(2 * math.pi * (0.06 + 0.16 * k / 10)), oy - ry * math.cos(2 * math.pi * (0.06 + 0.16 * k / 10))) for k in range(11)]
f.polyline(cur, 'ef')
f.head(cur[-1][0], cur[-1][1], cur[-1][0] - cur[-2][0], cur[-1][1] - cur[-2][1], 'efh', 9)
f.text(cur[3][0] - 12, cur[3][1] + 4, 'I', 'te', 'end', 14)
Px, Py = ox, oy - ry
Mx = 330
f.circ(Px, Py, 3.2, 'pt')
f.text(Px + 10, Py - 6, 'P', 'tx', 'start', 13)
f.circ(ox, oy, 3, 'pt')
f.text(ox - 8, oy + 16, 'O', 'tx', 'end', 13)
f.text(ox + 8, (Py + oy) / 2 + 4, 'R', 'tx', 'start', 13)
f.circ(Mx, oy, 4, 'ptM')
f.text(Mx - 10, oy + 18, 'M', 'tx', 'end', 14)
f.line(Px, Py, Mx, oy, 'ob2')
f.line(ox, oy + ry, Mx, oy, 'ob2')
aM = math.degrees(math.atan2(oy - Py, Mx - Px))
f.polyline(arc(Mx, oy, 46, 180, 180 - aM), 'ac')
f.text(Mx - 66, oy - 6, 'α', 'tc', 'middle', 14)
# dB en M (élément en P) : perpendiculaire à PM, dans le plan xz, vers +z et +x
ux, uy = Mx - Px, oy - Py
n = math.hypot(ux, uy)
ux, uy = ux / n, uy / n
vx, vy = -uy, ux
vx, vy = (vx, vy) if vy < 0 else (-vx, -vy)
f.arrow(Mx, oy, Mx + 58 * vx, oy + 58 * vy, 'fl', 'flh', 7)
f.text(Mx + 58 * vx + 6, oy + 58 * vy - 2, 'dB (élément en P)', 'tm', 'start', 12)
# dB' (élément diamétralement opposé) : composante radiale opposée
f.arrow(Mx, oy, Mx + 58 * vx, oy - 58 * vy, 'fl', 'flh', 7)
f.text(Mx + 58 * vx + 6, oy - 58 * vy + 12, 'dB′ (élément opposé)', 'tm', 'start', 12)
f.arrow(Mx + 4, oy, Mx + 112, oy, 'bl', 'blh', 9)
f.text(Mx + 118, oy + 22, 'B(M) = B[z] e[z]', 'tc', 'end', 14)
f.text(250, 262, 'les composantes radiales de dB et dB′ s\'annulent, les composantes axiales s\'ajoutent', 'tm', 'middle', 12)
FIG['ex3a'] = f.svg('Spire circulaire d\'axe Oz et champ élémentaire en un point M de l\'axe', cap('Spire de rayon R d\'axe Oz, parcourue par I dans le sens trigonométrique vu de +z. En M, dB (créé par l\'élément en P) est perpendiculaire à PM dans le plan (x, z) ; son symétrique dB′ (élément diamétralement opposé) a la même composante axiale et une composante radiale opposée.'), 500)

# lignes de champ de la spire (coupe méridienne y = 0)
f = Fig(480, 242)
sc = 58.0
cx, cy = 240, 112
S = lambda x, z: (cx + sc * x, cy - sc * z)
box = lambda x, z: -3.7 <= x <= 3.7 and -1.75 <= z <= 1.75
lines = []
for x0 in (0.0, 0.35, 0.7, 1.45, 1.8, 2.3, 3.0):
    ln = fline(loop_xz, (x0, 0.0), 0.04, box)
    lines.append(ln)
    if x0 > 1e-6:
        lines.append([(-x, z) for x, z in ln])
draw_lines(f, lines, S, [(0.25,), (0.5,), (0.75,), (0.4,), (0.62,)], 'fl', 'flh', 7)
# axe : flèche
f.wire(cx + sc, cy, False, 8)
f.wire(cx - sc, cy, True, 8)
f.text(cx + 8, 22, 'Oz', 'tm', 'start', 12, True)
f.text(cx, 234, 'coupe par un plan contenant l\'axe : courant entrant en x = R, sortant en x = −R', 'tm', 'middle', 12)
FIG['ex3b'] = f.svg('Lignes de champ d\'une spire dans un plan contenant l\'axe', cap('Lignes du champ d\'une spire (calcul numérique exact, intégrales elliptiques) dans un plan contenant l\'axe : sur l\'axe B est selon e[z] ; ailleurs B = B[r](r, z) e[r] + B[z](r, z) e[z], sans composante selon e[θ] : deux composantes qui dépendent de r et de z, donc le théorème d\'Ampère ne permet pas de conclure.'), 480)

# ---------------------------------------------------------------- Ex 4 : lignes de champ (fils parallèles)
K = 1.0


def wires_field(ws):
    """ws : liste (x, y, s) avec s=+1 courant sortant (sens trigonométrique), -1 entrant"""
    def Bf(x, y):
        bx = by = 0.0
        for (px, py, s) in ws:
            dx, dy = x - px, y - py
            r2 = dx * dx + dy * dy + 1e-12
            bx += -s * K * dy / r2
            by += s * K * dx / r2
        return bx, by
    return Bf


def panel(wires, seeds, scale, extra, title, sub, box, cx_=150, cy_=150, hs=7, fr=(0.3, 0.8), extra_seed_fn=None):
    f = Fig(300, 290)
    S = lambda x, y: (cx_ + scale * x, cy_ - scale * y)
    Bf = wires_field(wires)
    inb = lambda x, y: -box[0] <= x <= box[0] and -box[1] <= y <= box[1]
    lines = [fline(Bf, sd, 0.02, inb) for sd in seeds]
    if extra_seed_fn:
        lines = extra_seed_fn(lines)
    draw_lines(f, lines, S, fr, 'fl', 'flh', hs)
    if extra:
        extra(f, S)
    for (px, py, s) in wires:
        f.wire(S(px, py)[0], S(px, py)[1], s > 0, 7.5)
    f.text(150, 21, title, 'tx', 'middle', 14)
    f.text(150, 280, sub, 'tm', 'middle', 12)
    return f


d = 1.0
# a) deux fils, même sens
wa = [(-d / 2, 0, +1), (d / 2, 0, +1)]
seeds_a = [(0.5 + 0.07, 0), (0.5 + 0.14, 0), (0.5 + 0.19, 0), (0.92, 0), (1.1, 0), (1.3, 0)]


def mirror_x_same_sense(ln):
    """miroir x -> -x d'une ligne de champ de deux fils de même sens : le miroir inverse le sens de B (pseudo-vecteur), on inverse donc l'ordre des points"""
    return [(-x, y) for x, y in ln][::-1]


def extra_a(f, S):
    # lemniscate r^2 = 2 c^2 cos 2θ, c = d/2
    c = d / 2
    for lobe in (0, 1):
        ptsl = []
        for k in range(-90, 91):
            t = math.radians(k / 2.0)
            r = c * math.sqrt(2 * math.cos(2 * t))
            ptsl.append(S((1 if lobe == 0 else -1) * r * math.cos(t), r * math.sin(t)))
        f.polyline(ptsl, 'dsh')
    f.circ(*S(0, 0), 3.6, 'ptM')
    f.text(S(0, 0)[0], S(0, 0)[1] + 20, 'B = 0', 'te', 'middle', 12, True)


fa = panel(wa, seeds_a, 82, extra_a, 'a) deux fils, même sens', 'au milieu les deux champs se compensent', (1.78, 1.38),
           extra_seed_fn=lambda ls: ls + [mirror_x_same_sense(l) for l in ls[:3]])
FIG['ex4a'] = fa.svg('Lignes de champ de deux fils parcourus par des courants de même sens', cap('a) Deux courants de même sens (sortants) : lignes circulaires près de chaque fil, ovales englobant les deux fils plus loin, séparées par une courbe en huit passant par le point neutre du milieu où B = 0.'), 330)

# b) deux fils, sens opposés
wb = [(-d / 2, 0, +1), (d / 2, 0, -1)]
seeds_b = [(-0.5 - 0.14, 0), (-0.5 - 0.3, 0), (-0.5 - 0.55, 0), (-0.5 - 0.9, 0), (0.0, 0.0)]


def sym_b(ls):
    """miroir x -> -x (les courants sont aussi permutés et inversés : le sens de parcours est conservé)"""
    return ls + [[(-x, y) for x, y in ln] for ln in ls[:4]]


fb = panel(wb, seeds_b, 82, None, 'b) deux fils, sens opposés', "entre les fils les champs s'ajoutent", (1.78, 1.38),
           extra_seed_fn=sym_b)
FIG['ex4b'] = fb.svg('Lignes de champ de deux fils parcourus par des courants opposés', cap('b) Courants opposés (gauche sortant, droit entrant) : entre les fils les deux champs ont le même sens et s\'ajoutent ; les lignes sont des cercles (non centrés sur les fils) et la médiatrice est une ligne de champ rectiligne.'), 330)

# c) trois fils en triangle équilatéral
rho = 0.55
wc = [(rho * math.cos(math.radians(a)), rho * math.sin(math.radians(a)), +1) for a in (90, 210, 330)]
seeds_c = [(0, rho + 0.07), (0, rho + 0.13), (0, 0.9), (0, 1.1), (0, 1.35)]


def rot(ln, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(c * x - s * y, s * x + c * y) for x, y in ln]


def extra_c(f, S):
    # séparatrice : r = rho (-2 sin 3θ)^(1/3)
    pts = []
    for k in range(0, 3601):
        t = math.radians(k / 10.0)
        v = -2 * math.sin(3 * t)
        if v > 0:
            r = rho * v ** (1 / 3)
            pts.append(S(r * math.cos(t), r * math.sin(t)))
        else:
            if len(pts) > 2:
                f.polyline(pts, 'dsh')
            pts = []
    if len(pts) > 2:
        f.polyline(pts, 'dsh')
    f.circ(*S(0, 0), 3.6, 'ptM')
    f.text(S(0, 0)[0] + 9, S(0, 0)[1] + 4, 'B = 0', 'te', 'start', 12, True)


fc = panel(wc, seeds_c, 74, extra_c, 'c) trois fils, même sens', 'B = 0 au centre du triangle', (1.95, 1.6),
           extra_seed_fn=lambda ls: [r for l in ls for r in (l, rot(l, 120), rot(l, 240))])
FIG['ex4c'] = fc.svg('Lignes de champ de trois fils aux sommets d\'un triangle équilatéral', cap('c) Trois courants de même sens (sortants) : trois lobes circulaires autour des fils, séparés par une courbe à trois boucles ; en dehors, des ovales qui ressemblent de plus en plus à des cercles. Au centre B = 0.'), 330)

# d) fil + champ uniforme
B0 = 1.0
r0 = K / B0


def Bd(x, y):
    r2 = x * x + y * y + 1e-12
    return -K * y / r2 + B0, K * x / r2


def panel_d():
    f = Fig(300, 290)
    sc_ = 46.0
    cx_, cy_ = 150, 160
    S = lambda x, y: (cx_ + sc_ * x, cy_ - sc_ * y)
    inb = lambda x, y: -3.2 <= x <= 3.2 and -2.15 <= y <= 2.75
    seeds = [(-3.1, y) for y in (-1.75, -1.4, -1.0, -0.6, -0.25, 0.1, 0.5, 1.0, 1.6, 2.15, 2.45, 2.7)]
    lines = [fline(Bd, sd, 0.03, inb) for sd in seeds]
    inner = [fline(Bd, (x, 0.0), 0.012, inb) for x in (0.12, 0.2, 0.28)]
    draw_lines(f, lines, S, (0.15, 0.75), 'fl', 'flh', 7)
    draw_lines(f, inner, S, (0.3,), 'fl', 'flh', 6)
    # séparatrice (A = cste passant par le point neutre) : r sin θ = 1 + ln r ; d'abord la boucle fermée (œuf)
    egg = []
    for k in range(0, 401):
        r = 0.2784 + (1.0 - 0.2784) * k / 400.0
        s_ = (1 + math.log(r)) / r
        s_ = max(-1.0, min(1.0, s_))
        th = math.asin(s_)
        egg.append((r * math.cos(th), r * math.sin(th)))
    loop = egg + [(-x, y) for x, y in egg[::-1]]
    f.polyline([S(x, y) for x, y in loop], 'dsh')
    for sgn_ in (1, -1):
        br = []
        for k in range(0, 400):
            r = 1.0 + (3.9 - 1.0) * k / 399.0
            s_ = (1 + math.log(r)) / r
            th = math.asin(min(1.0, s_))
            x, y = r * math.cos(th), r * math.sin(th)
            if abs(x) > 3.2 or y > 2.75:
                break
            br.append(S(sgn_ * x, y))
        f.polyline(br, 'dsh')
    f.wire(S(0, 0)[0], S(0, 0)[1], True, 7.5)
    f.circ(*S(0, r0), 3.8, 'ptM')
    f.text(S(0, r0)[0] + 9, S(0, r0)[1] - 9, 'B = 0 en r[0]', 'te', 'start', 12, True)
    f.text(S(0, r0)[0] + 9, S(0, r0)[1] + 5, 'r[0] = μ[0]I/(2πB[0])', 'te', 'start', 11, True)
    f.arrow(12, 280, 56, 280, 'bl', 'blh', 7)
    f.text(62, 284, 'B[0] uniforme', 'tc', 'start', 12)
    f.text(150, 21, 'd) fil + champ uniforme', 'tx', 'middle', 14)
    return f


fd = panel_d()
FIG['ex4d'] = fd.svg('Lignes de champ d\'un fil dans un champ uniforme perpendiculaire', cap('d) Fil (courant sortant) dans un champ uniforme B[0] vers la droite : au-dessus du fil le champ du fil s\'oppose à B[0], d\'où un point d\'arrêt à la distance r[0] = μ[0]I/(2πB[0]) ; la courbe en pointillés (séparatrice) délimite les lignes qui entourent le fil.'), 330)

# ---------------------------------------------------------------- Ex 5 : solénoïde infini
f = Fig(580, 300)
xl, xr = 120, 300
ytop, ybot = 30, 270
f.line(xl, ytop, xl, ybot, 'ob')
f.line(xr, ytop, xr, ybot, 'ob')
for y in range(ytop + 12, ybot - 6, 20):
    f.wire(xl, y, True, 5.6)
    f.wire(xr, y, False, 5.6)
f.text((xl + xr) / 2, ytop - 6, 'solénoïde (n spires par mètre)', 'tm', 'middle', 12)
f.arrow(30, ybot + 14, 30, ytop + 10, 'ax', 'axh', 7)
f.text(38, ytop + 18, 'z', 'tm', 'start', 14)
for xb in (170, 210, 250):
    f.arrow(xb, 92, xb, 46, 'bl', 'blh', 7)
    f.arrow(xb, 262, xb, 220, 'bl', 'blh', 7)
f.text((xl + xr) / 2, 108, 'B = μ[0] n I e[z]', 'tc', 'middle', 14)
# contours d'Ampère (vers le haut côté intérieur, vers le bas côté extérieur)
def amp(f, x1, x2, y1, y2, lab, lx, ly):
    f.add('<rect class="gsl" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (x1, y1, x2 - x1, y2 - y1))
    ym = (y1 + y2) / 2
    f.head(x1, ym - 4, 0, -1, 'gsah', 8)
    f.head(x2, ym + 4, 0, 1, 'gsah', 8)
    f.text(lx, ly, lab, 'tg', 'middle', 13)


amp(f, 145, 215, 150, 200, 'C[1]', 180, 220)
amp(f, 250, 360, 150, 200, 'C[2]', 340, 220)
amp(f, 392, 452, 150, 200, 'C[3]', 422, 220)
f.text(420, 60, 'à l\'extérieur : B = 0', 'tc', 'middle', 14)
f.text(420, 80, '(B ne dépend que de r,', 'tm', 'middle', 12)
f.text(420, 96, 'tend vers 0 à l\'infini)', 'tm', 'middle', 12)
f.text(525, 250, 'sens du courant :', 'tm', 'end', 12)
f.text(525, 266, '⊙ à gauche, ⊗ à droite', 'tm', 'end', 12)
FIG['ex5'] = f.svg('Solénoïde infini en coupe et contours d\'Ampère', cap('Coupe d\'un solénoïde infini par un plan contenant l\'axe (courant sortant à gauche, entrant à droite : B vers le haut). C[1] et C[3] n\'enlacent aucun courant ; C[2], de longueur ℓ, enlace nℓ spires : μ[0]nℓI.'), 580)

# ---------------------------------------------------------------- Ex 6 : cylindre plein
f = Fig(580, 280)
cx, cy = 130, 140
Rr = 68
f.circ(cx, cy, Rr, 'qp')
for k in range(4):
    a = math.radians(90 * k + 45)
    f.circ(cx + 17 * math.cos(a), cy - 17 * math.sin(a), 2.2, 'pt')
for k in range(12):
    a = math.radians(30 * k + 15)
    f.circ(cx + 55 * math.cos(a), cy - 55 * math.sin(a), 2.2, 'pt')
f.circ(cx, cy, 36, 'gsl')
f.circ(cx, cy, 110, 'gsl')
circle_arrows(f, cx, cy, 36, (30, 150, 270), +1, 'gsah', 8)
circle_arrows(f, cx, cy, 110, (45, 165, 285), +1, 'gsah', 8)
f.line(cx, cy, cx + Rr * math.cos(math.radians(-60)), cy - Rr * math.sin(math.radians(-60)), 'dsh')
f.text(cx + 30, cy + 42, 'R', 'tx', 'start', 13)
f.text(cx + 27, cy - 30, 'C', 'tg', 'start', 13, True)
f.text(cx + 96, cy - 100, 'C′', 'tg', 'start', 13)
f.text(cx, 268, 'vue de dessus : j sortant (⊙), I selon e[z]', 'tm', 'middle', 12)
# graphe B(r)
gx, gy = 300, 230
f.arrow(gx, gy, 565, gy, 'ax', 'axh', 7)
f.arrow(gx, gy, gx, 40, 'ax', 'axh', 7)
f.text(566, gy + 17, 'r', 'tm', 'end', 14)
f.text(gx + 10, 46, 'B(r)', 'tm', 'start', 14)
xr_ = lambda r: gx + 95 * r  # r en unités de R
hB = 150.0
pts = [(xr_(r), gy - hB * r) for r in (0, 1.0)]
f.polyline(pts, 'cv1')
hy = [(xr_(r), gy - hB / r) for r in [1.0 + 0.04 * k for k in range(0, 48)]]
f.polyline(hy, 'cv1')
f.line(xr_(1.0), gy, xr_(1.0), gy - hB, 'dsh')
f.text(xr_(1.0), gy + 17, 'R', 'tx', 'middle', 13)
f.text(xr_(1.0) - 6, gy - hB - 8, 'μ[0]I/(2πR)', 'tx', 'end', 12)
f.text(gx + 58, gy - 108, '∝ r', 'tc', 'end', 13)
f.text(xr_(2.6), gy - hB / 2.6 - 16, 'μ[0]I/(2πr)', 'tc', 'middle', 12)
FIG['ex6'] = f.svg('Cylindre plein parcouru par un courant uniforme : contours d\'Ampère et courbe B(r)', cap('Fil cylindrique de rayon R, j uniforme sortant. Contours d\'Ampère circulaires C (r inférieur à R) et C′ (r supérieur à R). À droite : B croît linéairement jusqu\'à R puis décroît en 1/r ; la courbe est continue en r = R.'), 580)

# ---------------------------------------------------------------- Ex 7 : câble coaxial
f = Fig(600, 300)
cx, cy = 130, 150
R1_, R2_, R3_ = 34, 70, 104
dpath = ('M%.1f %.1f A %d %d 0 1 0 %.1f %.1f A %d %d 0 1 0 %.1f %.1f Z M%.1f %.1f A %d %d 0 1 1 %.1f %.1f A %d %d 0 1 1 %.1f %.1f Z'
         % (cx + R3_, cy, R3_, R3_, cx - R3_, cy, R3_, R3_, cx + R3_, cy, cx + R2_, cy, R2_, R2_, cx - R2_, cy, R2_, R2_, cx + R2_, cy))
f.path(dpath, 'qn')
f.circ(cx, cy, R3_, 'ob')
f.circ(cx, cy, R2_, 'ob')
f.circ(cx, cy, R1_, 'qp')
f.circ(cx, cy, R1_, 'ob')
f.text(cx, cy + 5, '⊙', 'tc', 'middle', 13)
f.text(cx + 87, cy + 4, '⊗', 'te', 'middle', 14)
f.text(cx - 87, cy + 4, '⊗', 'te', 'middle', 14)
for rr in (20, 52, 87, 120):
    f.circ(cx, cy, rr, 'gsl')
    circle_arrows(f, cx, cy, rr, (40,), +1, 'gsah', 7)
for rr, nm in ((20, 'C[a]'), (52, 'C[b]'), (87, 'C[c]'), (120, 'C[d]')):
    f.text(cx + (rr + 2) * math.cos(math.radians(70)), cy - (rr + 2) * math.sin(math.radians(70)) - 1, nm, 'tg', 'start', 12, True)
f.line(cx, cy, cx + R1_ * math.cos(math.radians(-55)), cy - R1_ * math.sin(math.radians(-55)), 'dsh')
f.line(cx, cy, cx + R2_ * math.cos(math.radians(-110)), cy - R2_ * math.sin(math.radians(-110)), 'dsh')
f.line(cx, cy, cx + R3_ * math.cos(math.radians(-150)), cy - R3_ * math.sin(math.radians(-150)), 'dsh')
f.text(cx + 14, cy + 30, 'R[1]', 'tx', 'start', 12)
f.text(cx - 40, cy + 60, 'R[2]', 'tx', 'end', 12)
f.text(cx - 94, cy + 62, 'R[3]', 'tx', 'end', 12)
f.text(cx, 286, 'R[1] \u003c R[2] \u003c R[3] (lecture du schéma)', 'tm', 'middle', 12)
gx, gy = 310, 240
f.arrow(gx, gy, 590, gy, 'ax', 'axh', 7)
f.arrow(gx, gy, gx, 40, 'ax', 'axh', 7)
f.text(591, gy + 17, 'r', 'tm', 'end', 14)
f.text(gx + 10, 46, 'B(r)', 'tm', 'start', 14)
xr_ = lambda r: gx + 1.95 * r
Hc = 4400.0
pa = [(xr_(r), gy - Hc / R1_ ** 2 * r) for r in (0, R1_)]
pb = [(xr_(r), gy - Hc / r) for r in [R1_ + (R2_ - R1_) * k / 30 for k in range(31)]]
pc = [(xr_(r), gy - Hc / r * (R3_ ** 2 - r ** 2) / (R3_ ** 2 - R2_ ** 2)) for r in [R2_ + (R3_ - R2_) * k / 30 for k in range(31)]]
f.polyline(pa + pb[1:] + pc[1:], 'cv1')
f.line(xr_(R3_), gy, xr_(R3_ + 60), gy, 'cv1')
for r, nm in ((R1_, 'R[1]'), (R2_, 'R[2]'), (R3_, 'R[3]')):
    f.line(xr_(r), gy + 3, xr_(r), gy - 3, 'ax')
    f.text(xr_(r), gy + 17, nm, 'tx', 'middle', 12)
f.line(xr_(R1_), gy, xr_(R1_), gy - Hc / R1_, 'dsh')
f.line(xr_(R2_), gy, xr_(R2_), gy - Hc / R2_, 'dsh')
f.text(xr_(R1_) - 6, gy - Hc / R1_ - 9, 'μ[0]I/(2πR[1])', 'tx', 'end', 12)
f.text(xr_(88), gy - Hc / 88 - 24, '∝ 1/r', 'tc', 'start', 12)
f.text(xr_(R3_ - 4), gy - 34, 'décroît jusqu\'à 0', 'tc', 'start', 12)
f.text(xr_(R3_ + 32), gy - 10, 'B = 0', 'tc', 'start', 12)
FIG['ex7'] = f.svg('Câble coaxial : contours d\'Ampère et courbe B(r)', cap('Câble coaxial (courant I sortant dans le cœur, retour entrant dans la gaine). Quatre contours d\'Ampère C[a] à C[d]. À droite : B(r) est continue ; elle croît dans le cœur, décroît en 1/r dans le vide, décroît jusqu\'à 0 dans la gaine, puis reste nulle (le câble ne rayonne pas).'), 600)

# ---------------------------------------------------------------- Ex 8 : tore à section rectangulaire
f = Fig(620, 305)
cx, cy = 132, 150
ri, ro = 50, 100
dpath = ('M%.1f %.1f A %d %d 0 1 0 %.1f %.1f A %d %d 0 1 0 %.1f %.1f Z M%.1f %.1f A %d %d 0 1 1 %.1f %.1f A %d %d 0 1 1 %.1f %.1f Z'
         % (cx + ro, cy, ro, ro, cx - ro, cy, ro, ro, cx + ro, cy, cx + ri, cy, ri, ri, cx - ri, cy, ri, ri, cx + ri, cy))
f.path(dpath, 'qg')
f.circ(cx, cy, ro, 'ob')
f.circ(cx, cy, ri, 'ob')
S8 = lambda x, y: (cx + y, cy + x)  # x vers le bas, y vers la droite


def pol(r, th):
    t = math.radians(th)
    return S8(r * math.cos(t), r * math.sin(t))


for k in range(24):
    a = pol(ri, 15 * k)
    b = pol(ro, 15 * k)
    f.line(a[0], a[1], b[0], b[1], 'ob2')
for k in range(8):
    th = 7.5 + 45 * k
    a = pol(ro - 6, th)
    b = pol(ri + 6, th)
    f.arrow(a[0], a[1], b[0], b[1], 'ef', 'efh', 6)
# contour d'Ampère r = 75 (sens e_theta) et lignes de B (sens opposé)
rm = 75
f.circ(cx, cy, rm, 'gsl')
for th in (10, 100, 190, 280):
    t = math.radians(th)
    # e_theta en coordonnées écran : (x,y)=(−sinθ, cosθ) -> écran (dx,dy) = (y, x) = (cosθ, −sinθ)
    p = pol(rm, th)
    dx, dy = math.cos(t), -math.sin(t)
    f.head(p[0] + dx * 4, p[1] + dy * 4, dx, dy, 'gsah', 8)
rb = 62
f.circ(cx, cy, rb, 'fl')
for th in (55, 145, 235, 325):
    t = math.radians(th)
    p = pol(rb, th)
    dx, dy = -math.cos(t), math.sin(t)
    f.head(p[0] + dx * 4, p[1] + dy * 4, dx, dy, 'flh', 8)
f.circ(cx, cy, 5, 'ob', 'fill:var(--surface)')
f.add('<circle class="pt" cx="%.1f" cy="%.1f" r="1.8"/>' % (cx, cy))
f.arrow(cx, cy, cx, cy + 128, 'ax', 'axh', 7)
f.text(cx - 8, cy + 134, 'x', 'tm', 'end', 14)
f.arrow(cx, cy, cx + 128, cy, 'ax', 'axh', 7)
f.text(cx + 130, cy - 8, 'y', 'tm', 'end', 14)
f.text(cx + 8, cy - 8, 'z', 'tm', 'start', 13)
pp = pol(90, 40)
f.circ(pp[0], pp[1], 3, 'pt')
f.text(pp[0] - 8, pp[1] + 4, 'P', 'tx', 'end', 13)
t = math.radians(40)
f.arrow(pp[0], pp[1], pp[0] + 34 * math.sin(t), pp[1] + 34 * math.cos(t), 'ax', 'axh', 6)
f.text(pp[0] + 38 * math.sin(t) - 2, pp[1] + 38 * math.cos(t) + 10, 'e[r]', 'tx', 'start', 13, True)
f.arrow(pp[0], pp[1], pp[0] + 34 * math.cos(t), pp[1] - 34 * math.sin(t), 'ax', 'axh', 6)
f.text(pp[0] + 38 * math.cos(t) + 4, pp[1] - 34 * math.sin(t) - 4, 'e[θ]', 'tx', 'start', 13, True)
f.polyline([pol(28, th) for th in range(0, 41, 4)], 'ac')
f.text(pol(36, 20)[0] + 4, pol(36, 20)[1] - 0, 'θ', 'tc', 'start', 13)
f.text(cx, 295, 'vue de dessus', 'tm', 'middle', 12)
# coupe
zx, zy = 440, 150
f.arrow(zx, zy + 88, zx, 36, 'ax', 'axh', 7)
f.text(zx + 8, 44, 'z', 'tm', 'start', 14)
f.arrow(zx - 130, zy, zx + 150, zy, 'ax', 'axh', 7)
f.text(zx + 152, zy + 16, 'y', 'tm', 'end', 14)
Ro_, aw, bh = 80, 50, 62
for sg in (1, -1):
    xc = zx + sg * Ro_
    f.rect(xc - aw / 2, zy - bh / 2, aw, bh, 'qg')
    # courants : extérieur vers le haut, intérieur vers le bas
    xo, xi = xc + sg * aw / 2, xc - sg * aw / 2
    f.arrow(xo, zy + 16, xo, zy - 16, 'ef', 'efh', 7)
    f.arrow(xi, zy - 16, xi, zy + 16, 'ef', 'efh', 7)
    # champ B : sortant à droite, entrant à gauche
    f.circ(xc, zy, 9, 'ac')
    if sg == 1:
        f.add('<circle class="blh" cx="%.1f" cy="%.1f" r="2.4"/>' % (xc, zy))
    else:
        d_ = 5.2
        f.line(xc - d_, zy - d_, xc + d_, zy + d_, 'ac')
        f.line(xc - d_, zy + d_, xc + d_, zy - d_, 'ac')
xc = zx + Ro_
f.arrow(xc - aw / 2, zy - bh / 2 - 12, xc + aw / 2, zy - bh / 2 - 12, 'dsh', 'efh', 5)
f.arrow(xc + aw / 2, zy - bh / 2 - 12, xc - aw / 2, zy - bh / 2 - 12, 'dsh', 'efh', 5)
f.text(xc, zy - bh / 2 - 18, 'a', 'tx', 'middle', 13)
f.arrow(xc + aw / 2 + 14, zy + bh / 2, xc + aw / 2 + 14, zy - bh / 2, 'dsh', 'efh', 5)
f.arrow(xc + aw / 2 + 14, zy - bh / 2, xc + aw / 2 + 14, zy + bh / 2, 'dsh', 'efh', 5)
f.text(xc + aw / 2 + 22, zy - 14, 'b', 'tx', 'start', 13)
f.arrow(zx, zy + 40, xc, zy + 40, 'dsh', 'efh', 5)
f.arrow(xc, zy + 40, zx, zy + 40, 'dsh', 'efh', 5)
f.text((zx + xc) / 2, zy + 56, 'R[0]', 'tx', 'middle', 13)
f.text(zx - 5, 280, 'coupe par le plan x = 0 : à droite e[θ] est entrant, donc B = −B e[θ] est sortant', 'tm', 'middle', 12)
FIG['ex8'] = f.svg('Tore de section rectangulaire : vue de dessus et vue en coupe', cap('Tore de rayon moyen R[0], de section a × b, bobiné de N[1] spires (courant I[1] : montant sur la paroi extérieure, descendant sur la paroi intérieure, entrant vers l\'axe sur la face supérieure). En vert, contour d\'Ampère de rayon r orienté selon e[θ] ; en bleu, le champ B, orienté en sens inverse (B[θ] \u003c 0).'), 620)

# ---------------------------------------------------------------- Ex 9 : effet Hall
f = Fig(560, 330)
ox, oy = 280, 190
V = lambda x, y, z: (ox + x + 0.6 * y, oy - z - 0.42 * y)
X1, Y1, Z1 = 120, 62, 24
front = [V(-X1, -Y1, Z1), V(X1, -Y1, Z1), V(X1, -Y1, -Z1), V(-X1, -Y1, -Z1)]
right = [V(X1, -Y1, Z1), V(X1, Y1, Z1), V(X1, Y1, -Z1), V(X1, -Y1, -Z1)]
top = [V(-X1, -Y1, Z1), V(X1, -Y1, Z1), V(X1, Y1, Z1), V(-X1, Y1, Z1)]
for a_, b_ in ((V(-X1, Y1, -Z1), V(-X1, Y1, Z1)), (V(-X1, Y1, -Z1), V(X1, Y1, -Z1)), (V(-X1, Y1, -Z1), V(-X1, -Y1, -Z1))):
    f.line(a_[0], a_[1], b_[0], b_[1], 'hid')
f.poly(front, 'box')
f.poly(right, 'box')
f.poly(top, 'boxb')
for face in (front, right, top):
    f.polyline(face + [face[0]], 'ob')
# courant I
a_, b_ = V(-X1 - 62, 0, 0), V(-X1 - 4, 0, 0)
f.arrow(a_[0], a_[1], b_[0], b_[1], 'ef', 'efh', 8)
f.text(a_[0] + 10, a_[1] - 12, 'I', 'te', 'middle', 15)
a_, b_ = V(X1 + 6, 0, 0), V(X1 + 64, 0, 0)
f.arrow(a_[0], a_[1], b_[0], b_[1], 'ef', 'efh', 8)
f.text(b_[0] - 8, b_[1] - 12, 'I', 'te', 'middle', 15)
# B vers le haut
a_ = V(0, 0, Z1)
f.arrow(a_[0], a_[1], a_[0], a_[1] - 74, 'bl', 'blh', 9)
f.text(a_[0] + 12, a_[1] - 62, 'B', 'tc', 'start', 16)
# signes de charge
for x in (-90, -50, 50, 90):
    p = V(x, Y1 - 10, Z1)
    f.text(p[0], p[1] + 4, '+', 'tc', 'middle', 14)
    p = V(x, -Y1 + 11, Z1)
    f.text(p[0], p[1] + 4, '−', 'te', 'middle', 14)
p1 = V(0, Y1 - 24, Z1)
p1p = V(0, -Y1 + 25, Z1)
f.circ(p1[0], p1[1], 3, 'pt')
f.text(p1[0] + 8, p1[1] + 1, '1', 'tx', 'start', 13)
f.circ(p1p[0], p1p[1], 3, 'pt')
f.text(p1p[0] + 8, p1p[1] + 14, '1′', 'tx', 'start', 13)
# E_H de 1 vers 1'
ea = V(-70, Y1 - 24, Z1)
eb = V(-70, -Y1 + 25, Z1)
f.arrow(ea[0], ea[1], eb[0], eb[1], 'ef', 'efh', 8)
f.text(ea[0] - 12, ea[1] + 16, 'E[H]', 'te', 'end', 14)
# électron, vitesse, force magnétique
pe = V(75, 6, Z1)
f.circ(pe[0], pe[1], 6.5, 'qn')
f.text(pe[0], pe[1] + 4, '−', 'te', 'middle', 11)
f.arrow(pe[0] - 8, pe[1], pe[0] - 52, pe[1], 'gsa', 'gsah', 7)
f.text(pe[0] - 30, pe[1] - 8, 'v', 'tg', 'middle', 13)
fa_ = (pe[0] - 5, pe[1] + 6)
fb_ = (fa_[0] - 0.6 * 44, fa_[1] + 0.42 * 44)
f.arrow(fa_[0], fa_[1], fb_[0], fb_[1], 'gsa', 'gsah', 7)
f.text(fb_[0] + 4, fb_[1] + 15, 'F[m]', 'tg', 'start', 13)
# repère
o3 = (60, 292)
f.arrow(o3[0], o3[1], o3[0] + 42, o3[1], 'ax', 'axh', 6)
f.text(o3[0] + 48, o3[1] + 4, 'x', 'tm', 'start', 13)
f.arrow(o3[0], o3[1], o3[0] + 0.6 * 42, o3[1] - 0.42 * 42, 'ax', 'axh', 6)
f.text(o3[0] + 0.6 * 42 + 5, o3[1] - 0.42 * 42 - 3, 'y', 'tm', 'start', 13)
f.arrow(o3[0], o3[1], o3[0], o3[1] - 44, 'ax', 'axh', 6)
f.text(o3[0] + 6, o3[1] - 44, 'z', 'tm', 'start', 13)
f.text(ox + 150, 260, 'v = −(j/ne) e[x],   F[m] = −e v ∧ B = −(jB/n) e[y]', 'tm', 'middle', 12)
f.text(ox + 150, 280, 'E[H] = −(jB/ne) e[y],   U[H] = V(1) − V(1′) = IB/(neh)', 'tm', 'middle', 12)
f.text(ox + 150, 300, 'face 1 (y = +b/2) positive, face 1′ (y = −b/2) négative', 'tm', 'middle', 12)
FIG['ex9'] = f.svg('Plaque semi-conductrice de type N dans un champ magnétique : effet Hall', cap('Plaque de type N : le courant I est selon +e[x], donc les électrons dérivent selon −e[x] (vitesse v). Dans B selon +e[z], la force magnétique F[m] = −e v ∧ B pousse les électrons vers la face 1′ (y = −b/2) : charge négative en 1′, positive en 1, d\'où un champ de Hall E[H] dirigé de 1 vers 1′.'), 560)

# =============================================================== utilitaires HTML
def mq(s):
    return '<div class="mq">\\[' + s.replace('&', '&amp;') + '\\]</div>'


def steps(lst):
    out = ['<ol class="steps">']
    for t, body in lst:
        out.append('<li class="step"><span class="sn"></span><div><div class="st">%s</div><div class="sd">\n%s</div></div></li>' % (t, body))
    out.append('</ol>')
    return '\n'.join(out)


def exo(ident, num, titre, tag, enonce, meth, stp, rep, piege, fig=''):
    return ('<article class="cx" id="%s">\n<header class="cx-hd"><span class="cx-num">Ex \\(%s\\)</span><h3>%s</h3><span class="cx-tag %s">%s</span></header>\n'
            '<div class="cx-enonce">%s</div>\n%s'
            '<details class="cx-meth"><summary>💡 Méthode et raisonnement</summary><div>\n%s</div></details>\n'
            '<details class="cx-corr"><summary>✅ Correction détaillée</summary><div>\n%s\n'
            '<div class="answer"><b class="lab">Réponse</b>%s</div>\n<div class="why"><b class="lab">Piège</b>%s</div>\n</div></details>\n</article>'
            % (ident, num, titre, 'td' if tag == 'TD' else 'es', tag, enonce, fig, meth, steps(stp), rep, piege))


TD5 = []

# =============================================================== Ex 1
TD5.append(exo('td5-1', '1', 'Champ magnétique d\'un courant angulaire', 'TD',
    r"Un fil de longueur infinie est courbé à angle droit en \(O\) ; il est parcouru par un courant d'intensité \(I\) (qui monte le long de la branche verticale puis repart vers la gauche le long de la branche horizontale). Le point \(M\) est sur le prolongement de la branche horizontale, à la distance \(a\) de \(O\). 1) Déterminer le champ magnétique élémentaire créé en \(M\) par un élément de circuit de longueur \(\mathrm{d}l\). 2) En déduire le champ magnétique total créé en \(M\).",
    r"<p>Le fil est un <b>courant filiforme</b> : on utilise la <b>loi de Biot et Savart</b> \(\mathrm{d}\vec B=\dfrac{\mu_0}{4\pi}\dfrac{I\,\mathrm{d}\vec l\wedge\overrightarrow{PM}}{PM^3}\), où \(P\) est le point courant du fil, \(\mathrm{d}\vec l\) l'élément de fil orienté dans le sens du courant et \(\overrightarrow{PM}\) le vecteur de \(P\) vers \(M\).</p>"
    r"<p>On coupe le fil en deux <b>demi-droites</b> et on regarde chacune : si \(\mathrm{d}\vec l\) est <b>parallèle</b> à \(\overrightarrow{PM}\), le produit vectoriel est nul et la branche ne contribue pas. Sinon, on prend comme variable d'intégration l'<b>angle</b> sous lequel on voit le fil depuis \(M\). Le sens de \(\vec B\) se lit à la règle du <b>tire-bouchon</b> : le trièdre \((\mathrm{d}\vec l,\overrightarrow{PM},\mathrm{d}\vec B)\) est direct.</p>",
    [("Repère et description du fil",
      r"<p>Axes : \(x\) vers la droite, \(y\) vers le haut, \(z\) <b>sortant</b> de la page (repère direct). \(M=(a,0,0)\), \(O\) à l'origine. Le courant arrive en \(O\) par le bas (\(\mathrm{d}\vec l\parallel+\vec e_y\)) et repart vers la gauche (\(\mathrm{d}\vec l\parallel-\vec e_x\)) : la continuité du courant impose ce sens sur la branche horizontale." + FIG['ex1']),
     ("Champ élémentaire, branche horizontale (question 1)",
      r"<p>Un point \(P=(x',0,0)\) avec \(x'\lt0\) : \(\overrightarrow{PM}=(a-x')\,\vec e_x\) est <b>colinéaire</b> à \(\mathrm{d}\vec l\). Donc</p>" + mq(r"\mathrm{d}\vec l\wedge\overrightarrow{PM}=\vec0\ \Longrightarrow\ \mathrm{d}\vec B=\vec0") + r"<p>M est sur le prolongement de cette branche : elle ne crée aucun champ en \(M\).</p>"),
     ("Champ élémentaire, branche verticale (question 1)",
      r"<p>\(P=(0,y',0)\) avec \(y'\in\,]-\infty,0]\), \(\mathrm{d}\vec l=\mathrm{d}y'\,\vec e_y\), \(\overrightarrow{PM}=a\,\vec e_x-y'\,\vec e_y\), \(PM=\sqrt{a^2+y'^2}\). Comme \(\vec e_y\wedge\vec e_x=-\vec e_z\) et \(\vec e_y\wedge\vec e_y=\vec0\) :</p>"
      + mq(r"\mathrm{d}\vec B=\frac{\mu_0I}{4\pi}\,\frac{\mathrm{d}y'\;a\,(\vec e_y\wedge\vec e_x)}{(a^2+y'^2)^{3/2}}=-\frac{\mu_0I\,a\,\mathrm{d}y'}{4\pi\,(a^2+y'^2)^{3/2}}\,\vec e_z")),
     ("Intégration (question 2)",
      r"<p>On intègre de \(y'=-\infty\) à \(y'=0\). Changement de variable avec l'angle \(\alpha=(\overrightarrow{MO},\overrightarrow{MP})\) : \(y'=-a\tan\alpha\), \(PM=\dfrac{a}{\cos\alpha}\), \(|\mathrm{d}y'|=\dfrac{a\,\mathrm{d}\alpha}{\cos^2\alpha}\), \(\alpha\) allant de \(0\) à \(\frac\pi2\) :</p>"
      + mq(r"\int_{-\infty}^{0}\frac{\mathrm{d}y'}{(a^2+y'^2)^{3/2}}=\int_0^{\pi/2}\frac{a\,\mathrm{d}\alpha/\cos^2\alpha}{a^3/\cos^3\alpha}=\frac1{a^2}\int_0^{\pi/2}\cos\alpha\,\mathrm{d}\alpha=\frac1{a^2}")
      + r"<p>Donc, en ajoutant la branche horizontale (nulle) :</p>" + mq(r"\vec B(M)=-\frac{\mu_0I\,a}{4\pi}\cdot\frac1{a^2}\,\vec e_z=-\frac{\mu_0I}{4\pi a}\,\vec e_z")),
     ("Sens et ordre de grandeur",
      r"<p>Tire-bouchon : \((\mathrm{d}\vec l,\overrightarrow{PM},\mathrm{d}\vec B)\approx(\vec e_y,\vec e_x,-\vec e_z)\) est direct : \(\vec B\) est <b>entrant</b> dans la page (croix sur la figure). Le module \(\dfrac{\mu_0I}{4\pi a}\) est la <b>moitié</b> du champ d'un fil infini \(\dfrac{\mu_0I}{2\pi a}\) : un fil semi-infini, dont le pied de la perpendiculaire passant par \(M\) est son extrémité, donne la moitié. Pour \(I=10\ \mathrm{A}\) et \(a=5\ \mathrm{cm}\) : \(B=\dfrac{10^{-7}\times10}{0{,}05}=2\times10^{-5}\ \mathrm{T}\).</p>")],
    r"1) Branche horizontale : \(\mathrm{d}\vec B=\vec0\) ; branche verticale : \(\mathrm{d}\vec B=-\dfrac{\mu_0Ia\,\mathrm{d}y'}{4\pi(a^2+y'^2)^{3/2}}\vec e_z\). 2) \(\vec B(M)=-\dfrac{\mu_0I}{4\pi a}\,\vec e_z\) : module \(\dfrac{\mu_0I}{4\pi a}\), sens <b>entrant</b>.",
    r"Ne pas oublier de regarder si \(\mathrm{d}\vec l\parallel\overrightarrow{PM}\) : la branche horizontale ne compte pas. Et la demi-droite verticale donne la <em>moitié</em> d'un fil infini (bornes \(0\) et \(\frac\pi2\) pour \(\alpha\), pas \(-\frac\pi2\) et \(\frac\pi2\))."))

# =============================================================== Ex 2
TD5.append(exo('td5-2', '2', 'Champ créé par quatre fils infinis', 'TD',
    r"Quatre fils infinis parallèles forment, dans un plan perpendiculaire, les sommets d'un carré de côté \(2b\). Ils sont parcourus par le même courant \(I\), dans le sens <b>entrant</b> dans la page (figure de l'énoncé). 1) Donner (résultat du cours) le champ magnétique d'un fil infini. 2) Déterminer le champ au centre \(O\) du carré par le calcul, et vérifier par les arguments de symétrie.",
    r"<p>Principe de <b>superposition</b> : le champ total est la somme des champs des quatre fils, chacun connu (fil infini). Pour chaque fil, il faut le <b>module</b> (distance \(b\sqrt2\) au centre) et la <b>direction/sens</b> : le champ est perpendiculaire au plan \((\text{fil},O)\), donc à la diagonale, et tourne autour du fil dans le sens du tire-bouchon.</p>"
    r"<p>Pour la vérification, on utilise les symétries <b>de \(\vec B\)</b>, inversées par rapport à celles de \(\vec E\) : <em>plan de symétrie des courants \(\Rightarrow\) \(\vec B\) orthogonal au plan</em> ; <em>plan d'antisymétrie \(\Rightarrow\) \(\vec B\) contenu dans le plan</em>.</p>",
    [("Fil infini (question 1)",
      r"<p>Pour un fil d'axe \(Oz\) parcouru par \(I\) dans le sens de \(+\vec e_z\), en coordonnées cylindriques d'axe le fil :</p>" + mq(r"\vec B(M)=\frac{\mu_0I}{2\pi r}\,\vec e_\theta") + r"<p>où \(r\) est la distance au fil. Ici le courant est <b>entrant</b> (selon \(-\vec e_z\)) : le sens de rotation s'inverse (sens horaire vu du dessus).</p>"),
     ("Un fil : module et direction (question 2)",
      r"<p>Repère \(x\) à droite, \(y\) en haut, \(z\) sortant ; le fil \(k\) est en \(P_k=(s_xb,\,s_yb)\) avec \(s_x,s_y=\pm1\). Distance au centre \(P_kO=b\sqrt2\) et, avec \(\vec u=-\vec e_z\) (sens du courant) :</p>"
      + mq(r"\vec B_k(O)=\frac{\mu_0I}{2\pi}\,\frac{\vec u\wedge\overrightarrow{P_kO}}{P_kO^2}=\frac{\mu_0I}{2\pi}\,\frac{(-\vec e_z)\wedge\big(-b\,(s_x\vec e_x+s_y\vec e_y)\big)}{2b^2}=\frac{\mu_0I}{4\pi b}\,\big(-s_y\,\vec e_x+s_x\,\vec e_y\big)")
      + r"<p>Module : \(\dfrac{\mu_0I}{4\pi b}\sqrt2=\dfrac{\mu_0I}{2\pi\,b\sqrt2}\), le même pour les quatre fils.</p>" + FIG['ex2']),
     ("Somme (question 2)",
      mq(r"\begin{array}{ll}\text{fil }1\ (+,+):&\dfrac{\mu_0I}{4\pi b}(-\vec e_x+\vec e_y)\\[6pt]\text{fil }2\ (-,+):&\dfrac{\mu_0I}{4\pi b}(-\vec e_x-\vec e_y)\\[6pt]\text{fil }3\ (-,-):&\dfrac{\mu_0I}{4\pi b}(+\vec e_x-\vec e_y)\\[6pt]\text{fil }4\ (+,-):&\dfrac{\mu_0I}{4\pi b}(+\vec e_x+\vec e_y)\end{array}")
      + mq(r"\vec B(O)=\vec B_1+\vec B_2+\vec B_3+\vec B_4=\vec0")
      + r"<p>Les fils diagonalement opposés (1 et 3, 2 et 4) créent des champs <b>opposés</b> de même module : ils se compensent deux à deux.</p>"),
     ("Vérification par symétrie",
      r"<p>Le plan \(x=0\) est un plan de <b>symétrie des courants</b> (il échange les fils 1 et 2, 3 et 4, qui portent le même courant) : en \(O\), \(\vec B\) est <b>orthogonal</b> à ce plan, donc selon \(\vec e_x\). De même le plan \(y=0\) est un plan de symétrie : \(\vec B(O)\parallel\vec e_y\). Un vecteur à la fois parallèle à \(\vec e_x\) et à \(\vec e_y\) est nul : \(\vec B(O)=\vec0\). (Les plans diagonaux le confirment.) Le plan \(z=0\), perpendiculaire aux fils, est un plan d'antisymétrie : \(\vec B\) y est contenu, \(B_z=0\), en accord avec le calcul.</p>")],
    r"\(\vec B_{\text{fil}}=\dfrac{\mu_0I}{2\pi r}\vec e_\theta\) ; chaque fil donne en \(O\) un champ de module \(\dfrac{\mu_0I}{2\pi b\sqrt2}\), perpendiculaire à la diagonale ; \(\vec B(O)=\vec0\) (compensation deux à deux, confirmée par les plans de symétrie \(x=0\) et \(y=0\)).",
    r"Pour \(\vec B\), un plan de symétrie des courants impose \(\vec B\) <em>orthogonal</em> au plan (pour \(\vec E\), c'est le contraire). Et \(\vec B(O)=\vec0\) n'est vrai qu'<b>au centre</b> : ailleurs (par exemple près d'un fil) le champ n'est pas nul."))

# =============================================================== Ex 3
TD5.append(exo('td5-3', '3', 'Champ créé par une spire sur son axe', 'TD',
    r"Spire circulaire de rayon \(R\), d'axe \(Oz\), parcourue par \(I\) (figure de l'énoncé : \(M\) sur l'axe, \(\alpha\) l'angle sous lequel on voit le rayon de la spire depuis \(M\)). 1) Composantes et dépendances de \(\vec B\) en tout point ; peut-on utiliser le théorème d'Ampère ? 2) Composantes et dépendances en un point \(M\) de l'axe. 3) Expression de \(\vec B(M)\) en fonction de \(\alpha\).",
    r"<p>Étape commune à toute étude de champ : <b>symétries et invariances</b> pour la direction et les dépendances de \(\vec B\). Ensuite, deux outils : <b>Biot et Savart</b> (toujours possible) et le <b>théorème d'Ampère</b> \(\oint_{\mathcal C}\vec B\cdot\mathrm{d}\vec l=\mu_0I_{enlac\acute e}\) (résultat standard, hors poly partie I ; voir <a href='cours.html#ch4-ampere'>le cours</a>).</p>"
    r"<p>Ampère n'est utile que s'il existe un <b>contour fermé</b> où \(\vec B\) est tangent et de <b>module constant</b> (ou orthogonal à \(\mathrm{d}\vec l\)) : il faut que \(\vec B\) n'ait qu'une composante et ne dépende que d'une variable, comme pour le fil, le cylindre, le solénoïde. Ici, il y aura deux composantes variables.</p>",
    [("Composantes et dépendances partout (question 1)",
      r"<p>Coordonnées cylindriques d'axe \(Oz\). <b>Invariance</b> par rotation autour de \(Oz\) : \(\vec B\) ne dépend pas de \(\theta\). <b>Symétries</b> : pour un point \(M\) hors de l'axe, le plan contenant \(M\) et l'axe \(Oz\) coupe la spire en deux points où le courant lui est perpendiculaire ; ce plan est un plan d'<b>antisymétrie</b> des courants. \(\vec B\) est donc <b>contenu</b> dans ce plan : pas de composante selon \(\vec e_\theta\).</p>"
      + mq(r"\vec B(M)=B_r(r,z)\,\vec e_r+B_z(r,z)\,\vec e_z")
      + r"<p>Il y a deux composantes qui dépendent de deux variables : aucun contour d'Ampère n'a un champ tangent et constant. <b>Le théorème d'Ampère ne permet pas</b> de calculer \(\vec B\) en tout point (la figure montre les lignes de champ, qui ne se laissent pas « capturer » par un contour simple).</p>" + FIG['ex3b']),
     ("Sur l'axe (question 2)",
      r"<p>Sur l'axe \(r=0\), tous les plans contenant \(Oz\) sont des plans d'antisymétrie : \(\vec B\) est contenu dans chacun d'eux, donc dans leur intersection, l'axe lui-même. Il reste</p>" + mq(r"\vec B(M)=B_z(z)\,\vec e_z") + r"<p>et \(B_z\) ne dépend que de \(z\).</p>"),
     ("Biot et Savart sur l'axe (question 3)",
      r"<p>\(P\) est le point courant de la spire : \(\overrightarrow{OP}=R\,\vec e_r\), \(\mathrm{d}\vec l=R\,\mathrm{d}\theta\,\vec e_\theta\), \(\overrightarrow{PM}=z\,\vec e_z-R\,\vec e_r\), \(PM=\sqrt{R^2+z^2}=\dfrac{R}{\sin\alpha}\). Avec \(\vec e_\theta\wedge\vec e_z=\vec e_r\) et \(\vec e_\theta\wedge\vec e_r=-\vec e_z\) :</p>"
      + mq(r"\mathrm{d}\vec B=\frac{\mu_0I}{4\pi}\,\frac{R\,\mathrm{d}\theta\,(z\,\vec e_r+R\,\vec e_z)}{PM^3}")
      + r"<p>Sur un tour, \(\displaystyle\int_0^{2\pi}\vec e_r\,\mathrm{d}\theta=\vec0\) : les composantes radiales des éléments diamétralement opposés s'annulent. Il reste (\(PM\) est constant sur la spire) :</p>"
      + mq(r"B_z=\frac{\mu_0I}{4\pi}\,\frac{R^2\cdot2\pi}{PM^3}=\frac{\mu_0I\,R^2}{2\,(R^2+z^2)^{3/2}}")
      + r"<p>Avec \(\dfrac{R^2}{PM^3}=\dfrac{\sin^3\alpha}{R}\) :</p>" + mq(r"\vec B(M)=\frac{\mu_0I}{2R}\,\sin^3\alpha\;\vec e_z=\frac{\mu_0I\,R^2}{2\,(R^2+z^2)^{3/2}}\,\vec e_z") + FIG['ex3a']),
     ("Cas particuliers et sens",
      r"<p>Au centre (\(z=0\), \(\alpha=\frac\pi2\)) : \(B=\dfrac{\mu_0I}{2R}\). Loin de la spire (\(|z|\gg R\)) : \(B\approx\dfrac{\mu_0IR^2}{2|z|^3}=\dfrac{\mu_0\,m}{2\pi|z|^3}\) avec \(m=I\pi R^2\) : la spire se comporte comme un dipôle magnétique. Sens : le courant tourne dans le sens trigonométrique vu de \(+z\), donc (tire-bouchon) \(\vec B\) est selon \(+\vec e_z\), des deux côtés de la spire (\(\sin^3\alpha\) est positif). Application : \(R=5\ \mathrm{cm}\), \(I=1\ \mathrm{A}\) : \(B(0)=\dfrac{4\pi\times10^{-7}}{0{,}10}\approx1{,}26\times10^{-5}\ \mathrm{T}\).</p>"
      r"<p>Pour info, hors de l'axe et près de lui, la conservation du flux (\(\mathrm{div}\,\vec B=0\)) donne \(B_r\approx\dfrac{3\mu_0IR^2\,z\,r}{4\,(R^2+z^2)^{5/2}}\) (vérifié numériquement).</p>")],
    r"1) \(\vec B=B_r(r,z)\vec e_r+B_z(r,z)\vec e_z\) (pas de \(\vec e_\theta\), pas de dépendance en \(\theta\)) ; Ampère inutilisable. 2) Sur l'axe : \(\vec B=B_z(z)\vec e_z\). 3) \(\vec B(M)=\dfrac{\mu_0I}{2R}\sin^3\alpha\,\vec e_z=\dfrac{\mu_0IR^2}{2(R^2+z^2)^{3/2}}\vec e_z\) ; au centre \(\dfrac{\mu_0I}{2R}\).",
    r"Ne pas vouloir appliquer Ampère « parce que c'est un cercle » : le champ n'est pas de module constant sur un contour simple. Attention aussi à l'angle : \(\alpha\) est l'angle <em>en \(M\)</em> entre l'axe et \(PM\), et \(\sin\alpha=\dfrac{R}{PM}\) (pas \(\cos\alpha\))."))

# =============================================================== Ex 4
TD5.append(exo('td5-4', '4', 'Lignes de champ magnétique', 'TD',
    r"1) Les lignes de champ d'un champ magnétique peuvent-elles se couper ? 2) Tracer les lignes de champ dans un plan perpendiculaire aux fils pour : a) deux fils parallèles distants de \(d\), de même intensité et de même sens ; b) deux fils parallèles distants de \(d\), de même intensité et de sens opposés ; c) trois fils parallèles aux sommets d'un triangle équilatéral, de même intensité et de même sens ; d) un fil parcouru par \(I\) placé dans un champ magnétique uniforme perpendiculaire au fil.",
    r"<p>On <b>superpose</b> les champs des fils (chacun fait des cercles autour du fil, orientés par le tire-bouchon) et on cherche, en chaque région, quel champ domine. Les points importants sont les <b>points neutres</b> (\(\vec B=\vec0\)), où la direction du champ n'est pas définie : c'est là, et seulement là, que des lignes de champ peuvent se croiser.</p>"
    r"<p>Rappel : en un point où \(\vec B\ne\vec0\), le champ est unique donc la ligne de champ l'est aussi ; et comme \(\mathrm{div}\,\vec B=0\) (pas de « charge magnétique »), les lignes ne naissent ni ne finissent nulle part : elles sont <b>fermées</b> (ou partent à l'infini). Pour tracer les schémas ci-dessous on a utilisé, pour des fils parallèles, le fait que les lignes de champ sont les courbes \(A_z=\text{cste}\) du potentiel vecteur \(A_z=-\frac{\mu_0}{2\pi}\sum_kI_k\ln r_k\) : le tracé est exact.</p>",
    [("Les lignes peuvent-elles se couper ? (question 1)",
      r"<p><b>Non</b>, sauf aux points où \(\vec B=\vec0\). En un point \(M\) où \(\vec B\ne\vec0\), le champ a <b>une</b> direction et <b>un</b> sens, donc une seule ligne de champ passe par \(M\) : deux lignes qui se coupaient donneraient deux directions de \(\vec B\) au point d'intersection. Aux points neutres (\(\vec B=\vec0\)) la direction est indéfinie et des lignes peuvent se rencontrer (points « selle » des figures ci-dessous).</p>"),
     ("a) Deux fils de même sens (question 2)",
      r"<p>Courants sortants. Près de chaque fil, le fil voisin est loin : lignes circulaires autour de chaque fil (sens trigonométrique). Au milieu \(M_0\) des fils, les deux champs sont égaux et opposés : \(\vec B(M_0)=\vec0\), c'est un point neutre où se croisent les deux boucles de la courbe en « huit » qui sépare les lignes entourant un seul fil de celles entourant les deux. Loin des fils, ovales de plus en plus circulaires (comme un fil unique portant \(2I\)).</p>" + FIG['ex4a']),
     ("b) Deux fils de sens opposés (question 2)",
      r"<p>Entre les fils, les champs sont de même sens et <b>s'ajoutent</b> : au milieu, \(B=2\times\dfrac{\mu_0I}{2\pi\,(d/2)}=\dfrac{2\mu_0I}{\pi d}\). Les lignes sortent de la région entre les fils, font le tour d'un fil et reviennent : ce sont des cercles <b>non concentriques</b> avec les fils (cercles d'Apollonius) ; la médiatrice des fils est une ligne de champ <b>rectiligne</b> (ligne fermée à l'infini). Pas de point neutre à distance finie.</p>" + FIG['ex4b']),
     ("c) Trois fils en triangle équilatéral (question 2)",
      r"<p>Au centre du triangle, les trois champs ont le même module et sont à \(120^\circ\) les uns des autres : leur somme est nulle, \(\vec B=\vec0\) (point neutre). Près de chaque fil, lignes circulaires ; la courbe à trois lobes passant par le centre sépare les lignes qui entourent un seul fil de celles qui entourent les trois ; très loin, on retrouve des cercles (champ d'un fil unique portant \(3I\)).</p>" + FIG['ex4c']),
     ("d) Fil et champ uniforme (question 2)",
      r"<p>Fil (courant sortant) en \(O\), \(\vec B_0=B_0\vec e_x\). Le champ du fil est \(\dfrac{\mu_0I}{2\pi r}\vec e_\theta\) ; sur l'axe \(Oy\) au-dessus du fil (\(\theta=\frac\pi2\), \(\vec e_\theta=-\vec e_x\)) il s'oppose à \(\vec B_0\) :</p>"
      + mq(r"B_x(0,y)=B_0-\frac{\mu_0I}{2\pi y}=0\ \Longrightarrow\ y=r_0=\frac{\mu_0I}{2\pi B_0}")
      + r"<p>C'est un point neutre (point d'arrêt). Pour \(r\lt r_0\) le fil domine : lignes fermées autour de lui ; pour \(r\gg r_0\), \(\vec B_0\) domine : lignes presque droites. Ordre de grandeur : \(I=3\ \mathrm{A}\), \(B_0=2\ \mathrm{mT}\) : \(r_0=\dfrac{2\times10^{-7}\times3}{2\times10^{-3}}=0{,}3\ \mathrm{mm}\).</p>" + FIG['ex4d'])],
    r"1) Non : une ligne de champ est unique en tout point où \(\vec B\ne\vec0\) ; elles ne se rencontrent qu'aux points neutres. Lignes toujours fermées. 2) a) boucles autour de chaque fil, « huit » séparateur, \(B=0\) au milieu ; b) cercles non concentriques, champ renforcé entre les fils (\(\frac{2\mu_0I}{\pi d}\) au milieu) ; c) trois lobes, \(B=0\) au centre ; d) point d'arrêt à \(r_0=\dfrac{\mu_0I}{2\pi B_0}\).",
    r"Les lignes de champ magnétique ne « partent » pas d'une source comme celles de \(\vec E\) : elles <b>tournent autour des courants</b>. Dans le cas a) le champ est <em>nul</em> (et non maximal) au milieu des deux fils ; dans le cas b) c'est le contraire."))

# =============================================================== Ex 5
TD5.append(exo('td5-5', '5', 'Champ magnétique d\'un solénoïde infini', 'TD',
    r"Solénoïde de rayon \(R\), d'axe \(Oz\), de hauteur \(H\) très grande devant \(R\) (supposé infini), parcouru par le courant \(I\). Le pas \(h\) est très petit devant \(R\) : on l'assimile à des spires jointives indépendantes, chacune parcourue par \(I\) ; \(n\) spires par unité de longueur. 1) Faire un schéma. 2) Composantes et dépendances de \(\vec B\) ; peut-on utiliser Ampère ? 3) Déterminer \(\vec B(M)\) en tout point.",
    r"<p>On fait d'abord les <b>symétries et invariances</b> : elles donnent la direction de \(\vec B\) et ses variables. Si \(\vec B\) est selon \(\vec e_z\) et ne dépend que de \(r\), on peut appliquer le <b>théorème d'Ampère</b> avec un <b>contour rectangulaire</b> à deux côtés parallèles à l'axe.</p>"
    r"<p><b>Mode d'emploi d'Ampère</b> : (1) orienter le contour \(\mathcal C\) ; (2) le sens de \(\mathcal C\) fixe, par la règle de la main droite, le signe des courants enlacés (un courant dans le sens du pouce, les doigts suivant \(\mathcal C\), compte \(+\)) ; (3) calculer \(\oint\vec B\cdot\mathrm{d}\vec l\) en tenant compte des côtés où \(\vec B\perp\mathrm{d}\vec l\) (contribution nulle) ; (4) calculer \(I_{enlac\acute e}\) et conclure.</p>",
    [("Schéma (question 1)",
      r"<p>Le solénoïde est une succession de spires jointives (\(n=\dfrac1h\) spires par mètre). Courant dans le sens trigonométrique vu de \(+z\) : sur la coupe par un plan contenant l'axe, courant <b>sortant</b> à gauche, <b>entrant</b> à droite. Les contours d'Ampère \(C_1,C_2,C_3\) sont des rectangles dans ce plan.</p>" + FIG['ex5']),
     ("Composantes et dépendances (question 2)",
      r"<p>Tout plan perpendiculaire à l'axe, \(z=\text{cste}\), est un plan de <b>symétrie</b> des courants (les spires sont dans de tels plans, les courants leur sont parallèles) : en un point de ce plan, \(\vec B\) est <b>orthogonal</b> au plan, donc selon \(\vec e_z\). Le solénoïde est infini : invariance par translation selon \(Oz\) et par rotation autour de \(Oz\) :</p>"
      + mq(r"\vec B(M)=B(r)\,\vec e_z")
      + r"<p>\(\vec B\) a <b>une seule composante</b> et ne dépend que de \(r\) : <b>on peut utiliser Ampère</b> avec un rectangle de côtés parallèle et perpendiculaire à l'axe.</p>"),
     ("Extérieur : \\(\\vec B=\\vec0\\) (question 3)",
      r"<p>Contour \(C_3\) rectangulaire de longueur \(\ell\), entièrement à l'extérieur, aux distances \(r_1\lt r_2\) de l'axe, orienté vers le haut en \(r_1\) puis vers le bas en \(r_2\). Les côtés horizontaux ne comptent pas (\(\vec B\parallel\vec e_z\perp\mathrm{d}\vec l\)) et aucun courant n'est enlacé :</p>"
      + mq(r"\oint_{C_3}\vec B\cdot\mathrm{d}\vec l=\big(B(r_1)-B(r_2)\big)\,\ell=\mu_0\times0\ \Longrightarrow\ B(r_1)=B(r_2)")
      + r"<p>\(B\) est donc <b>constant</b> à l'extérieur ; or il tend vers \(0\) quand \(r\to\infty\) (très loin des courants) : \(\vec B_{ext}=\vec0\).</p>"),
     ("Intérieur : \\(\\vec B\\) uniforme (question 3)",
      r"<p>Contour \(C_1\) entièrement à l'intérieur : même calcul, \(B(r_1)=B(r_2)\) pour tout \(r_1,r_2\lt R\) : le champ est <b>uniforme</b> dans le solénoïde.</p>"),
     ("Contour qui traverse le solénoïde (question 3)",
      r"<p>Contour \(C_2\), de longueur \(\ell\), orienté vers le haut à l'intérieur (\(r_1\lt R\)) et vers le bas à l'extérieur (\(r_2\gt R\)). Sa normale (règle de la main droite) est dirigée dans le sens du courant des spires sur la paroi de droite (entrant dans la page). Il est traversé par \(n\ell\) spires, chacune dans le sens positif :</p>"
      + mq(r"\oint_{C_2}\vec B\cdot\mathrm{d}\vec l=B_{int}\,\ell-B_{ext}\,\ell=\mu_0\,(n\ell)\,I\ \Longrightarrow\ B_{int}=\mu_0nI")
      + mq(r"\vec B(M)=\begin{cases}\mu_0\,n\,I\;\vec e_z&r\lt R\\[2pt]\vec0&r\gt R\end{cases}")
      + r"<p>Sens : tire-bouchon, courant trigonométrique vu de \(+z\) : \(\vec B\) selon \(+\vec e_z\). Application : \(n=1000\ \mathrm{spires/m}\), \(I=2\ \mathrm{A}\) : \(B=4\pi\times10^{-7}\times1000\times2\approx2{,}5\times10^{-3}\ \mathrm{T}\). Le champ est indépendant du rayon \(R\) et de la position dans la section.</p>")],
    r"\(\vec B=B(r)\vec e_z\) ; Ampère utilisable (contour rectangulaire). \(\vec B=\mu_0nI\,\vec e_z\) à l'intérieur (\(r\lt R\)), \(\vec B=\vec0\) à l'extérieur (\(r\gt R\)), avec \(n=\dfrac1h\) spires par unité de longueur.",
    r"Pour un solénoïde <em>fini</em> (\(H\) pas très grand devant \(R\)) le résultat \(\mu_0nI\) n'est valable qu'au centre ; sur l'axe, aux extrémités, on a environ la moitié, \(\frac{\mu_0nI}{2}\). Et le champ extérieur n'est pas nul par « symétrie » : il l'est parce qu'il est constant et tend vers \(0\) à l'infini."))

# =============================================================== Ex 6
TD5.append(exo('td5-6', '6', 'Champ magnétique créé par un cylindre', 'TD',
    r"Fil cylindrique rectiligne infini, de rayon \(R\), transportant le courant \(I\) avec une densité de courant \(\vec j\) uniforme, parallèle à l'axe. 1) Schéma. 2) Relation entre \(j\) et \(I\). 3) Composantes et dépendances de \(\vec B\) ; peut-on utiliser Ampère ? 4) \(\vec B(M)\) en tout point. 5) Que se passe-t-il si \(r\gg R\) ? (La numérotation de l'énoncé est un peu mélangée ; on traite les questions dans cet ordre.)",
    r"<p>Symétries de \(\vec B\) pour des courants parallèles à l'axe, puis <b>Ampère avec un contour circulaire d'axe \(Oz\)</b> (le champ y est tangent et de module constant). La difficulté est le <b>courant enlacé</b> : pour un courant réparti, \(I_{enlac\acute e}=\iint\vec j\cdot\mathrm{d}\vec S\) sur la surface (un disque) qui s'appuie sur le contour. À l'intérieur du fil, le disque ne contient qu'une partie du courant.</p>",
    [("Schéma (question 1)",
      r"<p>Le courant est selon \(+\vec e_z\) (sortant sur la vue de dessus), réparti uniformément dans le disque de rayon \(R\). On considère deux contours circulaires : \(C\) de rayon \(r\lt R\) et \(C'\) de rayon \(r\gt R\), orientés dans le sens trigonométrique (donc normale \(+\vec e_z\)).</p>" + FIG['ex6']),
     ("Relation \\(j\\)–\\(I\\) (question 2)",
      r"<p>\(I\) est le flux de \(\vec j\) à travers la section ; \(\vec j\) étant uniforme et normal à la section :</p>" + mq(r"I=\iint_{section}\vec j\cdot\mathrm{d}\vec S=j\,\pi R^2\ \Longrightarrow\ j=\frac{I}{\pi R^2}\quad[\mathrm{A\,m^{-2}}]")),
     ("Composantes et dépendances (question 3)",
      r"<p>Tout plan contenant l'axe est un plan de <b>symétrie</b> des courants (courants parallèles au plan) : en un point de ce plan, \(\vec B\) est <b>orthogonal</b> au plan, donc selon \(\vec e_\theta\). Invariances par translation selon \(Oz\) et rotation autour de \(Oz\) :</p>"
      + mq(r"\vec B(M)=B(r)\,\vec e_\theta")
      + r"<p>Sur un cercle d'axe \(Oz\) le champ est tangent et de module constant : <b>Ampère est utilisable</b>.</p>"),
     ("Circulation (question 4)",
      r"<p>\(\mathrm{d}\vec l=r\,\mathrm{d}\theta\,\vec e_\theta\) (contour orienté dans le sens de \(\vec e_\theta\)) :</p>" + mq(r"\oint\vec B\cdot\mathrm{d}\vec l=\int_0^{2\pi}B(r)\,r\,\mathrm{d}\theta=2\pi r\,B(r)=\mu_0I_{enlac\acute e}")),
     ("Courant enlacé et résultat (question 4)",
      mq(r"r\lt R:\ I_{enlac\acute e}=j\,\pi r^2=I\,\frac{r^2}{R^2}\qquad r\gt R:\ I_{enlac\acute e}=I")
      + mq(r"\vec B(M)=\begin{cases}\dfrac{\mu_0\,I\,r}{2\pi R^2}\,\vec e_\theta=\dfrac{\mu_0\,j\,r}{2}\,\vec e_\theta&r\le R\\[8pt]\dfrac{\mu_0\,I}{2\pi\,r}\,\vec e_\theta&r\ge R\end{cases}")
      + r"<p>Continuité en \(r=R\) : \(\dfrac{\mu_0I}{2\pi R}\) des deux côtés. \(B\) est nul sur l'axe, maximal à la surface (\(\dfrac{\mu_0I}{2\pi R}\)), puis décroît en \(\frac1r\) (courbe de la figure).</p>"),
     ("Si \\(r\\gg R\\) (question 5)",
      r"<p>À l'extérieur, \(\vec B=\dfrac{\mu_0I}{2\pi r}\vec e_\theta\) : <b>exactement</b> le champ d'un fil infini filiforme placé sur l'axe et parcouru par \(I\). De loin, on ne distingue pas la répartition du courant dans la section : seul \(I_{enlac\acute e}=I\) compte. Application : \(I=10\ \mathrm{A}\), \(R=1\ \mathrm{mm}\), à \(r=5\ \mathrm{cm}\) : \(B=\dfrac{2\times10^{-7}\times10}{0{,}05}=4\times10^{-5}\ \mathrm{T}\) ; à la surface \(B=\dfrac{2\times10^{-7}\times10}{10^{-3}}=2\times10^{-3}\ \mathrm{T}\).</p>")],
    r"\(I=j\pi R^2\) ; \(\vec B=B(r)\vec e_\theta\), Ampère utilisable (cercle d'axe \(Oz\)) ; \(\vec B=\dfrac{\mu_0Ir}{2\pi R^2}\vec e_\theta\) pour \(r\le R\), \(\vec B=\dfrac{\mu_0I}{2\pi r}\vec e_\theta\) pour \(r\ge R\) ; continu en \(R\) ; pour \(r\gg R\) : champ d'un fil infini.",
    r"À l'intérieur, le courant enlacé n'est pas \(I\) mais \(I\frac{r^2}{R^2}\) (rapport des aires) : oublier cela donne \(\frac{\mu_0I}{2\pi r}\) partout, faux et divergent sur l'axe. Sur l'axe, \(B=0\) (pas d'infini, contrairement au fil filiforme)."))

# =============================================================== Ex 7
TD5.append(exo('td5-7', '7', 'Champ magnétique d\'un câble coaxial', 'TD',
    r"Câble coaxial : conducteur cylindrique plein de rayon \(R_1\), entouré d'un conducteur externe occupant le volume compris entre les cylindres de rayons \(R_2\) et \(R_3\) (l'énoncé écrit « \(R_1\gt R_2\gt R_3\) » : <b>coquille d'énoncé</b>, la figure impose \(R_1\lt R_2\lt R_3\)) ; les trois cylindres sont coaxiaux. Le courant \(I\) circule dans le conducteur intérieur et revient en sens inverse dans le conducteur extérieur. 1) Composantes et dépendances de \(\vec B\) ; Ampère utilisable ? 2) Courant réparti uniformément dans les sections : \(\vec B(M)\) partout. 3) Courbe \(B(r)\) ; le champ est-il continu à la surface des conducteurs ?",
    r"<p>Même démarche que pour le cylindre plein : symétrie cylindrique, \(\vec B=B(r)\vec e_\theta\), <b>contour d'Ampère circulaire</b> de rayon \(r\) dans chacune des <b>quatre régions</b>. Le travail consiste à calculer le <b>courant enlacé</b> \(I_{enlac\acute e}(r)\) en comptant son <b>signe</b> : \(+I\) dans le cœur, \(-I\) (retour) dans le conducteur extérieur, réparti uniformément (proportionnel à l'aire).</p>",
    [("Composantes et dépendances (question 1)",
      r"<p>Les courants sont parallèles à l'axe : tout plan contenant \(Oz\) est un plan de symétrie, donc \(\vec B\) est orthogonal à ce plan, selon \(\vec e_\theta\). Invariances par translation selon \(Oz\) et rotation autour de l'axe :</p>"
      + mq(r"\vec B(M)=B(r)\,\vec e_\theta")
      + r"<p>Le champ est tangent et de module constant sur un cercle d'axe \(Oz\) : <b>Ampère est utilisable</b>. Convention : courant \(+I\) selon \(+\vec e_z\) (sortant) dans le cœur, \(-I\) dans le conducteur extérieur.</p>" + FIG['ex7']),
     ("Densités de courant (question 2)",
      mq(r"\vec j_1=\frac{I}{\pi R_1^2}\,\vec e_z\qquad\vec j_2=-\frac{I}{\pi\,(R_3^2-R_2^2)}\,\vec e_z")),
     ("Courant enlacé dans chaque région (question 2)",
      mq(r"\begin{array}{ll}r\lt R_1:&I_{enlac\acute e}=I\,\dfrac{r^2}{R_1^2}\\[6pt]R_1\lt r\lt R_2:&I_{enlac\acute e}=I\\[6pt]R_2\lt r\lt R_3:&I_{enlac\acute e}=I-I\,\dfrac{r^2-R_2^2}{R_3^2-R_2^2}=I\,\dfrac{R_3^2-r^2}{R_3^2-R_2^2}\\[8pt]r\gt R_3:&I_{enlac\acute e}=I-I=0\end{array}")),
     ("Champ en tout point (question 2)",
      r"<p>Avec \(2\pi rB(r)=\mu_0I_{enlac\acute e}\) dans chaque région :</p>"
      + mq(r"\vec B(M)=\begin{cases}\dfrac{\mu_0Ir}{2\pi R_1^2}\,\vec e_\theta&r\le R_1\\[8pt]\dfrac{\mu_0I}{2\pi r}\,\vec e_\theta&R_1\le r\le R_2\\[8pt]\dfrac{\mu_0I}{2\pi r}\,\dfrac{R_3^2-r^2}{R_3^2-R_2^2}\,\vec e_\theta&R_2\le r\le R_3\\[8pt]\vec0&r\ge R_3\end{cases}")),
     ("Courbe \\(B(r)\\) et continuité (question 3)",
      r"<p>La courbe (figure) est <b>continue</b> : en \(R_1\), \(\dfrac{\mu_0Ir}{2\pi R_1^2}\to\dfrac{\mu_0I}{2\pi R_1}\) et \(\dfrac{\mu_0I}{2\pi r}\to\dfrac{\mu_0I}{2\pi R_1}\) ; en \(R_2\), le facteur \(\dfrac{R_3^2-r^2}{R_3^2-R_2^2}\) vaut \(1\) ; en \(R_3\), il vaut \(0\), donc \(B\to0\). Le champ est continu à la traversée des surfaces des conducteurs car les courants sont <b>volumiques</b> (aucun courant surfacique) ; seule la dérivée a un point anguleux. Le maximum est en \(r=R_1\), de valeur \(\dfrac{\mu_0I}{2\pi R_1}\). Le champ est <b>nul à l'extérieur</b> : le câble ne rayonne pas, ce qui est l'intérêt du coaxial (courant total nul).</p>")],
    r"\(\vec B=B(r)\vec e_\theta\) ; \(B=\dfrac{\mu_0Ir}{2\pi R_1^2}\) (\(r\lt R_1\)), \(\dfrac{\mu_0I}{2\pi r}\) (\(R_1\lt r\lt R_2\)), \(\dfrac{\mu_0I}{2\pi r}\dfrac{R_3^2-r^2}{R_3^2-R_2^2}\) (\(R_2\lt r\lt R_3\)), \(0\) (\(r\gt R_3\)) ; \(B(r)\) continu.",
    r"Dans le conducteur extérieur, le courant de retour enlacé est proportionnel à l'<b>aire</b> \(\pi(r^2-R_2^2)\), pas à \(r-R_2\). Et ne pas oublier que le courant de retour compte avec un <em>signe</em> : la somme vaut bien \(0\) à l'extérieur. Lire l'ordre des rayons sur la figure (\(R_1\lt R_2\lt R_3\)) plutôt que dans l'énoncé."))

# =============================================================== Ex 8
TD5.append(exo('td5-8', '8', 'Champ magnétique d\'un tore de section rectangulaire', 'TD',
    r"Tore circulaire de rayon moyen \(R_0\), de section rectangulaire (largeur radiale \(a\), hauteur \(b\)), sur lequel sont bobinées \(N_1\) spires rectangulaires parcourues par le courant \(I_1\). 1) Préciser les lieux où le champ magnétique est défini. 2) Composantes et dépendances de \(\vec B\) en tout point. 3) Avec le théorème d'Ampère, déterminer \(\vec B\) en tout point.",
    r"<p>Les spires, bobinées sur la section, sont dans des <b>plans méridiens</b> (contenant l'axe \(Oz\)). Si les spires sont jointives, tout plan méridien est un plan de <b>symétrie</b> des courants : \(\vec B\) lui est orthogonal, donc selon \(\vec e_\theta\). Reste à choisir un <b>cercle d'axe \(Oz\)</b> comme contour d'Ampère et à compter les fils qui traversent le disque qu'il délimite, <b>avec leur sens</b>.</p>",
    [("Lieux où \\(\\vec B\\) est défini (question 1)",
      r"<p>Le champ est défini en tout point de l'espace sauf sur les fils des spires eux-mêmes (courants filiformes). On distingue trois régions : le <b>trou central</b> (\(r\lt R_0-\frac a2\)), l'<b>intérieur du tore</b> (\(R_0-\frac a2\lt r\lt R_0+\frac a2\) et \(|z|\lt\frac b2\)) et l'<b>extérieur</b> (le reste de l'espace).</p>" + FIG['ex8']),
     ("Composantes et dépendances (question 2)",
      r"<p>Coordonnées cylindriques d'axe \(Oz\). Plans méridiens = plans de symétrie des courants, donc \(\vec B\perp\) plan, soit \(\vec B\parallel\vec e_\theta\). Rotation autour de \(Oz\) (spires régulièrement réparties) : pas de dépendance en \(\theta\) :</p>"
      + mq(r"\vec B(M)=B_\theta(r,z)\,\vec e_\theta")
      + r"<p>Dépendance a priori en \(r\) <b>et</b> \(z\) ; le calcul d'Ampère montrera qu'à l'intérieur du tore \(B\) ne dépend en fait pas de \(z\).</p>"),
     ("Circulation sur un cercle d'axe \\(Oz\\) (question 3)",
      r"<p>Cercle \(\mathcal C\) de rayon \(r\), à la cote \(z\), orienté selon \(+\vec e_\theta\) (donc normale \(+\vec e_z\) pour le disque qui s'appuie dessus) :</p>"
      + mq(r"\oint_{\mathcal C}\vec B\cdot\mathrm{d}\vec l=2\pi r\,B_\theta(r,z)=\mu_0\,I_{enlac\acute e}")),
     ("Courant enlacé : on compte les fils qui traversent le disque (question 3)",
      r"<p>Courant \(I_1\) <b>montant</b> sur la paroi extérieure (\(r=R_0+\frac a2\)) et <b>descendant</b> sur la paroi intérieure (\(r=R_0-\frac a2\)) d'après la figure. Le disque bordé par \(\mathcal C\) (à la cote \(z\) avec \(|z|\lt\frac b2\)) est traversé par les parois intérieures des spires si \(r\gt R_0-\frac a2\), et par leurs parois extérieures si \(r\gt R_0+\frac a2\).</p>"
      + mq(r"\begin{array}{ll}r\lt R_0-\frac a2\ \text{(trou)}:&I_{enlac\acute e}=0\\[4pt]R_0-\frac a2\lt r\lt R_0+\frac a2,\ |z|\lt\frac b2:&I_{enlac\acute e}=-N_1I_1\ \ (\text{parois intérieures, courant descendant})\\[4pt]r\gt R_0+\frac a2\ \text{(extérieur)}:&I_{enlac\acute e}=-N_1I_1+N_1I_1=0\\[4pt]|z|\gt\frac b2:&I_{enlac\acute e}=0\end{array}")
      + r"<p>Dans la dernière ligne, le disque est au-dessus ou au-dessous du tore : aucun fil ne le traverse.</p>"),
     ("Résultat",
      mq(r"\vec B(M)=-\frac{\mu_0\,N_1\,I_1}{2\pi\,r}\,\vec e_\theta\quad\text{dans le tore}\qquad\vec B=\vec0\quad\text{ailleurs}")
      + r"<p>Le champ est donc <b>confiné dans le tore</b>, indépendant de \(z\) et de \(\theta\), en \(\frac1r\) (plus intense près de la paroi intérieure). Pour le sens indiqué sur la figure, \(\vec B\) est dirigé selon \(-\vec e_\theta\) (sens horaire vu de dessus) ; en inversant le sens du courant, on inverse le sens de \(\vec B\) (le module \(\dfrac{\mu_0N_1I_1}{2\pi r}\) est inchangé). Si \(a\ll R_0\), \(B\approx\dfrac{\mu_0N_1I_1}{2\pi R_0}\) : c'est un solénoïde de \(n=\dfrac{N_1}{2\pi R_0}\) spires par mètre refermé sur lui-même, d'où \(B=\mu_0nI_1\) (comparer à l'exercice 5).</p>")],
    r"1) \(\vec B\) défini partout sauf sur les fils. 2) \(\vec B=B_\theta(r,z)\vec e_\theta\). 3) \(\vec B=-\dfrac{\mu_0N_1I_1}{2\pi r}\vec e_\theta\) pour \(R_0-\frac a2\lt r\lt R_0+\frac a2\) et \(|z|\lt\frac b2\) (le signe dépend du sens du courant ; module \(\dfrac{\mu_0N_1I_1}{2\pi r}\)) ; \(\vec B=\vec0\) dans le trou central et à l'extérieur du tore.",
    r"Le champ n'est pas nul « parce qu'on est dans le tore » mais parce que le disque d'Ampère enlace \(N_1\) fils <em>tous dans le même sens</em> ; à l'extérieur il enlace aussi les fils retour, qui annulent exactement les premiers. Et le champ n'est pas uniforme dans la section : il varie en \(\frac1r\)."))

# =============================================================== Ex 9
TD5.append(exo('td5-9', '9', 'Effet Hall dans un semi-conducteur', 'TD',
    r"Plaque semi-conductrice de type \(N\) (porteurs : électrons de charge \(-e\)), de largeur \(b\) (selon \(y\)) et de hauteur \(h\) (selon \(z\)), parcourue dans le sens de sa longueur (\(x\)) par le courant \(I\) réparti sur toute la section : \(\vec j=j\,\vec e_x\), \(j\gt0\). Nombre de porteurs par unité de volume : \(n\). La plaque est dans un champ uniforme \(\vec B=B\,\vec e_z\), \(B\gt0\), grand devant le champ créé par \(I\). 1) Vitesse \(\vec v\) des électrons en fonction de \(\vec j,n,e\). 2) Expliquer l'apparition d'un champ de Hall ; sens et direction. 3) En régime permanent, \(\vec E_H\) par le bilan des forces selon \(\vec e_y\) sur un électron. 4) Intensité de ce champ en fonction de \(I,n,e,B,h,b\). 5) \(U_H=V(1)-V(1')\) ; montrer \(U_H=\dfrac{C_H}{h}IB\) et expliciter \(C_H\). 6) InSb : \(I=0{,}1\ \mathrm{A}\), \(C_H=385\times10^{-6}\ \mathrm{m^3\,C^{-1}}\), \(h=0{,}3\ \mathrm{mm}\), \(B=1\ \mathrm{T}\) : calculer \(U_H\) et \(n\).",
    r"<p>Effet Hall = <b>force de Lorentz</b> sur les porteurs mobiles : \(\vec F=q\,(\vec E+\vec v\wedge\vec B)\). Le champ \(\vec B\) dévie les porteurs vers un côté ; les charges s'accumulent sur les faces latérales et créent un <b>champ de Hall</b> qui s'oppose à la déviation. En <b>régime permanent</b>, plus de déviation : la force électrique de Hall compense exactement la force magnétique, d'où \(\vec E_H=-\vec v\wedge\vec B\). On en tire la <b>tension de Hall</b> en intégrant \(\vec E_H\) entre les faces.</p>",
    [("Vitesse des électrons (question 1)",
      r"<p>Les porteurs mobiles ont la charge volumique \(\rho_m=-ne\) et \(\vec j=\rho_m\vec v\) :</p>" + mq(r"\vec v=\frac{\vec j}{-ne}=-\frac{j}{ne}\,\vec e_x") + r"<p>Les électrons se déplacent selon \(-\vec e_x\), sens <b>opposé</b> à celui du courant.</p>"),
     ("Apparition du champ de Hall (question 2)",
      r"<p>Force magnétique sur un électron :</p>"
      + mq(r"\vec F_m=-e\,\vec v\wedge\vec B=-e\Big(-\frac{j}{ne}\Big)\vec e_x\wedge B\,\vec e_z=\frac{jB}{n}\,(\vec e_x\wedge\vec e_z)=-\frac{jB}{n}\,\vec e_y")
      + r"<p>Les électrons sont déviés vers \(-\vec e_y\), donc vers la face \(1'\) (en \(y=-\frac b2\)), qui se charge <b>négativement</b> ; la face \(1\) (en \(y=+\frac b2\)), appauvrie en électrons, devient <b>positive</b>. Ces charges créent un champ électrique de Hall de la face \(1\) (\(+\)) vers la face \(1'\) (\(-\)) : de <b>direction</b> \(\vec e_y\) et de <b>sens</b> \(-\vec e_y\).</p>" + FIG['ex9']),
     ("Régime permanent (question 3)",
      r"<p>Le courant circule toujours selon \(x\) : les électrons ne sont plus déviés, la somme des forces selon \(\vec e_y\) est nulle (force électrique de Hall \(-e\vec E_H\) plus force magnétique \(\vec F_m\)) :</p>"
      + mq(r"-e\,\vec E_H+\vec F_m=\vec0\ \Longrightarrow\ \vec E_H=-\frac{jB}{ne}\,\vec e_y\quad(=-\vec v\wedge\vec B)")
      + r"<p>On retrouve le sens \(-\vec e_y\), de \(1\) vers \(1'\).</p>"),
     ("Intensité du champ (question 4)",
      r"<p>\(I=j\,(b\,h)\), donc \(j=\dfrac{I}{bh}\) :</p>" + mq(r"E_H=\frac{jB}{ne}=\frac{I\,B}{n\,e\,b\,h}")),
     ("Tension de Hall (question 5)",
      r"<p>\(V(1)-V(1')=\displaystyle\int_1^{1'}\vec E_H\cdot\mathrm{d}\vec l\) ; de \(1\) à \(1'\), \(\mathrm{d}\vec l=-\mathrm{d}y\,\vec e_y\) (de \(y=+\frac b2\) à \(-\frac b2\)), \(\vec E_H\) uniforme :</p>"
      + mq(r"U_H=V(1)-V(1')=E_H\,b=\frac{I\,B}{n\,e\,h}=\frac{C_H}{h}\,I\,B\qquad C_H=\frac{1}{ne}")
      + r"<p>\(U_H\gt0\) : la face \(1\) est à un potentiel plus élevé. \(U_H\) ne dépend pas de la largeur \(b\) (elle se simplifie). <b>Unité de \(C_H\)</b> : \(\dfrac{1}{ne}\) s'exprime en \(\mathrm{m^3\,C^{-1}}\) (\(n\) en \(\mathrm{m^{-3}}\), \(e\) en \(\mathrm{C}\)) ; l'énoncé écrit \(\mathrm{m^3\,s^{-1}}\), c'est une <b>coquille</b> d'unité (vérification : \(\mathrm{m^3\,C^{-1}}\times\mathrm{m^{-1}}\times\mathrm{A}\times\mathrm{T}=\mathrm{V}\)).</p>"),
     ("Application numérique (question 6)",
      mq(r"U_H=\frac{C_H\,I\,B}{h}=\frac{385\times10^{-6}\times0{,}1\times1}{0{,}3\times10^{-3}}\approx0{,}128\ \mathrm{V}")
      + mq(r"n=\frac{1}{e\,C_H}=\frac{1}{1{,}602\times10^{-19}\times385\times10^{-6}}\approx1{,}6\times10^{22}\ \mathrm{m^{-3}}")
      + r"<p>Dans un métal comme le cuivre (\(n\approx8{,}5\times10^{28}\ \mathrm{m^{-3}}\)), le même montage donnerait \(U_H\approx2\times10^{-8}\ \mathrm{V}\) : l'effet Hall est environ cinq millions de fois plus fort dans ce semi-conducteur car \(n\) y est très faible. D'où l'utilisation en <b>capteur de champ magnétique</b> (sonde de Hall) ; la mesure de \(U_H\) donne aussi \(n\) et le <b>signe des porteurs</b> (pour un type \(P\), \(U_H\) change de signe).</p>")],
    r"1) \(\vec v=-\dfrac{j}{ne}\vec e_x\) ; 2) \(\vec F_m=-\dfrac{jB}{n}\vec e_y\) : accumulation d'électrons sur \(1'\), \(\vec E_H\) de \(1\) vers \(1'\) (\(-\vec e_y\)) ; 3) \(\vec E_H=-\dfrac{jB}{ne}\vec e_y\) ; 4) \(E_H=\dfrac{IB}{nebh}\) ; 5) \(U_H=\dfrac{IB}{neh}=\dfrac{C_H}{h}IB\), \(C_H=\dfrac1{ne}\) (en \(\mathrm{m^3\,C^{-1}}\)) ; 6) \(U_H\approx0{,}128\ \mathrm{V}\), \(n\approx1{,}6\times10^{22}\ \mathrm{m^{-3}}\).",
    r"Le sens du déplacement des électrons est <em>opposé</em> à celui du courant : prendre \(\vec v\parallel+\vec e_x\) inverse tous les signes. L'unité de \(C_H\) est \(\mathrm{m^3\,C^{-1}}\) (pas des \(\mathrm{m^3\,s^{-1}}\)). Et \(h\) (hauteur, selon \(z\), dans la direction de \(\vec B\)) est la dimension qui figure dans \(U_H\), pas la largeur \(b\)."))

TD5_SEC = ('<!-- TD5:DEBUT -->\n<section class="cx-chap" id="td5">\n<div class="cx-chap-hd">\n<span class="cx-chap-n">TD 5 · Magnétostatique</span>\n'
           '<h2>Biot et Savart, théorème d\'Ampère</h2>\n'
           '<p>Deux outils pour \\(\\vec B\\) : la <b>loi de Biot et Savart</b> (intégrale, toujours valable) et le <b>théorème d\'Ampère</b> \\(\\oint\\vec B\\cdot\\mathrm{d}\\vec l=\\mu_0I_{enlac\\acute e}\\) (rapide, mais seulement avec de fortes symétries ; résultat standard hors poly partie I). '
           'Les règles de symétrie de \\(\\vec B\\) sont <b>inversées</b> par rapport à \\(\\vec E\\). <a href="cours.html#ch4">Revoir le cours (Ch4)</a> · <a href="cours.html#ch4-ampere">Théorème d\'Ampère</a></p>\n</div>\n'
           + '\n'.join(TD5) + '\n</section>\n<!-- TD5:FIN -->\n')

TD5_CARD = ('<!-- TD5CARD:DEBUT -->\n<a class="cx-card" href="#td5"><span class="n">TD 5 · 6 pages · 9 fiches</span><span class="t">Magnétostatique : Biot et Savart, Ampère</span>'
            '<span class="d">Fil coudé, quatre fils, spire, lignes de champ, solénoïde, cylindre, câble coaxial, tore, effet Hall.</span><span class="cnt"></span><span class="bar"><i></i></span></a>\n<!-- TD5CARD:FIN -->\n')


def remplace_bloc(s, tag, bloc, ancre, avant=True):
    pat = re.compile(r'<!-- %s:DEBUT -->.*?<!-- %s:FIN -->\n?' % (tag, tag), re.S)
    if pat.search(s):
        return pat.sub(lambda m: bloc, s, count=1)
    i = s.index(ancre)
    if not avant:
        i += len(ancre)
    return s[:i] + bloc + s[i:]


s = lire('corriges.html')
s = remplace_bloc(s, 'TD5', TD5_SEC, '<!-- TD4:FIN -->\n', avant=False)
s = remplace_bloc(s, 'TD5CARD', TD5_CARD, '<!-- TD4CARD:FIN -->\n', avant=False)
s = s.replace('<h1>TD0, TD1, TD2bis, Gauss, TD3 (potentiel) et TD4 (condensateurs) corrigés pas à pas</h1>',
              '<h1>TD0, TD1, TD2bis, Gauss, TD3 (potentiel), TD4 (condensateurs) et TD5 (magnétostatique) corrigés pas à pas</h1>')
ecrire('corriges.html', s)
print('TD5 inséré :', len(TD5), 'exercices,', len(FIG), 'figures')
