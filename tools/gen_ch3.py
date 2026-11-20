"""Chapitre 3 (conducteurs et condensateurs) + corrigés du TD4 : schémas SVG et insertion idempotente dans
cours.html, formules.html, quiz.html, corriges.html, index.html, README.md.
Usage : python tools/gen_ch3.py   (relançable : les blocs sont repérés par des marqueurs de commentaire)."""
import html
import math
import os
import re

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


# =============================================================== schémas
def sb(s):
    """X[Y] -> indice SVG"""
    n = len(re.findall(r'\[([^\]]*)\]', s))
    s = re.sub(r'\[([^\]]*)\]', r'<tspan dy="3.2" font-size="72%">\1</tspan><tspan dy="-3.2">', s)
    return s + '</tspan>' * n


class Fig:
    def __init__(self, w, h):
        self.w, self.h, self.p = w, h, []

    def add(self, s):
        self.p.append(s)

    def line(self, x1, y1, x2, y2, c='ob'):
        self.add('<line class="%s" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (c, x1, y1, x2, y2))

    def arrow(self, x1, y1, x2, y2, c='ef', hc='efh', size=7):
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - size * math.cos(a), y2 - size * math.sin(a)
        self.line(x1, y1, bx, by, c)
        px, py = -math.sin(a) * size * 0.45, math.cos(a) * size * 0.45
        self.add('<polygon class="%s" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>' % (hc, x2, y2, bx + px, by + py, bx - px, by - py))

    def circ(self, cx, cy, r, c='ob', style=''):
        self.add('<circle class="%s" cx="%.1f" cy="%.1f" r="%.1f"%s/>' % (c, cx, cy, r, (' style="%s"' % style) if style else ''))

    def rect(self, x, y, w, h, c='ob'):
        self.add('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (c, x, y, w, h))

    def path(self, d, c='ob'):
        self.add('<path class="%s" d="%s"/>' % (c, d))

    def text(self, x, y, s, c='tx', anchor='middle', size=None):
        st = (' style="font-size:%spx"' % size) if size else ''
        self.add('<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' % (c, x, y, anchor, st, sb(s)))

    def signes(self, pts, signe='+', c='tc'):
        for x, y in pts:
            self.text(x, y + 4, signe, c, 'middle', 13)

    def svg(self, aria, caption, maxw=None):
        mw = maxw or self.w
        return ('<figure class="fgbox"><svg class="fg" viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:%dpx">%s</svg>'
                '<figcaption>%s</figcaption></figure>' % (self.w, self.h, aria, mw, ''.join(self.p), caption))


def cap(s):
    return re.sub(r'\[([^\]]*)\]', r'<sub>\1</sub>', s)


def ring_pts(cx, cy, r, n, a0=0.0):
    return [(cx + r * math.cos(a0 + 2 * math.pi * k / n), cy - r * math.sin(a0 + 2 * math.pi * k / n)) for k in range(n)]


FIG = {}

# ---- 1. conducteur à l'équilibre, effet de pointe
f = Fig(400, 240)
cx, cy = 165, 128


def surf(th):
    a, b = 98, 64
    r = a * b / math.sqrt((b * math.cos(th)) ** 2 + (a * math.sin(th)) ** 2)
    d = (th - 0.55 + math.pi) % (2 * math.pi) - math.pi
    r *= 1 + 0.5 * math.exp(-(d / 0.17) ** 2)
    return cx + r * math.cos(th), cy - r * math.sin(th)


pts = [surf(2 * math.pi * k / 220) for k in range(220)]
f.path('M' + ' L'.join('%.1f %.1f' % p for p in pts) + ' Z', 'qg')
for th, longu in [(0.0, 26), (0.3, 30), (0.55, 52), (0.8, 30), (1.25, 24), (1.9, 24), (2.5, 24), (3.14, 24), (3.8, 24), (4.5, 24), (5.2, 24), (5.8, 24)]:
    d = 0.01
    x, y = surf(th)
    x1, y1 = surf(th - d)
    x2, y2 = surf(th + d)
    tx, ty = x2 - x1, y2 - y1
    n = math.hypot(tx, ty)
    nx, ny = -ty / n, tx / n
    f.arrow(x + 3 * nx, y + 3 * ny, x + (3 + longu) * nx, y + (3 + longu) * ny)
    f.text(x - 9 * nx, y - 9 * ny + 4, '+', 'tc', 'middle', 13)
f.text(cx - 18, cy - 4, 'E[int] = 0', 'tx')
f.text(cx - 18, cy + 16, 'V = cste · ρ = 0', 'tm')
f.text(cx + 150, 40, 'pointe : σ grand,', 'te', 'start', 13)
f.text(cx + 150, 56, 'E grand', 'te', 'start', 13)
f.arrow(cx + 150, 62, cx + 102, 70, 'dsh', 'efh', 5)
f.text(cx + 150, 168, 'E = σ/ε[0] n[ext]', 'te', 'start', 13)
f.text(cx + 150, 184, 'normal à la surface', 'tm', 'start', 12)
f.text(cx, 228, 'charges à la surface uniquement', 'tm', 'middle', 13)
FIG['cond_pointe'] = f.svg('Conducteur à l\'équilibre : champ nul à l\'intérieur, champ normal à la surface, effet de pointe',
                           cap('Conducteur à l\'équilibre : charges à la surface, E[int] = 0, V constant, champ normal à la surface valant σ/ε[0]. Là où le rayon de courbure est petit (pointe), σ et le champ sont plus grands.'), 400)

# ---- 2. cavité, influence totale
f = Fig(400, 250)
cx, cy = 150, 125
f.circ(cx, cy, 100, 'qg')
f.circ(cx, cy, 48, 'ob', 'fill:var(--surface)')
f.circ(cx - 6, cy + 2, 6, 'qp')
f.text(cx - 6, cy - 12, '+q', 'tc', 'middle', 13)
for k in range(10):
    a = 2 * math.pi * k / 10 + 0.2
    f.arrow(cx - 6 + 9 * math.cos(a), cy + 2 - 9 * math.sin(a), cx + 41 * math.cos(a), cy - 41 * math.sin(a), 'ef', 'efh', 6)
f.signes(ring_pts(cx, cy, 57, 12, 0.1), '−', 'te')
f.signes(ring_pts(cx, cy, 92, 16, 0.2), '+', 'tc')
for p in ring_pts(cx, cy, 104, 8, 0.4):
    a = math.atan2(cy - p[1], p[0] - cx)
    f.arrow(cx + 104 * math.cos(a), cy - 104 * math.sin(a), cx + 130 * math.cos(a), cy - 130 * math.sin(a), 'ef', 'efh', 6)
f.text(268, 46, 'surface externe : +q', 'tc', 'start', 13)
f.text(268, 90, 'conducteur neutre :', 'tx', 'start', 13)
f.text(268, 107, 'E = 0, V = cste', 'tm', 'start', 13)
f.text(268, 150, 'surface interne : −q', 'te', 'start', 13)
f.text(268, 167, '(influence totale)', 'tm', 'start', 12)
FIG['cavite'] = f.svg('Charge dans une cavité d\'un conducteur : influence totale', cap('Une charge +q dans la cavité fait apparaître −q sur la surface interne (influence totale, Gauss) et +q sur la surface externe (conducteur neutre). Dans le métal, E = 0.'), 400)


# ---- 3. condensateur plan (avec ou sans axe)
def plan(axe):
    f = Fig(400, 230)
    f.rect(70, 150, 240, 12, 'qp')
    f.rect(70, 60, 240, 12, 'qn')
    f.signes([(x, 144) for x in range(86, 300, 30)], '+', 'tc')
    f.signes([(x, 80 + 6) for x in range(86, 300, 30)], '−', 'te')
    for x in range(95, 290, 40):
        f.arrow(x, 148, x, 76, 'ef', 'efh', 7)
    f.path('M68 146 C 22 138 22 84 68 76', 'efl' if False else 'ef')
    f.path('M312 146 C 358 138 358 84 312 76', 'ef')
    f.arrow(54, 78.5, 68, 76, 'ef', 'efh', 7)
    f.arrow(326, 78.5, 312, 76, 'ef', 'efh', 7)
    f.text(190, 186, 'E = σ/ε[0] entre les armatures,  E ≈ 0 à l\'extérieur', 'tx', 'middle', 13)
    f.text(190, 206, 'aux bords : lignes de champ courbées (effet de bord)', 'tm', 'middle', 12)
    f.text(190, 42, '−σ  (armature 2)', 'te', 'middle', 13)
    f.text(335, 160, '+σ (armature 1)', 'tc', 'start', 13) if False else None
    if axe:
        f.arrow(372, 168, 372, 36, 'ax', 'axh', 7)
        f.text(386, 44, 'z', 'tm', 'start', 13)
        f.text(364, 160, '0', 'tx', 'end', 13)
        f.text(364, 72, 'e', 'tx', 'end', 13)
        f.line(366, 156, 378, 156, 'ax')
        f.line(366, 66, 378, 66, 'ax')
        f.text(40, 156, '+σ', 'tc', 'middle', 13)
    else:
        f.arrow(385, 154, 385, 70, 'dsh', 'efh', 5)
        f.arrow(385, 70, 385, 154, 'dsh', 'efh', 5)
        f.text(393, 117, 'e', 'tx', 'start', 13)
        f.text(40, 156, '+σ', 'tc', 'middle', 13)
    return f


f = plan(False)
FIG['plan'] = f.svg('Condensateur plan : champ uniforme entre les armatures', cap('Condensateur plan : les charges +σ et −σ sont sur les faces en regard (influence totale). Le champ est uniforme entre les armatures, quasi nul à l\'extérieur (sauf aux bords).'), 400)
f = plan(True)
FIG['td4_plan'] = f.svg('Condensateur plan avec le repère Oz', cap('Repère Oz perpendiculaire aux armatures : armature 1 (+σ) en z = 0, armature 2 (−σ) en z = e. E = σ/ε[0] e[z] pour 0 &lt; z &lt; e, nul ailleurs.'), 400)

# ---- 4. TD4 ex.1 deux sphères reliées
f = Fig(420, 200)
f.circ(85, 100, 58, 'qg')
f.circ(335, 112, 30, 'qg')
f.signes(ring_pts(85, 100, 48, 8, 0.3), '+', 'tc')
f.signes(ring_pts(335, 112, 21, 8, 0.3), '+', 'tc')
f.line(143, 98, 305, 108, 'ob')
f.text(224, 90, 'fil conducteur', 'tm', 'middle', 12)
f.text(224, 128, 'd ≫ R[1], R[2]', 'tm', 'middle', 12)
f.line(85, 100, 143, 100, 'dsh')
f.text(115, 117, 'R[1]', 'tx', 'middle', 13)
f.line(335, 112, 335, 142, 'dsh')
f.text(349, 132, 'R[2]', 'tx', 'start', 13)
f.text(85, 38, 'S[1] : Q[1], σ[1]', 'tc', 'middle', 13)
f.text(335, 62, 'S[2] : Q[2], σ[2]', 'tc', 'middle', 13)
f.text(210, 178, 'même potentiel V : σ[1]/σ[2] = R[2]/R[1]  (la petite sphère est plus chargée en surface)', 'tm', 'middle', 12)
FIG['td4_ex1'] = f.svg('Deux sphères conductrices reliées par un fil', cap('Deux sphères reliées par un fil, très éloignées : un seul conducteur, un seul potentiel V ; la plus petite porte la plus grande densité surfacique.'), 420)

# ---- 5. TD4 ex.3 cylindrique (vue de dessus)
f = Fig(430, 250)
cx, cy = 125, 125
f.circ(cx, cy, 46, 'qp')
f.circ(cx, cy, 100, 'ob')
f.circ(cx, cy, 107, 'ob')
f.signes(ring_pts(cx, cy, 37, 8, -0.51), '+', 'tc')
f.signes(ring_pts(cx, cy, 92, 14, 0.1), '−', 'te')
for k in range(12):
    a = 2 * math.pi * k / 12 + 0.26
    f.arrow(cx + 50 * math.cos(a), cy - 50 * math.sin(a), cx + 84 * math.cos(a), cy - 84 * math.sin(a), 'ef', 'efh', 6)
f.text(cx, cy + 4, '⊙ Oz', 'tm', 'middle', 13)
f.line(cx, cy, cx + 46 * math.cos(-0.9), cy - 46 * math.sin(-0.9), 'dsh')
f.text(cx - 6, cy + 26, 'R[1]', 'tx', 'middle', 12)
f.line(cx, cy, cx + 104 * math.cos(0.75), cy - 104 * math.sin(0.75), 'dsh')
f.text(cx + 88, cy - 80, 'R[2]', 'tx', 'start', 13)
f.text(262, 60, 'armature intérieure : +Q', 'tc', 'start', 13)
f.text(262, 78, 'σ[1] = Q/(2πR[1]H)', 'tc', 'start', 13)
f.text(262, 118, 'armature extérieure : −Q', 'te', 'start', 13)
f.text(262, 136, 'σ[2] = −Q/(2πR[2]H)', 'te', 'start', 13)
f.text(262, 178, 'E radial entre R[1] et R[2],', 'tx', 'start', 13)
f.text(262, 195, 'E = 0 ailleurs', 'tx', 'start', 13)
f.text(262, 225, 'vue de dessus (H ≫ R[1], R[2])', 'tm', 'start', 12)
FIG['td4_ex3'] = f.svg('Condensateur cylindrique vu de dessus', cap('Condensateur cylindrique en coupe : le champ radial n\'existe qu\'entre les armatures, σ[1]R[1] = −σ[2]R[2].'), 430)

# ---- 6. TD4 ex.4 sphérique
f = Fig(430, 250)
cx, cy = 125, 125
f.circ(cx, cy, 44, 'qp')
d = ('M%.1f %.1f A 100 100 0 1 0 %.1f %.1f A 100 100 0 1 0 %.1f %.1f Z M%.1f %.1f A 114 114 0 1 1 %.1f %.1f A 114 114 0 1 1 %.1f %.1f Z'
     % (cx + 100, cy, cx - 100, cy, cx + 100, cy, cx + 114, cy, cx - 114, cy, cx + 114, cy))
f.path(d, 'qn')
f.circ(cx, cy, 100, 'ob')
f.circ(cx, cy, 114, 'ob')
f.signes(ring_pts(cx, cy, 35, 8, -0.51), '+', 'tc')
f.signes(ring_pts(cx, cy, 92, 14, 0.1), '−', 'te')
for k in range(12):
    a = 2 * math.pi * k / 12 + 0.26
    f.arrow(cx + 49 * math.cos(a), cy - 49 * math.sin(a), cx + 84 * math.cos(a), cy - 84 * math.sin(a), 'ef', 'efh', 6)
f.line(cx, cy, cx + 44 * math.cos(-0.9), cy - 44 * math.sin(-0.9), 'dsh')
f.text(cx - 6, cy + 26, 'R[A]', 'tx', 'middle', 12)
f.line(cx, cy, cx + 100 * math.cos(0.75), cy - 100 * math.sin(0.75), 'dsh')
f.text(cx + 98, cy - 92, 'R[B]', 'tx', 'middle', 13)
f.text(262, 50, 'A : sphère pleine, +Q', 'tc', 'start', 13)
f.text(262, 68, 'σ[A] = Q/(4πR[A]²)', 'tc', 'start', 13)
f.text(262, 108, 'B : sphère creuse (R[B] intérieur)', 'te', 'start', 13)
f.text(262, 126, 'σ[B] = −Q/(4πR[B]²)', 'te', 'start', 13)
f.text(262, 168, 'E radial pour R[A] &lt; r &lt; R[B],', 'tx', 'start', 13)
f.text(262, 185, 'E = 0 ailleurs', 'tx', 'start', 13)
f.text(262, 225, 'coupe passant par le centre', 'tm', 'start', 12)
FIG['td4_ex4'] = f.svg('Condensateur sphérique en coupe', cap('Condensateur sphérique : A (rayon extérieur R[A]) dans B (rayon intérieur R[B]) ; la charge −Q se place sur la face interne de B.'), 430)

# ---- 7. TD4 ex.5A disques : champ, équipotentielles, effets de bord
f = Fig(430, 250)
f.rect(90, 150, 230, 10, 'qp')
f.rect(90, 70, 230, 10, 'qn')
for x in (125, 165, 205, 245, 285):
    f.arrow(x, 148, x, 84, 'ef', 'efh', 7)
for x0, sgn in ((90, -1), (320, 1)):
    f.path('M%d 146 C %d 140 %d 90 %d 84' % (x0 + sgn * 4, x0 + sgn * 40, x0 + sgn * 40, x0 + sgn * 4), 'ef')
    f.path('M%d 146 C %d 140 %d 90 %d 84' % (x0 + sgn * 10, x0 + sgn * 82, x0 + sgn * 82, x0 + sgn * 10), 'ef')
for y in (96, 115, 134):
    f.line(96, y, 314, y, 'dsh')
    f.path('M96 %d C 70 %d 70 %d 60 %d' % (y, y, y, y), 'dsh')
f.text(205, 205, 'équipotentielles : plans parallèles aux disques (centre)', 'tm', 'middle', 12)
f.text(205, 224, 'lignes de champ droites au centre, courbées sur les bords', 'tm', 'middle', 12)
f.arrow(395, 168, 395, 40, 'ax', 'axh', 7)
f.text(409, 48, 'z', 'tm', 'start', 13)
f.text(387, 160, 'O', 'tx', 'end', 13)
f.text(387, 78, 'e', 'tx', 'end', 13)
f.text(205, 58, 'D[1]  (V[1])', 'te', 'middle', 13)
f.text(205, 182, 'D[0]  (V[0])', 'tc', 'middle', 13)
f.arrow(90, 190, 320, 190, 'dsh', 'efh', 5)
f.arrow(320, 190, 90, 190, 'dsh', 'efh', 5)
f.text(205, 187, '2a', 'tx', 'middle', 12) if False else None
FIG['td4_ex5'] = f.svg('Condensateur à disques : repère, équipotentielles et lignes de champ', cap('Deux disques de rayon a et d\'axe Oz, distants de e. Si e ≪ a, on retrouve le condensateur plan idéal : champ uniforme, équipotentielles planes ; sur les bords les lignes se courbent.'), 430)

# ---- 8. TD4 ex.5B déplacement d'armature à Q constant
f = Fig(470, 230)
for x0, ep, lab, ulab in ((30, 40, 'état initial', 'U = Qe/(ε[0]S)'), (250, 66, 'après déplacement', "U' = Q(e+h)/(ε[0]S)")):
    yb = 150
    f.rect(x0, yb, 150, 9, 'qp')
    f.rect(x0, yb - ep - 9, 150, 9, 'qn')
    for x in range(x0 + 25, x0 + 140, 30):
        f.arrow(x, yb - 2, x, yb - ep - 1, 'ef', 'efh', 6)
    f.signes([(x, yb - 6) for x in range(x0 + 12, x0 + 148, 24)], '+', 'tc')
    f.text(x0 + 75, 40, lab, 'tx', 'middle', 13)
    f.text(x0 + 75, 188, ulab, 'tx', 'middle', 13)
    f.text(x0 + 75, 208, 'Q constant, σ et E inchangés', 'tm', 'middle', 12)
    xd = x0 + 162
    f.arrow(xd, yb + 4, xd, yb - ep - 12, 'dsh', 'efh', 5)
    f.arrow(xd, yb - ep - 12, xd, yb + 4, 'dsh', 'efh', 5)
f.text(206, 125, 'e', 'tx', 'start', 13)
f.text(426, 118, 'e + h', 'tx', 'start', 13)
f.arrow(238, 100, 238, 78, 'ax', 'axh', 6)
f.text(230, 92, 'h', 'te', 'end', 13)
FIG['td4_ex5b'] = f.svg('Écartement des armatures à charge constante', cap("Condensateur isolé (Q constant) : on éloigne l'armature négative de h. Le champ ne change pas mais la tension augmente ; l'énergie stockée aussi (travail de l'opérateur)."), 470)

# ---- 9. TD4 ex.6 trois cylindres + E(r)
f = Fig(560, 285)
cx, cy = 125, 130
f.circ(cx, cy, 28, 'qp')
f.circ(cx, cy, 62, 'ob')
f.circ(cx, cy, 95, 'ob')
f.text(cx, cy + 4, '+Q', 'tc', 'middle', 12)
f.text(cx - 57, cy + 53, '−Q', 'te', 'middle', 12)
f.text(cx + 78, cy - 84, '+Q', 'tc', 'middle', 12)
for k in range(8):
    a = 2 * math.pi * k / 8 + 0.2
    f.arrow(cx + 33 * math.cos(a), cy - 33 * math.sin(a), cx + 57 * math.cos(a), cy - 57 * math.sin(a), 'ef', 'efh', 6)
    f.arrow(cx + 99 * math.cos(a), cy - 99 * math.sin(a), cx + 120 * math.cos(a), cy - 120 * math.sin(a), 'ef', 'efh', 6)
f.text(cx - 20, cy + 22, 'R[1]', 'tx', 'middle', 12) if False else None
f.text(cx, 275, 'vue de dessus : (1), (2), (3) de rayons R[1] &lt; R[2] &lt; R[3]', 'tm', 'middle', 12)
# graphe E(r)
gx, gy = 300, 230
f.arrow(gx, gy, 545, gy, 'ax', 'axh', 7)
f.arrow(gx, gy, gx, 40, 'ax', 'axh', 7)
f.text(548, gy + 16, 'r', 'tm', 'end', 13)
f.text(gx + 12, 44, 'E(r)', 'tm', 'start', 13)
xr = lambda r: gx + 25 + r * 1.9
k = 3900
f.line(gx, gy, xr(28), gy, 'ef')
pts = ['%.1f %.1f' % (xr(r), gy - k / r) for r in range(28, 63, 2)]
f.path('M' + ' L'.join(pts), 'ef')
f.line(xr(62), gy, xr(95), gy, 'ef')
pts = ['%.1f %.1f' % (xr(r), gy - k / r) for r in range(95, 121, 2)]
f.path('M' + ' L'.join(pts), 'ef')
for r, hh in ((28, k / 28), (62, k / 62), (95, k / 95)):
    f.line(xr(r), gy, xr(r), gy - hh, 'dsh')
for r, nm in ((28, 'R[1]'), (62, 'R[2]'), (95, 'R[3]')):
    f.text(xr(r), gy + 16, nm, 'tx', 'middle', 12)
f.text(xr(45), 78, 'Q/(2πε[0]hr)', 'tx', 'middle', 12)
f.text(xr(78), gy - 14, 'E = 0', 'tx', 'middle', 12)
f.text(xr(108), gy - 60, 'Q/(2πε[0]hr)', 'tx', 'middle', 12)
FIG['td4_ex6'] = f.svg('Trois cylindres coaxiaux : disposition et courbe E(r)', cap('Cylindres (1) +Q, (2) −Q, (3) +Q. Gauss : E = 0 pour r &lt; R[1] et pour R[2] &lt; r &lt; R[3] ; E = Q/(2πε[0]hr) entre R[1] et R[2] et au-delà de R[3].'), 560)

# =============================================================== utilitaires HTML
def mq(s):
    return '<div class="mq">\\[' + s + '\\]</div>'


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


# =============================================================== cours : chapitre 3
COURS = r"""<!-- CH3:DEBUT -->
<article class="chapter" id="ch3">
<div class="chapter-hd">
<span class="cn">CH 3</span>
<h2>Conducteurs à l'équilibre et condensateurs</h2>
<label class="chap-check"><input data-chk="3" type="checkbox"/> validé</label>
</div>
<div class="prose">
<div class="soon"><b>Source</b> : poly « Chap. 3 : Conducteurs à l'équilibre – Condensateurs » 2026/2027 et TD4. Le chapitre commence par la conduction (loi d'Ohm), puis traite de l'équilibre d'un conducteur (théorème de Coulomb), de la capacité et de l'énergie.</div>
<p>Un <span class="term">conducteur</span> contient des porteurs de charge libres (électrons dans un métal, ions dans une solution) qui se déplacent sous l'action d'un champ. À l'équilibre ils ne bougent plus en moyenne : c'est ce qui donne au conducteur ses propriétés très simples, base du calcul des condensateurs.</p>
<h3 id="ch3-ohm">Courant électrique et loi d'Ohm locale</h3>
<div class="box def"><div class="bt">◆ Intensité et densité de courant</div>
<div class="mq">\[I=\iint_{(S)}\vec j\cdot\vec n\,\mathrm{d}S\qquad\vec j=\rho\,\vec v\qquad[I]=\text{ampère (A)},\ \ [j]=\mathrm{A\,m^{-2}}\]</div>
<p>L'intensité est le <b>flux</b> de la densité de courant \(\vec j\) à travers la section \((S)\) ; \(\mathrm{d}q=I\,\mathrm{d}t\). Si \(\vec j\) est uniforme et normal à la section : \(I=jS\). Avec plusieurs types de porteurs : \(\vec j=\sum_i\rho_i\vec v_i\).</p></div>
<div class="box thm"><div class="bt">★ Loi d'Ohm locale et modèle de Drude</div>
<div class="mq">\[\vec j=\gamma\vec E\qquad\gamma=\frac{ne^2\tau}{m_e}\qquad[\gamma]=\mathrm{S\,m^{-1}}\]</div>
<p>Entre deux collisions, un électron obéit à \(m_e\,\dot{\vec v}=-e\vec E\) ; la vitesse d'ensemble est \(\vec v_{moy}=-\frac{e\tau}{m_e}\vec E\) (\(\tau\sim10^{-14}\ \mathrm{s}\) : temps entre deux collisions). Quand la température monte, les collisions sont plus fréquentes, \(\tau\) diminue, donc \(\gamma\) <b>diminue</b> pour un métal.</p></div>
<div class="box thm"><div class="bt">★ Résistance d'un fil cylindrique</div>
<div class="mq">\[U=RI\qquad R=\frac{\ell}{\gamma s}\qquad[R]=\text{ohm }(\Omega)\]</div>
<p>Pour un courant uniforme et axial sur la section \(s\) et la longueur \(\ell\) : \(I=\gamma Es\) et \(U=E\ell\), d'où \(R=\frac{\ell}{\gamma s}\). La résistivité \(\frac1\gamma\) varie à peu près linéairement avec \(T\) (thermomètre à résistance de platine).</p></div>
<div class="box ex"><div class="bt">✎ Ordre de grandeur : la vitesse des électrons</div><p>Fil de cuivre de section \(2{,}5\ \mathrm{mm^2}\), \(I=20\ \mathrm{A}\) : \(j=\frac{I}{s}=8\times10^6\ \mathrm{A\,m^{-2}}\). Charge libre volumique \(\rho=n e\approx1{,}4\times10^{10}\ \mathrm{C\,m^{-3}}\) (un électron libre par atome de cuivre), donc \(v=\frac{j}{\rho}\approx0{,}6\ \mathrm{mm\,s^{-1}}\) : très lente devant l'agitation thermique (\(\sim10^5\ \mathrm{m\,s^{-1}}\)).</p></div>
<h3 id="ch3-equilibre">Conducteur en équilibre électrostatique</h3>
<div class="box thm"><div class="bt">★ Propriétés à connaître (à l'équilibre)</div>
<ul>
<li>Pas de courant macroscopique : \(\vec j=\vec0\), donc, par la loi d'Ohm, <b>champ intérieur nul</b> : \(\vec E_{int}=\vec0\).</li>
<li>\(\vec E=-\overrightarrow{\mathrm{grad}}\,V=\vec0\) : le potentiel est <b>uniforme</b>, \(V_{int}=\text{cste}\). Le conducteur est un volume <b>équipotentiel</b> (sa surface aussi).</li>
<li>Gauss avec \(\vec E=\vec0\) donne \(\rho_{int}=0\) : toute la charge est <b>à la surface</b>, avec une densité \(\sigma(P)\).</li>
<li>Les lignes de champ sont orthogonales aux équipotentielles : à l'extérieur, au voisinage de la surface, \(\vec E\) est <b>normal</b> à la surface.</li>
</ul></div>
<div class="box thm"><div class="bt">★ Théorème de Coulomb</div>
<div class="mq">\[\vec E_{ext}(P)=\frac{\sigma(P)}{\varepsilon_0}\,\vec n_{ext}\]</div>
<p>\(\vec n_{ext}\) est la normale unitaire à la surface, dirigée vers l'extérieur du conducteur. Le champ au voisinage immédiat de la surface ne dépend que de la densité surfacique en ce point.</p></div>
<div class="box method"><div class="bt">▹ Pourquoi un facteur 2 de plus qu'un plan isolé</div>
<p>Près de \(P\), le champ est la somme du champ \(\vec E_1\) d'un petit morceau de surface (assimilé à un plan : \(\pm\frac{\sigma}{2\varepsilon_0}\vec n\)) et du champ \(\vec E_2\) du reste du conducteur, continu en traversant la surface. Dedans, \(\vec E_{int}=\vec0=-\frac{\sigma}{2\varepsilon_0}\vec n_{ext}+\vec E_2\), donc \(\vec E_2=\frac{\sigma}{2\varepsilon_0}\vec n_{ext}\) ; dehors, \(\vec E_{ext}=\frac{\sigma}{2\varepsilon_0}\vec n_{ext}+\vec E_2=\frac{\sigma}{\varepsilon_0}\vec n_{ext}\).</p></div>
<div class="box warn"><div class="bt">⚠ Plan isolé ou surface de conducteur</div><p>Le plan infini <em>isolé</em> donne \(\frac{\sigma}{2\varepsilon_0}\) de chaque côté ; <b>à la surface d'un conducteur</b> le champ est \(\frac{\sigma}{\varepsilon_0}\) d'un seul côté (et 0 de l'autre). Dans un condensateur plan, c'est la somme des deux plans qui donne aussi \(\frac{\sigma}{\varepsilon_0}\).</p></div>
FIG_COND_POINTE
<div class="box thm"><div class="bt">★ Trois conséquences</div>
<ul>
<li><b>Boule conductrice de charge \(Q\)</b> (charge uniforme en surface, \(\sigma=\frac{Q}{4\pi R^2}\)) : par Gauss, pour \(r&gt;R\), \(\vec E=\frac{Q}{4\pi\varepsilon_0r^2}\vec e_r\), comme une charge ponctuelle en son centre ; \(E=0\) et \(V=\frac{Q}{4\pi\varepsilon_0R}\) pour \(r&lt;R\).</li>
<li><b>Cavité contenant une charge \(q\)</b> : une surface de Gauss dans le métal entourant la cavité a un flux nul, donc la surface interne porte \(-q\) : c'est l'<b>influence totale</b>. Si le conducteur est neutre, la surface externe porte \(+q\).</li>
<li><b>Cavité vide</b> : la surface interne ne porte aucune charge, le champ y est nul et le potentiel égal à celui du conducteur. Aucune perturbation extérieure n'agit dans la cavité : c'est la <b>cage de Faraday</b>.</li>
</ul></div>
FIG_CAVITE
<h3 id="ch3-capa">Capacité d'un conducteur seul</h3>
<div class="box def"><div class="bt">◆ Capacité</div>
<div class="mq">\[C=\frac{Q}{V}>0\qquad[C]=\text{farad (F)}=\mathrm{C\,V^{-1}}\]</div>
<p>Si on porte un conducteur seul au potentiel \(V\) (avec \(V(\infty)=0\)), il se charge de \(Q=CV\), et \(C\) ne dépend que de sa <b>géométrie</b> : si on multiplie \(V\) par \(\lambda\), toutes les densités de charge sont multipliées par \(\lambda\).</p></div>
<div class="box thm"><div class="bt">★ Capacité d'une sphère de rayon \(R\)</div>
<div class="mq">\[V=\frac{Q}{4\pi\varepsilon_0R}\ \Longrightarrow\ C=4\pi\varepsilon_0R\]</div>
<p>Proportionnelle au rayon. Pour la Terre, \(C\approx0{,}7\ \mathrm{mF}\) : le farad est une très grande unité (on utilise \(\mathrm{pF}\), \(\mathrm{nF}\), \(\mu\mathrm{F}\)).</p></div>
<div class="box thm"><div class="bt">★ Effet de pointe</div>
<p>Deux sphères de rayons \(R_1\) et \(R_2\) reliées par un fil (très éloignées) sont au même potentiel \(V\) : \(\sigma_1=\frac{\varepsilon_0V}{R_1}\), \(\sigma_2=\frac{\varepsilon_0V}{R_2}\), d'où</p>
<div class="mq">\[\frac{\sigma_1}{\sigma_2}=\frac{R_2}{R_1}\qquad C=C_1+C_2=4\pi\varepsilon_0(R_1+R_2)\]</div>
<p>La densité de charge varie comme l'<b>inverse du rayon de courbure</b> : le champ \(\frac{\sigma}{\varepsilon_0}\) est très intense près des pointes (paratonnerre, foudre).</p></div>
<h3 id="ch3-cond">Condensateurs</h3>
<div class="box def"><div class="bt">◆ Influence partielle et totale</div>
<ul>
<li><b>Partielle</b> : un conducteur neutre (ou relié à la Terre) approché d'un conducteur chargé se couvre de charges de signe opposé : \(Q_2=C_{21}V_1\) avec \(C_{21}&lt;0\).</li>
<li><b>Totale</b> : si le conducteur 2 <em>entoure</em> le conducteur 1, toutes les lignes de champ issues de 1 arrivent sur 2 : \(Q_1=-Q_{2,int}\). L'ensemble des deux armatures forme un <b>condensateur</b>.</li>
</ul></div>
<div class="box thm"><div class="bt">★ Capacité d'un condensateur</div>
<div class="mq">\[Q=CU\qquad U=V_1-V_2\qquad Q=\text{charge de l'armature interne (ou positive)}\]</div>
<p>\(C\) ne dépend que de la géométrie (et du diélectrique) ; de \(10^{-12}\ \mathrm{F}\) à \(10^{-3}\ \mathrm{F}\) environ.</p></div>
FIG_PLAN
<div class="box method"><div class="bt">▹ Méthode : calculer une capacité</div>
<ol>
<li><b>Schéma</b> et repère adapté ; armatures chargées \(+Q\) et \(-Q\) (influence totale).</li>
<li><b>Champ</b> entre les armatures (Gauss ou plans superposés) en fonction de \(Q\) ou de \(\sigma\), et nul en dehors.</li>
<li><b>Tension</b> \(U=V_1-V_2=\int_1^2\vec E\cdot\mathrm{d}\vec l\) le long d'une ligne de champ.</li>
<li><b>Capacité</b> \(C=\frac{Q}{U}\) : \(Q\) doit se simplifier (si elle reste, c'est une erreur).</li>
</ol></div>
<div class="box thm"><div class="bt">★ Condensateurs usuels</div>
<div class="tbl-wrap s4-stack"><table>
<tr><th>Géométrie</th><th>Champ entre les armatures</th><th>Tension \(U\)</th><th>Capacité \(C\)</th></tr>
<tr><td data-l="Géométrie">Plan (surface \(S\), écart \(e\))</td><td data-l="Champ">\(\dfrac{\sigma}{\varepsilon_0}\vec e_z\) (uniforme)</td><td data-l="Tension">\(\dfrac{\sigma e}{\varepsilon_0}=\dfrac{Qe}{\varepsilon_0S}\)</td><td data-l="Capacité">\(\dfrac{\varepsilon_0S}{e}\)</td></tr>
<tr><td data-l="Géométrie">Cylindrique (\(R_1&lt;R_2\), hauteur \(H\gg R_2\))</td><td data-l="Champ">\(\dfrac{Q}{2\pi\varepsilon_0Hr}\vec e_r\)</td><td data-l="Tension">\(\dfrac{Q}{2\pi\varepsilon_0H}\ln\dfrac{R_2}{R_1}\)</td><td data-l="Capacité">\(\dfrac{2\pi\varepsilon_0H}{\ln(R_2/R_1)}\)</td></tr>
<tr><td data-l="Géométrie">Sphérique (\(R_A&lt;R_B\))</td><td data-l="Champ">\(\dfrac{Q}{4\pi\varepsilon_0r^2}\vec e_r\)</td><td data-l="Tension">\(\dfrac{Q(R_B-R_A)}{4\pi\varepsilon_0R_AR_B}\)</td><td data-l="Capacité">\(\dfrac{4\pi\varepsilon_0R_AR_B}{R_B-R_A}\)</td></tr>
</table></div>
<p>À \(R_2\to R_1\) (écart \(e=R_2-R_1\ll R_1\)), les deux formules cylindrique et sphérique tendent vers \(\frac{\varepsilon_0S}{e}\) avec \(S\) l'aire d'une armature : on retrouve le condensateur plan.</p></div>
<h3 id="ch3-energie">Énergie d'un condensateur</h3>
<div class="box thm"><div class="bt">★ Énergie stockée</div>
<div class="mq">\[W_E=\frac12\,Q\,U=\frac12\,C\,U^2=\frac{Q^2}{2C}\]</div>
<p>C'est l'énergie libérée à la décharge (on ramène \(U\) à zéro). Pour le condensateur plan : \(W_E=\frac12\frac{\varepsilon_0S}{e}(Ee)^2=\frac12\varepsilon_0E^2\times(Se)\) : une <b>densité volumique</b> \(\frac12\varepsilon_0E^2\) dans le volume entre les armatures.</p></div>
<div class="box warn"><div class="bt">⚠ Charge constante ou tension constante ?</div><p>Condensateur <b>isolé</b> : \(Q\) constante. Si on écarte les armatures, \(C\) diminue, \(U=\frac QC\) et \(W_E=\frac{Q^2}{2C}\) augmentent (l'opérateur fournit un travail), le champ \(\frac{\sigma}{\varepsilon_0}\) ne change pas. Condensateur <b>branché</b> sur un générateur : c'est \(U\) qui est constante. Toujours dire laquelle des deux est fixée avant de calculer.</p></div>
<div class="box ex corr-link"><div class="bt">✅ S'entraîner</div><p>Les 6 exercices du TD4 (deux sphères reliées, condensateurs plan, cylindrique, sphérique, disques, annale à trois cylindres) sont corrigés : <a href="corriges.html#td4">voir les corrigés du TD4</a>. Formules : <a href="formules.html#f-cond">conducteurs et condensateurs</a>.</p></div>
</div>
</article>
<!-- CH3:FIN -->
"""

COURS_TOC = """<!-- CH3TOC:DEBUT -->
<a href="#ch3">3 · Conducteurs et condensateurs</a>
<a href="#ch3-ohm">↳ Courant et loi d'Ohm</a>
<a href="#ch3-equilibre">↳ Conducteur à l'équilibre</a>
<a href="#ch3-capa">↳ Capacité d'un conducteur</a>
<a href="#ch3-cond">↳ Condensateurs</a>
<a href="#ch3-energie">↳ Énergie</a>
<!-- CH3TOC:FIN -->
"""

# =============================================================== formules
FORM = r"""<!-- F3:DEBUT -->
<section class="fgroup" id="f-cond">
<h2>Conducteurs et condensateurs</h2>
<div class="frow"><div class="fx">\(I=\displaystyle\iint\vec j\cdot\vec n\,\mathrm{d}S\ \ ;\ \ \vec j=\rho\vec v\ \ ;\ \ \vec j=\gamma\vec E\)</div><div class="fd"><span class="nm">Courant et loi d'Ohm locale</span>. \(\gamma=\frac{ne^2\tau}{m_e}\) (Drude). \(\gamma\) diminue quand \(T\) augmente (métal). <span class="unit">\(\mathrm{A},\ \mathrm{A\,m^{-2}},\ \mathrm{S\,m^{-1}}\)</span></div></div>
<div class="frow"><div class="fx">\(U=RI\ \ ;\ \ R=\dfrac{\ell}{\gamma s}\)</div><div class="fd"><span class="nm">Résistance d'un fil</span>. Section \(s\), longueur \(\ell\), courant uniforme et axial. <span class="unit">\(\Omega\)</span></div></div>
<div class="frow"><div class="fx">\(\vec E_{int}=\vec0\ \ ;\ \ V=\text{cste}\ \ ;\ \ \rho_{int}=0\)</div><div class="fd"><span class="nm">Conducteur à l'équilibre</span>. La charge est à la surface ; le conducteur est un volume équipotentiel. <span class="cond">équilibre électrostatique</span></div></div>
<div class="frow"><div class="fx">\(\vec E_{ext}=\dfrac{\sigma}{\varepsilon_0}\,\vec n_{ext}\)</div><div class="fd"><span class="nm">Théorème de Coulomb</span>. Champ au voisinage immédiat de la surface, normal à celle-ci. <span class="unit">\(\mathrm{V\,m^{-1}}\)</span> <span class="cond">surface d'un conducteur (pas \(\frac{\sigma}{2\varepsilon_0}\))</span></div></div>
<div class="frow"><div class="fx">\(C=\dfrac{Q}{V}\ \ ;\ \ C_{sph}=4\pi\varepsilon_0R\)</div><div class="fd"><span class="nm">Capacité d'un conducteur seul</span>. \(V(\infty)=0\). <span class="unit">\(\mathrm{F}\)</span></div></div>
<div class="frow"><div class="fx">\(\dfrac{\sigma_1}{\sigma_2}=\dfrac{R_2}{R_1}\ \ ;\ \ C=4\pi\varepsilon_0(R_1+R_2)\)</div><div class="fd"><span class="nm">Deux sphères reliées (effet de pointe)</span>. Même potentiel ; \(\sigma\) varie comme \(\frac1R\). <span class="cond">sphères éloignées</span></div></div>
<div class="frow"><div class="fx">\(Q=CU\ \ ;\ \ U=V_1-V_2=\displaystyle\int_1^2\vec E\cdot\mathrm{d}\vec l\)</div><div class="fd"><span class="nm">Condensateur</span>. \(+Q\) sur l'armature de potentiel \(V_1\), \(-Q\) sur l'autre (influence totale). <span class="unit">\(\mathrm{C},\ \mathrm{V}\)</span></div></div>
<div class="frow"><div class="fx">\(C=\dfrac{\varepsilon_0S}{e}\)</div><div class="fd"><span class="nm">Condensateur plan</span>. \(E=\frac{\sigma}{\varepsilon_0}\) entre les armatures, nul dehors. <span class="unit">\(\mathrm{F}\)</span> <span class="cond">\(e\ll\sqrt S\) (effets de bord négligés)</span></div></div>
<div class="frow"><div class="fx">\(C=\dfrac{2\pi\varepsilon_0H}{\ln(R_2/R_1)}\)</div><div class="fd"><span class="nm">Condensateur cylindrique</span>. \(E=\frac{Q}{2\pi\varepsilon_0Hr}\) pour \(R_1&lt;r&lt;R_2\). <span class="unit">\(\mathrm{F}\)</span> <span class="cond">\(H\gg R_2\)</span></div></div>
<div class="frow"><div class="fx">\(C=\dfrac{4\pi\varepsilon_0R_AR_B}{R_B-R_A}\)</div><div class="fd"><span class="nm">Condensateur sphérique</span>. \(E=\frac{Q}{4\pi\varepsilon_0r^2}\) pour \(R_A&lt;r&lt;R_B\). <span class="unit">\(\mathrm{F}\)</span></div></div>
<div class="frow"><div class="fx">\(W_E=\dfrac12QU=\dfrac12CU^2=\dfrac{Q^2}{2C}\)</div><div class="fd"><span class="nm">Énergie d'un condensateur</span>. Densité volumique \(\frac12\varepsilon_0E^2\). <span class="unit">\(\mathrm{J}\)</span> <span class="cond">préciser \(Q\) ou \(U\) constant</span></div></div>
</section>
<!-- F3:FIN -->
"""

EXPRESS_CH3 = r"""<!-- F3EXP:DEBUT -->
<div class="eg"><h4>Conducteurs</h4>
<div class="ei"><span class="nm">Coulomb</span><span class="vl">\(\vec E=\frac{\sigma}{\varepsilon_0}\vec n_{ext}\)</span></div>
<div class="ei"><span class="nm">Sphère</span><span class="vl">\(C=4\pi\varepsilon_0R\)</span></div>
<div class="ei"><span class="nm">Plan</span><span class="vl">\(C=\frac{\varepsilon_0S}{e}\)</span></div>
<div class="ei"><span class="nm">Cylindre</span><span class="vl">\(C=\frac{2\pi\varepsilon_0H}{\ln(R_2/R_1)}\)</span></div>
<div class="ei"><span class="nm">Sphères</span><span class="vl">\(C=\frac{4\pi\varepsilon_0R_AR_B}{R_B-R_A}\)</span></div>
<div class="ei"><span class="nm">Énergie</span><span class="vl">\(W=\frac12CU^2=\frac{Q^2}{2C}\)</span></div>
</div>
<!-- F3EXP:FIN -->
"""

# =============================================================== quiz
Q = [
    ("À l'équilibre électrostatique, le champ à l'intérieur d'un conducteur est :", "nul", ["uniforme et non nul", "dirigé vers la surface", "égal à \\(\\frac{\\sigma}{\\varepsilon_0}\\)"], "Sans courant macroscopique, la loi d'Ohm \\(\\vec j=\\gamma\\vec E=\\vec0\\) impose \\(\\vec E_{int}=\\vec0\\)."),
    ("Où se trouve la charge d'un conducteur à l'équilibre ?", "à la surface", ["répartie dans tout le volume", "au centre", "uniquement aux angles"], "\\(\\vec E_{int}=\\vec0\\) donne \\(\\rho_{int}=0\\) par Gauss : la charge est surfacique."),
    ("Le potentiel à l'intérieur d'un conducteur à l'équilibre est :", "uniforme (constant)", ["nul", "croissant vers la surface", "proportionnel à \\(r\\)"], "\\(\\vec E=-\\overrightarrow{\\mathrm{grad}}\\,V=\\vec0\\) : \\(V\\) est constant, le conducteur est équipotentiel."),
    ("Théorème de Coulomb : au voisinage immédiat de la surface d'un conducteur chargé (densité \\(\\sigma\\)), le champ vaut :", "\\(\\dfrac{\\sigma}{\\varepsilon_0}\\vec n_{ext}\\)", ["\\(\\dfrac{\\sigma}{2\\varepsilon_0}\\vec n_{ext}\\)", "\\(\\dfrac{2\\sigma}{\\varepsilon_0}\\vec n_{ext}\\)", "\\(\\dfrac{\\sigma}{4\\pi\\varepsilon_0}\\vec n_{ext}\\)"], "Le champ du petit plan (\\(\\frac{\\sigma}{2\\varepsilon_0}\\)) s'ajoute à celui du reste du conducteur (même valeur), d'où \\(\\frac{\\sigma}{\\varepsilon_0}\\)."),
    ("Le champ juste à l'extérieur d'un conducteur à l'équilibre est :", "normal à sa surface", ["tangent à sa surface", "toujours nul", "dirigé selon un rayon quelconque"], "La surface est équipotentielle et les lignes de champ lui sont orthogonales."),
    ("Un conducteur neutre contient une cavité avec une charge ponctuelle \\(q\\). La surface interne porte :", "\\(-q\\)", ["\\(+q\\)", "\\(0\\)", "\\(-q/2\\)"], "Gauss sur une surface dans le métal (flux nul) : \\(q+q_{int}=0\\). C'est l'influence totale ; la surface externe porte \\(+q\\)."),
    ("Un conducteur contient une cavité vide de charge. La charge de sa surface interne est :", "nulle", ["égale à celle de la surface externe", "opposée à celle de la surface externe", "infinie"], "Sinon des lignes de champ iraient d'un point à un autre de même potentiel : impossible. C'est la cage de Faraday."),
    ("La capacité d'une boule conductrice de rayon \\(R\\) (dans le vide) vaut :", "\\(4\\pi\\varepsilon_0R\\)", ["\\(4\\pi\\varepsilon_0R^2\\)", "\\(\\dfrac{4\\pi\\varepsilon_0}{R}\\)", "\\(\\varepsilon_0R\\)"], "\\(V=\\frac{Q}{4\\pi\\varepsilon_0R}\\) donc \\(C=\\frac{Q}{V}=4\\pi\\varepsilon_0R\\) : proportionnelle au rayon."),
    ("L'effet de pointe dit que la densité surfacique \\(\\sigma\\) est plus grande :", "là où le rayon de courbure est petit", ["là où le rayon de courbure est grand", "au centre du conducteur", "là où la surface est plane"], "Deux sphères reliées : \\(\\frac{\\sigma_1}{\\sigma_2}=\\frac{R_2}{R_1}\\). Près d'une pointe, le champ \\(\\frac{\\sigma}{\\varepsilon_0}\\) est très intense."),
    ("Deux sphères conductrices de rayons \\(R_1\\) et \\(R_2\\), éloignées, sont reliées par un fil. Le rapport \\(\\frac{\\sigma_1}{\\sigma_2}\\) vaut :", "\\(\\dfrac{R_2}{R_1}\\)", ["\\(\\dfrac{R_1}{R_2}\\)", "\\(\\dfrac{R_1^2}{R_2^2}\\)", "\\(1\\)"], "Même potentiel \\(V=\\frac{\\sigma R}{\\varepsilon_0}\\) : \\(\\sigma_1R_1=\\sigma_2R_2\\)."),
    ("La capacité d'un condensateur plan de surface \\(S\\) et d'écart \\(e\\) vaut :", "\\(\\dfrac{\\varepsilon_0S}{e}\\)", ["\\(\\dfrac{\\varepsilon_0e}{S}\\)", "\\(\\varepsilon_0Se\\)", "\\(\\dfrac{S}{\\varepsilon_0e}\\)"], "\\(E=\\frac{\\sigma}{\\varepsilon_0}\\), \\(U=Ee=\\frac{Qe}{\\varepsilon_0S}\\), \\(C=\\frac QU=\\frac{\\varepsilon_0S}{e}\\)."),
    ("On double l'écart \\(e\\) entre les armatures d'un condensateur plan. Sa capacité :", "est divisée par 2", ["est multipliée par 2", "est multipliée par 4", "ne change pas"], "\\(C=\\frac{\\varepsilon_0S}{e}\\) est inversement proportionnelle à \\(e\\)."),
    ("Le champ d'un condensateur plan idéal (armatures infinies) à l'extérieur des armatures vaut :", "\\(\\vec0\\)", ["\\(\\dfrac{\\sigma}{2\\varepsilon_0}\\vec e_z\\)", "\\(\\dfrac{\\sigma}{\\varepsilon_0}\\vec e_z\\)", "\\(\\dfrac{2\\sigma}{\\varepsilon_0}\\vec e_z\\)"], "Les deux plans \\(+\\sigma\\) et \\(-\\sigma\\) créent des champs opposés à l'extérieur, qui se compensent."),
    ("La capacité d'un condensateur cylindrique (rayons \\(R_1&lt;R_2\\), hauteur \\(H\\)) vaut :", "\\(\\dfrac{2\\pi\\varepsilon_0H}{\\ln(R_2/R_1)}\\)", ["\\(\\dfrac{2\\pi\\varepsilon_0H}{R_2-R_1}\\)", "\\(2\\pi\\varepsilon_0H\\ln\\dfrac{R_2}{R_1}\\)", "\\(\\dfrac{4\\pi\\varepsilon_0H}{\\ln(R_2/R_1)}\\)"], "\\(E=\\frac{Q}{2\\pi\\varepsilon_0Hr}\\), \\(U=\\frac{Q}{2\\pi\\varepsilon_0H}\\ln\\frac{R_2}{R_1}\\), \\(C=\\frac QU\\)."),
    ("La capacité d'un condensateur sphérique (\\(R_A&lt;R_B\\)) vaut :", "\\(\\dfrac{4\\pi\\varepsilon_0R_AR_B}{R_B-R_A}\\)", ["\\(4\\pi\\varepsilon_0(R_B-R_A)\\)", "\\(\\dfrac{4\\pi\\varepsilon_0(R_B-R_A)}{R_AR_B}\\)", "\\(4\\pi\\varepsilon_0R_AR_B\\)"], "\\(U=\\frac{Q}{4\\pi\\varepsilon_0}\\big(\\frac1{R_A}-\\frac1{R_B}\\big)=\\frac{Q(R_B-R_A)}{4\\pi\\varepsilon_0R_AR_B}\\)."),
    ("L'énergie stockée dans un condensateur de capacité \\(C\\) sous la tension \\(U\\) est :", "\\(\\dfrac12CU^2\\)", ["\\(CU^2\\)", "\\(\\dfrac12CU\\)", "\\(\\dfrac{C}{2U^2}\\)"], "\\(W_E=\\frac12QU\\) avec \\(Q=CU\\), soit \\(\\frac12CU^2=\\frac{Q^2}{2C}\\)."),
    ("Un condensateur plan isolé (charge \\(Q\\) constante) voit son écart doubler. L'énergie stockée :", "double", ["est divisée par 2", "est multipliée par 4", "reste constante"], "\\(W_E=\\frac{Q^2}{2C}\\) avec \\(C\\) divisée par 2 : \\(W_E\\) double. Le surplus est le travail fourni par l'opérateur."),
    ("La loi d'Ohm locale s'écrit :", "\\(\\vec j=\\gamma\\vec E\\)", ["\\(\\vec E=\\gamma\\vec j\\)", "\\(\\vec j=\\gamma\\,\\overrightarrow{\\mathrm{grad}}\\,V\\)", "\\(\\vec j=\\dfrac{\\vec E}{\\gamma}\\)"], "\\(\\gamma\\) (en \\(\\mathrm{S\\,m^{-1}}\\)) est la conductivité. Avec \\(U=E\\ell\\) et \\(I=jS\\), on retrouve \\(U=RI\\), \\(R=\\frac{\\ell}{\\gamma S}\\)."),
]

# =============================================================== corrigés TD4
TD4 = []

TD4.append(exo('td4-1', '1', 'Deux sphères conductrices reliées par un fil', 'TD',
    "Deux sphères conductrices à l'équilibre, \\(S_1\\) et \\(S_2\\) de rayons \\(R_1\\) et \\(R_2\\), chargées, sont reliées par un fil conducteur mais maintenues à une distance très grande devant leurs rayons (charge du fil négligée). 1) Faire un schéma. 2) Comparer les densités superficielles \\(\\sigma_1\\) et \\(\\sigma_2\\). 3) Capacité du conducteur formé.",
    "<p>Deux conducteurs reliés par un fil n'en font qu'<b>un seul</b> : à l'équilibre, ils sont au <b>même potentiel</b> \\(V\\). Comme les sphères sont très éloignées, chacune se comporte comme si l'autre n'existait pas (influence négligeable) : sa charge est uniforme et son potentiel vaut \\(\\frac{Q_i}{4\\pi\\varepsilon_0R_i}\\). On égalise les potentiels pour comparer les densités.</p>",
    [("Schéma", "<p>Voir la figure : deux sphères, un fil, \\(d\\gg R_1,R_2\\).</p>"),
     ("Potentiels égaux", "<p>Pour une sphère isolée de charge \\(Q_i\\) : \\(V_i=\\dfrac{Q_i}{4\\pi\\varepsilon_0R_i}=\\dfrac{\\sigma_i4\\pi R_i^2}{4\\pi\\varepsilon_0R_i}=\\dfrac{\\sigma_iR_i}{\\varepsilon_0}\\). Avec \\(V_1=V_2=V\\) :</p>" + mq(r"\frac{\sigma_1R_1}{\varepsilon_0}=\frac{\sigma_2R_2}{\varepsilon_0}\ \Longrightarrow\ \frac{\sigma_1}{\sigma_2}=\frac{R_2}{R_1}")),
     ("Capacité", "<p>Charge totale \\(Q=Q_1+Q_2=4\\pi\\varepsilon_0(R_1+R_2)V\\) (on néglige la charge du fil), donc</p>" + mq(r"C=\frac{Q}{V}=4\pi\varepsilon_0\,(R_1+R_2)=C_1+C_2"))],
    r"\(\dfrac{\sigma_1}{\sigma_2}=\dfrac{R_2}{R_1}\) : la petite sphère porte la plus grande densité (effet de pointe) ; \(C=4\pi\varepsilon_0(R_1+R_2)\), somme des deux capacités.",
    "Ne pas dire que les <em>charges</em> sont égales : ce sont les <em>potentiels</em> qui le sont. \\(Q_1/Q_2=R_1/R_2\\), alors que \\(\\sigma_1/\\sigma_2=R_2/R_1\\) (inverse).",
    FIG['td4_ex1']))

TD4.append(exo('td4-2', '2', 'Capacité d\'un condensateur plan', 'TD',
    "Deux armatures métalliques à l'équilibre, parallèles, de même surface \\(S\\) très grande devant l'épaisseur \\(e\\), chargées uniformément, dans le vide. 1) Définition d'un conducteur en équilibre. 2) Définition d'un condensateur. 3) Représenter le système avec le repère. 4) Champ d'un plan infini chargé (calculé), puis champ du condensateur partout. 5) Circulation du champ entre les armatures, lien avec le potentiel. 6) \\(U=V_1-V_2\\). 7) Capacité en fonction de \\(S\\) et \\(e\\).",
    "<p>On connaît le champ d'un plan infini chargé uniformément (à calculer par Gauss). Le condensateur plan, ce sont <b>deux plans</b> de charges opposées : on <b>superpose</b> leurs champs. On intègre ensuite le champ le long d'une ligne de champ (droite selon \\(z\\)) pour obtenir \\(U\\), puis \\(C=\\frac QU\\).</p>",
    [("Définitions (questions 1 et 2)", "<p>Un conducteur est à l'équilibre si ses charges libres ne se déplacent plus : \\(\\vec E_{int}=\\vec0\\), potentiel uniforme, charge à la surface. Un condensateur est un ensemble de deux conducteurs (armatures) en <b>influence totale</b> : \\(Q_1=-Q_2\\) ; il est caractérisé par \\(Q=CU\\).</p>"),
     ("Repère (question 3)", "<p>Axe \\(Oz\\) perpendiculaire aux armatures : armature 1 (charge \\(+Q\\), densité \\(+\\sigma\\)) en \\(z=0\\), armature 2 (\\(-Q\\), \\(-\\sigma\\)) en \\(z=e\\) ; \\(Q=\\sigma S\\).</p>"),
     ("Champ d'un plan infini (question 4)", "<p>Symétries : \\(\\vec E=E(z)\\vec e_z\\), \\(E(-z)=-E(z)\\). Gauss sur un cylindre d'axe \\(Oz\\), de base \\(S_0\\), à cheval sur le plan : \\(2S_0E=\\frac{\\sigma S_0}{\\varepsilon_0}\\), donc \\(\\vec E=\\pm\\dfrac{\\sigma}{2\\varepsilon_0}\\vec e_z\\) (\\(+\\) pour \\(z&gt;0\\)). Superposition des plans \\(z=0\\) (\\(+\\sigma\\)) et \\(z=e\\) (\\(-\\sigma\\)) :</p>" + mq(r"z<0:\ \ -\frac{\sigma}{2\varepsilon_0}+\frac{\sigma}{2\varepsilon_0}=0\qquad 0<z<e:\ \ \frac{\sigma}{2\varepsilon_0}+\frac{\sigma}{2\varepsilon_0}=\frac{\sigma}{\varepsilon_0}\qquad z>e:\ \ 0").replace('z<0', r'z\lt0').replace('0<z<e', r'0\lt z\lt e').replace('z>e', r'z\gt e')),
     ("Circulation et potentiel (questions 5 et 6)", "<p>Chemin : le segment de droite de \\(z=0\\) à \\(z=e\\) le long d'une ligne de champ, \\(\\mathrm{d}\\vec l=\\mathrm{d}z\\,\\vec e_z\\) :</p>" + mq(r"\int_{1}^{2}\vec E\cdot\mathrm{d}\vec l=\int_0^e\frac{\sigma}{\varepsilon_0}\,\mathrm{d}z=\frac{\sigma e}{\varepsilon_0}=V_1-V_2") + "<p>La circulation de \\(\\vec E\\) entre deux points est la différence de potentiel (\\(V_A-V_B=\\int_A^B\\vec E\\cdot\\mathrm{d}\\vec l\\)).</p>"),
     ("Capacité (question 7)", "<p>\\(Q=\\sigma S\\) et \\(U=\\dfrac{\\sigma e}{\\varepsilon_0}\\) :</p>" + mq(r"C=\frac{Q}{U}=\frac{\sigma S}{\sigma e/\varepsilon_0}=\frac{\varepsilon_0S}{e}"))],
    r"\(\vec E=\dfrac{\sigma}{\varepsilon_0}\vec e_z\) entre les armatures, \(\vec0\) ailleurs ; \(U=\dfrac{\sigma e}{\varepsilon_0}=\dfrac{Qe}{\varepsilon_0S}\) ; \(C=\dfrac{\varepsilon_0S}{e}\).",
    "Le champ \\(\\frac{\\sigma}{\\varepsilon_0}\\) (et non \\(\\frac{\\sigma}{2\\varepsilon_0}\\)) vient de la <em>somme</em> des deux plans. Et \\(\\sigma\\) disparaît de \\(C\\) : une capacité ne dépend que de la géométrie.",
    FIG['td4_plan']))

TD4.append(exo('td4-3', '3', 'Capacité d\'un condensateur cylindrique', 'TD',
    "Armature cylindrique intérieure de rayon \\(R_1\\), hauteur \\(H\\), charge \\(+Q\\), entourée d'une armature de rayon \\(R_2&gt;R_1\\), hauteur \\(H\\), charge \\(-Q\\) ; coaxiales ; \\(H\\gg R_1,R_2\\). Densités uniformes \\(\\sigma_1\\) et \\(\\sigma_2\\). 1) \\(\\sigma_1,\\sigma_2\\) en fonction des données. 2) Champ d'un cylindre infini d'axe \\(Oz\\), de rayon \\(R\\), de densité \\(\\sigma\\). 3) Champ du condensateur en fonction des densités. 4) Pourquoi \\(\\vec E=\\vec0\\) à l'extérieur ? 5) \\(U=V_1-V_2\\) puis \\(C\\).",
    "<p>\\(H\\gg R\\) : on traite les cylindres comme infinis (symétrie cylindrique, Gauss). Le champ du condensateur est la superposition des champs des deux cylindres ; la condition \\(Q_1=-Q_2\\) (influence totale) annule le champ à l'extérieur. On intègre \\(E(r)\\,\\mathrm{d}r\\) de \\(R_1\\) à \\(R_2\\).</p>",
    [("Densités (question 1)", "<p>Surface latérale \\(2\\pi RH\\) :</p>" + mq(r"\sigma_1=\frac{Q}{2\pi R_1H}\qquad\sigma_2=-\frac{Q}{2\pi R_2H}\qquad\Longrightarrow\ \ \sigma_1R_1=-\sigma_2R_2")),
     ("Cylindre infini de densité \\(\\sigma\\) (question 2)", "<p>Symétries : \\(\\vec E=E(r)\\vec e_r\\). Gauss sur un cylindre coaxial de rayon \\(r\\), hauteur \\(h\\) : \\(2\\pi rhE=\\frac{Q_{int}}{\\varepsilon_0}\\), avec \\(Q_{int}=0\\) pour \\(r&lt;R\\) et \\(\\sigma2\\pi Rh\\) pour \\(r&gt;R\\) :</p>" + mq(r"\vec E=\vec0\ \ (r\lt R)\qquad\vec E=\frac{\sigma R}{\varepsilon_0r}\vec e_r\ \ (r\gt R)")),
     ("Superposition (question 3)", "<p>Avec les deux cylindres :</p>" + mq(r"r\lt R_1:\ \vec0\qquad R_1\lt r\lt R_2:\ \ \vec E=\frac{\sigma_1R_1}{\varepsilon_0r}\vec e_r\qquad r\gt R_2:\ \ \frac{\sigma_1R_1+\sigma_2R_2}{\varepsilon_0r}\vec e_r")),
     ("Champ nul à l'extérieur (question 4)", "<p>\\(\\sigma_1R_1+\\sigma_2R_2=\\dfrac{Q}{2\\pi H}-\\dfrac{Q}{2\\pi H}=0\\) : charges totales opposées (influence totale), donc \\(\\vec E=\\vec0\\) pour \\(r&gt;R_2\\). Par Gauss : le flux sur une surface englobant les deux cylindres est nul.</p>"),
     ("Tension et capacité (question 5)", "<p>Entre les armatures, \\(E=\\dfrac{Q}{2\\pi\\varepsilon_0Hr}\\) :</p>" + mq(r"U=V_1-V_2=\int_{R_1}^{R_2}E\,\mathrm{d}r=\frac{Q}{2\pi\varepsilon_0H}\ln\frac{R_2}{R_1}") + mq(r"C=\frac{Q}{U}=\frac{2\pi\varepsilon_0H}{\ln(R_2/R_1)}"))],
    r"\(\vec E=\dfrac{Q}{2\pi\varepsilon_0Hr}\vec e_r\) pour \(R_1&lt;r&lt;R_2\), nul ailleurs ; \(U=\dfrac{Q}{2\pi\varepsilon_0H}\ln\dfrac{R_2}{R_1}\) ; \(C=\dfrac{2\pi\varepsilon_0H}{\ln(R_2/R_1)}\).",
    "Le logarithme porte sur un rapport \\(\\frac{R_2}{R_1}\\), sans dimension ; \\(C\\) est proportionnelle à \\(H\\) (on donne souvent \\(\\frac CH\\) en \\(\\mathrm{F\\,m^{-1}}\\)).",
    FIG['td4_ex3']))

TD4.append(exo('td4-4', '4', 'Condensateur sphérique', 'TD',
    "Deux conducteurs sphériques concentriques A et B, en influence totale, forment un condensateur sphérique ; l'un est creux. \\(R_A\\) : rayon extérieur de A ; \\(R_B\\) : rayon intérieur de B. Densités uniformes \\(\\sigma_A\\) et \\(\\sigma_B\\). 1) Schéma. 2) \\(\\sigma_A,\\sigma_B\\) en fonction des données. 3) Champ d'une sphère de rayon \\(R\\) et de densité \\(\\sigma\\). 4) Champ du condensateur. 5) Pourquoi \\(\\vec E=\\vec0\\) à l'extérieur ? 6) \\(V_A-V_B\\). 7) Capacité.",
    "<p>Même démarche que pour le condensateur cylindrique, en symétrie sphérique : Gauss sur une sphère de rayon \\(r\\), superposition des deux sphères chargées, puis \\(U=\\int E\\,\\mathrm{d}r\\) et \\(C=\\frac QU\\).</p>",
    [("Densités (question 2)", "<p>A porte \\(+Q\\), la face interne de B porte \\(-Q\\) (influence totale) :</p>" + mq(r"\sigma_A=\frac{Q}{4\pi R_A^2}\qquad\sigma_B=-\frac{Q}{4\pi R_B^2}\qquad\Longrightarrow\ \ \sigma_AR_A^2=-\sigma_BR_B^2")),
     ("Une sphère de densité \\(\\sigma\\) (question 3)", "<p>Symétrie sphérique : \\(\\vec E=E(r)\\vec e_r\\), \\(4\\pi r^2E=\\frac{Q_{int}}{\\varepsilon_0}\\) :</p>" + mq(r"\vec E=\vec0\ \ (r\lt R)\qquad\vec E=\frac{\sigma R^2}{\varepsilon_0r^2}\vec e_r\ \ (r\gt R)")),
     ("Superposition et extérieur (questions 4 et 5)", "<p>Pour \\(R_A&lt;r&lt;R_B\\), seule la sphère A agit (B est une coque, son champ est nul à l'intérieur) ; pour \\(r&gt;R_B\\) :</p>" + mq(r"R_A\lt r\lt R_B:\ \ \vec E=\frac{\sigma_AR_A^2}{\varepsilon_0r^2}\vec e_r=\frac{Q}{4\pi\varepsilon_0r^2}\vec e_r\qquad r\gt R_B:\ \ \frac{\sigma_AR_A^2+\sigma_BR_B^2}{\varepsilon_0r^2}=0") + "<p>Le champ est nul à l'extérieur car la charge totale est nulle (\\(+Q-Q\\)).</p>"),
     ("Tension (question 6)", mq(r"V_A-V_B=\int_{R_A}^{R_B}\frac{Q}{4\pi\varepsilon_0r^2}\,\mathrm{d}r=\frac{Q}{4\pi\varepsilon_0}\Big(\frac1{R_A}-\frac1{R_B}\Big)=\frac{Q\,(R_B-R_A)}{4\pi\varepsilon_0R_AR_B}")),
     ("Capacité (question 7)", mq(r"C=\frac{Q}{V_A-V_B}=\frac{4\pi\varepsilon_0R_AR_B}{R_B-R_A}") + "<p>Si \\(R_B\\to\\infty\\) : \\(C\\to4\\pi\\varepsilon_0R_A\\), la capacité de la sphère seule.</p>")],
    r"\(\vec E=\dfrac{Q}{4\pi\varepsilon_0r^2}\vec e_r\) pour \(R_A&lt;r&lt;R_B\), nul ailleurs ; \(V_A-V_B=\dfrac{Q(R_B-R_A)}{4\pi\varepsilon_0R_AR_B}\) ; \(C=\dfrac{4\pi\varepsilon_0R_AR_B}{R_B-R_A}\).",
    "Ne pas confondre \\(R_A\\) (rayon <em>extérieur</em> de A) et \\(R_B\\) (rayon <em>intérieur</em> de B). Test : \\(R_B\\to R_A\\) doit donner \\(C\\to\\infty\\) (armatures collées).",
    FIG['td4_ex4']))

TD4.append(exo('td4-5', '5', 'Condensateur à disques : géométrie, application et déplacement', 'TD',
    "Condensateur formé de deux disques \\((D_0)\\) et \\((D_1)\\), de même rayon \\(a\\), de même axe \\(Oz\\), parallèles, distants de \\(e\\), séparés par du vide (\\(\\varepsilon_0\\)), en influence totale, portés aux potentiels \\(V_0\\) et \\(V_1\\) (\\(V_0&gt;V_1\\)). <b>A.</b> 1) Schéma et repère. 2) Condition pour le traiter comme un condensateur plan infini. 3) \\(V(z)\\) entre les armatures en fonction de \\(\\sigma\\). 4) Équipotentielles et lignes de champ. 5) Capacité \\(C_0\\). AN : écart minimal dans l'air pour supporter \\(500\\ \\mathrm{V}\\), champ maximal \\(3\\times10^6\\ \\mathrm{V\\,m^{-1}}\\). <b>B.</b> Condensateur isolé (charge constante) : on éloigne l'armature négative de \\(h\\) (écart \\(e+h\\)). 1) Nouvelle tension. 2) Travail de l'opérateur. 3) Variation de l'énergie potentielle ; conclure.",
    "<p>Partie A : si \\(e\\ll a\\), les disques sont presque des plans infinis (on néglige les effets de bord) : champ uniforme entre eux, \\(\\vec E=\\frac{\\sigma}{\\varepsilon_0}\\vec e_z\\). Partie B : <b>isolé</b> veut dire \\(Q\\) (donc \\(\\sigma\\) et \\(E\\)) constant ; seule \\(U\\) change. Le travail de l'opérateur est égal au gain d'énergie du condensateur.</p>",
    [("Partie A : repère et condition (questions 1 et 2)", "<p>Repère \\(Oz\\) selon l'axe, \\(D_0\\) en \\(z=0\\), \\(D_1\\) en \\(z=e\\) (voir figure). Condensateur plan infini si <b>\\(e\\ll a\\)</b> (négliger les effets de bord).</p>" + FIG['td4_ex5']),
     ("Potentiel \\(V(z)\\) (question 3)", "<p>\\(\\vec E=\\frac{\\sigma}{\\varepsilon_0}\\vec e_z\\), \\(\\mathrm{d}V=-E\\,\\mathrm{d}z\\), \\(V(0)=V_0\\) :</p>" + mq(r"V(z)=V_0-\frac{\sigma}{\varepsilon_0}\,z\qquad V(e)=V_1\ \Longrightarrow\ \sigma=\frac{\varepsilon_0(V_0-V_1)}{e}")),
     ("Équipotentielles et lignes de champ (question 4)", "<p>Les équipotentielles sont des <b>plans parallèles aux disques</b> (\\(V\\) ne dépend que de \\(z\\)) ; les lignes de champ sont des droites parallèles à \\(Oz\\), orientées de \\(D_0\\) (potentiel le plus haut) vers \\(D_1\\). Sur les bords, elles se courbent (effet de bord).</p>"),
     ("Capacité et application numérique (question 5)", "<p>\\(S=\\pi a^2\\) :</p>" + mq(r"C_0=\frac{\varepsilon_0\pi a^2}{e}") + "<p>Le champ ne doit pas dépasser \\(E_{max}=3\\times10^6\\ \\mathrm{V\\,m^{-1}}\\) : \\(E=\\frac Ue\\le E_{max}\\), donc</p>" + mq(r"e_{min}=\frac{U}{E_{max}}=\frac{500}{3\times10^6}\approx1{,}7\times10^{-4}\ \mathrm{m}\approx0{,}17\ \mathrm{mm}")),
     ("Partie B : nouvelle tension (question 1)", "<p>\\(Q\\) constante, donc \\(\\sigma\\) et \\(E=\\frac{\\sigma}{\\varepsilon_0}\\) inchangés ; l'écart passe à \\(e+h\\) :</p>" + mq(r"U'=E\,(e+h)=\frac{Q\,(e+h)}{\varepsilon_0S}=U\Big(1+\frac he\Big)")),
     ("Travail de l'opérateur (question 2)", "<p>L'armature positive crée, au niveau de l'autre, un champ \\(\\frac{\\sigma}{2\\varepsilon_0}\\) (champ d'un seul plan) : l'armature négative subit la force attractive \\(F=Q\\frac{\\sigma}{2\\varepsilon_0}=\\dfrac{Q^2}{2\\varepsilon_0S}\\), constante. L'opérateur l'équilibre et déplace de \\(h\\) :</p>" + mq(r"W_{op}=F\,h=\frac{Q^2h}{2\varepsilon_0S}")),
     ("Variation d'énergie (question 3)", mq(r"\Delta W_E=\frac{Q^2}{2C'}-\frac{Q^2}{2C_0}=\frac{Q^2}{2\varepsilon_0S}\big[(e+h)-e\big]=\frac{Q^2h}{2\varepsilon_0S}") + "<p>On trouve \\(\\Delta W_E=W_{op}\\) : le travail fourni par l'opérateur est entièrement stocké dans le champ (énergie \\(\\frac12\\varepsilon_0E^2\\) dans le volume supplémentaire \\(Sh\\)). Conservation de l'énergie.</p>" + FIG['td4_ex5b'])],
    r"A) \(V(z)=V_0-\frac{\sigma}{\varepsilon_0}z\), \(C_0=\frac{\varepsilon_0\pi a^2}{e}\), \(e_{min}\approx0{,}17\ \mathrm{mm}\). B) \(U'=U\big(1+\frac he\big)\), \(W_{op}=\Delta W_E=\dfrac{Q^2h}{2\varepsilon_0S}\) (on fournit de l'énergie en écartant les armatures).",
    "À <b>charge constante</b>, \\(E\\) reste le même mais \\(U\\) augmente ; à <b>tension constante</b> (générateur branché), ce serait l'inverse. Le champ d'une armature seule vaut \\(\\frac{\\sigma}{2\\varepsilon_0}\\), pas \\(\\frac{\\sigma}{\\varepsilon_0}\\), pour le calcul de la force.",
    ''))

TD4.append(exo('td4-6', '6', 'Annale : trois cylindres coaxiaux', 'Annale',
    "Trois cylindres coaxiaux de hauteur \\(h\\gg R_1,R_2,R_3\\) : cylindre plein (1) de rayon \\(R_1\\), charge \\(+Q\\), potentiel \\(V_1\\) ; cylindre creux (2) de rayon \\(R_2\\), charge \\(-Q\\), potentiel \\(V_2\\) ; cylindre creux (3) de rayon \\(R_3\\), charge \\(+Q\\), potentiel \\(V_3\\). Charges en surface. 1) Direction et dépendances du champ. 2) Champ en tout point en fonction des densités. 3) On relie (3) à la Terre : montrer que la capacité par unité de longueur du condensateur (1)–(2) vaut \\(\\frac{2\\pi\\varepsilon_0}{\\ln(R_2/R_1)}\\). 4) Que devient la capacité si \\(R_1\\approx R_2\\) (\\(e=R_2-R_1\\)) ? 5) À quel condensateur cela fait-il penser ?",
    "<p>Symétrie cylindrique, Gauss région par région : \\(Q_{int}\\) change à chaque cylindre traversé (\\(+Q\\), puis \\(+Q-Q=0\\), puis \\(+Q\\)). Pour la question 3, la mise à la Terre fixe \\(V_3=0\\) et annule la charge du cylindre extérieur (le champ extérieur disparaît) : (1) et (2) forment alors un condensateur cylindrique complet.</p>",
    [("Direction et dépendances (question 1)", "<p>Tout plan contenant l'axe et tout plan perpendiculaire à l'axe sont des plans de symétrie pour la distribution : \\(\\vec E\\) est selon \\(\\vec e_r\\). Les cylindres sont infinis (\\(h\\gg R_i\\)) : invariance par translation selon \\(z\\) et par rotation autour de \\(Oz\\) :</p>" + mq(r"\vec E(M)=E(r)\,\vec e_r")),
     ("Champ par Gauss (question 2)", "<p>Cylindre de Gauss de rayon \\(r\\), hauteur \\(H\\) : \\(2\\pi rHE=\\frac{Q_{int}}{\\varepsilon_0}\\). Densités : \\(\\sigma_1=\\frac{Q}{2\\pi R_1h}\\), \\(\\sigma_2=-\\frac{Q}{2\\pi R_2h}\\), \\(\\sigma_3=\\frac{Q}{2\\pi R_3h}\\). Charge intérieure par hauteur \\(H\\) : \\(2\\pi H\\sum\\sigma_iR_i\\) :</p>" + mq(r"E(r)=\begin{cases}0&amp;r\lt R_1\\[2pt]\dfrac{\sigma_1R_1}{\varepsilon_0r}=\dfrac{Q}{2\pi\varepsilon_0hr}&amp;R_1\lt r\lt R_2\\[6pt]\dfrac{\sigma_1R_1+\sigma_2R_2}{\varepsilon_0r}=0&amp;R_2\lt r\lt R_3\\[6pt]\dfrac{\sigma_1R_1+\sigma_2R_2+\sigma_3R_3}{\varepsilon_0r}=\dfrac{Q}{2\pi\varepsilon_0hr}&amp;r\gt R_3\end{cases}") + "<p>Le champ est donc nul entre (2) et (3) : (3) n'a pas de charge sur sa face interne.</p>"),
     ("Mise à la Terre de (3) (question 3)", "<p>\\(V_3=0\\) : (3), relié à la Terre, perd sa charge extérieure (le champ pour \\(r&gt;R_3\\) disparaît ; entre (2) et (3) il était déjà nul), donc \\(V_2=V_3=0\\). Pour (1) et (2) (charges \\(+Q\\) et \\(-Q\\), influence totale) :</p>" + mq(r"V_1-V_2=\int_{R_1}^{R_2}\frac{Q}{2\pi\varepsilon_0hr}\,\mathrm{d}r=\frac{Q}{2\pi\varepsilon_0h}\ln\frac{R_2}{R_1}") + mq(r"\frac{C}{h}=\frac{Q}{h\,(V_1-V_2)}=\frac{2\pi\varepsilon_0}{\ln(R_2/R_1)}\qquad[\mathrm{F\,m^{-1}}]")),
     ("Armatures très proches (question 4)", "<p>\\(R_2=R_1+e\\) avec \\(e\\ll R_1\\) : \\(\\ln\\dfrac{R_2}{R_1}=\\ln\\Big(1+\\dfrac{e}{R_1}\\Big)\\approx\\dfrac{e}{R_1}\\), donc</p>" + mq(r"C\approx\frac{2\pi\varepsilon_0R_1h}{e}=\frac{\varepsilon_0S}{e}\quad\text{avec}\ \ S=2\pi R_1h")),
     ("Interprétation (question 5)", "<p>On retrouve exactement la capacité du <b>condensateur plan</b> de surface \\(S=2\\pi R_1h\\) (aire de l'armature) et d'écart \\(e\\) : quand l'écart est faible devant le rayon de courbure, une armature cylindrique est localement plane. Même conclusion pour le condensateur sphérique.</p>" + FIG['td4_ex6'])],
    r"\(\vec E=E(r)\vec e_r\) ; \(E=0\) pour \(r&lt;R_1\) et pour \(R_2&lt;r&lt;R_3\) ; \(E=\dfrac{Q}{2\pi\varepsilon_0hr}\) pour \(R_1&lt;r&lt;R_2\) et pour \(r&gt;R_3\). \(\dfrac Ch=\dfrac{2\pi\varepsilon_0}{\ln(R_2/R_1)}\) ; si \(R_1\approx R_2\) : \(C=\dfrac{\varepsilon_0S}{e}\), condensateur plan.",
    "Le champ n'est pas nul pour \\(r&gt;R_3\\) <em>avant</em> la mise à la Terre : la charge totale vaut \\(+Q\\). Penser à calculer \\(Q_{int}\\) région par région, sans oublier le signe de chaque cylindre.",
    ''))

TD4_SEC = ('<!-- TD4:DEBUT -->\n<section class="cx-chap" id="td4">\n<div class="cx-chap-hd">\n<span class="cx-chap-n">TD 4 · Conducteurs et condensateurs</span>\n'
           '<h2>Capacités et énergie</h2>\n'
           '<p>Même schéma pour tous les condensateurs : <b>champ</b> entre les armatures (Gauss, superposition, influence totale), <b>tension</b> par intégration le long d\'une ligne de champ, puis <b>\\(C=\\frac QU\\)</b>. <a href="cours.html#ch3">Revoir le cours (Ch3)</a></p>\n</div>\n'
           + '\n'.join(TD4) + '\n</section>\n<!-- TD4:FIN -->\n')

TD4_CARD = ('<!-- TD4CARD:DEBUT -->\n<a class="cx-card" href="#td4"><span class="n">TD 4 · 4 pages · 6 fiches</span><span class="t">Conducteurs et condensateurs</span>'
            '<span class="d">Sphères reliées, condensateurs plan, cylindrique, sphérique, disques, annale à trois cylindres.</span><span class="cnt"></span><span class="bar"><i></i></span></a>\n<!-- TD4CARD:FIN -->\n')


# =============================================================== insertion idempotente
def remplace_bloc(s, tag, bloc, ancre, avant=True):
    """remplace le bloc <!-- TAG:DEBUT -->..<!-- TAG:FIN --> ou l'insère avant/après l'ancre"""
    pat = re.compile(r'<!-- %s:DEBUT -->.*?<!-- %s:FIN -->\n?' % (tag, tag), re.S)
    if pat.search(s):
        return pat.sub(lambda m: bloc, s, count=1)
    i = s.index(ancre)
    if not avant:
        i += len(ancre)
    return s[:i] + bloc + s[i:]


# cours.html
s = lire('cours.html')
cours = COURS.replace('FIG_COND_POINTE', FIG['cond_pointe']).replace('FIG_CAVITE', FIG['cavite']).replace('FIG_PLAN', FIG['plan'])
s = remplace_bloc(s, 'CH3', cours, '</div>\n</div>\n</div>\n</main>')
s = remplace_bloc(s, 'CH3TOC', COURS_TOC, '</aside>')
s = s.replace('outils mathématiques, électrostatique (charges, Coulomb, symétries, Gauss) et potentiel électrostatique.', 'outils mathématiques, électrostatique (charges, Coulomb, symétries, Gauss), potentiel électrostatique, conducteurs et condensateurs.')
ecrire('cours.html', s)

# formules.html
s = lire('formules.html')
s = remplace_bloc(s, 'F3', FORM, '<section class="fgroup" id="f-express">')
if 'href="#f-cond"' not in s:
    s = s.replace('<a href="#f-pot">Potentiel et énergie</a>', '<a href="#f-pot">Potentiel et énergie</a>\n<a href="#f-cond">Conducteurs et condensateurs</a>', 1)
if 'F3EXP:DEBUT' in s:
    s = remplace_bloc(s, 'F3EXP', EXPRESS_CH3, '')
else:
    i = s.index('<div class="eg"><h4>Charges</h4>')
    s = s[:i] + EXPRESS_CH3 + s[i:]
ecrire('formules.html', s)

# quiz.html
s = lire('quiz.html')
items = []
for q, bon, mauvais, exp in Q:
    opts = [bon] + mauvais
    items.append('<li data-c="0" data-exp="%s"><p>%s</p><ul>%s</ul></li>'
                 % (html.escape(exp, quote=True).replace('&amp;lt;', '&lt;').replace('&amp;gt;', '&gt;'), q,
                    ''.join('<li>%s</li>' % o for o in opts)))
bloc = '<!-- QCH3:DEBUT -->\n' + '\n'.join(items) + '\n<!-- QCH3:FIN -->\n'
s = remplace_bloc(s, 'QCH3', bloc, '</ol>\n</div>\n</main>')
n_total = s.count('<li data-c=')
s = re.sub(r'\d+ questions à choix unique : repères, gradient, flux, charges \(interro\), Coulomb, symétries et Gauss \(DS1\), puis potentiel et énergie \(Ch2\)\.',
           '%d questions à choix unique : repères, gradient, flux, charges (interro), Coulomb, symétries et Gauss (DS1), potentiel et énergie (Ch2), puis conducteurs et condensateurs (Ch3).' % n_total, s)
s = re.sub(r'<button data-n="\d+" type="button">Les \d+</button>', '<button data-n="%d" type="button">Les %d</button>' % (n_total, n_total), s)
ecrire('quiz.html', s)

# corriges.html
s = lire('corriges.html')
s = remplace_bloc(s, 'TD4', TD4_SEC, '</div>\n</main>\n<div class="foot">')
s = remplace_bloc(s, 'TD4CARD', TD4_CARD, '</nav>\n<div class="cx-toolbar">')
s = s.replace('<h1>TD0, TD1, TD2bis, Gauss et TD3 (potentiel) corrigés pas à pas</h1>', '<h1>TD0, TD1, TD2bis, Gauss, TD3 (potentiel) et TD4 (condensateurs) corrigés pas à pas</h1>')
ecrire('corriges.html', s)

# index.html
s = lire('index.html')
s = s.replace('<div class="n">3</div><div class="l">Chapitres</div>', '<div class="n">4</div><div class="l">Chapitres</div>')
s = re.sub(r'<div class="n">\d+</div><div class="l">Fiches corrigées</div>', '<div class="n">%d</div><div class="l">Fiches corrigées</div>' % (len(re.findall(r'<article class="cx" id=', lire('corriges.html')))), s)
s = re.sub(r'<div class="n">\d+</div><div class="l">Questions de quiz</div>', '<div class="n">%d</div><div class="l">Questions de quiz</div>' % n_total, s)
s = re.sub(r'<p>\d+ questions à choix multiples', '<p>%d questions à choix multiples' % n_total, s)
s = s.replace('Ch1 électrostatique (charges, Coulomb, symétries, Gauss) et Ch2 potentiel et énergie.</p><span class="tag">3 chapitres →</span>', 'Ch1 électrostatique (charges, Coulomb, symétries, Gauss), Ch2 potentiel et énergie et Ch3 conducteurs et condensateurs.</p><span class="tag">4 chapitres →</span>')
carte = ('<!-- IDX3:DEBUT -->\n<div class="s4-card"><h4>Ch3 · Conducteurs et condensateurs</h4><p>Loi d\'Ohm, conducteur à l\'équilibre, théorème de Coulomb, cage de Faraday, capacité, condensateurs plan, cylindrique et sphérique, énergie. '
         '<a href="cours.html#ch3">Cours</a> · <a href="corriges.html#td4">TD4</a> · <a href="formules.html#f-cond">Formules</a></p></div>\n<!-- IDX3:FIN -->\n')
s = remplace_bloc(s, 'IDX3', carte, '</div>\n<div class="s4-tip" style="margin-top:18px">')
ecrire('index.html', s)

# README
s = lire('README.md')
if 'Ch3' not in s:
    s = s.replace('Ch2 Potentiel et énergie', 'Ch2 Potentiel et énergie, Ch3 Conducteurs et condensateurs')
    s = s.replace("TD3 (potentiel) corrigés pas à pas (méthode + correction)", "TD3 (potentiel) et TD4 (conducteurs, condensateurs) corrigés pas à pas (méthode + correction)")
ecrire('README.md', s)
print('Ch3 + TD4 insérés :', n_total, 'questions,', len(FIG), 'figures')
