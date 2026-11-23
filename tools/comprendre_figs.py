"""Figures SVG de comprendre.html (importées par tools/gen_comprendre.py).
Chaque figure est une fonction sans argument qui renvoie le code HTML <figure class="fgbox">...</figure>.
Les classes CSS (ob, qp, qn, ef, efh, bl, blh, ax, axh, tx, tm, tc, te, tg, dsh...) sont celles de css/style.css."""
import math
import re


def sb(s):
    """X[Y] -> indice SVG ; X^[Y] -> exposant SVG"""
    s = re.sub(r'\^\[([^\]]*)\]', r'<tspan dy="-4.5" font-size="72%">\1</tspan><tspan dy="4.5">', s)
    n_sup = s.count('<tspan dy="4.5">')
    s = re.sub(r'\[([^\]]*)\]', r'<tspan dy="3.2" font-size="72%">\1</tspan><tspan dy="-3.2">', s)
    n_sub = s.count('<tspan dy="-3.2">')
    # fermeture des tspan « de retour » en fin de chaîne (dans l'ordre inverse d'ouverture : on ferme tout à la fin)
    return s + '</tspan>' * (n_sup + n_sub)


def cap(s):
    return re.sub(r'\[([^\]]*)\]', r'<sub>\1</sub>', s)


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

    def varrow(self, x, y, vx, vy, L, c='ef', hc='efh', size=7):
        """flèche partant de (x, y) pixel, dirigée selon le vecteur MATHÉMATIQUE (vx, vy) (y vers le haut), de longueur L px"""
        n = math.hypot(vx, vy)
        self.arrow(x, y, x + L * vx / n, y - L * vy / n, c, hc, size)
        return x + L * vx / n, y - L * vy / n

    def circ(self, cx, cy, r, c='ob', style=''):
        self.add('<circle class="%s" cx="%.1f" cy="%.1f" r="%.1f"%s/>' % (c, cx, cy, r, (' style="%s"' % style) if style else ''))

    def ell(self, cx, cy, rx, ry, c='ob'):
        self.add('<ellipse class="%s" cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f"/>' % (c, cx, cy, rx, ry))

    def rect(self, x, y, w, h, c='ob'):
        self.add('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (c, x, y, w, h))

    def path(self, d, c='ob'):
        self.add('<path class="%s" d="%s"/>' % (c, d))

    def poly(self, pts, c='ob'):
        self.add('<polygon class="%s" points="%s"/>' % (c, ' '.join('%.1f,%.1f' % p for p in pts)))

    def text(self, x, y, s, c='tx', anchor='middle', size=None, halo=False):
        st = (' style="font-size:%spx"' % size) if size else ''
        cl = c + (' halo' if halo else '')
        self.add('<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' % (cl, x, y, anchor, st, sb(s)))

    def signes(self, pts, signe='+', c='tc', size=13):
        for x, y in pts:
            self.text(x, y + 4, signe, c, 'middle', size)

    def out_sym(self, x, y, r=8):
        """courant / champ sortant de la feuille (cercle pointé)"""
        self.circ(x, y, r, 'ob', 'fill:var(--surface)')
        self.circ(x, y, 2.4, 'pt')

    def in_sym(self, x, y, r=8):
        """courant / champ entrant dans la feuille (cercle croisé)"""
        self.circ(x, y, r, 'ob', 'fill:var(--surface)')
        d = r * 0.68
        self.line(x - d, y - d, x + d, y + d, 'ob')
        self.line(x - d, y + d, x + d, y - d, 'ob')

    def dot(self, x, y, r=3.2, c='pt'):
        self.circ(x, y, r, c)

    def svg(self, aria, caption, maxw=None):
        mw = maxw or self.w
        return ('<figure class="fgbox"><svg class="fg" viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:%dpx">%s</svg>'
                '<figcaption>%s</figcaption></figure>' % (self.w, self.h, aria, mw, ''.join(self.p), cap(caption)))


def pol(ox, oy, r, th_deg):
    """polaire -> pixel (angle trigonométrique, y écran vers le bas)"""
    t = math.radians(th_deg)
    return ox + r * math.cos(t), oy - r * math.sin(t)


FIG = {}


# ============================================================== CH0
def fig_cyl():
    f = Fig(460, 270)
    ox, oy = 90, 232
    f.arrow(ox - 20, oy, ox + 345, oy, 'ax', 'axh', 7)
    f.text(ox + 352, oy + 5, 'x', 'tm', 'start', 13)
    f.arrow(ox, oy + 15, ox, oy - 220, 'ax', 'axh', 7)
    f.text(ox + 8, oy - 214, 'y', 'tm', 'start', 13)
    f.text(ox - 10, oy + 16, 'O', 'tx', 'end', 13)

    def cell(r1, r2, t1, t2, c):
        a = pol(ox, oy, r1, t1)
        b = pol(ox, oy, r2, t1)
        cc = pol(ox, oy, r2, t2)
        d = pol(ox, oy, r1, t2)
        f.path('M%.1f %.1f L%.1f %.1f A%d %d 0 0 0 %.1f %.1f L%.1f %.1f A%d %d 0 0 1 %.1f %.1f Z'
               % (a[0], a[1], b[0], b[1], r2, r2, cc[0], cc[1], d[0], d[1], r1, r1, a[0], a[1]), c)

    t1, t2 = 30, 50
    cell(150, 185, t1, t2, 'qp')
    cell(60, 95, t1, t2, 'qn')
    # rayons pointillés
    for t in (t1, t2):
        p = pol(ox, oy, 215, t)
        f.line(ox, oy, p[0], p[1], 'dsh')
    # arc de l'angle theta
    p0 = pol(ox, oy, 40, 0)
    p1 = pol(ox, oy, 40, t1)
    f.path('M%.1f %.1f A40 40 0 0 0 %.1f %.1f' % (p0[0], p0[1], p1[0], p1[1]), 'ac')
    f.text(ox + 55, oy - 11, 'θ', 'tc', 'middle', 15)
    p1 = pol(ox, oy, 125, t1)
    p2 = pol(ox, oy, 125, t2)
    f.path('M%.1f %.1f A125 125 0 0 0 %.1f %.1f' % (p1[0], p1[1], p2[0], p2[1]), 'ec')
    f.text(*pol(ox, oy, 137, 40), 'dθ', 'te', 'middle', 14)
    # étiquettes
    lab = pol(ox, oy, 168, t1)
    f.text(lab[0] + 10, lab[1] + 17, 'dr', 'tx', 'start', 14)
    lab = pol(ox, oy, 202, 51)
    f.text(lab[0] - 6, lab[1] - 6, 'r dθ', 'tg', 'start', 14)
    f.text(ox + 118, oy - 36, 'même dθ, arc plus court', 'tm', 'start', 12, halo=True)
    # base locale au centre de la grande cellule
    c = pol(ox, oy, 167.5, 40)
    er = (math.cos(math.radians(40)), math.sin(math.radians(40)))
    f.varrow(c[0], c[1], er[0], er[1], 36, 'bl', 'blh', 7)
    f.varrow(c[0], c[1], -er[1], er[0], 36, 'ef', 'efh', 7)
    f.text(c[0] + 31, c[1] - 5, 'e[r]', 'tc', 'start', 14, halo=True)
    f.text(c[0] - 46, c[1] - 34, 'e[θ]', 'te', 'middle', 14, halo=True)
    f.dot(c[0], c[1], 2.4)
    FIG['cyl'] = f.svg('Cellule élémentaire en coordonnées cylindriques vue de dessus',
                       'Vue de dessus (plan xOy). La cellule entre r et r+dr, θ et θ+dθ est presque un rectangle de côtés <b>dr</b> et <b>r dθ</b> : son aire est r dr dθ. À même dθ, un arc loin de l\'axe est plus long qu\'un arc près de l\'axe.', 460)


def fig_sph():
    f = Fig(440, 322)
    ox, oy, R = 130, 172, 130
    f.circ(ox, oy, R, 'ob2')
    f.ell(ox, oy, R, 34, 'hid2')
    f.arrow(ox, oy + 135, ox, 16, 'ax', 'axh', 7)
    f.text(ox + 10, 24, 'z', 'tm', 'start', 13)
    f.text(ox - 10, oy + 16, 'O', 'tx', 'end', 13)
    th = math.radians(40)
    mx, my = ox + R * math.sin(th), oy - R * math.cos(th)
    # petit cercle (parallèle)
    rho = R * math.sin(th)
    f.ell(ox, my, rho, 22, 'dsh')
    f.line(ox, my, mx, my, 'dsh')
    f.text(ox + rho / 2, my - 7, 'r sinθ', 'tg', 'middle', 14, halo=True)
    f.line(ox, oy, mx, my, 'ob')
    f.text(ox + 70, oy - 36, 'r', 'tx', 'start', 15, halo=True)
    # arc de theta
    f.path('M%.1f %.1f A45 45 0 0 1 %.1f %.1f' % (ox, oy - 45, ox + 45 * math.sin(th), oy - 45 * math.cos(th)), 'ac')
    f.text(ox + 16, oy - 55, 'θ', 'tc', 'middle', 15)
    # base locale en M
    f.arrow(mx, my, mx + 34 * math.sin(th), my - 34 * math.cos(th), 'bl', 'blh', 7)
    f.text(mx + 40 * math.sin(th) + 4, my - 40 * math.cos(th) - 2, 'e[r]', 'tc', 'start', 14, halo=True)
    f.arrow(mx, my, mx + 34 * math.cos(th), my + 34 * math.sin(th), 'ef', 'efh', 7)
    f.text(mx + 36 * math.cos(th) + 6, my + 36 * math.sin(th) + 12, 'e[θ]', 'te', 'start', 14, halo=True)
    f.arrow(mx, my, mx - 4, my - 30, 'nb', 'nbh', 7)
    f.text(mx - 8, my - 36, 'e[φ]', 'tg', 'end', 14, halo=True)
    f.dot(mx, my, 3.4, 'ptM')
    f.text(mx + 14, my + 5, 'M', 'tx', 'start', 14)
    f.text(268, 122, 'cercle de rayon r sinθ', 'tm', 'start', 12.5)
    f.text(268, 138, '(parcouru quand φ varie)', 'tm', 'start', 12.5)
    f.arrow(266, 128, ox + rho * 0.8 + 6, my + 22 * 0.6 + 2, 'dsh', 'efh', 5)
    f.text(300, 230, 'e[φ] est perpendiculaire à la', 'tm', 'start', 12.5)
    f.text(300, 246, 'page (vers le fond en M)', 'tm', 'start', 12.5)
    FIG['sph'] = f.svg('Coordonnées sphériques : r, theta et le cercle de rayon r sin theta',
                       'Coupe par le plan contenant Oz et M. En faisant varier <b>φ</b>, M décrit un cercle de rayon r sinθ (sa distance à l\'axe), donc un arc de longueur <b>r sinθ dφ</b>. En faisant varier θ, M décrit un arc de grand cercle de longueur <b>r dθ</b>.', 440)


def fig_grad():
    f = Fig(440, 292)
    cx, cy = 140, 135
    a, b = 52, 33
    for s in (1, 2, 3, 4):
        f.ell(cx, cy, a * s, b * s, 'ob2' if s != 2 else 'ob')
    f.dot(cx, cy, 3.2)
    f.text(cx - 8, cy + 18, 'V max', 'tm', 'end', 12)
    for s, v in ((1, 'V = 4'), (2, 'V = 3'), (3, 'V = 2'), (4, 'V = 1')):
        f.text(cx + 6, cy - b * s - 3, v, 'tx', 'start', 12, halo=True)
    t = math.radians(35)
    s = 2
    px, py = cx + a * s * math.cos(t), cy - b * s * math.sin(t)
    # tangente et normale
    nx, ny = math.cos(t) / a, math.sin(t) / b  # gradient de s (math)
    n = math.hypot(nx, ny)
    nx, ny = nx / n, ny / n
    tx_, ty_ = -ny, nx
    f.line(px - 52 * tx_, py + 52 * ty_, px + 52 * tx_, py - 52 * ty_, 'dsh')
    f.arrow(px, py, px - 52 * nx, py + 52 * ny, 'bl', 'blh', 8)
    f.arrow(px, py, px + 52 * nx, py - 52 * ny, 'ef', 'efh', 8)
    f.dot(px, py, 3.6, 'ptM')
    f.text(px - 52 * nx - 2, py + 52 * ny + 20, 'grad V', 'tc', 'end', 14, halo=True)
    f.text(px + 52 * nx + 6, py - 52 * ny - 4, 'E = −grad V', 'te', 'start', 14, halo=True)
    f.text(px - 54 * tx_ + 4, py + 54 * ty_ + 14, 'tangente', 'tm', 'start', 12, halo=True)
    f.text(220, 286, 'courbes de niveau de V (comme une carte topographique)', 'tm', 'middle', 12)
    FIG['grad'] = f.svg('Gradient perpendiculaire aux courbes de niveau',
                        'Le gradient est <b>perpendiculaire</b> aux courbes de niveau et pointe vers les valeurs <b>croissantes</b> (la plus forte pente montante). Le champ E = −grad V pointe à l\'opposé : vers les V décroissants.', 440)


def fig_flux_cyl():
    f = Fig(470, 250)
    cx, rx, ry, ytop, ybot = 150, 62, 18, 66, 196
    f.ell(cx, ytop, rx, ry, 'qp0')
    f.path('M%d %d A%d %d 0 0 1 %d %d' % (cx - rx, ybot, rx, ry, cx + rx, ybot), 'hid')
    f.path('M%d %d A%d %d 0 0 0 %d %d' % (cx - rx, ybot, rx, ry, cx + rx, ybot), 'ob')
    f.line(cx - rx, ytop, cx - rx, ybot, 'ob')
    f.line(cx + rx, ytop, cx + rx, ybot, 'ob')
    f.ell(cx, ytop, rx, ry, 'ob')
    # champ radial sur la face latérale
    f.arrow(cx - rx, 130, cx - rx - 40, 130, 'bl', 'blh', 7)
    f.arrow(cx + rx, 130, cx + rx + 40, 130, 'bl', 'blh', 7)
    for x in (cx - 30, cx, cx + 30):
        f.arrow(x, 135 + 0.0, x + (x - cx) * 0.55, 160, 'bl', 'blh', 6)
    f.text(cx + rx + 46, 134, 'A', 'tc', 'start', 15)
    f.text(cx - rx - 46, 134, 'A', 'tc', 'end', 15)
    # dS sur la face latérale (droite) : meme direction
    # face haute : A dans le plan, dS vertical
    f.arrow(cx, ytop, cx, ytop - 42, 'nb', 'nbh', 7)
    f.text(cx + 8, ytop - 38, 'dS (faces haute et basse)', 'tg', 'start', 12.5)
    f.arrow(cx + 20, ytop + 3, cx + 46, ytop + 3, 'bl', 'blh', 6)
    f.arrow(cx - 20, ytop + 3, cx - 46, ytop + 3, 'bl', 'blh', 6)
    # cotes
    f.arrow(cx - rx - 14, ytop, cx - rx - 14, ybot, 'dsh', 'efh', 5)
    f.arrow(cx - rx - 14, ybot, cx - rx - 14, ytop, 'dsh', 'efh', 5)
    f.text(cx - rx - 20, (ytop + ybot) / 2 + 24, 'h', 'tx', 'end', 14)
    f.line(cx, ybot + 24, cx + rx, ybot + 24, 'dsh')
    f.text(cx + rx / 2, ybot + 40, 'a', 'tx', 'middle', 14)
    # panneau texte
    f.text(300, 76, 'face latérale (r = a) :', 'tx', 'start', 13)
    f.text(300, 94, 'A ∥ dS et A = A[0] a', 'tc', 'start', 13)
    f.text(300, 112, 'partout pareil : Φ = A × S', 'tm', 'start', 12.5)
    f.text(300, 156, 'faces haute et basse :', 'tx', 'start', 13)
    f.text(300, 174, 'A ⟂ dS, produit scalaire nul', 'te', 'start', 13)
    f.text(300, 192, 'donc Φ = 0', 'te', 'start', 13)
    FIG['flux_cyl'] = f.svg('Flux du champ A = A0 r e_r à travers un cylindre fermé',
                            'Cylindre fermé de rayon a et de hauteur h, champ radial A = A[0] r e[r]. Seule la face latérale « voit » le champ passer à travers elle ; les deux disques sont parallèles au champ.', 470)


# ============================================================== CH1
def fig_sym_E():
    f = Fig(540, 250)
    d, yc, my = 80, 205, 118
    for cx, signs, titre, note in ((135, (1, 1), 'deux charges égales', 'E reste DANS le plan de symétrie'),
                                   (410, (1, -1), 'deux charges opposées', 'E est PERPENDICULAIRE au plan d\'antisymétrie')):
        f.line(cx, 28, cx, 232, 'dsh')
        f.text(cx, 16, titre, 'tx', 'middle', 13.5)
        f.text(cx, 247, note, 'tm', 'middle', 12)
        f.circ(cx - d, yc, 13, 'qp')
        f.text(cx - d, yc + 5, '+', 'tc', 'middle', 16)
        f.circ(cx + d, yc, 13, 'qp' if signs[1] > 0 else 'qn')
        f.text(cx + d, yc + 5, '+' if signs[1] > 0 else '−', 'tc' if signs[1] > 0 else 'te', 'middle', 16)
        # champs en M
        e1 = (d, my - yc)  # direction (math) : M - charge1 = (d, yc - my) en math
        e1 = (d, yc - my)
        e2 = (-d, yc - my) if signs[1] > 0 else (-d, -(yc - my))
        # pour une charge négative : champ dirigé VERS la charge : M->charge = (d, -(yc-my)) ; ici composante -(M-charge) = (+d, -(yc-my))
        if signs[1] < 0:
            e2 = (d, -(yc - my))
        n1 = math.hypot(*e1)
        L1 = 50
        # vecteurs de longueur proportionnelle à 1/dist^2 identique ici
        p1 = (cx + L1 * e1[0] / n1, my - L1 * e1[1] / n1)
        p2 = (cx + L1 * e2[0] / n1, my - L1 * e2[1] / n1)
        tot = (p1[0] + p2[0] - cx, p1[1] + p2[1] - my)
        f.line(p1[0], p1[1], tot[0], tot[1], 'dsh')
        f.line(p2[0], p2[1], tot[0], tot[1], 'dsh')
        f.arrow(cx, my, p1[0], p1[1], 'efl', 'efh', 6)
        f.arrow(cx, my, p2[0], p2[1], 'efl', 'efh', 6)
        f.arrow(cx, my, tot[0], tot[1], 'ef', 'efh', 8)
        f.dot(cx, my, 3.6, 'ptM')
        f.text(cx + (8 if signs[1] > 0 else -10), my + 18 if signs[1] > 0 else my + 5, 'M', 'tx', 'start' if signs[1] > 0 else 'end', 14)
        f.text(p1[0] + (8 if p1[0] > cx else -8), p1[1] - 2, 'E[1]', 'te', 'start' if p1[0] > cx else 'end', 13, halo=True)
        f.text(p2[0] + (8 if p2[0] > cx else -8), p2[1] - 2, 'E[2]', 'te', 'start' if p2[0] > cx else 'end', 13, halo=True)
        f.text(tot[0] + (10 if tot[0] > cx + 1 else 0), tot[1] - 8 if abs(tot[0] - cx) < 1 else tot[1] + 5, 'E', 'te', 'start', 15, halo=True)
    FIG['sym_E'] = f.svg('Symétrie et antisymétrie pour le champ électrique',
                         'À gauche, le plan médiateur (pointillés) est un plan de <b>symétrie</b> des charges : les composantes horizontales de E[1] et E[2] se compensent, E est dans le plan. À droite, c\'est un plan d\'<b>antisymétrie</b> : les composantes verticales se compensent, E est perpendiculaire au plan.', 540)


def fig_gauss_sph():
    f = Fig(450, 296)
    cx, cy = 140, 140
    f.circ(cx, cy, 70, 'qp')
    for k in range(12):
        a = 2 * math.pi * k / 12 + 0.26
        f.text(cx + 61 * math.cos(a), cy - 61 * math.sin(a) + 4, '+', 'tc', 'middle', 13)
    f.text(cx, cy + 4, '+', 'tc', 'middle', 13)
    f.circ(cx, cy, 112, 'gs')
    f.circ(cx, cy, 40, 'gs')
    for k in range(8):
        a = 2 * math.pi * k / 8 + 0.2
        f.arrow(cx + 112 * math.cos(a), cy - 112 * math.sin(a), cx + 136 * math.cos(a), cy - 136 * math.sin(a), 'ef', 'efh', 6)
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.55
        f.arrow(cx + 41 * math.cos(a), cy - 41 * math.sin(a), cx + 58 * math.cos(a), cy - 58 * math.sin(a), 'ef', 'efh', 5)
    a = math.radians(-65)
    f.line(cx, cy, cx + 112 * math.cos(a), cy - 112 * math.sin(a), 'dsh')
    f.text(cx + 50 * math.cos(a) + 10, cy - 50 * math.sin(a) + 4, 'r', 'tx', 'start', 14, halo=True)
    f.line(cx, cy, cx + 70 * math.cos(math.radians(150)), cy - 70 * math.sin(math.radians(150)), 'dsh')
    f.text(cx + 72 * math.cos(math.radians(150)) - 4, cy - 72 * math.sin(math.radians(150)) - 4, 'R', 'tx', 'end', 14)
    f.text(300, 60, 'dehors (r > R) :', 'tx', 'start', 13)
    f.text(300, 78, 'Q[int] = Q', 'tc', 'start', 13)
    f.text(300, 96, 'toute la charge compte', 'tm', 'start', 12)
    f.text(300, 140, 'dedans (r < R) :', 'tx', 'start', 13)
    f.text(300, 158, 'Q[int] < Q', 'tc', 'start', 13)
    f.text(300, 176, 'seule la charge à', 'tm', 'start', 12)
    f.text(300, 192, 'l\'intérieur de la sphère', 'tm', 'start', 12)
    f.text(300, 208, 'pointillée compte', 'tm', 'start', 12)
    f.text(cx, 290, 'surfaces de Gauss (pointillés) : sphères de rayon r', 'tm', 'middle', 12)
    FIG['gauss_sph'] = f.svg('Surfaces de Gauss pour une boule chargée',
                             'Boule de rayon R uniformément chargée. Les sphères en pointillés sont des surfaces de Gauss : E est radial et de même norme en tous leurs points, donc le flux se calcule sans intégrale.', 450)


def fig_E_r():
    f = Fig(450, 250)
    x0, y0 = 56, 205
    sx, sy = 112, 140  # px par R, px par E(R)
    f.arrow(x0 - 10, y0, x0 + 3 * sx + 24, y0, 'ax', 'axh', 7)
    f.arrow(x0, y0 + 8, x0, y0 - 175, 'ax', 'axh', 7)
    f.text(x0 + 3 * sx + 24, y0 + 18, 'r', 'tm', 'end', 14)
    f.text(x0 + 8, y0 - 168, 'E', 'tm', 'start', 14)
    pts = []
    for k in range(0, 101):
        x = k / 100.0
        pts.append((x0 + x * sx, y0 - x * sy))
    for k in range(0, 201):
        x = 1 + 2 * k / 200.0
        pts.append((x0 + x * sx, y0 - sy / x**2))
    f.add('<polyline class="cv2" fill="none" points="%s"/>' % ' '.join('%.1f,%.1f' % p for p in pts))
    f.line(x0 + sx, y0, x0 + sx, y0 - sy, 'dsh')
    f.line(x0, y0 - sy, x0 + sx, y0 - sy, 'dsh')
    f.text(x0 + sx, y0 + 18, 'R', 'tx', 'middle', 14)
    f.text(x0 - 6, y0 - sy + 5, 'E(R)', 'tx', 'end', 13)
    for xr, lab in ((0.5, 'E(R)/2'), (2.0, 'E(R)/4')):
        yy = y0 - (xr * sy if xr < 1 else sy / xr**2)
        f.dot(x0 + xr * sx, yy, 3.6, 'ptM')
    f.text(x0 + 0.5 * sx - 8, y0 - 0.5 * sy - 10, 'E(R)/2', 'tx', 'end', 12.5, halo=True)
    f.text(x0 + 2 * sx + 4, y0 - sy / 4 - 12, 'E(R)/4', 'tx', 'start', 12.5, halo=True)
    f.text(x0 + 0.42 * sx, y0 + 18, 'R/2', 'tm', 'middle', 12)
    f.text(x0 + 2 * sx, y0 + 18, '2R', 'tm', 'middle', 12)
    f.text(x0 + 0.46 * sx - 22, y0 - 110, 'droite (∝ r)', 'te', 'end', 13, halo=True)
    f.text(x0 + 1.55 * sx, y0 - 95, '1/r² (comme une', 'te', 'start', 13, halo=True)
    f.text(x0 + 1.55 * sx, y0 - 78, 'charge ponctuelle)', 'te', 'start', 13, halo=True)
    FIG['E_r'] = f.svg('Champ d\'une boule uniformément chargée en fonction de r',
                       'E(r) pour une boule uniformément chargée : proportionnel à r à l\'intérieur, en 1/r² à l\'extérieur, continu en r = R.', 450)


# ============================================================== CH2
def fig_fil_EV():
    f = Fig(540, 250)

    def panel(ox, titre, kind):
        oy = 190
        f.arrow(ox - 6, oy, ox + 220, oy, 'ax', 'axh', 7)
        f.text(ox + 220, oy + 17, 'r', 'tm', 'end', 14)
        f.text(ox + 100, 16, titre, 'tx', 'middle', 13.5)
        sx = 70  # px par R0
        xR = ox + sx
        f.line(xR, 28, xR, oy + 4, 'dsh')
        f.text(xR, oy + 17, 'R[0]', 'tx', 'middle', 13)
        pts = []
        if kind == 'E':
            f.arrow(ox, oy + 6, ox, 30, 'ax', 'axh', 7)
            f.text(ox + 8, 38, 'E', 'tm', 'start', 14)
            for k in range(0, 121):
                r = 0.34 + (3.0 - 0.34) * k / 120.0
                yv = 52 / r
                pts.append((ox + sx * r, oy - min(yv, 150)))
            f.add('<polyline class="cv2" fill="none" points="%s"/>' % ' '.join('%.1f,%.1f' % p for p in pts))
            f.text(ox + sx * 1.4, oy - 92, 'E = λ / (2π ε[0] r)', 'te', 'start', 12.5, halo=True)
            f.text(ox + sx * 1.4, oy - 75, 'tend vers 0 lentement', 'tm', 'start', 12, halo=True)
        else:
            y0 = 112  # V = V0 = 0 en R0
            f.arrow(ox, oy + 6, ox, 30, 'ax', 'axh', 7)
            f.text(ox + 8, 38, 'V', 'tm', 'start', 14)
            f.line(ox, y0, ox + 214, y0, 'dsh')
            f.text(ox - 4, y0 + 5, 'V[0]', 'tx', 'end', 13)
            for k in range(0, 121):
                r = 0.34 + (3.0 - 0.34) * k / 120.0
                yv = y0 + 40 * math.log(r)
                pts.append((ox + sx * r, yv))
            f.add('<polyline class="cv1" fill="none" points="%s"/>' % ' '.join('%.1f,%.1f' % p for p in pts))
            f.dot(xR, y0, 3.6, 'ptM')
            # tangente en R0 de pente 40/70 px/px (descend a droite : en écran, y augmente quand r augmente) -> V' = -k/r
            f.line(xR - 38, y0 - 38 * 40 / sx, xR + 38, y0 + 38 * 40 / sx, 'dsh')
            f.text(ox + sx * 1.3, y0 - 34, 'V = V[0] − λ/(2π ε[0]) ln(r/R[0])', 'tc', 'start', 12, halo=True)
            f.text(ox + sx * 1.3, y0 - 18, 'décroît sans jamais se stabiliser', 'tm', 'start', 12, halo=True)
            f.text(ox + sx * 2.0, y0 + 63, 'pente = −E', 'tm', 'start', 12.5, halo=True)

    panel(24, 'champ E(r)', 'E')
    panel(290, 'potentiel V(r)', 'V')
    FIG['fil_EV'] = f.svg('Champ et potentiel d\'un fil infini', 'Fil infini chargé : E(r) en 1/r, V(r) logarithmique. La pente de V(r) est −E : plus le champ est fort, plus V change vite. V ne peut pas valoir 0 « à l\'infini » ; on impose V(R[0]) = V[0].', 540)


def fig_equi():
    f = Fig(420, 280)
    cx, cy = 150, 140
    for k in range(12):
        a = 2 * math.pi * k / 12 + 0.1
        f.arrow(cx + 14 * math.cos(a), cy - 14 * math.sin(a), cx + 124 * math.cos(a), cy - 124 * math.sin(a), 'efl', 'efh', 7)
    for r, v in ((45, 'V[1]'), (80, 'V[2]'), (112, 'V[3]')):
        f.circ(cx, cy, r, 'ob')
    f.circ(cx, cy, 11, 'qp')
    f.text(cx, cy + 5, '+', 'tc', 'middle', 14)
    f.text(cx + 47, cy + 16, 'V[1]', 'tx', 'start', 13, halo=True)
    f.text(cx + 82, cy + 16, 'V[2]', 'tx', 'start', 13, halo=True)
    f.text(cx + 114, cy + 16, 'V[3]', 'tx', 'start', 13, halo=True)
    f.text(300, 100, 'V[1] > V[2] > V[3]', 'tc', 'start', 14)
    f.text(300, 120, 'les lignes de champ', 'tm', 'start', 12.5)
    f.text(300, 136, 'coupent les équipotentielles', 'tm', 'start', 12.5)
    f.text(300, 152, 'à angle droit, en allant', 'tm', 'start', 12.5)
    f.text(300, 168, 'vers les V décroissants', 'tm', 'start', 12.5)
    FIG['equi'] = f.svg('Équipotentielles et lignes de champ', 'Vue en coupe d\'un fil (ou d\'une charge ponctuelle) positif : cercles = équipotentielles (même altitude de potentiel), flèches orange = lignes de champ, toujours perpendiculaires aux cercles et dirigées vers les V décroissants.', 420)


# ============================================================== CH3
def fig_superpo():
    f = Fig(540, 290)
    y1, y2 = 200, 110  # plaques z = 0 et z = e
    cols = (110, 280, 450)
    titres = ('plan +σ seul', 'plan −σ seul', 'somme')
    for cx, t in zip(cols, titres):
        f.text(cx, 18, t, 'tx', 'middle', 13.5)
    f.text(6, y1 - 4, 'z = 0', 'tm', 'start', 12)
    f.text(6, y2 - 4, 'z = e', 'tm', 'start', 12)
    f.text(6, 262, 'z < 0', 'tm', 'start', 12)
    f.text(6, 160, '0 < z < e', 'tm', 'start', 12)
    f.text(6, 68, 'z > e', 'tm', 'start', 12)
    for i, cx in enumerate(cols):
        plus = (i == 0)
        both = (i == 2)
        w = 130
        f.rect(cx - w / 2, y1 - 4, w, 8, 'qp' if (plus or both) else 'qp0')
        f.rect(cx - w / 2, y2 - 4, w, 8, 'qn' if (i == 1 or both) else 'qp0')
        if plus or both:
            f.text(cx - w / 2 + 12, y1 + 16, '+σ', 'tc', 'start', 12)
        if i == 1 or both:
            f.text(cx - w / 2 + 12, y2 - 10, '−σ', 'te', 'start', 12)
    # colonne 1 : plan en z=0 : champ vers le haut au-dessus, vers le bas dessous (partout)
    for cx in (cols[0],):
        f.arrow(cx, 222, cx, 258, 'bl', 'blh', 7)
        f.arrow(cx, 190, cx, 148, 'bl', 'blh', 7)
        f.arrow(cx, 100, cx, 58, 'bl', 'blh', 7)
        for y in (240, 168, 78):
            f.text(cx + 12, y + 5, 'σ/2ε[0]', 'tc', 'start', 12, halo=True)
    # colonne 2 : plan en z=e, charge -sigma : champ vers le plan, donc vers le haut en dessous, vers le bas au-dessus
    cx = cols[1]
    f.arrow(cx, 258, cx, 226, 'ef', 'efh', 7)
    f.arrow(cx, 190, cx, 148, 'ef', 'efh', 7)
    f.arrow(cx, 58, cx, 94, 'ef', 'efh', 7)
    for y in (240, 168, 78):
        f.text(cx + 12, y + 5, 'σ/2ε[0]', 'te', 'start', 12, halo=True)
    # colonne 3 : somme
    cx = cols[2]
    f.arrow(cx, 192, cx, 124, 'nb', 'nbh', 8)
    f.text(cx + 14, 164, 'σ/ε[0]', 'tg', 'start', 13, halo=True)
    f.text(cx, 252, 'E = 0', 'tg', 'middle', 15)
    f.text(cx, 66, 'E = 0', 'tg', 'middle', 15)
    FIG['superpo'] = f.svg('Superposition de deux plans chargés',
                           'Un plan chargé crée σ/2ε[0] de chaque côté, dirigé en s\'éloignant du plan (+σ, bleu) ou en s\'en approchant (−σ, orange). Entre les plans les deux champs sont dans le même sens et s\'additionnent ; à l\'extérieur ils sont opposés et s\'annulent.', 540)


def fig_cond_ex():
    f = Fig(570, 200)
    x0, x1 = 70, 240
    ya, yb = 36, 136
    f.rect(x0, ya - 6, x1 - x0, 10, 'qn')
    f.rect(x0, yb - 4, x1 - x0, 10, 'qp')
    f.signes([(x, yb - 12) for x in range(78, 235, 28)], '+', 'tc', 12)
    f.signes([(x, ya + 14) for x in range(78, 235, 28)], '−', 'te', 12)
    for x in range(78, 235, 34):
        f.arrow(x, yb - 20, x, ya + 18, 'ef', 'efh', 6)
    f.arrow(x1 + 22, yb - 4, x1 + 22, ya + 4, 'dsh', 'efh', 5)
    f.arrow(x1 + 22, ya + 4, x1 + 22, yb - 4, 'dsh', 'efh', 5)
    f.text(x1 + 30, (ya + yb) / 2 + 4, 'e = 1 mm', 'tx', 'start', 13)
    f.text((x0 + x1) / 2, yb + 28, 'S = 100 cm²', 'tx', 'middle', 13)
    f.line(x0, yb + 12, x1, yb + 12, 'dsh')
    # générateur (symbole pile) entre les deux armatures
    mid = (ya + yb) / 2
    f.line(x0 - 20, yb + 1, x0, yb + 1, 'ob')
    f.line(x0 - 20, ya - 1, x0, ya - 1, 'ob')
    f.line(x0 - 20, yb + 1, x0 - 20, mid + 8, 'ob')
    f.line(x0 - 20, ya - 1, x0 - 20, mid - 8, 'ob')
    f.line(x0 - 31, mid + 8, x0 - 9, mid + 8, 'ob')
    f.line(x0 - 26, mid - 8, x0 - 14, mid - 8, 'ob')
    f.text(x0 - 38, mid - 2, 'U', 'tx', 'end', 14)
    f.text(x0 - 38, mid + 13, '100 V', 'tx', 'end', 12.5)
    f.text(350, 52, 'Q = C U = 8,85 nC', 'tc', 'start', 13)
    f.text(350, 74, 'σ = Q/S = 8,85×10^[−7] C·m^[−2]', 'tc', 'start', 12.5)
    f.text(350, 96, 'E = σ/ε[0] = U/e = 10^[5] V·m^[−1]', 'te', 'start', 12.5)
    f.text(350, 118, 'C = ε[0]S/e ≈ 88,5 pF', 'tg', 'start', 13)
    FIG['cond_ex'] = f.svg('Condensateur plan de l\'exemple : S = 100 cm², e = 1 mm, U = 100 V',
                           'Le condensateur de l\'exemple : armature 1 (+Q) en bas, armature 2 (−Q) en haut, tension U = 100 V. Les ordres de grandeur sont ceux d\'un petit composant réel.', 570)


# ============================================================== CH4
def fig_lorentz():
    f = Fig(540, 270)
    cx, cy, R = 170, 140, 88
    # champ B sortant : points
    for gx in range(30, 340, 44):
        for gy in range(30, 260, 44):
            dd = math.hypot(gx - cx, gy - cy)
            if abs(dd - R) < 16:
                continue
            f.circ(gx, gy, 5.5, 'ax', 'fill:none')
            f.circ(gx, gy, 1.6, 'axh')
    f.circ(cx, cy, R, 'cv1')
    # particule en haut, v vers la droite, F vers le bas
    px, py = cx, cy - R
    f.arrow(px, py, px + 58, py, 'nb', 'nbh', 8)
    f.text(px + 64, py + 5, 'v', 'tg', 'start', 15)
    f.arrow(px, py, px, py + 50, 'nc', 'nch', 8)
    f.text(px + 8, py + 36, 'F', 'te', 'start', 15, halo=True)
    f.circ(px, py, 9, 'qp')
    f.text(px, py + 5, '+', 'tc', 'middle', 13)
    # rayon
    a = math.radians(-40)
    f.line(cx, cy, cx + R * math.cos(a), cy - R * math.sin(a), 'dsh')
    f.text(cx + 50 * math.cos(a) + 2, cy - 50 * math.sin(a) + 18, 'r', 'tx', 'middle', 15, halo=True)
    f.dot(cx, cy, 3, 'pt')
    # panneau texte
    f.text(360, 54, 'B sort de la page (⊙)', 'tx', 'start', 13)
    f.text(360, 76, 'q > 0 : rotation horaire', 'tx', 'start', 13)
    f.text(360, 98, 'F = q v ∧ B  est ⟂ v', 'te', 'start', 13)
    f.text(360, 120, 'donc |v| = constante', 'tm', 'start', 12.5)
    f.text(360, 168, 'r = m v / (|q| B)', 'tc', 'start', 15)
    f.text(360, 190, 'B plus fort → r plus petit', 'tm', 'start', 12.5)
    f.text(360, 206, 'v plus grand → r plus grand', 'tm', 'start', 12.5)
    FIG['lorentz'] = f.svg('Trajectoire circulaire d\'une charge dans un champ magnétique uniforme',
                           'Une charge positive dans un champ B uniforme sortant de la feuille. La force magnétique est toujours perpendiculaire à la vitesse : elle courbe la trajectoire sans changer la vitesse, d\'où un cercle de rayon r = mv/(|q|B).', 540)


def fig_biot_fil():
    f = Fig(520, 310)
    wx, oy = 90, 160
    mx = 270
    f.arrow(wx, 292, wx, 14, 'ob', 'efh', 8)
    f.text(wx - 12, 28, 'I', 'tx', 'end', 15)
    f.text(wx - 10, oy + 16, 'O', 'tx', 'end', 14)
    f.dot(wx, oy, 3)
    zp = 90
    f.dot(wx, oy - zp, 3.4)
    f.text(wx - 10, oy - zp + 4, 'P', 'tx', 'end', 14)
    f.dot(wx, oy + zp, 3, 'ptM')
    f.text(wx - 10, oy + zp + 5, "P′ (−z)", 'tm', 'end', 12.5)
    # dl au voisinage de P
    f.arrow(wx + 7, oy - zp + 10, wx + 7, oy - zp - 14, 'bl', 'blh', 6)
    f.text(wx + 14, oy - zp - 10, 'dℓ = dz e[z]', 'tc', 'start', 12.5)
    # M
    f.line(wx, oy, mx, oy, 'dsh')
    f.text((wx + mx) / 2, oy + 18, 'r', 'tx', 'middle', 15)
    f.line(wx, oy - zp, mx, oy, 'ob')
    f.text(190, oy - 60, 'PM', 'tx', 'end', 14, halo=True)
    f.line(wx, oy + zp, mx, oy, 'hid2')
    f.line(wx - 6, oy - zp, wx - 6, oy, 'dsh')
    f.text(wx - 24, oy - zp / 2 + 5, 'z', 'tx', 'end', 14)
    # angle alpha en M
    a0 = math.pi
    a1 = math.pi - math.atan2(zp, mx - wx)
    rr = 52
    f.path('M%.1f %.1f A%d %d 0 0 1 %.1f %.1f' % (mx + rr * math.cos(a0), oy - rr * math.sin(a0) * 0 + 0, rr, rr, mx + rr * math.cos(a1), oy - rr * math.sin(a1)), 'ac')
    f.text(mx - 66, oy - 12, 'α', 'tc', 'middle', 16)
    # dB en M : entrant
    f.in_sym(mx, oy, 10)
    f.text(mx, oy + 30, 'M', 'tx', 'middle', 15)
    f.text(mx + 18, oy - 6, 'dB entrant', 'tc', 'start', 14)
    f.text(mx + 18, oy + 10, '(e[θ] = e[y] vers le fond)', 'tm', 'start', 12)
    f.text(mx + 44, 40, 'tire-bouchon :', 'tx', 'start', 13)
    f.text(mx + 44, 58, 'dℓ → PM tourne à droite', 'tm', 'start', 12)
    f.text(mx + 44, 74, 'donc dB part vers le fond', 'tm', 'start', 12)
    f.text(mx + 44, 250, 'P et P′ donnent le même dB :', 'tm', 'start', 12)
    f.text(mx + 44, 266, 'on double le demi-fil', 'tm', 'start', 12)
    FIG['biot_fil'] = f.svg('Géométrie du calcul du champ d\'un fil infini par Biot et Savart',
                            'Le fil porte le courant I vers +z. P est un point courant du fil, M le point où l\'on cherche le champ, α l\'angle (MO, MP). Les points P et P′, symétriques par rapport à O, créent en M le même champ élémentaire : on peut intégrer de 0 à π/2 et doubler.', 520)


def fig_EB_fil():
    f = Fig(540, 278)
    for cx, kind in ((140, 'E'), (410, 'B')):
        cy = 140
        if kind == 'E':
            f.text(cx, 16, 'fil chargé (λ > 0) : E radial', 'te', 'middle', 13.5)
            for k in range(12):
                a = 2 * math.pi * k / 12 + 0.1
                f.arrow(cx + 20 * math.cos(a), cy - 20 * math.sin(a), cx + 104 * math.cos(a), cy - 104 * math.sin(a), 'ef', 'efh', 7)
            f.circ(cx, cy, 11, 'qp')
            f.text(cx, cy + 5, '+', 'tc', 'middle', 14)
            f.text(cx, 270, 'les lignes partent du fil et vont à l\'infini', 'tm', 'middle', 12)
        else:
            f.text(cx, 16, 'fil parcouru par I (sortant) : B circulaire', 'tc', 'middle', 13.5)
            for r in (42, 74, 104):
                f.circ(cx, cy, r, 'fl')
                for ang in (35, 125, 215, 305):
                    a = math.radians(ang)
                    px, py = cx + r * math.cos(a), cy - r * math.sin(a)
                    tx_, ty_ = -math.sin(a), math.cos(a)  # tangent anti-horaire (math)
                    f.arrow(px - 0.5 * tx_, py + 0.5 * ty_, px + 12 * tx_, py - 12 * ty_, 'bl', 'blh', 8)
            f.out_sym(cx, cy, 10)
            f.text(cx, 270, 'les lignes se referment autour du fil', 'tm', 'middle', 12)
    FIG['EB_fil'] = f.svg('Lignes de E et de B autour d\'un fil infini',
                          'Même géométrie, deux champs bien différents : E rayonne depuis les charges (lignes ouvertes), B tourne autour des courants (lignes fermées, dans le sens du tire-bouchon).', 540)


def fig_sym_B():
    f = Fig(540, 250)
    d, yc, my = 80, 205, 118
    for cx, s2, titre, note in ((135, 1, 'deux courants égaux (sortants)', 'B est PERPENDICULAIRE au plan de symétrie'),
                                (410, -1, 'deux courants opposés', 'B reste DANS le plan d\'antisymétrie')):
        f.line(cx, 28, cx, 232, 'dsh')
        f.text(cx, 16, titre, 'tx', 'middle', 13.5)
        f.text(cx, 247, note, 'tm', 'middle', 12)
        f.out_sym(cx - d, yc, 12)
        if s2 > 0:
            f.out_sym(cx + d, yc, 12)
        else:
            f.in_sym(cx + d, yc, 12)
        # champs : B_i = s_i * (e_z ^ r_i)/|r_i|^2 ; r_i = M - source ; math coords
        def b(src_x, s):
            rx_, ry_ = cx - src_x, my - yc
            ry_ = -(my - yc)  # math : M - src = (cx - src_x, yc - my)
            ry_ = yc - my
            return (s * -ry_, s * rx_)
        b1 = b(cx - d, 1)
        b2 = b(cx + d, s2)
        L1 = 50
        n1 = math.hypot(*b1)
        p1 = (cx + L1 * b1[0] / n1, my - L1 * b1[1] / n1)
        p2 = (cx + L1 * b2[0] / n1, my - L1 * b2[1] / n1)
        tot = (p1[0] + p2[0] - cx, p1[1] + p2[1] - my)
        f.line(p1[0], p1[1], tot[0], tot[1], 'dsh')
        f.line(p2[0], p2[1], tot[0], tot[1], 'dsh')
        f.arrow(cx, my, p1[0], p1[1], 'bl', 'blh', 6)
        f.arrow(cx, my, p2[0], p2[1], 'bl', 'blh', 6)
        f.arrow(cx, my, tot[0], tot[1], 'nb', 'nbh', 8)
        f.dot(cx, my, 3.6, 'ptM')
        f.text(cx + 8, my + 18, 'M', 'tx', 'start', 14)
        f.text(p1[0] + (8 if p1[0] > cx else -8), p1[1] + (-2 if p1[1] < my - 5 else 14), 'B[1]', 'tc', 'start' if p1[0] > cx else 'end', 13, halo=True)
        f.text(p2[0] + (8 if p2[0] > cx else -8), p2[1] + (-2 if p2[1] < my - 5 else 14), 'B[2]', 'tc', 'start' if p2[0] > cx else 'end', 13, halo=True)
        if abs(tot[0] - cx) < 1:
            f.text(cx + 8, tot[1] - 4, 'B', 'tg', 'start', 15, halo=True)
        else:
            f.text(tot[0] + (8 if tot[0] > cx else -8), tot[1] + 18, 'B', 'tg', 'start' if tot[0] > cx else 'end', 15, halo=True)
    FIG['sym_B'] = f.svg('Symétrie et antisymétrie pour le champ magnétique',
                         'Vue de dessus, fils perpendiculaires à la feuille. Chaque B[i] est perpendiculaire au segment qui joint le fil à M (règle du tire-bouchon). À gauche (plan de symétrie des courants) les composantes verticales se compensent : B est horizontal, perpendiculaire au plan. À droite (antisymétrie) les composantes horizontales se compensent : B est dans le plan. C\'est exactement l\'inverse de E.', 540)


def fig_td5_1():
    f = Fig(470, 290)
    ox, oy = 150, 110
    f.arrow(ox, 270, ox, oy + 2, 'ob', 'efh', 8)
    f.line(ox, oy, 24, oy, 'ob')
    f.arrow(ox - 40, oy, ox - 76, oy, 'ob', 'efh', 7)
    f.text(ox - 10, 262, 'I', 'tx', 'end', 15)
    f.text(ox + 10, oy - 10, 'O', 'tx', 'start', 14)
    f.dot(ox, oy, 3)
    mx = 330
    f.text(mx, oy + 30, 'M', 'tx', 'middle', 15)
    f.line(ox, oy, mx, oy, 'dsh')
    f.text((ox + mx) / 2, oy - 8, 'a', 'tx', 'middle', 15)
    # point courant P sur le fil vertical
    py = 200
    f.dot(ox, py, 3.4)
    f.text(ox - 10, py + 4, 'P', 'tx', 'end', 14)
    f.line(ox, py, mx, oy, 'ob')
    f.text(250, py - 40, 'PM', 'tx', 'start', 14, halo=True)
    f.arrow(ox + 8, py + 12, ox + 8, py - 14, 'bl', 'blh', 6)
    f.text(ox + 16, py + 8, 'dℓ', 'tc', 'start', 13)
    f.in_sym(mx, oy, 10)
    f.text(mx + 18, oy - 6, 'B entrant', 'tc', 'start', 14)
    # tronçon horizontal
    f.text(ox - 14, oy + 22, 'tronçon horizontal :', 'tm', 'end', 12)
    f.text(ox - 14, oy + 38, 'dℓ ∥ PM donc B = 0', 'te', 'end', 12.5)
    FIG['td5_1'] = f.svg('Fil courbé à angle droit : point M dans le prolongement du tronçon horizontal',
                         'Fil infini courbé à angle droit en O (courant vers le haut, puis vers la gauche). M est sur le prolongement du tronçon horizontal à la distance a de O. Le tronçon horizontal ne crée aucun champ en M ; le tronçon vertical (semi-infini) crée B entrant.', 470)


def build():
    for fn in (fig_cyl, fig_sph, fig_grad, fig_flux_cyl, fig_sym_E, fig_gauss_sph, fig_E_r, fig_fil_EV, fig_equi,
               fig_superpo, fig_cond_ex, fig_lorentz, fig_biot_fil, fig_EB_fil, fig_sym_B, fig_td5_1):
        fn()
    return FIG
