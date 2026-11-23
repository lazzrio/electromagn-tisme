TOC = [('cp2-comp', 'Pour comprendre'), ('cp2-ex', 'Exemple guidé (TD3)'), ('cp2-test', 'Test de compréhension')]

CH = r'''<!-- ============ CH 2 ============ -->
<article class="chapter cp-chap" id="cp2">
<div class="chapter-hd">
<span class="cn">CH 2</span>
<h2>Potentiel et énergie</h2>
</div>
<div class="prose">
<div class="cp-idea"><span class="cp-k">L'idée en une phrase</span><p>Le potentiel \(V\) est « l'altitude électrique » : un seul nombre par point à la place d'un vecteur, dont la pente (changée de signe) redonne le champ, et qui, multiplié par la charge, donne l'énergie.</p></div>

<h3 id="cp2-comp">Pour comprendre</h3>

<h4>Pourquoi un potentiel existe : le champ est « conservatif »</h4>
<p>Pour le poids, le travail pour passer d'un point A à un point B ne dépend que de la différence d'altitude, pas du chemin (escalier ou ascenseur, même effort). On définit alors l'énergie potentielle \(mgz\). La force de Coulomb a exactement la même propriété (c'est une force centrale en \(1/r^2\)) : la <b>circulation</b> du champ entre A et B ne dépend pas du chemin, et elle est nulle sur un contour fermé. On peut donc définir une « altitude » \(V\).</p>
<div class="mq">\[V_A-V_B=\int_A^B\vec E\cdot\mathrm{d}\vec\ell\qquad\Longleftrightarrow\qquad\mathrm{d}V=-\vec E\cdot\mathrm{d}\vec\ell\qquad[V]=\text{volt}\]</div>
<p><b>Pourquoi le signe moins ?</b> Une charge positive lâchée dans un champ se déplace dans le sens de \(\vec E\), donc <i>vers les potentiels qui diminuent</i>, comme une bille qui roule vers le bas. Le champ pointe donc « vers le bas » du paysage de potentiel : \(\vec E=-\overrightarrow{\mathrm{grad}}\,V\) (rappel du Ch0 : le gradient pointe vers le haut).</p>
<p><b>Détail pratique :</b> \(V_A-V_B=\int_A^B\vec E\cdot\mathrm{d}\vec\ell\) : « départ moins arrivée ». Vérifie toujours le signe sur la charge ponctuelle : \(V_A-V_B=\frac{q}{4\pi\varepsilon_0}\big(\frac1{r_A}-\frac1{r_B}\big)\).</p>
<p>Autre point fondamental : \(V\) n'est défini qu'<b>à une constante près</b>, comme une altitude dépend du niveau de référence choisi (la mer, le sol du labo...). Seules les <i>différences</i> de potentiel sont mesurables (c'est une tension), et le champ, qui ne dépend que de la pente, n'est pas affecté par ce choix.</p>

<h4>Potentiel d'une charge ponctuelle : le démonter</h4>
<p>Avec \(\vec E=\frac{q}{4\pi\varepsilon_0r^2}\vec e_r\) et \(\mathrm{d}\vec\ell=\mathrm{d}r\,\vec e_r+\dots\), on a \(\vec e_r\cdot\mathrm{d}\vec\ell=\mathrm{d}r\) (les autres composantes de \(\mathrm{d}\vec\ell\) sont perpendiculaires à \(\vec e_r\)). Donc \(\mathrm{d}V=-\frac{q}{4\pi\varepsilon_0r^2}\mathrm{d}r\) et, en intégrant :</p>
<div class="mq">\[V(r)=\frac{q}{4\pi\varepsilon_0\,r}+\text{cste}\qquad\text{cste}=0\ \text{si}\ V(\infty)=0\]</div>
<p>La constante est nulle si on décide que le potentiel s'annule à l'infini : c'est le choix naturel pour toute distribution <b>finie</b>. Exemple concret : un proton crée à la distance de Bohr \(a_0=5{,}3\times10^{-11}\ \mathrm m\) le potentiel \(\frac{e}{4\pi\varepsilon_0a_0}\approx27\ \mathrm V\) ; un électron placé là a une énergie potentielle \(-27\ \mathrm{eV}\) (en électronvolts, ce que « coûte » une charge \(e\) pour franchir 1 V). Son énergie totale est \(-13{,}6\ \mathrm{eV}\) car l'énergie cinétique compense la moitié : on retrouve l'énergie d'ionisation de l'hydrogène.</p>

<h4>Distribution infinie : pas de « zéro à l'infini »</h4>
<p>Pour un fil, un cylindre ou un plan infinis, le champ ne décroît pas assez vite : \(\int E\,\mathrm{d}r\) diverge quand \(r\to\infty\) (pour le fil, \(\int\frac{\mathrm{d}r}{r}=\ln r\to\infty\)). On ne peut donc pas imposer \(V(\infty)=0\). On choisit un autre point de référence : « \(V(R_0)=V_0\) », avec un rayon \(R_0\) donné par l'énoncé. Le logarithme porte alors sur un rapport sans dimension \(\frac{r}{R_0}\).</p>

<h4>Deux sens de passage entre \(\vec E\) et \(V\)</h4>
<ul>
<li><b>De \(V\) à \(\vec E\) : dériver</b> (gradient, avec les \(\frac1r\) du Ch0). Facile, toujours possible.</li>
<li><b>De \(\vec E\) à \(V\) : intégrer</b> \(\mathrm{d}V=-\vec E\cdot\mathrm{d}\vec\ell\). Si \(\vec E=E(r)\vec e_r\) : \(V(r)=-\int E(r)\,\mathrm{d}r+\text{cste}\). S'il y a plusieurs régions (sphères concentriques...), on intègre région par région et on <b>raccorde les constantes</b> en imposant que \(V\) soit continu aux interfaces, en partant de la référence.</li>
</ul>
<p>Pourquoi \(V\) est-il continu même quand \(E\) ne l'est pas ? Parce que \(V\) est une intégrale de \(E\) : un champ qui saute (couche chargée en surface) donne seulement un changement brutal de <i>pente</i>, pas un saut de \(V\) (tant que \(E\) reste fini).</p>

<h4>Équipotentielles : le relief vu du dessus</h4>
{{FIG:equi}}
<p>Une surface équipotentielle relie les points de même \(V\) (les courbes de niveau). Pour un déplacement le long d'une équipotentielle, \(\mathrm{d}V=-\vec E\cdot\mathrm{d}\vec\ell=0\) : \(\vec E\perp\mathrm{d}\vec\ell\), donc <b>les lignes de champ coupent les équipotentielles à angle droit</b>, en allant vers les \(V\) décroissants. Charge ponctuelle : sphères ; fil ou cylindre infini : cylindres coaxiaux ; plan infini : plans parallèles.</p>

<h4>De l'énergie : ce que fait le potentiel pour une charge</h4>
<p>Une charge \(q\) qui va de A à B voit son énergie potentielle varier de \(q(V_B-V_A)\), et le champ lui fournit le travail \(W_{AB}=q\,(V_A-V_B)\). Retiens : <b>une charge positive « descend » les potentiels, une charge négative les « monte »</b>, en gagnant de l'énergie cinétique. Application : un électron lâché dans une tension de \(100\ \mathrm V\) gagne \(100\ \mathrm{eV}=1{,}6\times10^{-17}\ \mathrm J\), donc \(v=\sqrt{2eU/m_e}\approx5{,}9\times10^6\ \mathrm{m\cdot s^{-1}}\) (2 % de la vitesse de la lumière : c'est le principe du tube cathodique). Pour deux charges ponctuelles, l'énergie d'interaction est \(\frac{q_1q_2}{4\pi\varepsilon_0r_{12}}\) : positive si elles se repoussent (il a fallu forcer pour les rapprocher), négative si elles s'attirent.</p>
<div class="box warn"><div class="bt">⚠ Erreurs typiques</div><p>Écrire \(V(\infty)=0\) pour une distribution infinie ; oublier le signe − dans \(\vec E=-\overrightarrow{\mathrm{grad}}V\) ; inverser les bornes de \(\int\vec E\cdot\mathrm{d}\vec\ell\) ; croire que \(\vec E=\vec 0\) impose \(V=0\) (non : \(V\) est seulement <i>constant</i>) ; oublier le facteur \(q\) entre \(V\) (en volts) et l'énergie (en joules).</p></div>

<h3 id="cp2-ex">Exemple guidé avec le TD</h3>
<div class="cp-td">
<p class="s4-small">TD3, exercice 2 (corrigé complet : <a href="corriges.html#td3-2">corriges.html#td3-2</a>)</p>
<div class="cp-enonce"><span class="cp-lab">Énoncé</span>Fil infini d'axe \(Oz\), de densité linéique \(\lambda\) uniforme. 1) Direction et dépendances de \(\vec E\). 2) Calculer \(\vec E(M)\). 3) En déduire \(V(M)\) avec \(V(R_0)=V_0\). 4) Tracer \(E\) et \(V\) et interpréter.</div>
<div class="cp-q"><span class="cp-lab">Ce qu'on cherche</span><p>Le champ <i>puis</i> le potentiel d'un fil infini. Valeurs réalistes : \(\lambda=1\ \mathrm{nC\cdot m^{-1}}\), référence \(V_0=0\) en \(R_0=10\ \mathrm{cm}\).</p></div>
<div class="cp-q"><span class="cp-lab">Quel outil, et pourquoi</span><p>Symétrie cylindrique infinie : Gauss donne \(\vec E\) en deux lignes. Ensuite on <i>intègre</i> \(\mathrm{d}V=-\vec E\cdot\mathrm{d}\vec\ell\) (on va de \(\vec E\) à \(V\)). On sait déjà qu'on ne pourra pas prendre \(V(\infty)=0\).</p></div>
<ol class="steps">
<li class="step"><span class="sn"></span><div><div class="st">Symétries et invariances</div><div class="sd">
<p>Le plan contenant l'axe et M, et le plan perpendiculaire à l'axe passant par M, sont deux plans de symétrie : \(\vec E\) est selon leur intersection, c'est-à-dire \(\vec e_r\). Le fil est invariant par translation selon \(z\) et par rotation d'angle \(\theta\) : \(E\) ne dépend que de \(r\). Donc \(\vec E=E(r)\,\vec e_r\).</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Gauss avec un cylindre de rayon \(r\) et de hauteur \(h\)</div><div class="sd">
<p>Sur les deux bases, \(\mathrm{d}\vec S=\pm\mathrm{d}S\,\vec e_z\perp\vec E\) : flux nul. Sur la face latérale, \(\vec E\parallel\mathrm{d}\vec S\) et \(E\) constant : flux \(E\cdot2\pi rh\). La charge intérieure est celle de la portion de fil de longueur \(h\) : \(\lambda h\).</p>
<div class="mq">\[E(r)\cdot2\pi rh=\frac{\lambda h}{\varepsilon_0}\ \Longrightarrow\ \vec E=\frac{\lambda}{2\pi\varepsilon_0\,r}\,\vec e_r\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Du champ au potentiel : intégrer \(\mathrm{d}V=-E\,\mathrm{d}r\)</div><div class="sd">
<p><i>Pourquoi \(\mathrm{d}r\) seul ?</i> \(\mathrm{d}V=-\vec E\cdot\mathrm{d}\vec\ell=-E(r)\,\vec e_r\cdot(\mathrm{d}r\,\vec e_r+r\,\mathrm{d}\theta\,\vec e_\theta+\mathrm{d}z\,\vec e_z)=-E(r)\,\mathrm{d}r\) : les autres déplacements sont perpendiculaires au champ.</p>
<div class="mq">\[V(r)=-\frac{\lambda}{2\pi\varepsilon_0}\ln r+\text{cste}\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Constante : on impose \(V(R_0)=V_0\)</div><div class="sd">
<p>\(\text{cste}=V_0+\frac{\lambda}{2\pi\varepsilon_0}\ln R_0\), d'où, en regroupant les deux logarithmes en un seul <b>rapport sans dimension</b> :</p>
<div class="mq">\[V(r)=V_0-\frac{\lambda}{2\pi\varepsilon_0}\ln\frac{r}{R_0}\]</div>
<p>On ne pouvait pas écrire \(V(\infty)=0\) : \(\ln r\to+\infty\) donc \(V\to-\infty\) (pour \(\lambda\gt0\)).</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Application numérique</div><div class="sd">
<p>Le coefficient \(\dfrac{\lambda}{2\pi\varepsilon_0}\) vaut \(\dfrac{10^{-9}}{2\pi\times8{,}85\times10^{-12}}\approx18\ \mathrm V\) (ses unités : \(\frac{\mathrm{C\cdot m^{-1}}}{\mathrm{F\cdot m^{-1}}}=\mathrm V\), c'est bien un potentiel). Donc :</p>
<div class="mq">\[E(1\,\mathrm{cm})\approx1{,}8\times10^{3}\ \mathrm{V\cdot m^{-1}}\qquad E(10\,\mathrm{cm})\approx1{,}8\times10^{2}\ \mathrm{V\cdot m^{-1}}\]</div>
<div class="mq">\[\begin{gathered}V(1\,\mathrm{cm})=-18\ln(0{,}1)\approx+41\ \mathrm V\\ V(1\,\mathrm m)=-18\ln(10)\approx-41\ \mathrm V\\ V(1\,\mathrm{km})=-18\ln(10^4)\approx-166\ \mathrm V\end{gathered}\]</div>
<p>Remarque : \(V\) diverge, mais <i>très</i> lentement : à \(10^6\ \mathrm m\) du fil, \(V\approx-290\ \mathrm V\) seulement. Et la différence entre 1 cm et 10 cm est de \(18\ln10\approx41\ \mathrm V\) : un proton amené de 10 cm à 1 cm du fil demanderait \(41\ \mathrm{eV}\) à l'opérateur.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Vérifications et interprétation</div><div class="sd">
<p><b>Dérivée :</b> \(-\frac{\mathrm{d}V}{\mathrm{d}r}=\frac{\lambda}{2\pi\varepsilon_0r}=E\) ✓ (en repassant par le gradient, on retombe sur le champ). <b>Signe :</b> pour \(\lambda\gt0\), \(\vec E\) s'éloigne du fil et \(V\) décroît quand \(r\) augmente : le champ pointe vers les \(V\) décroissants ✓. <b>Forme :</b> \(E\propto1/r\) (hyperbole), \(V\propto-\ln r\) ; la pente de la courbe \(V(r)\) est \(-E\). Les équipotentielles sont des cylindres coaxiaux.</p></div></div></li>
</ol>
{{FIG:fil_EV}}
<div class="cp-ret"><span class="cp-lab">À retenir</span><ul>
<li>\(\mathrm{d}V=-\vec E\cdot\mathrm{d}\vec\ell\) : avec \(\vec E=E(r)\vec e_r\), \(V(r)=-\int E\,\mathrm{d}r\).</li>
<li>Distribution infinie : jamais \(V(\infty)=0\) ; on fixe \(V(R_0)=V_0\) et le logarithme contient un rapport \(\frac{r}{R_0}\).</li>
<li>Contrôle gagnant : redériver \(V\) et retrouver \(E\) ; vérifier que \(E\) pointe vers les \(V\) décroissants.</li>
</ul>
<a class="cp-link" href="corriges.html#td3-2">→ Voir le corrigé complet du TD3 ex. 2</a></div>
</div>

<h3 id="cp2-test">Test de compréhension</h3>
<details class="s4-qa"><summary>1. Pourquoi ne peut-on pas imposer \(V(\infty)=0\) pour un fil infini chargé ?</summary><div class="s4-ans">Parce que \(V(r)=V_0-\frac{\lambda}{2\pi\varepsilon_0}\ln\frac r{R_0}\) tend vers \(\mp\infty\) quand \(r\to\infty\) : il n'existe pas de valeur finie à l'infini. Physiquement, le fil lui-même est infini : il y a toujours de la charge « à l'infini » qui continue de contribuer. On fixe donc le potentiel en un point à distance finie \(R_0\).</div></details>
<details class="s4-qa"><summary>2. Un proton est lâché sans vitesse dans un champ électrostatique. Vers quels potentiels va-t-il, et que devient son énergie ?</summary><div class="s4-ans">Vers les potentiels décroissants, dans le sens de \(\vec E\). Son énergie potentielle \(qV\) diminue, son énergie cinétique augmente de la même quantité (la somme est conservée, la force de Coulomb étant conservative). Un électron ferait l'inverse en direction, car sa charge est négative : il va vers les potentiels croissants, mais perd aussi de l'énergie potentielle \(qV\).</div></details>
<details class="s4-qa"><summary>3. Dans une région, \(V\) est constant. Que vaut \(\vec E\) ? Et si \(\vec E=\vec 0\) dans une région, que vaut \(V\) ?</summary><div class="s4-ans">Si \(V\) est constant, son gradient est nul donc \(\vec E=-\overrightarrow{\mathrm{grad}}V=\vec0\). Réciproquement, si \(\vec E=\vec 0\) dans une région connexe, \(V\) y est <i>constant</i>, mais pas forcément nul : l'intérieur d'une sphère chargée en surface a \(E=0\) et \(V=\frac{\sigma R}{\varepsilon_0}\). Ce raisonnement sert dans le chapitre suivant (conducteurs).</div></details>
<a class="cp-back" href="#haut">↑ Retour au sommaire</a>
</div>
</article>
'''
