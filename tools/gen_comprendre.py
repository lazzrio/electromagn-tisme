"""Génère comprendre.html (page « Comprendre le cours ») et le bloc CSS /* comprendre:debut */.../* comprendre:fin */
de css/style.css.  Idempotent : relançable à volonté.
Usage : python tools/gen_comprendre.py
Contenu : tools/comprendre_ch0.py ... comprendre_ch4.py (variable CH, avec des marqueurs {{FIG:nom}}),
figures : tools/comprendre_figs.py.  Vérifications numériques : tools/verif_comprendre.py."""
import importlib
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import comprendre_figs  # noqa: E402

CSS_DEBUT = '/* comprendre:debut */'
CSS_FIN = '/* comprendre:fin */'

CSS = r'''/* comprendre:debut */
/* Page « Comprendre le cours » (généré par tools/gen_comprendre.py) */
.cp-chap{scroll-margin-top:72px;margin-bottom:46px}
.cp-idea{margin:16px 0 8px;padding:16px 20px;border-radius:14px;border:1px solid color-mix(in srgb,var(--accent) 35%,transparent);border-left:5px solid var(--accent);background:var(--accent-soft)}
.cp-idea .cp-k{font-family:var(--f-mono);font-size:11.5px;letter-spacing:.09em;text-transform:uppercase;font-weight:600;color:var(--accent);display:block;margin-bottom:5px}
.cp-idea p{margin:0;font-family:var(--f-disp);font-style:italic;font-weight:600;font-size:18px;line-height:1.4}
.cp-td{margin:14px 0;padding:18px 20px;border-radius:14px;background:var(--surface);border:1px solid var(--line);box-shadow:var(--shadow)}
.cp-td>:first-child{margin-top:0}
.cp-enonce{background:var(--surface2);border-left:3px solid var(--accent2);border-radius:8px;padding:11px 14px;font-size:14.5px;margin:10px 0 14px}
.cp-lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;color:var(--accent2);display:block;margin:0 0 3px}
.cp-q{margin:14px 0 6px;padding:11px 14px;border-radius:10px;background:var(--amber-soft);border:1px solid color-mix(in srgb,var(--accent2) 30%,transparent);font-size:14.8px}
.cp-q p{margin:4px 0}
.cp-ret{margin:16px 0 4px;padding:12px 16px;border-radius:10px;background:var(--good-soft);border:1px solid color-mix(in srgb,var(--good) 40%,transparent);font-size:14.8px}
.cp-ret .cp-lab{color:var(--good)}
.cp-ret ul{margin:4px 0 0;padding-left:20px}
.cp-ret li{margin:3px 0}
.cp-an{margin:12px 0;padding:11px 14px;border-radius:10px;background:var(--surface2);border:1px dashed var(--line);font-size:14.5px}
.cp-an .cp-lab{color:var(--muted)}
.cp-back{display:inline-block;margin:6px 0 0;font-family:var(--f-mono);font-size:12px}
.cp-chap .steps .sd{color:var(--ink);font-size:14.8px}
.cp-chap .steps .sd p{margin:6px 0}
.cp-chap .steps .st{font-size:15px}
.cp-chap details.s4-qa .mq{margin:8px 0}
.cp-chap .tbl-wrap td{vertical-align:top}
.cp-chap .fgbox{margin:14px 0}
.cp-chap .mq{margin:10px 0}
.cp-link{display:inline-flex;align-items:center;gap:6px;margin-top:6px;font-weight:600}
.cp-hero{margin:14px 0 4px}
@media(max-width:640px){
  .cp-td{padding:14px 12px}
  .cp-idea p{font-size:16.5px}
  .cp-idea{padding:13px 14px}
}
/* comprendre:fin */'''

HEAD = r'''<!DOCTYPE html>

<html lang="fr">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Comprendre le cours — Électromagnétisme</title>
<meta content="Comprendre le cours d'électromagnétisme ING2 : pour chaque chapitre (outils mathématiques, électrostatique, potentiel, conducteurs et condensateurs, champ magnétique), l'idée, les explications pas à pas, un exercice de TD résolu comme avec un tuteur et un test de compréhension." name="description"/>
<meta content="light" name="color-scheme"/>
<meta content="#1d5fc4" name="theme-color"/>

<link href="assets/favicon.svg" rel="icon" type="image/svg+xml"/>
<link href="assets/icon-192.png" rel="apple-touch-icon"/>
<link href="manifest.webmanifest" rel="manifest"/>
<meta content="Comprendre le cours — Électromagnétisme" property="og:title"/>
<meta content="Une page pour vraiment comprendre chaque chapitre : analogies, pourquoi des formules, exemple guidé avec le TD, test de compréhension." property="og:description"/>
<meta content="website" property="og:type"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,500;0,600;0,700;0,800;1,600;1,700&amp;family=Source+Sans+3:ital,wght@0,400;0,600;1,400&amp;family=JetBrains+Mono:wght@400;500;600&amp;display=swap" rel="stylesheet"/>
<link href="css/style.css" rel="stylesheet"/>
<link crossorigin="anonymous" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" rel="stylesheet"/>
<script>try{var t=JSON.parse(localStorage.getItem("em_theme"));if(t)document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>
</head>
<body>
<div class="topbar">
<div class="topbar-in">
<a aria-label="Accueil du site" class="brand" href="index.html">
<span class="chip-logo"><svg fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><path d="M13 2 L5 13 h6 l-1.5 9 L19 10 h-6 z"></path></svg></span>
      Électromagnétisme
    </a>
<nav aria-label="Navigation principale" class="nav" id="nav">
<a href="index.html">Accueil</a>
<a class="nav-hot" href="revision-ds.html">🎯 Révision DS</a>
<a href="cours.html">📚 Cours</a>
<a aria-current="page" class="active" href="comprendre.html">💡 Comprendre</a>
<a href="formules.html">📘 Formules</a>
<a href="corriges.html">✅ TD corrigés</a>
<a href="quiz.html">🧠 Quiz</a>
<a href="ds1-complet.html">📝 DS1</a>
</nav>
<button aria-label="Changer de thème" class="theme-btn" id="themeBtn" title="Thème clair / sombre">
<svg fill="none" id="thIcon" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"></svg>
</button>
<button aria-expanded="false" aria-label="Menu" class="burger" id="burger"><svg fill="none" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"></path></svg></button>
</div>
</div>
<main>
<div class="wrap" id="haut">
<div class="page-head">
<span class="eyebrow">💡 Comprendre</span>
<h1>Comprendre le cours</h1>
<p>Le cours te dit <i>quoi</i> ; cette page t'explique <i>pourquoi</i>. Pour chaque chapitre : l'idée en une phrase, les notions expliquées pas à pas (analogies, d'où sort chaque formule, erreurs classiques), un exercice du TD résolu comme avec un tuteur, puis un mini-test. Lis un chapitre, essaie l'exemple <b>avant</b> de lire la solution, réponds au test sans regarder.</p>
</div>
<nav aria-label="Chapitres" class="cx-index">
<a class="cx-card" href="#cp0"><span class="n">Ch 0 · TD0</span><span class="t">Outils mathématiques</span><span class="d">Repères, dℓ, dS, dτ, gradient, flux, circulation. Exemple : flux à travers un cylindre.</span></a>
<a class="cx-card" href="#cp1"><span class="n">Ch 1 · TD2bis</span><span class="t">Électrostatique</span><span class="d">Charges, Coulomb, superposition, symétries, Gauss. Exemple : boule chargée.</span></a>
<a class="cx-card" href="#cp2"><span class="n">Ch 2 · TD3</span><span class="t">Potentiel et énergie</span><span class="d">Le potentiel comme une altitude. Exemple : potentiel d'un fil infini.</span></a>
<a class="cx-card" href="#cp3"><span class="n">Ch 3 · TD4</span><span class="t">Conducteurs et condensateurs</span><span class="d">Équilibre, capacité, énergie. Exemple : le condensateur plan.</span></a>
<a class="cx-card" href="#cp4"><span class="n">Ch 4 · TD5</span><span class="t">Champ magnétique</span><span class="d">Lorentz, Biot et Savart, symétries inversées. Exemples : cercle de Larmor, courant angulaire.</span></a>
</nav>
<div class="course-layout">
<aside class="toc" id="toc">
<div class="toc-title">Chapitres</div>
{{TOC}}
</aside>
<div class="course-content">
'''

TAIL = r'''</div>
</div>
</div>
</main>
<div class="foot">
<div class="wrap">
<span>Électromagnétisme · ECE ING2 \(\cdot \,S_{3}\,2026-2027\)</span>
<span><a href="index.html">Accueil</a> · <a href="revision-ds.html">Révision DS</a> · <a href="cours.html">Cours</a> · <a href="comprendre.html">Comprendre</a> · <a href="formules.html">Formules</a> · <a href="corriges.html">TD corrigés</a> · <a href="quiz.html">Quiz</a></span>
</div>
</div>
<a aria-label="Revenir en haut de la page" class="cx-top" href="#">↑</a>
<script crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<script src="js/maths.js"></script>
<script src="js/site.js"></script>
</body>
</html>
'''

CHAPS = [
    ('comprendre_ch0', 'cp0', '0 · Outils mathématiques'),
    ('comprendre_ch1', 'cp1', '1 · Électrostatique'),
    ('comprendre_ch2', 'cp2', '2 · Potentiel et énergie'),
    ('comprendre_ch3', 'cp3', '3 · Conducteurs et condensateurs'),
    ('comprendre_ch4', 'cp4', '4 · Champ magnétique'),
]


def main():
    figs = comprendre_figs.build()
    corps, toc = [], []
    for mod, cid, titre in CHAPS:
        m = importlib.import_module(mod)
        toc.append('<a href="#%s">%s</a>' % (cid, titre))
        for sid, stitre in m.TOC:
            toc.append('<a href="#%s">↳ %s</a>' % (sid, stitre))
        corps.append(m.CH)
    html = HEAD.replace('{{TOC}}', '\n'.join(toc)) + '\n'.join(corps) + TAIL
    # fractions « dfrac » dans le texte courant (pas dans les formules centrées) : \frac, pour ne pas écarter les lignes
    html = re.sub(r'\\\((.*?)\\\)', lambda m: '\\(' + m.group(1).replace('\\dfrac', '\\frac') + '\\)', html, flags=re.S)
    used = set()
    for k, v in figs.items():
        tag = '{{FIG:%s}}' % k
        if tag in html:
            used.add(k)
        html = html.replace(tag, v)
    if '{{FIG:' in html:
        raise SystemExit('figure inconnue dans le contenu : ' + html[html.index('{{FIG:'):][:40])
    inutilisees = sorted(set(figs) - used)
    if inutilisees:
        print('figures non utilisées :', inutilisees)
    with open(os.path.join(ROOT, 'comprendre.html'), 'w', encoding='utf-8', newline='') as f:
        f.write(html.replace('\r\n', '\n').replace('\n', '\r\n'))
    # CSS : un aller-retour lecture -> écriture
    p = os.path.join(ROOT, 'css', 'style.css')
    s = open(p, encoding='utf-8', newline='').read()
    crlf = '\r\n' in s
    s = s.replace('\r\n', '\n')
    if CSS_DEBUT in s:
        i = s.index(CSS_DEBUT)
        j = s.index(CSS_FIN) + len(CSS_FIN)
        s = s[:i] + CSS + s[j:]
    else:
        s = s.rstrip('\n') + '\n' + CSS + '\n'
    if crlf:
        s = s.replace('\n', '\r\n')
    tmp = p + '.tmp'
    open(tmp, 'w', encoding='utf-8', newline='').write(s)
    os.replace(tmp, p)
    print('comprendre.html : %d octets, %d figures' % (len(html), len(used)))


if __name__ == '__main__':
    main()
