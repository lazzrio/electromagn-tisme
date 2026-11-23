"""Chapitre 4 (champ magnétique, début du chapitre) : schémas SVG et insertion idempotente dans
cours.html, formules.html, quiz.html, index.html, README.md.
Usage : python tools/gen_ch4.py   (relançable : les blocs sont repérés par des marqueurs de commentaire)."""
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
    try:
        open(os.path.join(ROOT, p), 'w', encoding='utf-8', newline='').write(s)
    except OSError:
        tmp = os.path.join(ROOT, p + '.tmp')
        open(tmp, 'w', encoding='utf-8', newline='').write(s)
        os.replace(tmp, os.path.join(ROOT, p))


def sb(s):
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

    def path(self, d, c='ob'):
        self.add('<path class="%s" d="%s"/>' % (c, d))

    def rect(self, x, y, w, h, c='ob'):
        self.add('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (c, x, y, w, h))

    def text(self, x, y, s, c='tx', anchor='middle', size=None):
        st = (' style="font-size:%spx"' % size) if size else ''
        self.add('<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' % (c, x, y, anchor, st, sb(s)))

    RING = {'te': 'ec', 'bl': 'ac', 'ax': 'ob', 'tc': 'ac'}

    def dot_out(self, x, y, r=7, c='ob'):
        """courant / champ sortant (point dans un cercle)"""
        self.circ(x, y, r, self.RING.get(c, c), 'fill:var(--surface)')
        self.circ(x, y, 1.8, 'pt')

    def cross_in(self, x, y, r=7, c='ob'):
        """courant / champ entrant (croix dans un cercle)"""
        c = self.RING.get(c, c)
        self.circ(x, y, r, c, 'fill:var(--surface)')
        d = r * 0.62
        self.line(x - d, y - d, x + d, y + d, c)
        self.line(x - d, y + d, x + d, y - d, c)

    def svg(self, aria, caption, maxw=None):
        mw = maxw or self.w
        return ('<figure class="fgbox"><svg class="fg" viewBox="0 0 %d %d" role="img" aria-label="%s" style="max-width:%dpx">%s</svg>'
                '<figcaption>%s</figcaption></figure>' % (self.w, self.h, aria, mw, ''.join(self.p), caption))


def cap(s):
    return re.sub(r'\[([^\]]*)\]', r'<sub>\1</sub>', s)


FIG = {}

# ---- 1. force de Lorentz et trajectoire circulaire (B uniforme sortant de la page)
f = Fig(420, 270)
cx, cy, R = 150, 135, 78
f.circ(cx, cy, R, 'dsh')
for x in range(30, 290, 40):
    for y in range(24, 260, 46):
        if math.hypot(x - cx, y - cy) > R + 18 or True:
            f.dot_out(x + 6, y, 4.5, 'ax')
px, py = cx + R, cy
f.circ(px, py, 6, 'qp')
f.arrow(px, py, px, py - 52, 'bl', 'blh', 8)
f.text(px + 12, py - 40, 'v', 'tc', 'start', 14)
f.arrow(px, py, px - 52, py, 'ef', 'efh', 8)
f.text(px - 40, py - 10, 'f[m]', 'te', 'middle', 14)
f.line(cx, cy, cx + 55, cy - 55, 'dsh')
f.text(cx + 14, cy - 32, 'r', 'tx', 'start', 14)
f.circ(cx, cy, 2.6, 'pt')
f.text(316, 60, 'B uniforme, sortant (⊙)', 'tx', 'start', 13)
f.text(316, 92, 'q &gt; 0 : f[m] = q v ∧ B', 'tc', 'start', 13)
f.text(316, 122, 'f[m] ⟂ v : ne travaille pas', 'tx', 'start', 13)
f.text(316, 140, '|v| constante', 'tx', 'start', 13)
f.text(316, 176, 'f[m] est la force centripète :', 'tm', 'start', 12)
f.text(316, 194, 'm v²/r = |q| v B', 'tx', 'start', 13)
f.text(316, 218, 'r = m v / (|q| B)', 'te', 'start', 14)
FIG['lorentz'] = f.svg('Force de Lorentz et trajectoire circulaire d\'une particule chargée dans un champ magnétique uniforme',
                       cap('Dans un champ B uniforme perpendiculaire à la vitesse, la force magnétique est toujours orthogonale à v : elle courbe la trajectoire sans changer la vitesse, d\'où un cercle de rayon r = mv/(|q|B).'), 420)

# ---- 2. Biot et Savart : géométrie du fil infini
f = Fig(420, 290)
wx = 120
f.arrow(wx, 270, wx, 20, 'bl', 'blh', 9)
f.text(wx - 10, 30, 'z', 'tm', 'end', 14)
f.text(wx - 12, 150, 'I', 'tc', 'end', 15)
f.line(wx - 4, 205, wx + 4, 205, 'ob')
f.circ(wx, 205, 4, 'qp')
f.text(wx - 12, 209, 'O', 'tx', 'end', 13)
Mx, My = 290, 205
f.circ(Mx, My, 5, 'ptM')
f.text(Mx + 10, My + 20, 'M', 'tx', 'start', 14)
Py = 110
f.circ(wx, Py, 5, 'qp')
f.text(wx - 12, Py + 4, 'P', 'tx', 'end', 14)
f.arrow(wx, Py + 2, wx, Py - 28, 'bl', 'blh', 8)
f.text(wx + 10, Py - 14, 'dℓ = dz e[z]', 'tc', 'start', 12)
f.line(wx, Py, Mx, My, 'dsh')
f.text(205, 135, 'PM', 'tx', 'middle', 14)
f.line(wx, My, Mx, My, 'ob')
f.text(205, My + 20, 'r', 'tx', 'middle', 14)
f.path('M %.1f %.1f A 38 38 0 0 0 %.1f %.1f' % (Mx - 38 * math.cos(math.atan2(My - Py, Mx - wx)), My - 38 * math.sin(math.atan2(My - Py, Mx - wx)) * 1, Mx - 38, My), 'ac') if False else None
f.cross_in(Mx, My - 34, 8, 'te')
f.text(Mx + 14, My - 30, 'dB ∥ e[θ]', 'te', 'start', 13)
f.text(310, 48, 'dB = μ[0] I dℓ ∧ PM / (4π PM³)', 'tx', 'start', 12)
f.text(310, 66, 'dℓ ∧ PM : sortant de la page… ou', 'tm', 'start', 11) if False else None
f.text(310, 66, 'tire-bouchon : (dℓ, PM, dB) direct', 'tm', 'start', 12)
f.text(310, 92, 'M dans le plan de la page :', 'tm', 'start', 12)
f.text(310, 108, 'dB entrant (⊗)', 'te', 'start', 12)
f.text(130, 284, '', 'tx')
FIG['biot'] = f.svg('Géométrie de la loi de Biot et Savart pour un fil infini', cap('Un élément dℓ = dz e[z] du fil en P crée en M un champ élémentaire dB perpendiculaire au plan (dℓ, PM) : ici entrant dans la page (tire-bouchon : dℓ vers PM, on visse vers l\'intérieur de la page). On somme sur tout le fil.'), 420)

# ---- 3. lignes de champ autour d'un fil + B(r)
f = Fig(440, 250)
cx, cy = 105, 118
f.dot_out(cx, cy, 8, 'bl')
for R, op in ((30, 1), (52, 1), (74, 1), (96, 1)):
    f.circ(cx, cy, R, 'ec')
    for a in (math.pi / 4, 3 * math.pi / 4 + math.pi, 0.0):
        pass
    # flèche en sens trigonométrique : au sommet du cercle, B va vers la gauche (e_theta)
    x, y = cx, cy - R
    f.add('<polygon class="efh" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>' % (x - 7, y, x + 1, y - 4.5, x + 1, y + 4.5))
f.text(cx, 240, 'I sortant (⊙) : B tourne dans le sens trigonométrique (e[θ])', 'tm', 'middle', 11)
f.text(cx + 100, 16, 'règle du tire-bouchon', 'tm', 'middle', 12) if False else None
# courbe B(r) = k / r
gx, gy = 265, 205
f.arrow(gx, gy, 430, gy, 'ax', 'axh', 7)
f.arrow(gx, gy, gx, 30, 'ax', 'axh', 7)
f.text(430, gy + 16, 'r', 'tm', 'end', 13)
f.text(gx + 8, 34, 'B(r)', 'tm', 'start', 13)
pts = ['%.1f %.1f' % (gx + 20 + (r - 12) * 1.75, gy - 560 / r) for r in range(12, 96, 3)]
f.path('M' + ' L'.join(pts), 'ef')
f.text(370, 80, 'B = μ[0] I / (2π r)', 'te', 'middle', 14)
f.text(370, 98, 'décroît en 1/r', 'tm', 'middle', 12)
FIG['lignes_fil'] = f.svg('Lignes de champ magnétique autour d\'un fil infini et décroissance du champ', cap('Les lignes de champ d\'un fil infini sont des cercles centrés sur le fil, orientés par la règle du tire-bouchon (ici le courant sort de la page : sens trigonométrique). Le module du champ décroît en 1/r.'), 440)

# ---- 4. symétries du champ du fil infini (vue dans le plan contenant le fil)
f = Fig(430, 270)
wx = 120
f.arrow(wx, 200, wx, 18, 'bl', 'blh', 9)
f.text(wx - 12, 40, 'I', 'tc', 'end', 15)
f.line(30, 135, 410, 135, 'dsh')
f.text(404, 124, 'plan d\'antisymétrie Π*', 'tm', 'end', 12)
f.text(wx - 28, 252, 'plan de la page = plan de symétrie Π', 'tm', 'start', 12) if False else None
Mx = 290
f.circ(Mx, 135, 5, 'ptM')
f.text(Mx + 9, 154, 'M', 'tx', 'start', 14)
f.cross_in(Mx, 90, 9, 'te')
f.text(Mx + 16, 94, 'B(M)', 'te', 'start', 13)
f.dot_out(wx - 70, 90, 9, 'te')
f.text(wx - 84, 94, 'B(M″)', 'te', 'end', 13)
f.circ(wx - 70, 135, 5, 'ptM')
f.text(wx - 62, 154, 'M″', 'tx', 'start', 13)
f.text(215, 214, 'Π = plan de la page (contient le fil et M) : plan de symétrie, B(M) ⟂ Π', 'tx', 'middle', 12)
f.text(215, 232, "Π* (⟂ au fil, passant par M) : plan d'antisymétrie, B(M) ∈ Π*", 'tx', 'middle', 12)
f.text(215, 250, "de l'autre côté du fil, B change de sens (⊙ au lieu de ⊗)", 'tx', 'middle', 12)
f.text(290, 55, '⊗ = entrant', 'tm', 'start', 12)
f.text(290, 70, '⊙ = sortant', 'tm', 'start', 12)
FIG['sym'] = f.svg('Symétries du champ magnétique d\'un fil infini', cap('Le plan de la page contient le fil : c\'est un plan de symétrie des courants, donc B lui est perpendiculaire (⊗ à droite, ⊙ à gauche : B change de sens de part et d\'autre du fil). Le plan horizontal Π* ⟂ au fil est un plan d\'antisymétrie : B y est contenu.'), 430)


# =============================================================== contenu HTML
COURS = r"""<!-- CH4:DEBUT -->
<article class="chapter" id="ch4">
<div class="chapter-hd">
<span class="cn">CH 4</span>
<h2>Le champ magnétique (début du chapitre)</h2>
<label class="chap-check"><input data-chk="4" type="checkbox"/> validé</label>
</div>
<div class="prose">
<div class="soon"><b>Source</b> : poly « Chap. 4 : Champ magnétique – partie I » 2026/2027. Cette partie va de l'introduction au calcul du champ d'un <b>fil infini</b> par la loi de Biot et Savart. Le théorème d'Ampère, la force de Laplace et l'effet Hall (sommaire du poly) ne sont pas encore dans le document disponible : le théorème d'Ampère est résumé en fin de chapitre pour le <b>TD5</b> ; la force de Laplace et l'effet Hall seront complétés avec le poly.</div>
<p>Le champ magnétique \(\vec B\) est la deuxième « composante » du champ électromagnétique. Dans ce chapitre on étudie les champs <span class="term">magnétostatiques</span>, créés par des <b>courants</b> qui ne dépendent pas du temps. Le chapitre se construit <b>en parallèle de l'électrostatique</b> (distributions, invariances, symétries) : attention, les règles de symétrie sont <b>inversées</b> par rapport à \(\vec E\).</p>
<h3 id="ch4-intro">Aimants, boussole et champ terrestre</h3>
<div class="box def"><div class="bt">◆ Aimants et pôles</div>
<p>Un aimant a toujours <b>deux pôles</b> (nord et sud) : deux pôles de même nature se <b>repoussent</b>, deux pôles de nature différente <b>s'attirent</b>. La « pierre d'aimant » est la magnétite (\(\mathrm{Fe_3O_4}\)).</p></div>
<div class="box thm"><div class="bt">★ Le champ magnétique se détecte avec une boussole</div>
<p>En un point de la Terre, sans aimant ni circuit, l'aiguille d'une boussole s'oriente selon la direction Sud-Nord : il règne un <b>champ magnétique terrestre</b>. Un aimant modifie le champ : la boussole change d'orientation, et la direction de l'aiguille varie d'un point à l'autre. L'espace est caractérisé par un vecteur \(\vec B(M)\) dont la <b>direction</b> est celle de la boussole et le <b>sens</b> va de son pôle sud vers son pôle nord. Plus \(B\) est grand, plus l'aiguille oscille vite autour de sa position d'équilibre.</p></div>
<p>La <b>limaille de fer</b> saupoudrée autour d'un aimant s'aimante et se comporte comme de petites boussoles : elle matérialise les <b>lignes de champ</b> (le « spectre magnétique »).</p>
<h3 id="ch4-lorentz">Force de Lorentz</h3>
<div class="box thm"><div class="bt">★ Force de Lorentz</div>
<div class="mq">\[\vec f=q\big(\vec E+\vec v\wedge\vec B\big)=\underbrace{q\vec E}_{\text{électrique}}+\underbrace{q\,\vec v\wedge\vec B}_{\vec f_m\ \text{magnétique}}\]</div>
<p>\(q\) : charge (C) ; \(\vec v\) : vitesse de la particule (\(\mathrm{m\,s^{-1}}\)) ; \(\vec E\) : champ électrique (\(\mathrm{V\,m^{-1}}\)). La partie électrique est la force de Coulomb ; la partie magnétique est <b>nulle pour une charge immobile</b> et <b>orthogonale à \(\vec v\)</b> (produit vectoriel).</p></div>
<div class="box def"><div class="bt">◆ Unité du champ magnétique</div>
<div class="mq">\[[B]=\frac{[f_m]}{[q][v]}=\frac{\mathrm{M\,L\,T^{-2}}}{\mathrm{I\,T}\cdot\mathrm{L\,T^{-1}}}=\mathrm{M\,I^{-1}\,T^{-2}}\ \Longrightarrow\ \mathrm{kg\,A^{-1}\,s^{-2}}=\text{tesla (T)}\]</div>
<p>Ordres de grandeur : champ terrestre \(4{,}7\times10^{-5}\ \mathrm{T}\) ; aimant permanent \(0{,}1\ \mathrm{T}\) ; électroaimant \(10\ \mathrm{T}\). L'unité montre que le <b>courant électrique</b> intervient dans la création du champ.</p></div>
FIG_LORENTZ
<div class="box thm"><div class="bt">★ Mouvement d'une particule chargée</div>
<ul>
<li>Le champ <b>électrique</b> accélère les particules (deuxième loi de Newton) et peut dévier leur trajectoire (parabole) : canon à électrons, déviation du spot d'un oscilloscope analogique, accélérateurs.</li>
<li>Le champ <b>magnétique</b> fait circuler la particule sur une trajectoire <b>circulaire</b> (la plus générale est une <b>hélice</b>). La vitesse n'est pas modifiée car la force magnétique <b>ne travaille pas</b> (\(\vec f_m\perp\vec v\), théorème de l'énergie cinétique).</li>
<li>Pour \(\vec v\perp\vec B\) uniforme : \(m\dfrac{v^2}{r}=|q|vB\), soit <b>\(r=\dfrac{m\,v}{|q|\,B}\)</b> (résultat classique de mécanique, non démontré dans le poly). Exemple : électron à \(10^6\ \mathrm{m\,s^{-1}}\) dans \(1\ \mathrm{mT}\) : \(r\approx5{,}7\ \mathrm{mm}\).</li>
</ul></div>
<p><b>Applications</b> : le <span class="term">cyclotron</span> (deux demi-cylindres creux « dees » placés dans un champ \(\vec B\) uniforme perpendiculaire à leur base, avec une tension sinusoïdale entre eux : la particule tourne dans les dees et est accélérée à chaque passage dans l'intervalle) ; le <span class="term">spectromètre de masse</span> à analyseur magnétique (les ions sont triés selon leur rapport masse/charge, usages en chimie, biochimie, géologie…).</p>
<h3 id="ch4-biot">Courant filiforme et loi de Biot et Savart</h3>
<div class="box def"><div class="bt">◆ Courant filiforme</div>
<p>On étudie des courants circulant dans des fils dont l'épaisseur est négligeable. (Il existe aussi des courants surfaciques, et des courants volumiques de densité \(\vec j=\rho_d\,\vec v\).)</p></div>
<div class="box thm"><div class="bt">★ Loi de Biot et Savart</div>
<div class="mq">\[\vec B(M)=\int_{P\in\mathcal L}\mathrm{d}\vec B\qquad\mathrm{d}\vec B=\frac{\mu_0}{4\pi}\,\frac{I\,\mathrm{d}\vec l\wedge\overrightarrow{PM}}{PM^3}\]</div>
<p>\(I\) : intensité du courant (A) ; \(\mathrm{d}\vec l\) : élément de fil en \(P\), orienté dans le sens du courant ; \(\overrightarrow{PM}\) : de \(P\) vers le point \(M\) où l'on cherche le champ ; \(\mu_0\) : perméabilité magnétique du vide, <b>\(\mu_0=4\pi\times10^{-7}\ \mathrm{SI}\)</b>, liée à \(\varepsilon_0\) par <b>\(c^2=\dfrac{1}{\varepsilon_0\mu_0}\)</b>.</p></div>
<div class="box method"><div class="bt">▹ Règle du tire-bouchon : le sens de \(\vec B\)</div>
<p>Le trièdre \((\mathrm{d}\vec l,\ \overrightarrow{PM},\ \mathrm{d}\vec B)\) est <b>direct</b> : on fait tourner le premier vecteur vers le deuxième ; le sens de vissage d'un tire-bouchon donne le sens du champ. De même, un courant dirigé vers vous crée des lignes de champ qui tournent dans le sens trigonométrique.</p></div>
<div class="box warn"><div class="bt">⚠ Une loi « artificielle »</div><p>Isoler une portion de circuit parcourue par un courant est <b>impossible</b> (on peut isoler des charges, pas un morceau de circuit) : la loi de Biot et Savart n'est qu'un <b>artifice de calcul</b> pour le champ d'une portion. Le champ d'un courant filiforme est <b>continu et défini partout sauf sur les fils</b>.</p></div>
<h3 id="ch4-lignes">Lignes de champ et pseudo-vecteur</h3>
<div class="box def"><div class="bt">◆ Lignes de champ (spectre magnétique)</div>
<p>Comme pour \(\vec E\) : lignes orientées suivant le champ, sur lesquelles il est tangent. Mais les lignes de champ magnétique sont <b>fermées</b> (elles se rebouclent), alors que celles de \(\vec E\) partent des charges positives.</p></div>
<div class="box thm"><div class="bt">★ \(\vec B\) est un pseudo-vecteur</div>
<p>Contrairement à \(\vec E\) (vrai vecteur), \(\vec B\) est un <b>pseudo-vecteur</b> : son sens dépend de l'<b>orientation de l'espace</b>. Cela vient du produit vectoriel de Biot et Savart (produit de deux vrais vecteurs). L'espace est orienté dans le sens direct quand \((\vec u_x,\vec u_y,\vec u_z)\) suit pouce, index, majeur de la main droite. Conséquence : un plan de symétrie transforme une base directe en base indirecte, et \(\vec B\) <b>change de sens</b> de part et d'autre de ce plan.</p></div>
<h3 id="ch4-sym">Invariances, symétries et antisymétries</h3>
<div class="box method"><div class="bt">▹ Invariances</div>
<p>Même démarche que pour \(\vec E\) : on déplace \(M\) par translation le long de la distribution ou par rotation autour d'elle ; si \(M\) voit la même distribution, \(\vec B\) ne dépend pas de la coordonnée correspondante.</p></div>
<div class="box thm"><div class="bt">★ Plan de symétrie, plan d'antisymétrie des courants</div>
<div class="tbl-wrap s4-stack"><table>
<tr><th>Si la distribution de courants admet…</th><th>Alors, pour \(M\) dans ce plan</th><th>Et pour \(M'\) symétrique de \(M\)</th></tr>
<tr><td data-l="Plan">un <b>plan de symétrie</b></td><td data-l="En M">\(\vec B(M)\) est <b>orthogonal</b> au plan</td><td data-l="En M'">\(\vec B(M')\) est l'<b>opposé du symétrique</b> de \(\vec B(M)\)</td></tr>
<tr><td data-l="Plan">un <b>plan d'antisymétrie</b></td><td data-l="En M">\(\vec B(M)\) est <b>contenu</b> dans le plan</td><td data-l="En M'">\(\vec B(M')\) est le <b>symétrique</b> de \(\vec B(M)\)</td></tr>
</table></div>
<p>Un seul plan suffit pour trouver la <b>direction</b> de \(\vec B\).</p></div>
<div class="box warn"><div class="bt">⚠ Règles inversées par rapport à \(\vec E\)</div><p>\(\vec E\) possède les <b>mêmes</b> symétries que ses sources ; \(\vec B\) est <b>antisymétrique</b> par rapport à un plan si ce plan est un plan de symétrie des courants (et inversement). Pour \(\vec E\) : plan de symétrie ⇒ \(\vec E\) <em>dans</em> le plan ; pour \(\vec B\) : plan de symétrie ⇒ \(\vec B\) <em>perpendiculaire</em> au plan.</p></div>
<h3 id="ch4-fil">Champ d'un fil infini par la méthode intégrale</h3>
<p>Fil infini d'axe \(Oz\), parcouru par le courant \(I\) (dans le sens de \(\vec e_z\)). On cherche \(\vec B\) en \(M\) à la distance \(r\) du fil, en coordonnées cylindriques.</p>
FIG_BIOT
<div class="box method"><div class="bt">▹ Étape 1 : symétries et invariances</div>
<p>Le plan perpendiculaire au fil passant par \(M\) est un plan d'<b>antisymétrie</b> : \(\vec B\) est <b>contenu</b> dans ce plan. La règle du tire-bouchon donne le sens de \(\vec e_\theta\) (la base \((\vec e_r,\vec e_\theta,\vec e_z)\) est directe). Invariance par rotation autour du fil et par translation selon \(Oz\) : \(\vec B\) ne dépend que de \(r\) :</p>
<div class="mq">\[\vec B(M)=B_\theta(r)\,\vec e_\theta\]</div></div>
<div class="box method"><div class="bt">▹ Étape 2 : champ élémentaire</div>
<p>Avec \(\mathrm{d}\vec l=\mathrm{d}z\,\vec e_z\) et \(\overrightarrow{PM}=\overrightarrow{PO}+\overrightarrow{OM}=-z\,\vec e_z+r\,\vec e_r\) :</p>
<div class="mq">\[\vec e_z\wedge\overrightarrow{PM}=r\,\vec e_\theta\qquad\mathrm{d}\vec B=\frac{\mu_0I}{4\pi}\frac{r\,\mathrm{d}z}{PM^3}\,\vec e_\theta\]</div>
<p>On choisit l'angle \(\alpha\) (entre \(PM\) et le plan perpendiculaire au fil) comme paramètre : \(z=r\tan\alpha\), \(\mathrm{d}z=\dfrac{r\,\mathrm{d}\alpha}{\cos^2\alpha}\), \(PM=\dfrac{r}{\cos\alpha}\), d'où</p>
<div class="mq">\[\mathrm{d}\vec B=\frac{\mu_0I}{4\pi r}\cos\alpha\,\mathrm{d}\alpha\ \vec e_\theta\]</div></div>
<div class="box method"><div class="bt">▹ Étape 3 : intégration</div>
<p>Fil infini : \(\alpha\) varie de \(-\frac\pi2\) à \(\frac\pi2\) (ou de \(0\) à \(\frac\pi2\) en doublant, par symétrie de part et d'autre de \(O\)) :</p>
<div class="mq">\[B_\theta(r)=\int_{-\pi/2}^{\pi/2}\frac{\mu_0I}{4\pi r}\cos\alpha\,\mathrm{d}\alpha=\frac{\mu_0I}{4\pi r}\big[\sin\alpha\big]_{-\pi/2}^{\pi/2}=\frac{\mu_0I}{2\pi r}\]</div></div>
<div class="box thm"><div class="bt">★ Champ magnétique d'un fil infini</div>
<div class="mq">\[\vec B(M)=\frac{\mu_0\,I}{2\pi\,r}\,\vec e_\theta\]</div>
<p>Le module décroît en \(\frac1r\) ; les lignes de champ sont des cercles d'axe le fil, orientés par le tire-bouchon. Application numérique : \(I=10\ \mathrm{A}\), \(r=5\ \mathrm{cm}\) : \(B=\dfrac{4\pi\times10^{-7}\times10}{2\pi\times0{,}05}=4\times10^{-5}\ \mathrm{T}\), du même ordre que le champ terrestre.</p></div>
FIG_LIGNES
FIG_SYM
<h3 id="ch4-ampere">Théorème d'Ampère (outil du TD5)</h3>
<div class="soon"><b>Hors poly partie I</b> : le théorème d'Ampère est annoncé au sommaire du chapitre 4 mais n'est pas dans le document disponible. Cette section donne le résultat standard dont le TD5 a besoin ; compare-la avec ton cours d'amphi.</div>
<div class="box thm"><div class="bt">★ Théorème d'Ampère</div>
<div class="mq">\[\oint_{\mathcal C}\vec B\cdot\mathrm{d}\vec l=\mu_0\,I_{enlac\acute e}\]</div>
<p>La circulation de \(\vec B\) le long d'un <b>contour fermé orienté</b> \(\mathcal C\) (contour d'Ampère) vaut \(\mu_0\) fois le courant qui le traverse. Le sens du contour fixe, par la règle de la main droite (tire-bouchon), le signe des courants : un courant dans le sens du pouce, quand les doigts suivent \(\mathcal C\), compte \(+\).</p></div>
<div class="box method"><div class="bt">▹ Quand et comment l'utiliser (comme Gauss pour \(\vec E\))</div>
<ol>
<li><b>Symétries et invariances</b> : trouver la direction de \(\vec B\) et ses dépendances (plan de symétrie ⇒ \(\vec B\perp\) plan ; plan d'antisymétrie ⇒ \(\vec B\in\) plan).</li>
<li><b>Contour d'Ampère</b> : un contour sur lequel \(\vec B\) est <b>tangent et de module constant</b> (cercle d'axe le fil, rectangle le long d'un solénoïde…) ou <b>orthogonal</b> à \(\mathrm{d}\vec l\) (contribution nulle).</li>
<li>Calculer la circulation, puis le <b>courant enlacé</b> \(I_{enlac\acute e}\) (intégrer \(\vec j\) sur la surface qui s'appuie sur le contour si le courant est réparti).</li>
</ol></div>
<div class="box thm"><div class="bt">★ Résultats classiques (démontrés dans les corrigés du TD5)</div>
<div class="tbl-wrap s4-stack"><table>
<tr><th>Distribution</th><th>Champ</th></tr>
<tr><td data-l="Distribution">Fil infini</td><td data-l="Champ">\(\dfrac{\mu_0I}{2\pi r}\vec e_\theta\)</td></tr>
<tr><td data-l="Distribution">Cylindre plein (rayon \(R\), \(\vec j\) uniforme)</td><td data-l="Champ">\(\dfrac{\mu_0Ir}{2\pi R^2}\vec e_\theta\) (\(r\lt R\)) ; \(\dfrac{\mu_0I}{2\pi r}\vec e_\theta\) (\(r\gt R\))</td></tr>
<tr><td data-l="Distribution">Solénoïde infini (\(n\) spires par mètre)</td><td data-l="Champ">\(\mu_0nI\,\vec e_z\) à l'intérieur ; \(\vec0\) à l'extérieur</td></tr>
<tr><td data-l="Distribution">Tore (\(N\) spires, rayon moyen \(R_0\))</td><td data-l="Champ">\(\dfrac{\mu_0NI}{2\pi r}\vec e_\theta\) dans le tore ; \(\vec0\) ailleurs</td></tr>
<tr><td data-l="Distribution">Spire circulaire (rayon \(R\)), sur l'axe</td><td data-l="Champ">\(\dfrac{\mu_0I}{2R}\sin^3\alpha\,\vec e_z=\dfrac{\mu_0IR^2}{2(R^2+z^2)^{3/2}}\vec e_z\) (Biot et Savart, pas Ampère)</td></tr>
</table></div></div>
<div class="box ex corr-link"><div class="bt">✅ S'entraîner</div><p>Les 9 exercices du TD5 (courant angulaire, quatre fils, spire, lignes de champ, solénoïde, cylindre, coaxial, tore, effet Hall) sont corrigés : <a href="corriges.html#td5">voir les corrigés du TD5</a>. Formules : <a href="formules.html#f-mag">champ magnétique</a>. Quiz : questions sur le Ch4 à la fin de <a href="quiz.html">la banque</a>.</p></div>
</div>
</article>
<!-- CH4:FIN -->
"""

COURS_TOC = """<!-- CH4TOC:DEBUT -->
<a href="#ch4">4 · Champ magnétique</a>
<a href="#ch4-intro">↳ Aimants et boussole</a>
<a href="#ch4-lorentz">↳ Force de Lorentz</a>
<a href="#ch4-biot">↳ Biot et Savart</a>
<a href="#ch4-lignes">↳ Lignes de champ, pseudo-vecteur</a>
<a href="#ch4-sym">↳ Symétries de B</a>
<a href="#ch4-fil">↳ Fil infini</a>
<a href="#ch4-ampere">↳ Théorème d'Ampère</a>
<!-- CH4TOC:FIN -->
"""

FORM = r"""<!-- F4:DEBUT -->
<section class="fgroup" id="f-mag">
<h2>Champ magnétique</h2>
<div class="frow"><div class="fx">\(\vec f=q\big(\vec E+\vec v\wedge\vec B\big)\)</div><div class="fd"><span class="nm">Force de Lorentz</span>. Partie électrique \(q\vec E\), partie magnétique \(\vec f_m=q\vec v\wedge\vec B\) (nulle si \(\vec v=\vec0\), orthogonale à \(\vec v\), ne travaille pas). <span class="unit">\(\mathrm{N}\)</span></div></div>
<div class="frow"><div class="fx">\([B]=\mathrm{kg\,A^{-1}\,s^{-2}}=\mathrm{T}\)</div><div class="fd"><span class="nm">Unité de \(\vec B\)</span>. Terre \(4{,}7\times10^{-5}\ \mathrm{T}\) ; aimant \(0{,}1\ \mathrm{T}\) ; électroaimant \(10\ \mathrm{T}\). <span class="unit">\(\mathrm{T}\)</span></div></div>
<div class="frow"><div class="fx">\(r=\dfrac{m\,v}{|q|\,B}\)</div><div class="fd"><span class="nm">Rayon de la trajectoire circulaire</span>. \(\vec v\perp\vec B\) uniforme ; \(|\vec v|\) constante. <span class="unit">\(\mathrm{m}\)</span> <span class="cond">\(\vec B\) uniforme, pas de champ \(\vec E\)</span></div></div>
<div class="frow"><div class="fx">\(\mathrm{d}\vec B=\dfrac{\mu_0}{4\pi}\dfrac{I\,\mathrm{d}\vec l\wedge\overrightarrow{PM}}{PM^3}\)</div><div class="fd"><span class="nm">Loi de Biot et Savart</span>. \(\vec B=\int\mathrm{d}\vec B\) sur la ligne \(\mathcal L\) ; sens par le tire-bouchon (\(\mathrm{d}\vec l,\overrightarrow{PM},\mathrm{d}\vec B\) direct). <span class="unit">\(\mathrm{T}\)</span> <span class="cond">courant filiforme</span></div></div>
<div class="frow"><div class="fx">\(\mu_0=4\pi\times10^{-7}\ \mathrm{SI}\ \ ;\ \ c^2=\dfrac{1}{\varepsilon_0\mu_0}\)</div><div class="fd"><span class="nm">Perméabilité du vide</span>. Lie électricité et magnétisme à la vitesse de la lumière \(c\). <span class="unit">\(\mathrm{T\,m\,A^{-1}}\)</span></div></div>
<div class="frow"><div class="fx">\(\vec B(M)=\dfrac{\mu_0\,I}{2\pi\,r}\,\vec e_\theta\)</div><div class="fd"><span class="nm">Fil infini</span>. Coordonnées cylindriques d'axe le fil, \(I\) dans le sens de \(\vec e_z\) ; module en \(\frac1r\). <span class="unit">\(\mathrm{T}\)</span> <span class="cond">fil infini, filiforme</span></div></div>
<div class="frow"><div class="fx">plan de symétrie : \(\vec B\perp\) plan ; plan d'antisymétrie : \(\vec B\in\) plan</div><div class="fd"><span class="nm">Symétries du champ magnétique</span>. <b>Inversé</b> par rapport à \(\vec E\). \(\vec B\) est un pseudo-vecteur : en \(M'\) symétrique par un plan de symétrie, \(\vec B(M')=-\mathrm{sym}\,\vec B(M)\) ; par un plan d'antisymétrie, \(\vec B(M')=\mathrm{sym}\,\vec B(M)\).</div></div>
<div class="frow"><div class="fx">\(\displaystyle\oint_{\mathcal C}\vec B\cdot\mathrm{d}\vec l=\mu_0\,I_{\text{enlacé}}\)</div><div class="fd"><span class="nm">Théorème d'Ampère</span>. Contour d'Ampère orienté ; signe des courants par la règle de la main droite. <span class="unit">\(\mathrm{T\,m}\)</span> <span class="cond">symétries fortes ; hors poly partie I</span></div></div>
<div class="frow"><div class="fx">\(B=\mu_0\,n\,I\ \ (\text{intérieur})\ ;\ \ B=0\ \ (\text{extérieur})\)</div><div class="fd"><span class="nm">Solénoïde infini</span>. \(n\) spires par mètre, champ uniforme selon \(\vec e_z\). <span class="unit">\(\mathrm{T}\)</span></div></div>
<div class="frow"><div class="fx">\(B=\dfrac{\mu_0Ir}{2\pi R^2}\ (r\lt R)\ ;\ \dfrac{\mu_0I}{2\pi r}\ (r\gt R)\)</div><div class="fd"><span class="nm">Cylindre plein infini</span>. Courant uniforme de densité \(j=\frac{I}{\pi R^2}\). Champ continu en \(R\). <span class="unit">\(\mathrm{T}\)</span></div></div>
<div class="frow"><div class="fx">\(B=\dfrac{\mu_0NI}{2\pi r}\)</div><div class="fd"><span class="nm">Tore</span>. \(N\) spires, champ nul hors du tore. <span class="unit">\(\mathrm{T}\)</span></div></div>
<div class="frow"><div class="fx">\(B_z=\dfrac{\mu_0I}{2R}\sin^3\alpha=\dfrac{\mu_0IR^2}{2(R^2+z^2)^{3/2}}\)</div><div class="fd"><span class="nm">Spire circulaire sur son axe</span>. Au centre : \(\frac{\mu_0I}{2R}\). <span class="unit">\(\mathrm{T}\)</span></div></div>
</section>
<!-- F4:FIN -->
"""

EXPRESS = r"""<!-- F4EXP:DEBUT -->
<div class="eg"><h4>Magnétisme</h4>
<div class="ei"><span class="nm">Lorentz</span><span class="vl">\(\vec f=q(\vec E+\vec v\wedge\vec B)\)</span></div>
<div class="ei"><span class="nm">Rayon</span><span class="vl">\(r=\frac{mv}{|q|B}\)</span></div>
<div class="ei"><span class="nm">Biot-Savart</span><span class="vl">\(\mathrm{d}\vec B=\frac{\mu_0}{4\pi}\frac{I\mathrm{d}\vec l\wedge\overrightarrow{PM}}{PM^3}\)</span></div>
<div class="ei"><span class="nm">Fil infini</span><span class="vl">\(B=\frac{\mu_0I}{2\pi r}\)</span></div>
<div class="ei"><span class="nm">\(\mu_0\)</span><span class="vl">\(4\pi\times10^{-7}\)</span></div>
</div>
<!-- F4EXP:FIN -->
"""

Q = [
    ("Quelle est l'unité SI du champ magnétique ?", "le tesla (T)", ["le weber (Wb)", "le henry (H)", "le \\(\\mathrm{V\\,m^{-1}}\\)"], "\\([B]=\\frac{[f]}{[q][v]}=\\mathrm{kg\\,A^{-1}\\,s^{-2}}\\), qu'on appelle le tesla."),
    ("Quelle est la force de Lorentz subie par une charge \\(q\\) de vitesse \\(\\vec v\\) ?", "\\(q\\big(\\vec E+\\vec v\\wedge\\vec B\\big)\\)", ["\\(q\\big(\\vec E+\\vec v\\cdot\\vec B\\big)\\)", "\\(q\\vec v\\wedge\\vec E+\\vec B\\)", "\\(q\\vec E\\wedge\\vec B\\)"], "Partie électrique de Coulomb \\(q\\vec E\\) plus partie magnétique \\(q\\vec v\\wedge\\vec B\\) (produit vectoriel)."),
    ("Un champ magnétique seul agit sur une charge immobile avec une force :", "nulle", ["parallèle à \\(\\vec B\\)", "perpendiculaire à \\(\\vec B\\), non nulle", "égale à \\(q\\vec B\\)"], "\\(\\vec f_m=q\\vec v\\wedge\\vec B=\\vec0\\) si \\(\\vec v=\\vec0\\). Une charge immobile ne « sent » pas \\(\\vec B\\)."),
    ("Le travail de la force magnétique sur une particule chargée est :", "nul", ["positif", "négatif", "égal à \\(qvB\\)"], "\\(\\vec f_m\\perp\\vec v\\) : sa puissance \\(\\vec f_m\\cdot\\vec v\\) est nulle, donc l'énergie cinétique et \\(|\\vec v|\\) restent constantes."),
    ("Une particule chargée entre avec \\(\\vec v\\perp\\vec B\\) dans un champ magnétique uniforme. Sa trajectoire est :", "un cercle", ["une droite", "une parabole", "une hélice de pas non nul"], "La force magnétique, toujours \\(\\perp\\vec v\\), joue le rôle de force centripète. (La trajectoire la plus générale, avec une composante de \\(\\vec v\\) selon \\(\\vec B\\), est une hélice.)"),
    ("Rayon de la trajectoire circulaire d'une particule de masse \\(m\\), charge \\(q\\), vitesse \\(v\\) dans un champ \\(B\\) uniforme (\\(\\vec v\\perp\\vec B\\)) :", "\\(\\dfrac{mv}{|q|B}\\)", ["\\(\\dfrac{|q|B}{mv}\\)", "\\(\\dfrac{mv^2}{|q|B}\\)", "\\(\\dfrac{m}{|q|vB}\\)"], "\\(m\\frac{v^2}{r}=|q|vB\\) donne \\(r=\\frac{mv}{|q|B}\\) : plus \\(B\\) est grand, plus le cercle est petit."),
    ("La loi de Biot et Savart s'écrit :", "\\(\\mathrm{d}\\vec B=\\dfrac{\\mu_0}{4\\pi}\\dfrac{I\\,\\mathrm{d}\\vec l\\wedge\\overrightarrow{PM}}{PM^3}\\)", ["\\(\\mathrm{d}\\vec B=\\dfrac{\\mu_0}{4\\pi}\\dfrac{I\\,\\mathrm{d}\\vec l\\cdot\\overrightarrow{PM}}{PM^3}\\)", "\\(\\mathrm{d}\\vec B=\\dfrac{1}{4\\pi\\varepsilon_0}\\dfrac{I\\,\\mathrm{d}\\vec l\\wedge\\overrightarrow{PM}}{PM^2}\\)", "\\(\\mathrm{d}\\vec B=\\dfrac{\\mu_0}{2\\pi}\\dfrac{I\\,\\mathrm{d}\\vec l}{PM}\\)"], "Produit <em>vectoriel</em> de \\(\\mathrm{d}\\vec l\\) et \\(\\overrightarrow{PM}\\), divisé par \\(PM^3\\) (le module décroît en \\(\\frac1{PM^2}\\))."),
    ("La valeur de la perméabilité magnétique du vide dans le SI est :", "\\(\\mu_0=4\\pi\\times10^{-7}\\)", ["\\(\\mu_0=4\\pi\\times10^{7}\\)", "\\(\\mu_0=\\dfrac{1}{4\\pi\\varepsilon_0}\\)", "\\(\\mu_0=8{,}85\\times10^{-12}\\)"], "\\(\\mu_0=4\\pi\\times10^{-7}\\ \\mathrm{SI}\\). La valeur \\(8{,}85\\times10^{-12}\\) est celle de \\(\\varepsilon_0\\)."),
    ("Quel lien relie \\(\\mu_0\\), \\(\\varepsilon_0\\) et la vitesse de la lumière \\(c\\) ?", "\\(c^2=\\dfrac{1}{\\varepsilon_0\\mu_0}\\)", ["\\(c=\\varepsilon_0\\mu_0\\)", "\\(c^2=\\varepsilon_0\\mu_0\\)", "\\(c=\\dfrac{\\mu_0}{\\varepsilon_0}\\)"], "Cette relation fondamentale unifie l'électricité et le magnétisme avec l'optique."),
    ("Dans la loi de Biot et Savart, le sens de \\(\\mathrm{d}\\vec B\\) se trouve avec la règle du tire-bouchon : le trièdre \\((\\dots)\\) est direct.", "\\((\\mathrm{d}\\vec l,\\ \\overrightarrow{PM},\\ \\mathrm{d}\\vec B)\\)", ["\\((\\overrightarrow{PM},\\ \\mathrm{d}\\vec B,\\ \\mathrm{d}\\vec l)\\) dans l'ordre inverse", "\\((\\vec B,\\ \\vec E,\\ \\vec v)\\)", "\\((\\mathrm{d}\\vec B,\\ \\mathrm{d}\\vec l,\\ \\overrightarrow{PM})\\) indirect"], "On fait tourner \\(\\mathrm{d}\\vec l\\) vers \\(\\overrightarrow{PM}\\) ; le sens de vissage donne \\(\\mathrm{d}\\vec B\\)."),
    ("Le champ magnétique est :", "un pseudo-vecteur", ["un vrai vecteur comme \\(\\vec E\\)", "un scalaire", "toujours colinéaire à \\(\\vec E\\)"], "Il provient d'un produit vectoriel : son sens dépend de l'orientation de l'espace."),
    ("Une distribution de courants admet un plan de symétrie. En un point \\(M\\) de ce plan, le champ \\(\\vec B\\) est :", "orthogonal à ce plan", ["contenu dans ce plan", "nul", "quelconque"], "Pour \\(\\vec B\\), c'est l'inverse de \\(\\vec E\\) : plan de symétrie ⇒ \\(\\vec B\\) perpendiculaire au plan."),
    ("Une distribution de courants admet un plan d'antisymétrie. En un point \\(M\\) de ce plan, le champ \\(\\vec B\\) est :", "contenu dans ce plan", ["orthogonal à ce plan", "nul", "radial"], "Plan d'antisymétrie des courants ⇒ \\(\\vec B\\) contenu dans le plan (pour le fil infini : le plan perpendiculaire au fil passant par \\(M\\))."),
    ("Le champ magnétique d'un fil infini parcouru par un courant \\(I\\) vaut, à la distance \\(r\\) :", "\\(\\dfrac{\\mu_0I}{2\\pi r}\\vec e_\\theta\\)", ["\\(\\dfrac{\\mu_0I}{4\\pi r}\\vec e_r\\)", "\\(\\dfrac{\\mu_0I}{2\\pi r^2}\\vec e_\\theta\\)", "\\(\\dfrac{\\mu_0I}{2r}\\vec e_z\\)"], "Intégrale de Biot et Savart avec \\(\\alpha\\) de \\(-\\frac\\pi2\\) à \\(\\frac\\pi2\\) : \\(B_\\theta=\\frac{\\mu_0I}{4\\pi r}\\times2\\)."),
    ("Comment varie le module du champ d'un fil infini avec la distance \\(r\\) au fil ?", "en \\(\\dfrac{1}{r}\\)", ["en \\(\\dfrac{1}{r^2}\\)", "il est uniforme", "en \\(r\\)"], "\\(B=\\frac{\\mu_0I}{2\\pi r}\\) : même dépendance que le champ électrique d'un fil chargé infini."),
    ("Un fil infini est parcouru par \\(I=10\\ \\mathrm{A}\\). L'ordre de grandeur du champ à \\(r=5\\ \\mathrm{cm}\\) est :", "\\(4\\times10^{-5}\\ \\mathrm{T}\\)", ["\\(4\\times10^{-2}\\ \\mathrm{T}\\)", "\\(4\\ \\mathrm{T}\\)", "\\(4\\times10^{-9}\\ \\mathrm{T}\\)"], "\\(B=\\frac{4\\pi\\times10^{-7}\\times10}{2\\pi\\times0{,}05}=4\\times10^{-5}\\ \\mathrm{T}\\), comparable au champ terrestre."),
    ("Le champ magnétique créé par un courant filiforme est défini et continu :", "partout sauf sur le fil", ["partout, y compris sur le fil", "seulement dans le plan du circuit", "seulement à l'infini"], "Sur le fil lui-même, \\(PM\\to0\\) : le champ y diverge et n'est pas défini."),
    ("Le théorème d'Ampère s'écrit :", "\\(\\oint\\vec B\\cdot\\mathrm{d}\\vec l=\\mu_0I_{\\text{enlacé}}\\)", ["\\(\\oint\\vec B\\cdot\\mathrm{d}\\vec S=\\mu_0I\\)", "\\(\\oint\\vec B\\cdot\\mathrm{d}\\vec l=\\dfrac{I}{\\mu_0}\\)", "\\(\\oint\\vec B\\cdot\\mathrm{d}\\vec l=\\dfrac{Q_{int}}{\\varepsilon_0}\\)"], "Circulation de \\(\\vec B\\) sur un contour fermé = \\(\\mu_0\\) fois le courant enlacé (l'analogue de Gauss pour \\(\\vec E\\) utilise un flux)."),
    ("Champ magnétique à l'intérieur d'un solénoïde infini de \\(n\\) spires par mètre parcouru par \\(I\\) :", "\\(\\mu_0nI\\), uniforme", ["\\(\\dfrac{\\mu_0nI}{2\\pi r}\\)", "nul", "\\(\\dfrac{\\mu_0I}{2\\pi r}\\)"], "Contour rectangulaire d'Ampère : \\(BL=\\mu_0nLI\\). À l'extérieur, le champ est nul."),
    ("Champ à l'intérieur (\\(r\\lt R\\)) d'un fil cylindrique plein de rayon \\(R\\), courant \\(I\\) uniforme :", "\\(\\dfrac{\\mu_0Ir}{2\\pi R^2}\\), croissant avec \\(r\\)", ["\\(\\dfrac{\\mu_0I}{2\\pi r}\\)", "nul", "\\(\\dfrac{\\mu_0I}{2\\pi R}\\), constant"], "Le courant enlacé par un cercle de rayon \\(r\\lt R\\) vaut \\(I\\frac{r^2}{R^2}\\). Le champ est continu en \\(r=R\\)."),
    ("Peut-on utiliser le théorème d'Ampère pour le champ d'une spire circulaire en tout point ?", "non : pas assez de symétries", ["oui, avec un contour circulaire d'axe Oz", "oui, comme pour le solénoïde infini", "oui, mais seulement hors de l'axe"], "\\(\\vec B\\) n'a pas de direction ni de module constants sur un contour simple : on utilise Biot et Savart (sur l'axe : \\(\\frac{\\mu_0IR^2}{2(R^2+z^2)^{3/2}}\\))."),
    ("Les lignes de champ magnétique :", "sont fermées et ne se coupent pas", ["partent des charges positives", "se coupent aux pôles", "sont toujours rectilignes"], "Il n'existe pas de « charge magnétique » : les lignes de \\(\\vec B\\) se rebouclent ; elles ne se coupent pas (sauf aux points où \\(\\vec B=\\vec0\\))."),
]


def remplace_bloc(s, tag, bloc, ancre, avant=True):
    pat = re.compile(r'<!-- %s:DEBUT -->.*?<!-- %s:FIN -->\n?' % (tag, tag), re.S)
    if pat.search(s):
        return pat.sub(lambda m: bloc, s, count=1)
    i = s.index(ancre)
    if not avant:
        i += len(ancre)
    return s[:i] + bloc + s[i:]


# cours.html
s = lire('cours.html')
cours = (COURS.replace('FIG_LORENTZ', FIG['lorentz']).replace('FIG_BIOT', FIG['biot'])
         .replace('FIG_LIGNES', FIG['lignes_fil']).replace('FIG_SYM', FIG['sym']))
s = remplace_bloc(s, 'CH4', cours, '</div>\n</div>\n</div>\n</main>')
s = remplace_bloc(s, 'CH4TOC', COURS_TOC, '</aside>')
s = s.replace('potentiel électrostatique, conducteurs et condensateurs.', 'potentiel électrostatique, conducteurs et condensateurs, champ magnétique.', 1)
ecrire('cours.html', s)

# formules.html
s = lire('formules.html')
s = remplace_bloc(s, 'F4', FORM, '<section class="fgroup" id="f-express">')
if 'href="#f-mag"' not in s:
    s = s.replace('<a href="#f-cond">Conducteurs et condensateurs</a>', '<a href="#f-cond">Conducteurs et condensateurs</a>\n<a href="#f-mag">Champ magnétique</a>', 1)
if 'F4EXP:DEBUT' in s:
    s = remplace_bloc(s, 'F4EXP', EXPRESS, '')
else:
    i = s.index('<!-- F3EXP:FIN -->') + len('<!-- F3EXP:FIN -->\n')
    s = s[:i] + EXPRESS + s[i:]
ecrire('formules.html', s)

# quiz.html
s = lire('quiz.html')
items = []
for q, bon, mauvais, exp in Q:
    items.append('<li data-c="0" data-exp="%s"><p>%s</p><ul>%s</ul></li>'
                 % (html.escape(exp, quote=True).replace('&amp;lt;', '&lt;').replace('&amp;gt;', '&gt;'), q, ''.join('<li>%s</li>' % o for o in [bon] + mauvais)))
bloc = '<!-- QCH4:DEBUT -->\n' + '\n'.join(items) + '\n<!-- QCH4:FIN -->\n'
s = remplace_bloc(s, 'QCH4', bloc, '</ol>\n</div>\n</main>')
n_total = s.count('<li data-c=')
s = re.sub(r'\d+ questions à choix unique : (.*?)puis conducteurs et condensateurs \(Ch3\)\.', lambda m: '%d questions à choix unique : %spuis conducteurs et condensateurs (Ch3) et champ magnétique (Ch4).' % (n_total, m.group(1)), s)
s = re.sub(r'<button data-n="\d+" type="button">Les \d+</button>', '<button data-n="%d" type="button">Les %d</button>' % (n_total, n_total), s)
ecrire('quiz.html', s)

# index.html
s = lire('index.html')
s = s.replace('<div class="n">4</div><div class="l">Chapitres</div>', '<div class="n">5</div><div class="l">Chapitres</div>')
s = re.sub(r'<div class="n">\d+</div><div class="l">Questions de quiz</div>', '<div class="n">%d</div><div class="l">Questions de quiz</div>' % n_total, s)
s = re.sub(r'<p>\d+ questions à choix multiples', '<p>%d questions à choix multiples' % n_total, s)
s = s.replace('et Ch3 conducteurs et condensateurs.</p><span class="tag">4 chapitres →</span>', 'Ch3 conducteurs et condensateurs et Ch4 champ magnétique.</p><span class="tag">5 chapitres →</span>')
carte = ('<!-- IDX4:DEBUT -->\n<div class="s4-card"><h4>Ch4 · Champ magnétique</h4><p>Boussole, force de Lorentz, loi de Biot et Savart, tire-bouchon, pseudo-vecteur, symétries de \\(\\vec B\\), champ du fil infini. '
         '<a href="cours.html#ch4">Cours</a> · <a href="formules.html#f-mag">Formules</a></p></div>\n<!-- IDX4:FIN -->\n')
s = remplace_bloc(s, 'IDX4', carte, '</div>\n<div class="s4-tip" style="margin-top:18px">')
ecrire('index.html', s)

# README
s = lire('README.md')
if 'Ch4' not in s:
    s = s.replace('Ch3 Conducteurs et condensateurs', 'Ch3 Conducteurs et condensateurs, Ch4 Champ magnétique (début : Lorentz, Biot et Savart, symétries, fil infini)', 1)
ecrire('README.md', s)
print('Ch4 inséré :', n_total, 'questions,', len(FIG), 'figures')
