# Génère les schémas SVG des fiches ds1.html, revision-ds.html et interro-s40.html et les insère à leur place.
# Usage : python tools/gen_fiches_figs.py   (relançable : chaque figure est encadrée par
#         <!-- fiches-fig:nom --> ... <!-- /fiches-fig:nom --> et remplacée si elle existe déjà).
# Le script ajoute aussi (idempotent) un bloc de CSS dans css/style.css sous le marqueur « fiches-figs ».
# Les figures réutilisent les classes .fgbox / .fg de ds1-complet.html (variables de couleur du site, thèmes clair et sombre).
import html, math, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CSS = os.path.join(ROOT, 'css', 'style.css')


def num(v):
    s = ('%.1f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


# ------------------------------------------------------------ texte : E_{r} indice, x^{2} exposant
def tx(s):
    out, ouverts = '', 0
    for part in re.split(r'([_^]\{[^}]*\})', s):
        m = re.match(r'([_^])\{([^}]*)\}$', part)
        if m:
            dy = 3.2 if m.group(1) == '_' else -5
            out += '<tspan dy="%s" font-size="72%%">%s</tspan><tspan dy="%s">' % (dy, html.escape(m.group(2)), -dy)
            ouverts += 1
        else:
            out += html.escape(part)
    return out + '</tspan>' * ouverts


class F:
    def __init__(self, w, h):
        self.w, self.h, self.p = w, h, []

    def a(self, s): self.p.append(s)

    def text(self, x, y, s, cls='tx', anchor='middle', size=None, halo=True):
        st = ' style="font-size:%spx"' % size if size else ''
        if halo: cls += ' halo'
        self.a('<text class="%s" x="%s" y="%s" text-anchor="%s"%s>%s</text>' % (cls, num(x), num(y), anchor, st, tx(s)))

    def line(self, x1, y1, x2, y2, cls='ob'):
        self.a('<line class="%s" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (cls, num(x1), num(y1), num(x2), num(y2)))

    def arrow(self, x1, y1, x2, y2, lc='ef', hc='efh', hl=9.0, hw=3.6):
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        bx, by = x2 - ux * hl, y2 - uy * hl
        self.line(x1, y1, bx + ux * 1.5, by + uy * 1.5, lc)
        self.a('<polygon class="%s" points="%s,%s %s,%s %s,%s"/>' % (
            hc, num(x2), num(y2), num(bx - uy * hw), num(by + ux * hw), num(bx + uy * hw), num(by - ux * hw)))

    def circ(self, x, y, r, cls='pt'):
        self.a('<circle class="%s" cx="%s" cy="%s" r="%s"/>' % (cls, num(x), num(y), num(r)))

    def rect(self, x, y, w, h, cls='box', rx=0):
        self.a('<rect class="%s" x="%s" y="%s" width="%s" height="%s"%s/>' % (
            cls, num(x), num(y), num(w), num(h), ' rx="%s"' % rx if rx else ''))

    def ellipse(self, x, y, rx, ry, cls='ob'):
        self.a('<ellipse class="%s" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (cls, num(x), num(y), num(rx), num(ry)))

    def path(self, d, cls='ob'):
        self.a('<path class="%s" d="%s"/>' % (cls, d))

    def poly(self, pts, cls='ob', close=False):
        d = 'M' + ' L'.join('%s %s' % (num(x), num(y)) for x, y in pts) + (' Z' if close else '')
        self.path(d, cls)

    def charge(self, x, y, sign, r=12):
        self.circ(x, y, r, 'qp' if sign > 0 else 'qn')
        k = r * 0.5
        self.line(x - k, y, x + k, y, 'bl' if sign > 0 else 'ef')
        if sign > 0:
            self.line(x, y - k, x, y + k, 'bl')

    def axes(self, x0, y0, x1, y1, xl, yl):
        """axe horizontal de (x0,y0) à (x1,y0), axe vertical de (x0,y0) à (x0,y1)"""
        self.arrow(x0, y0, x1, y0, 'ax', 'axh', 8, 3.2)
        self.arrow(x0, y0, x0, y1, 'ax', 'axh', 8, 3.2)
        self.text(x1 - 2, y0 + 17, xl, 'tm', 'end')
        self.text(x0 + 8, y1 + 8, yl, 'tm', 'start')

    def svg(self, name, aria, caption, maxw=None, frame='fgbox fiche'):
        body = ''.join(self.p)
        mw = maxw or int(self.w * 1.12)
        return ('<!-- fiches-fig:%s -->\n<figure class="%s"><svg class="fg" viewBox="0 0 %d %d" role="img" aria-label="%s" '
                'style="max-width:%spx">%s</svg><figcaption>%s</figcaption></figure>\n<!-- /fiches-fig:%s -->'
                % (name, frame, self.w, self.h, html.escape(aria, quote=True), mw, body, caption, name))


FIG = {}


# ============================================================ outils de tracé de courbes
class Plot:
    """repère de tracé : origine pixel (ox, oy), échelles px par unité"""
    def __init__(self, f, ox, oy, sx, sy):
        self.f, self.ox, self.oy, self.sx, self.sy = f, ox, oy, sx, sy

    def X(self, x): return self.ox + self.sx * x

    def Y(self, y): return self.oy - self.sy * y

    def curve(self, fn, x0, x1, cls, n=60):
        pts = [(self.X(x0 + (x1 - x0) * i / n), self.Y(fn(x0 + (x1 - x0) * i / n))) for i in range(n + 1)]
        self.f.poly(pts, cls)

    def segment(self, x0, y0, x1, y1, cls):
        self.f.line(self.X(x0), self.Y(y0), self.X(x1), self.Y(y1), cls)

    def tickx(self, x, lab, dy=17, cls='tm'):
        self.f.line(self.X(x), self.oy - 4, self.X(x), self.oy + 4, 'ax')
        self.f.text(self.X(x), self.oy + dy, lab, cls)

    def ticky(self, y, lab, dx=8, cls='tm'):
        self.f.line(self.ox - 4, self.Y(y), self.ox + 4, self.Y(y), 'ax')
        self.f.text(self.ox - dx, self.Y(y) + 5, lab, cls, 'end')

    def dashx(self, x, y0, y1, cls='dsh'):
        self.f.line(self.X(x), self.Y(y0), self.X(x), self.Y(y1), cls)

    def dashy(self, y, x0, x1, cls='dsh'):
        self.f.line(self.X(x0), self.Y(y), self.X(x1), self.Y(y), cls)


def legend(f, x, y, items, gap=20):
    for i, (cls, lab) in enumerate(items):
        yy = y + gap * i
        f.line(x, yy, x + 24, yy, cls)
        f.text(x + 30, yy + 4.5, lab, 'tx', 'start', 13)


# ============================================================ 1. Coulomb : forces et sens
f = F(340, 216)
for k, (yc, s2, titre, ty) in enumerate([(54, +1, 'même signe : répulsion', 14), (166, -1, 'signes opposés : attraction', 126)]):
    f.text(8, ty, titre, 'tx', 'start', 14)
    f.charge(95, yc, +1); f.charge(245, yc, s2)
    f.text(95, yc + 27, 'q_{1}', 'tm'); f.text(245, yc + 27, 'q_{2}', 'tm')
    if s2 > 0:
        f.arrow(262, yc, 322, yc); f.text(292, yc - 12, 'F_{1/2}', 'te')
        f.arrow(78, yc, 18, yc); f.text(48, yc - 12, 'F_{2/1}', 'te')
    else:
        f.arrow(228, yc, 178, yc); f.text(203, yc - 12, 'F_{1/2}', 'te')
        f.arrow(112, yc, 162, yc); f.text(137, yc - 12, 'F_{2/1}', 'te')
f.arrow(128, 54, 212, 54, 'bl', 'blh', 8, 3.2); f.text(170, 44, 'u_{12}', 'tc')
f.line(95, 100, 245, 100, 'dsh'); f.line(95, 95, 95, 105, 'dsh'); f.line(245, 95, 245, 105, 'dsh'); f.text(170, 93, 'd', 'tm')
FIG['coulomb'] = f.svg('coulomb', 'Force de Coulomb entre deux charges : répulsion si elles ont le même signe, attraction sinon',
    'Force exercée par 1 sur 2 : \\(\\vec F_{1/2}=\\frac{q_1q_2}{4\\pi\\varepsilon_0d^2}\\vec u_{12}\\), avec \\(\\vec u_{12}\\) unitaire dirigé de 1 vers 2. '
    'Si \\(q_1q_2\\gt0\\) elle est selon \\(+\\vec u_{12}\\) (répulsion), si \\(q_1q_2\\lt0\\) selon \\(-\\vec u_{12}\\) (attraction). Principe d\'action-réaction : \\(\\vec F_{2/1}=-\\vec F_{1/2}\\).')

# ============================================================ 2. plan de symétrie / d'antisymétrie
f = F(340, 340)
Mx = 170
for k, (oy, s2, titre) in enumerate([(0, +1, 'Plan de symétrie : E dans le plan'), (172, -1, "Plan d'antisymétrie : E perpendiculaire au plan")]):
    f.text(8, oy + 15, titre, 'tx', 'start', 14)
    f.line(Mx, oy + 26, Mx, oy + 166, 'dsh'); f.text(Mx + 7, oy + 40, 'Π', 'tm', 'start')
    yc, ym = oy + 54, oy + 112
    f.charge(80, yc, +1); f.charge(260, yc, s2)
    f.line(80, yc, Mx, ym, 'dsh'); f.line(260, yc, Mx, ym, 'dsh')
    ux, uy = 90 / math.hypot(90, 58), 58 / math.hypot(90, 58)
    L = 40
    f.arrow(Mx, ym, Mx + ux * L, ym + uy * L, 'bl', 'blh'); f.text(Mx + ux * L + 6, ym + uy * L + 12, 'dE_{1}', 'tc', 'start')
    if s2 > 0:
        f.arrow(Mx, ym, Mx - ux * L, ym + uy * L, 'bl', 'blh'); f.text(Mx - ux * L - 6, ym + uy * L + 12, 'dE_{2}', 'tc', 'end')
        f.arrow(Mx, ym, Mx, ym + 2 * uy * L, 'ef', 'efh'); f.text(Mx + 7, ym + 2 * uy * L + 4, 'E', 'te', 'start')
    else:
        f.arrow(Mx, ym, Mx + ux * L, ym - uy * L, 'bl', 'blh'); f.text(Mx + ux * L + 6, ym - uy * L - 4, 'dE_{2}', 'tc', 'start')
        f.arrow(Mx, ym, Mx + 2 * ux * L, ym, 'ef', 'efh'); f.text(Mx + 2 * ux * L + 8, ym + 4, 'E', 'te', 'start')
    f.circ(Mx, ym, 4.5, 'ptM'); f.text(Mx - 9, ym - 8, 'M', 'te', 'end')
FIG['symetries'] = f.svg('symetries', "Plan de symétrie, E dans le plan ; plan d'antisymétrie, E perpendiculaire au plan",
    'En haut, deux charges identiques symétriques par rapport au plan \\(\\Pi\\) : les composantes perpendiculaires à \\(\\Pi\\) se compensent, '
    '\\(\\vec E\\in\\Pi\\). En bas, charges opposées : les composantes dans \\(\\Pi\\) se compensent, \\(\\vec E\\perp\\Pi\\). '
    'Deux plans de symétrie : \\(\\vec E\\) selon leur intersection ; deux plans d\'antisymétrie : \\(\\vec E=\\vec0\\).')

# ============================================================ 3. Gauss : sphère
f = F(340, 252)
cx, cy = 170, 126
f.circ(cx, cy, 40, 'qp0'); f.circ(cx, cy, 40, 'ob2')
f.a('<circle class="gs" cx="%s" cy="%s" r="82"/>' % (cx, cy))
for k in range(8):
    t = math.radians(22.5 + 45 * k)
    f.arrow(cx + 82 * math.cos(t), cy - 82 * math.sin(t), cx + 114 * math.cos(t), cy - 114 * math.sin(t), 'ef', 'efh', 8, 3.2)
f.circ(cx, cy, 3.2, 'pt'); f.text(cx + 3, cy + 18, 'O', 'tm', 'start')
tm_ = math.radians(112.5)
Mx_, My_ = cx + 82 * math.cos(tm_), cy - 82 * math.sin(tm_)
f.line(cx, cy, Mx_, My_, 'dsh'); f.circ(Mx_, My_, 4.5, 'ptM')
f.text(Mx_ - 8, My_ + 2, 'M', 'te', 'end')
f.text(cx - 26, cy - 42, 'r', 'tm')
f.text(cx + 62, cy + 96, 'S_{G}', 'tg', 'start', 15)
FIG['gauss_sphere'] = f.svg('gauss_sphere', 'Surface de Gauss sphérique de rayon r centrée sur la charge, champ radial sortant',
    '<b>Sphère de Gauss</b> (charge ponctuelle, boule, coquille) : \\(\\vec E=E(r)\\,\\vec e_r\\parallel\\mathrm{d}\\vec S\\), \\(E\\) constant sur \\(S_G\\). '
    '\\(\\Phi=E(r)\\,4\\pi r^2=\\frac{Q_{int}}{\\varepsilon_0}\\).', 300)

# ============================================================ 4. Gauss : cylindre coaxial
f = F(340, 262)
cx = 170
f.rect(cx - 12, 8, 24, 244, 'qp0'); f.line(cx - 12, 8, cx - 12, 252, 'ob2'); f.line(cx + 12, 8, cx + 12, 252, 'ob2')
R, ytop, ybot, ry = 78, 64, 198, 16
f.a('<path class="gs" d="M%s %s v%s a%s %s 0 0 0 %s 0 v%s a%s %s 0 0 0 %s 0 Z"/>' % (
    cx - R, ytop, ybot - ytop, R, ry, 2 * R, -(ybot - ytop), R, ry, -2 * R))
f.a('<ellipse class="gsl" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (cx, ytop, R, ry))
f.a('<path class="gsl" d="M%s %s a%s %s 0 0 1 %s 0"/>' % (cx - R, ybot, R, ry, 2 * R))
for yy in (92, 131, 170):
    f.arrow(cx + R, yy, cx + R + 38, yy, 'ef', 'efh', 8, 3.2)
    f.arrow(cx - R, yy, cx - R - 38, yy, 'ef', 'efh', 8, 3.2)
f.text(cx + R + 42, 134, 'E', 'te', 'start')
f.arrow(cx + 40, ytop - 4, cx + 40, ytop - 28, 'gsa', 'gsah', 8, 3.2); f.text(cx + 48, ytop - 14, 'dS', 'tg', 'start')
f.arrow(cx + 40, ybot + 14, cx + 40, ybot + 36, 'gsa', 'gsah', 8, 3.2); f.text(cx + 48, ybot + 34, 'dS', 'tg', 'start')
f.line(cx, ybot, cx + R, ybot, 'dsh'); f.text(cx + R / 2 - 6, ybot + 14, 'r', 'tm')
f.arrow(30, ytop, 30, ybot, 'ax', 'axh', 7, 3); f.arrow(30, ybot, 30, ytop, 'ax', 'axh', 7, 3)
f.text(38, (ytop + ybot) / 2 + 5, 'h', 'tm', 'start')
f.text(cx + 18, 22, 'z', 'tm', 'start')
FIG['gauss_cyl'] = f.svg('gauss_cyl', 'Surface de Gauss cylindrique coaxiale de rayon r et de hauteur h autour d\'un fil ou d\'un cylindre infini',
    '<b>Cylindre de Gauss</b> coaxial (fil, cylindre infini) : sur la face latérale \\(\\vec E\\parallel\\mathrm{d}\\vec S\\) et \\(E(r)\\) est constant ; '
    'sur les bases \\(\\mathrm{d}\\vec S=\\pm\\,r\\,\\mathrm{d}r\\,\\mathrm{d}\\theta\\,\\vec e_z\\perp\\vec E\\) : flux nul. \\(\\Phi=E(r)\\,2\\pi rh\\).', 300)

# ============================================================ 5. Gauss : plan infini
f = F(340, 238)
yp = 119
f.line(14, yp, 326, yp, 'bl'); f.line(14, yp, 326, yp, 'bl')
for x in range(34, 330, 46):
    f.text(x, yp - 4, '+', 'tc', size=15)
f.text(326, yp - 8, 'σ', 'tc', 'end', 15)
f.a('<rect class="gs" x="105" y="58" width="130" height="122"/>')
for xx in (42, 170, 298):
    f.arrow(xx, yp - 8, xx, 22, 'ef', 'efh', 8, 3.2) if xx != 170 else f.arrow(xx, yp - 8, xx, 36, 'ef', 'efh', 8, 3.2)
    f.arrow(xx, yp + 8, xx, 216, 'ef', 'efh', 8, 3.2) if xx != 170 else f.arrow(xx, yp + 8, xx, 202, 'ef', 'efh', 8, 3.2)
f.arrow(132, 58, 132, 38, 'gsa', 'gsah', 8, 3.2); f.text(140, 46, 'dS', 'tg', 'start')
f.arrow(132, 180, 132, 200, 'gsa', 'gsah', 8, 3.2); f.text(140, 202, 'dS', 'tg', 'start')
f.circ(206, 58, 4.5, 'ptM'); f.text(214, 54, 'M', 'te', 'start')
f.circ(206, 180, 4.5, 'ptM'); f.text(214, 196, "M'", 'te', 'start')
f.arrow(272, yp, 272, 58, 'ax', 'axh', 7, 3); f.text(279, 92, 'z', 'tm', 'start')
f.text(298, 78, 'E', 'te', 'start'); f.text(298, 168, 'E', 'te', 'start')
FIG['gauss_plan'] = f.svg('gauss_plan', 'Cylindre de Gauss à cheval sur un plan infini chargé, champ perpendiculaire au plan de part et d\'autre',
    '<b>Boîte de Gauss</b> à cheval sur le plan (bases d\'aire \\(S\\) en \\(\\pm z\\)) : \\(\\vec E=E(z)\\vec e_z\\) avec \\(E(-z)=-E(z)\\). Flux nul sur la face latérale, '
    '\\(\\Phi=2SE\\) sur les deux bases, \\(Q_{int}=\\sigma S\\) donc \\(E=\\frac{\\sigma}{2\\varepsilon_0}\\).', 320)

# ============================================================ 6. deux plans ±σ : superposition
f = F(340, 232)
xa, xb = 118, 222
f.line(xa, 24, xa, 214, 'bl'); f.line(xb, 24, xb, 214, 'ef')
f.text(xa, 16, '+σ', 'tc', size=15); f.text(xb, 16, '−σ', 'te', size=15)
f.arrow(xa - 6, 62, xa - 52, 62, 'bl', 'blh', 8, 3); f.arrow(xa + 6, 62, xa + 52, 62, 'bl', 'blh', 8, 3)
f.arrow(xb - 54, 118, xb - 6, 118, 'ef', 'efh', 8, 3); f.arrow(xb + 54, 118, xb + 6, 118, 'ef', 'efh', 8, 3)
f.arrow(xa + 6, 176, xb - 6, 176, 'gsa', 'gsah', 10, 4)
f.text((xa + xb) / 2, 166, 'σ/ε₀', 'tg', size=14)
f.text(xa - 52, 180, '0', 'tg', 'middle', 16); f.text(xb + 52, 180, '0', 'tg', 'middle', 16)
f.text(xa - 56, 54, 'σ/2ε₀', 'tc', 'middle', 12); f.text(xa + 56, 54, 'σ/2ε₀', 'tc', 'middle', 12)
f.text(xb - 56, 110, 'σ/2ε₀', 'te', 'middle', 12); f.text(xb + 56, 110, 'σ/2ε₀', 'te', 'middle', 12)
f.text(8, 40, '(1)', 'tm', 'start', 12); f.text(8, 96, '(2)', 'tm', 'start', 12); f.text(8, 152, '(1)+(2)', 'tm', 'start', 12)
FIG['plans'] = f.svg('plans', 'Deux plans infinis chargés +σ et −σ : champ nul à l\'extérieur et σ sur epsilon zéro entre les plans',
    '<b>Condensateur plan idéal</b> par superposition de deux plans infinis ((1) plan \\(+\\sigma\\) seul, (2) plan \\(-\\sigma\\) seul) : le champ s\'ajoute entre les plans (\\(\\frac{\\sigma}{2\\varepsilon_0}+\\frac{\\sigma}{2\\varepsilon_0}\\)) et se compense à l\'extérieur.', 340)

# ============================================================ 7. sphère pleine : E(r) et V(r)
f = F(340, 398)
R_ = 80
P = Plot(f, 52, 176, R_, 120)           # x en unité de R, y en unité de E0
f.axes(52, 176, 326, 34, 'r', 'E')
P.curve(lambda r: r, 0, 1, 'cv1'); P.curve(lambda r: 1 / r ** 2, 1, 3.3, 'cv1')
f.line(P.X(0), P.Y(0) - 1.5, P.X(1), P.Y(0) - 1.5, 'cv2'); P.curve(lambda r: 1 / r ** 2, 1, 3.3, 'cv2')
P.dashx(1, 0, 1, 'dsh'); P.dashy(1, 0, 1, 'dsh')
P.tickx(1, 'R'); P.ticky(1, 'E₀')
f.text(P.X(1) + 8, P.Y(1) - 14, 'saut σ/ε₀', 'tm', 'start', 13)
legend(f, 196, 54, [('cv1', 'boule, volume ρ'), ('cv2', 'coquille, surface σ')])
f.text(P.X(0.45) - 6, P.Y(0.45) - 10, '∝ r', 'tc', 'end', 13); f.text(P.X(2.1), P.Y(0.23) - 14, '∝ 1/r²', 'tm', 'middle', 13)
# V(r)
P2 = Plot(f, 52, 384, R_, 92)
f.axes(52, 384, 326, 216, 'r', 'V')
Vv = lambda r: 1.5 - 0.5 * r * r
P2.curve(Vv, 0, 1, 'cv1'); P2.curve(lambda r: 1 / r, 1, 3.3, 'cv1')
f.line(P2.X(0), P2.Y(1) - 1.5, P2.X(1), P2.Y(1) - 1.5, 'cv2'); P2.curve(lambda r: 1 / r, 1, 3.3, 'cv2')
P2.dashx(1, 0, 1, 'dsh'); P2.dashy(1, 0, 1, 'dsh'); P2.dashy(1.5, 0, 0, 'dsh')
P2.tickx(1, 'R'); P2.ticky(1, 'V₀'); P2.ticky(1.5, '3V₀/2')
f.text(P2.X(0.5), P2.Y(1) + 20, 'plateau : E = 0', 'tm', 'middle', 13)
f.text(P2.X(2.2), P2.Y(1 / 2.2) - 14, '∝ 1/r', 'tm', 'middle', 13)
FIG['sphere_ev'] = f.svg('sphere_ev', 'Champ E(r) et potentiel V(r) d\'une boule chargée en volume et d\'une coquille chargée en surface, de même charge Q',
    'Même charge totale \\(Q\\) : \\(E_0=\\frac{Q}{4\\pi\\varepsilon_0R^2}\\), \\(V_0=\\frac{Q}{4\\pi\\varepsilon_0R}\\). À l\'extérieur les deux sont identiques (charge ponctuelle). '
    '\\(V\\) est continu partout ; \\(E\\) est continu pour la boule, il saute de \\(\\sigma/\\varepsilon_0\\) pour la coquille (\\(V\\) y est constant).', 340)

# ============================================================ 8. cylindre infini plein : E(r) et V(r)
f = F(340, 398)
P = Plot(f, 52, 176, 70, 120)
f.axes(52, 176, 326, 34, 'r', 'E')
P.curve(lambda r: r, 0, 1, 'cv1'); P.curve(lambda r: 1 / r, 1, 4.1, 'cv1')
P.dashx(1, 0, 1); P.dashy(1, 0, 1)
P.tickx(1, 'R'); P.ticky(1, 'E₀')
f.text(P.X(0.5) - 8, P.Y(0.5) - 8, '∝ r', 'tc', 'end', 13); f.text(P.X(2.4), P.Y(1 / 2.4) - 14, '∝ 1/r', 'tm', 'middle', 13)
f.text(P.X(1.9), 60, 'E₀ = ρR/2ε₀', 'tm', 'middle', 13)
# V : référence V(R0)=V0 avec R0 = 3R ; unité E0*R ; le niveau V0 est placé à 0,6 au-dessus de l'axe
f2 = Plot(f, 52, 384, 70, 70)
f.axes(52, 384, 326, 216, 'r', 'V')
b0 = 0.6
Vout = lambda r: b0 + math.log(3 / r)
Vin = lambda r: Vout(1) + 0.5 * (1 - r * r)
f2.curve(Vin, 0, 1, 'cv1'); f2.curve(Vout, 1, 4.1, 'cv1')
f2.dashx(1, 0, Vout(1)); f2.dashy(b0, 0, 3, 'dsh'); f2.dashx(3, 0, b0)
f2.tickx(1, 'R'); f2.tickx(3, 'R₀'); f2.ticky(b0, 'V₀')
f.circ(f2.X(3), f2.Y(b0), 4, 'ptM')
f.text(f2.X(1.35), f2.Y(1.6), 'V₀ − (λ/2πε₀) ln(r/R₀)', 'tm', 'start', 13)
FIG['cyl_ev'] = f.svg('cyl_ev', 'Champ E(r) et potentiel V(r) d\'un cylindre infini chargé en volume, avec V(R0)=V0',
    '\\(E_0=\\frac{\\rho R}{2\\varepsilon_0}\\) ; à l\'extérieur \\(E=\\frac{\\lambda}{2\\pi\\varepsilon_0r}\\) en \\(1/r\\) (comme le fil). \\(V\\) décroît en \\(-\\frac{\\lambda}{2\\pi\\varepsilon_0}\\ln\\frac{r}{R_0}\\), '
    'valeur \\(V_0\\) imposée en \\(R_0\\) (pas de \\(V(\\infty)=0\\) : le logarithme diverge).', 340)

# ============================================================ 9. plan infini : E(z) et V(z)
f = F(340, 316)
P = Plot(f, 170, 84, 54, 46)
f.arrow(30, 84, 326, 84, 'ax', 'axh', 8, 3.2); f.arrow(170, 140, 170, 22, 'ax', 'axh', 8, 3.2)
f.text(324, 102, 'z', 'tm', 'end'); f.text(178, 30, 'E', 'tm', 'start')
f.line(P.X(-2.8), P.Y(-1), P.X(0), P.Y(-1), 'cv1'); f.line(P.X(0), P.Y(1), P.X(2.8), P.Y(1), 'cv1')
f.a('<line class="dsh" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (num(P.X(0)), num(P.Y(-1)), num(P.X(0)), num(P.Y(1))))
f.text(P.X(1.4), P.Y(1) - 8, 'σ/2ε₀', 'tm', 'middle', 13); f.text(P.X(-1.4), P.Y(-1) + 18, '−σ/2ε₀', 'tm', 'middle', 13)
f.text(178, P.Y(0.45), 'saut σ/ε₀', 'tm', 'start', 13)
Q = Plot(f, 170, 280, 54, 46)
f.arrow(30, 280, 326, 280, 'ax', 'axh', 8, 3.2); f.arrow(170, 296, 170, 160, 'ax', 'axh', 8, 3.2)
f.text(324, 298, 'z', 'tm', 'end'); f.text(180, 170, 'V', 'tm', 'start')
f.poly([(Q.X(-2.8), Q.Y(2.0 - 0.55 * 2.8)), (Q.X(0), Q.Y(2.0)), (Q.X(2.8), Q.Y(2.0 - 0.55 * 2.8))], 'cv1')
f.text(Q.X(0) - 8, Q.Y(2.0) - 8, 'V₀', 'tm', 'end'); f.circ(Q.X(0), Q.Y(2.0), 4, 'ptM')
f.text(Q.X(1.6), Q.Y(2.0 - 0.55 * 1.6) - 12, 'V₀ − σ|z|/2ε₀', 'tm', 'start', 13)
FIG['plan_ev'] = f.svg('plan_ev', 'Champ E(z) et potentiel V(z) d\'un plan infini uniformément chargé',
    '\\(E(z)\\) est uniforme de chaque côté, de signe opposé, avec un saut de \\(\\sigma/\\varepsilon_0\\) en \\(z=0\\). \\(V(z)\\) est continu, maximal sur le plan (pour \\(\\sigma\\gt0\\)) '
    'et décroît linéairement : \\(V=V_0-\\frac{\\sigma|z|}{2\\varepsilon_0}\\). Un plan infini n\'a pas de \\(V(\\infty)=0\\).', 340)


# ============================================================ 10. doublet : lignes de champ et équipotentielles (calcul numérique)
def doublet():
    W, H = 340, 250
    sc = 70.0
    x0, y0 = W / 2, H / 2
    a = 0.8                      # charges en (-a, 0) [+] et (+a, 0) [-]
    xm, ym = (W / 2) / sc - 0.05, (H / 2) / sc - 0.05

    def E(x, y):
        r1 = math.hypot(x + a, y) ** 3; r2 = math.hypot(x - a, y) ** 3
        return (x + a) / r1 - (x - a) / r2, y / r1 - y / r2

    def V(x, y):
        return 1 / math.hypot(x + a, y) - 1 / math.hypot(x - a, y)

    f = F(W, H)
    f.rect(0, 0, W, H, 'fg-bg')
    f.a('<clipPath id="dclip"><rect x="0" y="0" width="%d" height="%d"/></clipPath><g clip-path="url(#dclip)">' % (W, H))
    # équipotentielles : marching squares
    n = 0.025
    nx, ny = int(2 * xm / n), int(2 * ym / n)
    xs = [-xm + i * n for i in range(nx + 1)]; ys = [-ym + j * n for j in range(ny + 1)]
    grid = [[V(x, y) if min(math.hypot(x + a, y), math.hypot(x - a, y)) > 1e-3 else 1e3 for y in ys] for x in xs]
    for lev in (-2.5, -1.2, -0.6, -0.25, 0.25, 0.6, 1.2, 2.5):
        segs = []
        for i in range(nx):
            for j in range(ny):
                c = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
                v = [grid[p][q] - lev for p, q in c]
                pts = []
                for k in range(4):
                    p1, p2 = c[k], c[(k + 1) % 4]
                    v1, v2 = v[k], v[(k + 1) % 4]
                    if (v1 > 0) != (v2 > 0):
                        t = v1 / (v1 - v2)
                        pts.append((xs[p1[0]] + t * (xs[p2[0]] - xs[p1[0]]), ys[p1[1]] + t * (ys[p2[1]] - ys[p1[1]])))
                if len(pts) == 2:
                    segs.append((pts[0], pts[1]))
                elif len(pts) == 4:
                    segs.append((pts[0], pts[1])); segs.append((pts[2], pts[3]))
        d = ''.join('M%s %s L%s %s' % (num(x0 + sc * p[0]), num(y0 - sc * p[1]), num(x0 + sc * q[0]), num(y0 - sc * q[1])) for p, q in segs)
        f.a('<path class="ec" d="%s" stroke-linecap="round"/>' % d)
    # plan médiateur V = 0
    f.line(x0, 0, x0, H, 'ec')
    # lignes de champ depuis la charge +
    for k in range(14):
        th = 2 * math.pi * (k + 0.5) / 14
        x, y = -a + 0.06 * math.cos(th), 0.06 * math.sin(th)
        pts = [(x, y)]
        for _ in range(900):
            ex, ey = E(x, y); nrm = math.hypot(ex, ey)
            h = 0.03
            def fdir(px, py):
                gx, gy = E(px, py); g = math.hypot(gx, gy); return gx / g, gy / g
            k1 = fdir(x, y); k2 = fdir(x + h / 2 * k1[0], y + h / 2 * k1[1]); k3 = fdir(x + h / 2 * k2[0], y + h / 2 * k2[1]); k4 = fdir(x + h * k3[0], y + h * k3[1])
            x += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); y += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            pts.append((x, y))
            if abs(x) > xm + 0.3 or abs(y) > ym + 0.3 or math.hypot(x - a, y) < 0.08:
                break
        spts = [(x0 + sc * p[0], y0 - sc * p[1]) for p in pts]
        f.a('<path class="fl" d="%s"/>' % ('M' + ' L'.join('%s %s' % (num(p[0]), num(p[1])) for p in spts)))
        # flèche au tiers de la longueur
        i = max(2, len(spts) // 3) if len(spts) > 6 else 1
        (px, py), (qx, qy) = spts[i - 1], spts[i]
        L = math.hypot(qx - px, qy - py) or 1
        ux, uy = (qx - px) / L, (qy - py) / L
        f.a('<polygon class="flh" points="%s,%s %s,%s %s,%s"/>' % (num(qx + ux * 5), num(qy + uy * 5), num(qx - ux * 4 - uy * 4), num(qy - uy * 4 + ux * 4), num(qx - ux * 4 + uy * 4), num(qy - uy * 4 - ux * 4)))
    f.a('</g>')
    f.charge(x0 - sc * a, y0, +1, 10); f.charge(x0 + sc * a, y0, -1, 10)
    return f


f = doublet()
f.text(176, 14, 'V = 0', 'tm', 'start', 12)
FIG['doublet'] = f.svg('doublet', 'Lignes de champ et équipotentielles d\'un doublet +q, −q',
    'Doublet \\((+q,-q)\\) (calcul numérique). Les lignes de champ (bleu) partent de \\(+\\) et arrivent sur \\(-\\) ; les équipotentielles (orange) leur sont partout perpendiculaires. '
    'Le plan médiateur est une équipotentielle \\(V=0\\) et un plan d\'antisymétrie (lignes de champ perpendiculaires au plan). \\(\\vec E\\) pointe vers les \\(V\\) décroissants.', 340)


# ============================================================ interro : vocabulaire s4-fig (w, cur, dash, dot, t, tn, ti) ; repère cylindrique
def s4(parts, aria, vb, caption, name):
    return ('<!-- fiches-fig:%s -->\n<figure class="s4-fig"><svg aria-label="%s" role="img" viewBox="%s">%s</svg><figcaption>%s</figcaption></figure>\n<!-- /fiches-fig:%s -->'
            % (name, html.escape(aria, quote=True), vb, ''.join(parts), caption, name))


def hd(x, y, dx, dy, cls='curh', l=8, w=3.4):
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    return '<polygon class="%s" points="%s,%s %s,%s %s,%s"/>' % (cls, num(x), num(y), num(x - ux * l - uy * w), num(y - uy * l + ux * w), num(x - ux * l + uy * w), num(y - uy * l - ux * w))


def varrow(x1, y1, x2, y2, cls='cur'):
    L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L
    return '<path class="%s" d="M%s %s L%s %s"/>' % (cls, num(x1), num(y1), num(x2 - ux * 6), num(y2 - uy * 6)) + hd(x2, y2, ux, uy)


parts = [
    '<path class="w" d="M110 150 V18 M110 150 H285 M110 150 L32 215"></path>',
    '<path class="w dash" d="M200 62 V178 M110 150 L200 178"></path>',
    '<path class="cur" d="M86 170 A32 32 0 0 0 140 159"></path>',
    varrow(200, 62, 200, 30), varrow(200, 62, 236, 52), varrow(200, 62, 230, 80),
    '<circle class="dot" cx="200" cy="62" r="4"></circle><circle class="dot" cx="200" cy="178" r="3"></circle>',
    '<text class="t" x="115" y="20">z</text><text class="t" x="275" y="142">y</text><text class="t" x="22" y="212">x</text>',
    '<text class="t" x="96" y="166">O</text><text class="tn" x="170" y="60">M</text><text class="t" x="206" y="196">m</text>',
    '<text class="ti" x="146" y="182">r</text><text class="ti" x="207" y="128">z</text><text class="ti" x="100" y="196">θ</text>',
    '<text class="ti" x="206" y="22">e<tspan dy="3" font-size="72%">z</tspan></text>',
    '<text class="ti" x="240" y="52">e<tspan dy="3" font-size="72%">θ</tspan></text>',
    '<text class="ti" x="228" y="98">e<tspan dy="3" font-size="72%">r</tspan></text>',
]
FIG['i_cyl'] = s4(parts, 'Coordonnées cylindriques : r distance à l\'axe Oz, theta angle entre Ox et Om, z hauteur, et base mobile e_r, e_theta, e_z en M.', '0 0 300 235',
    'Cylindrique : \\(r=Om\\) (distance à l\'axe), \\(\\theta\\) entre \\(Ox\\) et \\(\\overrightarrow{Om}\\), \\(z\\) la hauteur. Base mobile en \\(M\\) : \\(\\vec e_r\\) s\'éloigne de l\'axe, \\(\\vec e_\\theta\\) tourne dans le sens croissant de \\(\\theta\\), \\(\\vec e_z\\) est fixe.', 'i_cyl')

# ============================================================ interro : éléments de surface et de volume (cylindrique, sphérique)
f = F(340, 214)
# --- cylindrique, vue de dessus
Ox, Oy = 34, 172
f.arrow(Ox, Oy, 160, Oy, 'ax', 'axh', 8, 3.2); f.arrow(Ox, Oy, Ox, 28, 'ax', 'axh', 8, 3.2)
f.text(158, Oy + 16, 'x', 'tm', 'end'); f.text(Ox + 8, 34, 'y', 'tm', 'start')
r1, r2, t1, t2 = 70, 112, math.radians(22), math.radians(58)
P1 = (Ox + r1 * math.cos(t1), Oy - r1 * math.sin(t1)); P2 = (Ox + r1 * math.cos(t2), Oy - r1 * math.sin(t2))
P3 = (Ox + r2 * math.cos(t2), Oy - r2 * math.sin(t2)); P4 = (Ox + r2 * math.cos(t1), Oy - r2 * math.sin(t1))
f.a('<path class="qp" d="M%s %s A%s %s 0 0 0 %s %s L%s %s A%s %s 0 0 1 %s %s Z"/>' % (
    num(P1[0]), num(P1[1]), r1, r1, num(P2[0]), num(P2[1]), num(P3[0]), num(P3[1]), r2, r2, num(P4[0]), num(P4[1])))
f.line(Ox, Oy, Ox + (r2 + 14) * math.cos(t1), Oy - (r2 + 14) * math.sin(t1), 'dsh')
f.line(Ox, Oy, Ox + (r2 + 14) * math.cos(t2), Oy - (r2 + 14) * math.sin(t2), 'dsh')
f.a('<path class="ac" d="M%s %s A38 38 0 0 0 %s %s"/>' % (num(Ox + 38 * math.cos(t1)), num(Oy - 38 * math.sin(t1)), num(Ox + 38 * math.cos(t2)), num(Oy - 38 * math.sin(t2))))
f.text(Ox + 54, Oy - 28, 'dθ', 'tc', 'middle', 14)
tm_ = (t1 + t2) / 2; rm = (r1 + r2) / 2
cxp, cyp = Ox + rm * math.cos(tm_), Oy - rm * math.sin(tm_)
f.arrow(cxp, cyp, cxp + 30 * math.cos(tm_), cyp - 30 * math.sin(tm_), 'ef', 'efh', 8, 3.2)
f.arrow(cxp, cyp, cxp - 30 * math.sin(tm_), cyp - 30 * math.cos(tm_), 'bl', 'blh', 8, 3.2)
f.text(cxp + 36 * math.cos(tm_) + 2, cyp - 36 * math.sin(tm_) + 8, 'e_{r}', 'te', 'start', 13)
f.text(cxp - 30 * math.sin(tm_) - 6, cyp - 30 * math.cos(tm_) - 6, 'e_{θ}', 'tc', 'end', 13)
f.text(Ox + 96 * math.cos(t1) + 12, Oy - 96 * math.sin(t1) + 18, 'dr', 'tg', 'start', 13)
f.text(Ox + 124 * math.cos(tm_) - 6, Oy - 124 * math.sin(tm_) - 12, 'r dθ', 'tg', 'start', 13)
f.text(8, 16, 'cylindrique, z fixé', 'tx', 'start', 13)
f.text(8, 204, 'dS = r dr dθ', 'tx', 'start', 13)
# --- sphérique, patch sur la sphère
cx, cy, R = 252, 96, 64
cE, sE = math.cos(math.radians(24)), math.sin(math.radians(24))


def pr(r, th, ph):
    X, Y, Z = r * math.sin(th) * math.cos(ph), r * math.sin(th) * math.sin(ph), r * math.cos(th)
    return cx + X, cy - (Z * cE + Y * sE)


f.circ(cx, cy, R, 'qp0'); f.circ(cx, cy, R, 'ob2')
f.a('<path class="hid" d="M%s %s %s"/>' % (num(cx - R), num(cy), ' '.join('L%s %s' % (num(pr(R, math.pi / 2, math.radians(a))[0]), num(pr(R, math.pi / 2, math.radians(a))[1])) for a in range(180, 361, 6))))
f.a('<path class="ob2" d="M%s %s %s"/>' % (num(cx - R), num(cy), ' '.join('L%s %s' % (num(pr(R, math.pi / 2, math.radians(a))[0]), num(pr(R, math.pi / 2, math.radians(a))[1])) for a in range(180, -1, -6))))
f.arrow(cx, cy, cx, cy - R * cE - 22, 'ax', 'axh', 7, 3); f.text(cx + 8, cy - R * cE - 20, 'z', 'tm', 'start')
th0, th1, ph0, ph1 = math.radians(46), math.radians(86), math.radians(-100), math.radians(-50)
edge = []
for i in range(0, 13): edge.append(pr(R, th0, ph0 + (ph1 - ph0) * i / 12))
for i in range(0, 13): edge.append(pr(R, th0 + (th1 - th0) * i / 12, ph1))
for i in range(0, 13): edge.append(pr(R, th1, ph1 - (ph1 - ph0) * i / 12))
for i in range(0, 13): edge.append(pr(R, th1 - (th1 - th0) * i / 12, ph0))
f.poly(edge, 'qn', close=True)
mid = pr(R, (th0 + th1) / 2, (ph0 + ph1) / 2)
f.line(cx, cy, mid[0], mid[1], 'dsh')
f.a('<path class="ac" d="M%s"/>' % ' L'.join('%s %s' % (num(pr(26, t, (ph0 + ph1) / 2)[0]), num(pr(26, t, (ph0 + ph1) / 2)[1])) for t in [i * (th0 + th1) / 2 / 10 for i in range(11)]))
f.text(cx + 10, cy - 36, 'θ', 'tc', 'start', 13)
d1 = pr(R + 24, (th0 + th1) / 2, (ph0 + ph1) / 2)
f.arrow(mid[0], mid[1], d1[0], d1[1], 'ef', 'efh', 7, 3)
f.text(d1[0] + 4, d1[1] + 14, 'e_{r}', 'te', 'start', 13)
f.text(pr(R, th0, (ph0 + ph1) / 2)[0] - 30, pr(R, th0, (ph0 + ph1) / 2)[1] - 14, 'R sinθ dφ', 'tg', 'end', 13)
f.text(pr(R, (th0 + th1) / 2, ph1)[0] + 12, pr(R, (th0 + th1) / 2, ph1)[1] + 18, 'R dθ', 'tg', 'start', 13)
f.text(cx + 76, 16, 'sphérique, r = R', 'tx', 'end', 13)
f.text(332, 204, 'dS = R² sinθ dθ dφ', 'tx', 'end', 13)
FIG['i_elem'] = f.svg('i_elem', 'Éléments de surface : en cylindrique r dr dtheta vu de dessus, en sphérique R carré sinus theta dtheta dphi sur la sphère.',
    'À gauche, vue de dessus (\\(z\\) fixé) : côtés \\(\\mathrm{d}r\\) et \\(r\\,\\mathrm{d}\\theta\\), donc \\(\\mathrm{d}S=r\\,\\mathrm{d}r\\,\\mathrm{d}\\theta\\) et \\(\\mathrm{d}\\tau=r\\,\\mathrm{d}r\\,\\mathrm{d}\\theta\\,\\mathrm{d}z\\). '
    'À droite, sur la sphère de rayon \\(R\\) : le côté « méridien » vaut \\(R\\,\\mathrm{d}\\theta\\), le côté « parallèle » vaut \\(R\\sin\\theta\\,\\mathrm{d}\\varphi\\) (rayon du parallèle \\(R\\sin\\theta\\)).', frame='s4-fig')

# ============================================================ interro : orientation de dS (cylindre, sphère) et flux d'un champ radial
f = F(340, 222)
# cylindre
cx = 86
R_, yt, yb, ry = 52, 54, 156, 13
f.a('<path class="gs" d="M%s %s v%s a%s %s 0 0 0 %s 0 v%s a%s %s 0 0 0 %s 0 Z"/>' % (cx - R_, yt, yb - yt, R_, ry, 2 * R_, -(yb - yt), R_, ry, -2 * R_))
f.a('<ellipse class="gsl" cx="%s" cy="%s" rx="%s" ry="%s"/>' % (cx, yt, R_, ry))
for yy in (84, 118):
    f.arrow(cx + R_ + 2, yy, cx + R_ + 32, yy, 'ef', 'efh', 8, 3)
    f.arrow(cx - R_ - 2, yy, cx - R_ - 32, yy, 'ef', 'efh', 8, 3)
f.text(26, 76, 'A', 'te', 'middle', 14)
f.arrow(cx + R_ + 2, 101, cx + R_ + 28, 101, 'gsa', 'gsah', 8, 3); f.text(cx + R_ + 32, 106, 'dS', 'tg', 'start', 13)
f.arrow(cx + 28, yt - 6, cx + 28, yt - 30, 'gsa', 'gsah', 8, 3); f.text(cx + 36, yt - 14, '+e_{z}', 'tg', 'start', 13)
f.arrow(cx + 28, yb + 18, cx + 28, yb + 42, 'bl', 'blh', 8, 3); f.text(cx + 36, yb + 40, '−e_{z}', 'tc', 'start', 13)
f.text(cx - 24, 14, 'bases : A ⟂ dS', 'tm', 'middle', 12)
f.text(cx, 206, 'latérale : dS ∥ A', 'tm', 'middle', 12)
# sphère
sx, sy, Rs = 252, 108, 62
f.circ(sx, sy, Rs, 'qp0'); f.circ(sx, sy, Rs, 'ob2')
for k in range(8):
    t = math.radians(15 + 45 * k)
    f.arrow(sx + Rs * math.cos(t), sy - Rs * math.sin(t), sx + (Rs + 24) * math.cos(t), sy - (Rs + 24) * math.sin(t), 'ef', 'efh', 7, 2.8)
t = math.radians(52)
t2 = math.radians(-128)
f.arrow(sx + (Rs + 26) * math.cos(t2), sy - (Rs + 26) * math.sin(t2), sx + (Rs - 24) * math.cos(t2), sy - (Rs - 24) * math.sin(t2), 'bl', 'blh', 8, 3)
f.circ(sx + Rs * math.cos(math.radians(-128)), sy - Rs * math.sin(math.radians(-128)), 3.5, 'pt')
f.text(sx + 64 * math.cos(math.radians(-128)) - 8, sy - 64 * math.sin(math.radians(-128)) + 30, 'dS entrant', 'tc', 'middle', 12)
f.text(sx, 210, 'dS sortant : +e_{r}', 'tg', 'middle', 12)
f.arrow(sx + 4, sy - 2, sx + 4 + 40 * math.cos(math.radians(40)), sy - 2 - 40 * math.sin(math.radians(40)), 'gsa', 'gsah', 8, 3)
FIG['i_flux'] = f.svg('i_flux', 'Orientation de dS pour un champ radial : cylindre (latérale +e_r, bases plus ou moins e_z) et sphère (sortant ou entrant).',
    'Champ radial \\(\\vec A=A_0\\,r\\,\\vec e_r\\) (orange). <b>Cylindre</b> : sur la latérale \\(\\mathrm{d}\\vec S\\parallel\\vec A\\) ; sur les bases \\(\\mathrm{d}\\vec S=\\pm\\,r\\,\\mathrm{d}r\\,\\mathrm{d}\\theta\\,\\vec e_z\\perp\\vec A\\) : flux nul. '
    '<b>Sphère</b> : flux sortant avec \\(+\\,R^2\\sin\\theta\\,\\mathrm{d}\\theta\\,\\mathrm{d}\\varphi\\,\\vec e_r\\) ; flux « de l\'extérieur vers l\'intérieur » avec \\(-\\vec e_r\\) (signe \\(-\\)).', frame='s4-fig')

# ============================================================ interro : les quatre modèles de charge
f = F(340, 230)
# (1) ponctuelle
f.charge(85, 44, +1, 13)
f.text(85, 84, 'ponctuelle : q (C)', 'tx', 'middle', 13); f.text(85, 100, 'Q = q', 'tm', 'middle', 13)
# (2) linéique
wire = [(194, 56), (218, 34), (248, 26), (278, 36), (302, 50), (326, 44)]
f.poly(wire, 'bl')
f.line(248, 26, 278, 36, 'ef'); f.text(263, 20, 'dl', 'te', 'middle', 13)
f.a('<line class="ef" x1="248" y1="26" x2="278" y2="36" stroke-width="5"/>')
f.text(255, 84, 'linéique : λ (C·m⁻¹)', 'tx', 'middle', 13); f.text(255, 100, 'Q = ∫ λ dl', 'tm', 'middle', 13)
# (3) surfacique
f.poly([(26, 164), (146, 164), (160, 134), (40, 134)], 'qp', close=True)
f.poly([(78, 156), (104, 156), (110, 144), (84, 144)], 'qn', close=True)
f.text(96, 128, 'dS', 'te', 'middle', 13)
f.text(85, 198, 'surfacique : σ (C·m⁻²)', 'tx', 'middle', 13); f.text(85, 214, 'Q = ∬ σ dS', 'tm', 'middle', 13)
# (4) volumique
f.ellipse(255, 152, 62, 34, 'qp')
f.rect(245, 144, 20, 16, 'qn')
f.text(284, 150, 'dτ', 'te', 'start', 13)
f.text(255, 198, 'volumique : ρ (C·m⁻³)', 'tx', 'middle', 13); f.text(255, 214, 'Q = ∭ ρ dτ', 'tm', 'middle', 13)
FIG['i_modeles'] = f.svg('i_modeles', 'Les quatre modèles de charge : ponctuelle, linéique, surfacique, volumique, avec leur élément de charge.',
    '\\(\\mathrm{d}q=\\lambda\\,\\mathrm{d}l\\), \\(\\sigma\\,\\mathrm{d}S\\) ou \\(\\rho\\,\\mathrm{d}\\tau\\) : on intègre l\'élément de charge sur la dimension de l\'objet. Densité uniforme : \\(Q=\\lambda L=\\sigma S=\\rho V\\).', frame='s4-fig')

CSS_BLOCK = '''/* fiches-figs:start (généré par tools/gen_fiches_figs.py) */
.fg .halo{paint-order:stroke;stroke:var(--surface2);stroke-width:4px;stroke-linejoin:round}
.s4-fig .fg .halo{stroke:var(--surface)}
.fgbox.fiche{margin:14px 0}
.fgbox.fiche figcaption{font-family:var(--f-body);font-size:13.5px;text-align:left;line-height:1.55}
.fgbox.fiche figcaption b{color:var(--ink)}
.s4-fig svg.fg{max-width:420px}
.tbl-wrap th .katex{text-transform:none}
/* fiches-figs:end */'''


def ensure_css():
    s = open(CSS, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    blk = CSS_BLOCK.replace('\n', nl)
    a, b = s.find('/* fiches-figs:start'), s.find('/* fiches-figs:end */')
    if a >= 0 and b > a:
        s = s[:a] + blk + s[b + len('/* fiches-figs:end */'):]
    else:
        s = s.rstrip() + nl + blk + nl
    open(CSS, 'w', encoding='utf-8', newline='').write(s)


# ============================================================ insertion dans les pages
def grid(*names):
    return '<div class="fgrid">\n' + '\n'.join(FIG[n] for n in names) + '\n</div>'


ADD = {}

ADD['ds1_primitives'] = r'''<li><b>Primitives utiles</b> : \(\displaystyle\int\frac{r\,\mathrm{d}r}{(r^2+z^2)^{3/2}}=-\frac{1}{\sqrt{r^2+z^2}}\) ; \(\displaystyle\int\frac{\mathrm{d}z}{(r^2+z^2)^{3/2}}=\frac{z}{r^2\sqrt{r^2+z^2}}\).</li>'''

ADD['ds1_qint'] = r'''<p>\(Q_{int}=\sum q_i\) (charges ponctuelles) ou \(\iiint_{V_G}\rho\,\mathrm{d}\tau\) (volume de \(S_G\)) ; une charge surfacique ou linéique traversée compte par \(\sigma\times\)aire ou \(\lambda\times\)longueur de la partie <b>intérieure</b> à \(S_G\).</p>'''

ADD['ds1_plans'] = r'''<h3>Plusieurs objets : superposition, deux plans \(\pm\sigma\)</h3>
<p>Pour des objets coaxiaux ou concentriques, on peut soit <b>sommer les champs</b> de chaque objet (chacun calculé par Gauss), soit calculer directement le \(Q_{int}\) total. Exemple (condensateur plan idéal, plans \(z=0\) chargé \(+\sigma\) et \(z=d\) chargé \(-\sigma\)) : entre les plans \(\vec E=\frac{\sigma}{\varepsilon_0}\vec e_z\), à l'extérieur \(\vec E=\vec0\). Cela donne une différence de potentiel \(V_1-V_2=\frac{\sigma d}{\varepsilon_0}\).</p>'''

ADD['ds1_lignes'] = r'''<li>Équation d'une ligne de champ en cartésien : \(\dfrac{\mathrm{d}x}{E_x}=\dfrac{\mathrm{d}y}{E_y}=\dfrac{\mathrm{d}z}{E_z}\).</li>'''

ADD['ds1_qa'] = r'''<h3>Questions de cours types</h3>
<details class="s4-qa"><summary>Énoncer le théorème de Gauss en définissant chaque terme.</summary><div class="s4-ans">\(\oiint_{S_G}\vec E\cdot\mathrm{d}\vec S=\frac{Q_{int}}{\varepsilon_0}\) : \(S_G\) surface fermée fictive orientée vers l'extérieur, \(\vec E\) le champ <b>total</b> (toutes les charges) sur \(S_G\), \(Q_{int}\) la charge contenue à l'intérieur de \(S_G\) seulement.</div></details>
<details class="s4-qa"><summary>Flux nul à travers une surface fermée : \(\vec E=\vec0\) partout dessus ? Et réciproquement ?</summary><div class="s4-ans">Non : \(\Phi=0\) donne seulement \(Q_{int}=0\). Réciproquement, \(\vec E=\vec0\) en tout point de \(S\) donne \(\Phi=0\) donc \(Q_{int}=0\).</div></details>
<details class="s4-qa"><summary>On remplace la sphère de Gauss autour d'une charge par un cube qui la contient : le flux change-t-il ?</summary><div class="s4-ans">Non, il est identique (\(q/\varepsilon_0\)) : le flux ne dépend que de \(Q_{int}\), pas de la forme de la surface.</div></details>
<details class="s4-qa"><summary>Deux plans de symétrie passent par \(M\) : que dire de \(\vec E(M)\) ? Et avec deux plans d'antisymétrie ?</summary><div class="s4-ans">\(\vec E\) appartient aux deux plans, donc à leur intersection (une droite). Avec deux plans d'antisymétrie, \(\vec E\) est perpendiculaire aux deux : \(\vec E=\vec0\).</div></details>
<details class="s4-qa"><summary>Pourquoi ne peut-on pas utiliser Gauss pour un disque chargé ?</summary><div class="s4-ans">Un disque est fini : il n'a ni symétrie sphérique, ni symétrie cylindrique infinie, ni invariance de plan infini. Hors de l'axe \(\vec E\) a deux composantes et dépend de \(r\) et \(z\). On utilise Coulomb direct (sur l'axe : \(E_z=\frac{\sigma}{2\varepsilon_0}\big(1-\frac{z}{\sqrt{z^2+R^2}}\big)\)).</div></details>'''

ADD['rev_rows'] = r'''<tr><td data-l="Source">Disque \((R,\sigma)\), axe, \(z&gt;0\)</td><td data-l="r&lt;R" colspan="2">\(E_z=\frac{\sigma}{2\varepsilon_0}\Big(1-\frac{z}{\sqrt{z^2+R^2}}\Big)\) (Coulomb)</td><td data-l="V">\(\frac{\sigma}{2\varepsilon_0}\big(\sqrt{z^2+R^2}-z\big)\)</td></tr>
<tr><td data-l="Source">Fil fini \(L\), médiatrice</td><td data-l="r&lt;R" colspan="2">\(E_r=\frac{\lambda L}{2\pi\varepsilon_0r\sqrt{4r^2+L^2}}\), \(E_z=0\)</td><td data-l="V">\(L\to\infty\) : \(\frac{\lambda}{2\pi\varepsilon_0r}\)</td></tr>
<tr><td data-l="Source">Deux plans \(\pm\sigma\) (écart \(d\))</td><td data-l="r&lt;R" colspan="2">\(E=\frac{\sigma}{\varepsilon_0}\) entre les plans, \(0\) à l'extérieur</td><td data-l="V">\(V_1-V_2=\frac{\sigma d}{\varepsilon_0}\)</td></tr>'''

ADD['rev_courbes'] = r'''<h3>Courbes \(E\) et \(V\) à savoir tracer</h3>
<p class="s4-sub">Pour chaque courbe : l'allure à l'intérieur, l'allure à l'extérieur, la continuité de \(V\) et le saut éventuel de \(E\).</p>''' + '\n' + '@@GRID@@'

ADD['rev_lignes'] = r'''<h3>Lignes de champ et équipotentielles</h3>
<ul>
<li>Les équipotentielles (\(V=\) cste) sont <b>perpendiculaires</b> aux lignes de champ et ne se croisent jamais ; \(\vec E\) pointe vers les potentiels décroissants.</li>
<li>Lignes de champ serrées : \(E\) grand. Équipotentielles serrées : \(V\) varie vite donc \(E=\lvert\overrightarrow{\mathrm{grad}}\,V\rvert\) grand.</li>
<li>Charge ponctuelle : équipotentielles = sphères centrées sur la charge. Plan infini : plans parallèles. Fil ou cylindre infini : cylindres coaxiaux.</li>
</ul>''' + '\n' + '@@FIG:doublet@@'

ADD['rev_qa'] = r'''<details class="s4-qa"><summary>Quelle relation entre équipotentielles et lignes de champ ?</summary><div class="s4-ans">Les lignes de champ sont partout perpendiculaires aux équipotentielles (\(\vec E=-\overrightarrow{\mathrm{grad}}\,V\) est normal aux surfaces \(V=\) cste) et orientées vers les \(V\) décroissants. Elles ne se coupent pas, et deux équipotentielles de valeurs différentes non plus.</div></details>
<details class="s4-qa"><summary>Quel est le champ entre deux plans infinis \(+\sigma\) et \(-\sigma\), et à l'extérieur ?</summary><div class="s4-ans">Par superposition de deux plans (\(\frac{\sigma}{2\varepsilon_0}\) chacun) : \(E=\frac{\sigma}{\varepsilon_0}\) entre les plans, dirigé du plan \(+\) vers le plan \(-\), et \(0\) à l'extérieur. La tension vaut \(U=\frac{\sigma d}{\varepsilon_0}\).</div></details>'''

# (page, nom, ancre (texte contenu dans une ligne), position, contenu)
# position 'after' : après la ligne qui contient l'ancre ; 'before' : avant cette ligne ;
# 'before-tbl' : avant le <div class="tbl-wrap"> qui précède l'ancre
INSERTS = [
    ('ds1.html', 'fig:coulomb', r'\vec F_{1/2}=\frac{q_1q_2}', 'after', lambda: FIG['coulomb']),
    ('ds1.html', 'add:ds1_primitives', r'<b>Disque sur son axe</b>', 'after', lambda: ADD['ds1_primitives']),
    ('ds1.html', 'fig:symetries', r'<tr><th>Distribution</th><th>Direction</th>', 'before-tbl', lambda: FIG['symetries']),
    ('ds1.html', 'add:ds1_qint', r'<p>\(S_G\) : surface fermée fictive', 'after', lambda: ADD['ds1_qint']),
    ('ds1.html', 'fig:gauss3', r'<h3>Résultats à savoir retrouver</h3>', 'before', lambda: grid('gauss_sphere', 'gauss_cyl', 'gauss_plan')),
    ('ds1.html', 'fig:plans', r'<h3>Déterminer une constante et son unité</h3>', 'before', lambda: ADD['ds1_plans'] + '\n' + FIG['plans']),
    ('ds1.html', 'add:ds1_lignes', r'<li>Tangentes à \(\vec E\)', 'after', lambda: ADD['ds1_lignes']),
    ('ds1.html', 'add:ds1_qa', '<span class="s4-lbl">Pour s\'entraîner</span>', 'before', lambda: ADD['ds1_qa']),
    ('revision-ds.html', 'add:rev_rows', r'Dipôle, \(r\gg d\)', 'before', lambda: ADD['rev_rows']),
    ('revision-ds.html', 'fig:rev_courbes', r'<span class="s4-lbl">Contrôle rapide</span>', 'before',
     lambda: ADD['rev_courbes'].replace('@@GRID@@', grid('sphere_ev', 'cyl_ev', 'plan_ev'))),
    ('revision-ds.html', 'fig:rev_lignes', r'<span class="s4-lbl">Contrôle rapide</span>', 'after',
     lambda: ADD['rev_lignes'].replace('@@FIG:doublet@@', FIG['doublet'])),
    ('revision-ds.html', 'add:rev_qa', 'Comment justifier à l\'écrit', 'after', lambda: ADD['rev_qa']),
    ('interro-s40.html', 'fig:i_cyl', r'En cylindrique, \(r=Om\)', 'after-fig', lambda: FIG['i_cyl']),
    ('interro-s40.html', 'fig:i_modeles', r'<th>Densité et unité</th>', 'before-tbl', lambda: FIG['i_modeles']),
    ('interro-s40.html', 'fig:i_elem', r'<h3>Passage entre repères</h3>', 'before', lambda: FIG['i_elem']),
    ('interro-s40.html', 'fig:i_flux', r'<p><b>1. Cylindre</b>', 'before', lambda: FIG['i_flux']),
]


def wrap(kind, name, body):
    return '<!-- fiches-blk:%s -->\n%s\n<!-- /fiches-blk:%s -->' % (name, body, name)


def apply_inserts():
    pages = {}
    for page, key, anchor, pos, fn in INSERTS:
        kind, name = key.split(':')
        path = os.path.join(ROOT, page)
        if page not in pages:
            pages[page] = open(path, encoding='utf-8').read()          # lecture en mode texte : \r\n -> \n
        s = pages[page]
        # retirer l'ancien bloc
        s = re.sub(r'<!-- fiches-blk:%s -->.*?<!-- /fiches-blk:%s -->\n?' % (re.escape(name), re.escape(name)), '', s, flags=re.S)
        body = fn()
        i = s.find(anchor)
        if i < 0:
            raise SystemExit('ancre introuvable dans %s : %s' % (page, anchor))
        ls = s.rfind('\n', 0, i) + 1
        le = s.find('\n', i) + 1
        if pos == 'after':
            at = le
        elif pos == 'before':
            at = ls
        elif pos == 'before-tbl':
            at = s.rfind('<div class="tbl-wrap', 0, i)
            at = s.rfind('\n', 0, at) + 1
        elif pos == 'after-fig':
            at = s.find('</figure>', i)
            at = s.find('\n', at) + 1
        s = s[:at] + wrap(kind, name, body) + '\n' + s[at:]
        pages[page] = s
    for page, s in pages.items():
        open(os.path.join(ROOT, page), 'w', encoding='utf-8', newline='\r\n').write(s)
        print('OK', page, len(re.findall(r'<!-- fiches-fig:', s)), 'figures,', len(re.findall(r'<!-- fiches-blk:', s)), 'blocs')


if __name__ == '__main__':
    ensure_css()
    apply_inserts()
