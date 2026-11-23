TOC = [('cp1-comp', 'Pour comprendre'), ('cp1-ex', 'Exemple guidé (TD2bis)'), ('cp1-test', 'Test de compréhension')]

CH = r'''<!-- ============ CH 1 ============ -->
<article class="chapter cp-chap" id="cp1">
<div class="chapter-hd">
<span class="cn">CH 1</span>
<h2>Électrostatique</h2>
</div>
<div class="prose">
<div class="cp-idea"><span class="cp-k">L'idée en une phrase</span><p>Des charges immobiles créent dans tout l'espace un champ \(\vec E\) ; pour le trouver on additionne les contributions de chaque charge (Coulomb), ou, quand la symétrie est assez forte, on lit le champ directement sur le flux à travers une surface bien choisie (Gauss).</p></div>

<h3 id="cp1-comp">Pour comprendre</h3>

<h4>Charge, densité : décrire « beaucoup de charges » avec un nombre</h4>
<p>Un morceau de plastique frotté porte des milliards de milliards de charges élémentaires (\(e=1{,}6\times10^{-19}\ \mathrm C\)). Impossible de les compter une par une, alors on fait comme avec la population d'un pays : on parle de <b>densité</b>. Selon la forme de l'objet, on choisit la densité qui a du sens :</p>
<div class="tbl-wrap"><table>
<thead><tr><th>Objet</th><th>Densité</th><th>Définition</th><th>Unité</th><th>Charge totale (uniforme)</th></tr></thead>
<tbody>
<tr><td>fil, ligne</td><td>\(\lambda\) (linéique)</td><td>\(\lambda=\dfrac{\mathrm{d}q}{\mathrm{d}\ell}\)</td><td>\(\mathrm{C\cdot m^{-1}}\)</td><td>\(Q=\lambda L\)</td></tr>
<tr><td>plaque, disque, coquille</td><td>\(\sigma\) (surfacique)</td><td>\(\sigma=\dfrac{\mathrm{d}q}{\mathrm{d}S}\)</td><td>\(\mathrm{C\cdot m^{-2}}\)</td><td>\(Q=\sigma S\)</td></tr>
<tr><td>objet plein</td><td>\(\rho\) (volumique)</td><td>\(\rho=\dfrac{\mathrm{d}q}{\mathrm{d}\tau}\)</td><td>\(\mathrm{C\cdot m^{-3}}\)</td><td>\(Q=\rho V\)</td></tr>
</tbody></table></div>
<p>Si la densité <b>n'est pas uniforme</b>, la charge totale est une intégrale : \(Q=\iiint\rho\,\mathrm{d}\tau\). C'est là que le chapitre 0 sert : il faut le bon \(\mathrm{d}\tau\) avec ses facteurs. Astuce unités : si \(\rho=A_1/r^2\), alors \(A_1\) s'exprime en \(\mathrm{C\cdot m^{-3}\times m^2=C\cdot m^{-1}}\) ; l'unité de la constante se déduit toujours de celle de la densité.</p>

<h4>Coulomb : la force, puis le champ</h4>
<p>Deux charges ponctuelles \(q_1\) et \(q_2\) à la distance \(d\) :</p>
<div class="mq">\[\vec F_{1\to2}=\frac{1}{4\pi\varepsilon_0}\frac{q_1q_2}{d^2}\,\vec u_{12}\qquad\frac{1}{4\pi\varepsilon_0}\approx9\times10^9\ \mathrm{N\cdot m^2\cdot C^{-2}}\]</div>
<p>Lis-la comme une phrase : la force est proportionnelle aux deux charges (plus il y a de charge, plus ça tire), décroît comme \(1/d^2\) (la même « influence » est diluée sur la surface d'une sphère de plus en plus grande, \(4\pi d^2\)), et le signe de \(q_1q_2\) donne répulsion ou attraction. Le facteur \(\frac{1}{4\pi\varepsilon_0}\) est une constante de conversion d'unités.</p>
<div class="cp-an"><span class="cp-lab">Ordre de grandeur : l'atome d'hydrogène</span>Proton et électron à \(a_0=5{,}3\times10^{-11}\ \mathrm m\) : \(F=\dfrac{e^2}{4\pi\varepsilon_0a_0^2}\approx8{,}2\times10^{-8}\ \mathrm N\). C'est minuscule en newtons, mais énorme pour un électron de masse \(9\times10^{-31}\ \mathrm{kg}\). La force gravitationnelle entre les mêmes particules est \(\approx3{,}6\times10^{-47}\ \mathrm N\) : l'électrostatique est environ \(2\times10^{39}\) fois plus forte. Voilà pourquoi la gravité ne compte pas en chimie.</div>
<p>On sépare ensuite « celle qui crée » de « celle qui subit » : \(\vec F=q_2\vec E_1\), où \(\vec E_1\) est le <b>champ créé par \(q_1\)</b>. Le champ est une propriété de <i>l'espace autour de \(q_1\)</i>, qui existe même si on n'y met aucune charge-test. Il se mesure en \(\mathrm{V\cdot m^{-1}}\) (ou \(\mathrm{N\cdot C^{-1}}\)) : la force par unité de charge. Au niveau de l'électron de l'hydrogène, \(E=\frac{e}{4\pi\varepsilon_0a_0^2}\approx5\times10^{11}\ \mathrm{V\cdot m^{-1}}\), un des champs les plus intenses qui existent.</p>
<div class="mq">\[\vec E(M)=\frac{q}{4\pi\varepsilon_0}\frac{\overrightarrow{PM}}{PM^3}\qquad(\text{charge }q\text{ en }P)\]</div>
<p>Pourquoi \(\overrightarrow{PM}/PM^3\) ? Parce que c'est \(\vec u/PM^2\) écrit avec \(\vec u=\overrightarrow{PM}/PM\) : la direction (de la charge vers M) et la décroissance en \(1/PM^2\) sont dans la même fraction, ce qui évite de définir \(\vec u\) à part.</p>

<h4>Superposition : on additionne des <i>vecteurs</i></h4>
<p>Si plusieurs charges sont présentes, chacune agit comme si elle était seule (linéarité) : \(\vec E=\sum\vec E_i\). Pour une distribution continue, on remplace la somme par une intégrale sur \(\mathrm{d}q=\lambda\mathrm{d}\ell\), \(\sigma\mathrm{d}S\) ou \(\rho\mathrm{d}\tau\). La seule difficulté est que ce sont des <b>vecteurs</b> : on ne peut additionner les normes qu'après avoir projeté sur une base. D'où l'importance de savoir <i>à l'avance</i> quelles composantes vont s'annuler.</p>

<h4>Symétries et invariances : savoir avant de calculer</h4>
<p>Deux questions à poser <b>avant</b> tout calcul, et qui font gagner un temps énorme :</p>
<ul>
<li><b>Dans quelle direction pointe \(\vec E\) ?</b> (symétries) ;</li>
<li><b>De quelles coordonnées dépend sa norme ?</b> (invariances).</li>
</ul>
<p>Invariances : tu fais bouger M le long d'une coordonnée (translation ou rotation). Si, vu de M, la distribution a exactement la même allure avant et après, la norme de \(\vec E\) ne peut pas changer. Fil infini sur \(Oz\) : glisser M le long de \(z\) ou le faire tourner autour du fil ne change rien, donc \(E=E(r)\).</p>
<p>Symétries : le principe de Curie dit que <b>les effets ont au moins les symétries des causes</b>. Si un plan est un plan de symétrie des charges et que M est dans ce plan, le champ ne peut pas « choisir » un côté du plan, donc il reste dans le plan. Si c'est un plan d'<b>anti</b>symétrie (charges opposées en miroir), les composantes parallèles au plan se compensent et le champ est perpendiculaire au plan.</p>
{{FIG:sym_E}}
<p>Le même calcul en maths, pour la figure de gauche : deux charges \(+q\) en \((\mp d,0)\), M en \((0,y)\) donne \(E_x=0\) et \(E_y=\dfrac{2q\,y}{4\pi\varepsilon_0(d^2+y^2)^{3/2}}\). Les composantes horizontales se compensent exactement : c'est ce que la symétrie prédisait sans calcul.</p>
<div class="tbl-wrap"><table>
<thead><tr><th>Distribution</th><th>Direction de \(\vec E\)</th><th>Dépendance</th></tr></thead>
<tbody>
<tr><td>charge ponctuelle, sphère ou boule \(\rho(r)\)</td><td>\(\vec e_r\) (sphérique)</td><td>\(E(r)\)</td></tr>
<tr><td>fil ou cylindre infini</td><td>\(\vec e_r\) (cylindrique)</td><td>\(E(r)\)</td></tr>
<tr><td>plan infini</td><td>\(\vec e_z\) (normal au plan)</td><td>\(E(z)\), impair en \(z\)</td></tr>
</tbody></table></div>

<h4>Gauss : « tout ce qui sort vient de l'intérieur »</h4>
<p>Pense à un robinet dans une pièce fermée : le débit total qui sort par les murs ne dépend que de ce que fournit le robinet, pas de la forme de la pièce. Gauss dit la même chose pour le champ électrique :</p>
<div class="mq">\[\oiint_{S_G}\vec E\cdot\mathrm{d}\vec S=\frac{Q_{int}}{\varepsilon_0}\]</div>
<p>La surface de Gauss \(S_G\) n'existe pas physiquement : c'est <b>toi</b> qui l'inventes, passant par M. Le théorème est toujours vrai, mais il n'est <b>utile</b> que si tu choisis \(S_G\) de sorte que \(\vec E\) soit soit parallèle, soit perpendiculaire à \(\mathrm{d}\vec S\), et de norme constante sur chaque morceau : alors le flux vaut simplement \(E\times\) (aire) et on isole \(E\). C'est possible seulement avec une symétrie <b>sphérique</b>, <b>cylindrique infinie</b> ou <b>plane infinie</b>. Un disque fini ou un fil de longueur finie : pas de surface qui convienne, donc Coulomb direct.</p>
{{FIG:gauss_sph}}
<p>Pour une symétrie sphérique, \(\vec E=E(r)\vec e_r\) et la sphère de rayon \(r\) donne un flux \(E(r)\times4\pi r^2\) :</p>
<div class="mq">\[E(r)\,4\pi r^2=\frac{Q_{int}(r)}{\varepsilon_0}\ \Longrightarrow\ E(r)=\frac{Q_{int}(r)}{4\pi\varepsilon_0r^2}\]</div>
<p>Lecture : <b>le champ à la distance \(r\) est celui d'une charge ponctuelle placée au centre, mais avec seulement la charge contenue dans la sphère de rayon \(r\)</b>. Le travail se résume à calculer \(Q_{int}(r)\) région par région. Pour un fil infini, avec un cylindre de rayon \(r\) et de hauteur \(h\) (les deux bases n'ont aucun flux), \(E\cdot2\pi rh=\frac{\lambda h}{\varepsilon_0}\), donc \(E=\frac{\lambda}{2\pi\varepsilon_0r}\) : en \(1/r\), car le « mur » cylindrique grandit comme \(r\), pas comme \(r^2\).</p>
<div class="box warn"><div class="bt">⚠ Erreurs typiques</div><p>(1) Utiliser Gauss sans symétrie suffisante. (2) Intégrer \(Q_{int}\) jusqu'à \(R\) au lieu de \(r\) quand \(r\lt R\). (3) Croire qu'un flux nul impose \(\vec E=\vec 0\) : il dit seulement \(Q_{int}=0\). (4) Recopier \(\frac{Q}{4\pi\varepsilon_0r^2}\) par habitude : ce \(4\pi r^2\) est l'aire de la sphère de Gauss. Avec un cylindre, la surface vaut \(2\pi rh\) et le résultat change (\(\frac{\lambda}{2\pi\varepsilon_0r}\)).</p></div>

<h4>Lignes de champ : un dessin du champ</h4>
<p>Une ligne de champ est une courbe tangente à \(\vec E\) en chaque point, orientée dans son sens. Elle indique la <b>direction</b> du champ ; plus elles sont serrées, plus le champ est intense. Elles partent des charges positives, arrivent sur les négatives (ou à l'infini) et ne se coupent jamais (sinon \(\vec E\) aurait deux directions au point de croisement).</p>

<h3 id="cp1-ex">Exemple guidé avec le TD</h3>
<div class="cp-td">
<p class="s4-small">TD2bis, exercice 1 (corrigé complet : <a href="corriges.html#td2bis-1">corriges.html#td2bis-1</a>)</p>
<div class="cp-enonce"><span class="cp-lab">Énoncé</span>Une sphère de centre \(O\), de rayon \(R\) et de charge totale \(Q\) a une densité (a) \(\rho_0\) uniforme ; (b) \(\dfrac{A_1}{r^2}\) ; (c) \(A_2r^2\). Donner le champ en tout point, puis \(\rho_0\), \(A_1\), \(A_2\) en fonction de \(Q\) et \(R\), avec leurs unités. Nous détaillons (a), puis nous donnons (b) et (c) qui se font exactement pareil.</div>
<div class="cp-q"><span class="cp-lab">Ce qu'on cherche</span><p>Le champ \(\vec E(M)\) en tout point : donc à l'intérieur (\(r\lt R\)) <b>et</b> à l'extérieur (\(r\gt R\)). Valeurs réalistes : \(Q=1\ \mathrm{nC}\) (une charge facile à produire par frottement), \(R=2\ \mathrm{cm}\).</p></div>
<div class="cp-q"><span class="cp-lab">Quel outil, et pourquoi</span><p>La distribution est à symétrie <b>sphérique</b> (la densité ne dépend que de \(r\)) : Gauss s'applique et évite toute intégrale vectorielle. L'étape clé sera \(Q_{int}(r)\).</p></div>
<ol class="steps">
<li class="step"><span class="sn"></span><div><div class="st">Symétries et invariances : direction et dépendance</div><div class="sd">
<p>Tout plan contenant \(O\) et M est plan de symétrie de la boule : \(\vec E\) appartient à tous ces plans, donc à leur intersection, la droite \((OM)\) : \(\vec E=E\,\vec e_r\). La boule est invariante par rotation autour de \(O\) : \(E\) ne dépend ni de \(\theta\) ni de \(\varphi\). Donc</p>
<div class="mq">\[\vec E(M)=E(r)\,\vec e_r\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Constante \(\rho_0\) à partir de la charge totale</div><div class="sd">
<p><i>Pourquoi ?</i> L'énoncé donne \(Q\), pas \(\rho_0\), et Gauss demande des charges.</p>
<div class="mq">\[Q=\iiint\rho_0\,\mathrm{d}\tau=\rho_0\cdot\tfrac43\pi R^3\ \Longrightarrow\ \rho_0=\frac{3Q}{4\pi R^3}\ \ (\mathrm{C\cdot m^{-3}})\]</div>
<p>Application numérique : \(\rho_0=\dfrac{3\times10^{-9}}{4\pi(0{,}02)^3}\approx3{,}0\times10^{-5}\ \mathrm{C\cdot m^{-3}}\).</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Surface de Gauss : la sphère de rayon \(r\)</div><div class="sd">
<p>Sur cette sphère, \(\mathrm{d}\vec S=\mathrm{d}S\,\vec e_r\) est parallèle à \(\vec E\) et \(E(r)\) est constant (il ne dépend que de \(r\)) : le flux sort de l'intégrale.</p>
<div class="mq">\[\Phi=\oiint E(r)\,\mathrm{d}S=E(r)\cdot4\pi r^2\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Charge intérieure \(Q_{int}(r)\), région par région</div><div class="sd">
<p>C'est ici qu'on se trompe le plus. <b>À l'intérieur (\(r\lt R\))</b> : seule la boule de rayon \(r\) est contenue dans la surface de Gauss, donc on intègre de \(0\) à \(r\) (pas à \(R\)) :</p>
<div class="mq">\[Q_{int}(r)=\rho_0\cdot\tfrac43\pi r^3=Q\,\frac{r^3}{R^3}\]</div>
<p><b>À l'extérieur (\(r\gt R\))</b> : toute la charge est dedans, \(Q_{int}=Q\).</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Champ</div><div class="sd">
<div class="mq">\[E(r)=\frac{Q_{int}(r)}{4\pi\varepsilon_0r^2}=\begin{cases}\dfrac{Q\,r}{4\pi\varepsilon_0R^3} & r\lt R\\[10pt]\dfrac{Q}{4\pi\varepsilon_0r^2} & r\gt R\end{cases}\]</div>
<p>Dedans, \(Q_{int}\propto r^3\) croît plus vite que \(r^2\) : le champ <i>croît</i> linéairement. Dehors, le champ est exactement celui d'une charge ponctuelle \(Q\) au centre.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Application numérique et ordres de grandeur</div><div class="sd">
<p>À la surface : \(E(R)=\dfrac{Q}{4\pi\varepsilon_0R^2}=\dfrac{9\times10^{9}\times10^{-9}}{(0{,}02)^2}\approx2{,}2\times10^{4}\ \mathrm{V\cdot m^{-1}}\). À \(r=R/2\) : moitié, \(1{,}1\times10^4\ \mathrm{V\cdot m^{-1}}\). À \(r=2R\) (4 cm) : quart, \(5{,}6\times10^3\ \mathrm{V\cdot m^{-1}}\). Pour comparer, l'air claque vers \(3\times10^6\ \mathrm{V\cdot m^{-1}}\) : notre nanocoulomb est largement sans danger.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Vérifications</div><div class="sd">
<p><b>Continuité :</b> en \(r=R\) les deux expressions valent \(\frac{Q}{4\pi\varepsilon_0R^2}\) (pas de charge surfacique, donc pas de saut). <b>Cas limite :</b> pour \(r\gg R\) on retrouve le champ d'une charge ponctuelle. <b>Unités :</b> \(\frac{\mathrm C}{\mathrm{F\cdot m^{-1}}\cdot\mathrm m^2}=\mathrm{V\cdot m^{-1}}\) ✓.</p></div></div></li>
</ol>
{{FIG:E_r}}
<div class="cp-an"><span class="cp-lab">Les modèles (b) et (c) : mêmes étapes, autre \(Q_{int}\)</span>(b) \(\rho=A_1/r^2\) : \(Q=4\pi A_1R\), donc \(A_1=\frac{Q}{4\pi R}\) (en \(\mathrm{C\cdot m^{-1}}\)), \(Q_{int}(r)=4\pi A_1r\) et \(E=\frac{Q}{4\pi\varepsilon_0Rr}\) pour \(r\lt R\). (c) \(\rho=A_2r^2\) : \(A_2=\frac{5Q}{4\pi R^5}\) (en \(\mathrm{C\cdot m^{-5}}\)), \(Q_{int}=Q\frac{r^5}{R^5}\) et \(E=\frac{Q\,r^3}{4\pi\varepsilon_0R^5}\). Dans les trois cas, <b>dehors</b> le champ est \(\frac{Q}{4\pi\varepsilon_0r^2}\) : de l'extérieur, Gauss ne « voit » que la charge totale, pas comment elle est répartie.</div>
<div class="cp-ret"><span class="cp-lab">À retenir</span><ul>
<li>Gauss en 5 temps : symétries, invariances, surface de Gauss, \(Q_{int}\) région par région, \(E=\dfrac{Q_{int}}{\varepsilon_0\,S_G}\).</li>
<li>\(Q_{int}(r)\) s'intègre jusqu'à \(r\), pas jusqu'à \(R\), à l'intérieur de la distribution.</li>
<li>Dehors d'une distribution à symétrie sphérique : champ d'une charge ponctuelle \(Q\) au centre.</li>
<li>Contrôles : continuité en \(r=R\), unités, cas limite \(r\gg R\).</li>
</ul>
<a class="cp-link" href="corriges.html#td2bis-1">→ Voir le corrigé complet du TD2bis ex. 1</a></div>
</div>

<h3 id="cp1-test">Test de compréhension</h3>
<details class="s4-qa"><summary>1. Peut-on trouver le champ d'un disque chargé de rayon \(R\) en un point de son axe par le théorème de Gauss ?</summary><div class="s4-ans">Pas pour en tirer le champ. Le théorème de Gauss reste vrai, mais il n'existe aucune surface fermée passant par M sur laquelle \(\vec E\) soit constant et parallèle ou perpendiculaire à \(\mathrm{d}\vec S\) : un disque fini n'a pas la symétrie sphérique, cylindrique infinie ou plane infinie. On utilise Coulomb direct : par symétrie seule la composante selon l'axe survit, \(E_z=\frac{\sigma}{2\varepsilon_0}\big(1-\frac{z}{\sqrt{z^2+R^2}}\big)\).</div></details>
<details class="s4-qa"><summary>2. Deux charges \(+q\) et \(-q\) ; M est sur le plan médiateur. Dans quelle direction pointe \(\vec E\) en M ?</summary><div class="s4-ans">Perpendiculairement au plan médiateur, en allant vers la charge négative. Le plan médiateur est un plan d'<b>anti</b>symétrie des charges (les charges en miroir sont opposées) : les composantes de \(\vec E_1\) et \(\vec E_2\) parallèles au plan se compensent, celles qui sont perpendiculaires s'ajoutent. Pour deux charges <i>égales</i>, ce serait l'inverse : \(\vec E\) dans le plan.</div></details>
<details class="s4-qa"><summary>3. Pourquoi, en dehors d'une boule chargée à symétrie sphérique, le champ est-il le même quel que soit le modèle de densité (uniforme, en \(1/r^2\), en \(r^2\)...) ?</summary><div class="s4-ans">Parce que Gauss ne fait intervenir que \(Q_{int}\), la charge totale contenue dans la surface de Gauss. Pour \(r\gt R\), la sphère de rayon \(r\) contient toute la boule, donc \(Q_{int}=Q\) quelle que soit la façon dont la charge est répartie à l'intérieur, et \(E=\frac{Q}{4\pi\varepsilon_0r^2}\). La répartition n'influence le champ qu'à l'intérieur de la distribution, par \(Q_{int}(r)\).</div></details>
<a class="cp-back" href="#haut">↑ Retour au sommaire</a>
</div>
</article>
'''
