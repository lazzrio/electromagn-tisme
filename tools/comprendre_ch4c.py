C = r'''
<h3 id="cp4-ex">Exemple guidé avec le TD</h3>
<div class="cp-td">
<p class="s4-small">TD5, exercice 1 (corrigé complet : <a href="corriges.html#td5-1">corriges.html#td5-1</a>)</p>
<div class="cp-enonce"><span class="cp-lab">Énoncé</span>Un fil de longueur infinie est courbé à angle droit. Il est parcouru par un courant d'intensité \(I\). 1) Déterminer le champ magnétique élémentaire créé en M par un élément de circuit de longueur \(\mathrm{d}\ell\), M étant sur le prolongement du tronçon horizontal, à la distance \(a\) du coude O. 2) En déduire le champ total en M.</div>
<div class="cp-q"><span class="cp-lab">Ce qu'on cherche</span><p>Le vecteur \(\vec B(M)\) : sa norme <i>et</i> son sens. Valeurs réalistes : \(I=10\ \mathrm A\), \(a=5\ \mathrm{cm}\) (même courant et même distance que pour le fil infini, ce qui permet de comparer).</p></div>
<div class="cp-q"><span class="cp-lab">Quel outil, et pourquoi</span><p>Biot et Savart, tronçon par tronçon. Le fil courbé n'a aucune symétrie suffisante pour utiliser Ampère (le champ n'a pas de direction simple), donc on <b>découpe en deux tronçons rectilignes</b> et on additionne les champs, en réutilisant la technique du fil infini.</p></div>
{{FIG:td5_1}}
<ol class="steps">
<li class="step"><span class="sn"></span><div><div class="st">Repère et champ élémentaire (question 1)</div><div class="sd">
<p>Origine en O, axe \(Ox\) vers M (horizontal, vers la droite), axe \(Oy\) vers le haut, \(\vec e_z\) sortant de la feuille : M est en \((a,0,0)\). Pour un élément de courant \(I\,\mathrm{d}\vec\ell\) en P :</p>
<div class="mq">\[\mathrm{d}\vec B=\frac{\mu_0I}{4\pi}\,\frac{\mathrm{d}\vec\ell\wedge\overrightarrow{PM}}{PM^3}\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Tronçon horizontal : contribution nulle</div><div class="sd">
<p>Le tronçon horizontal est sur l'axe \(Ox\), et M aussi. Donc en tout point P de ce tronçon, \(\mathrm{d}\vec\ell\) (le long de l'axe) et \(\overrightarrow{PM}\) (le long de l'axe) sont <b>parallèles</b> : \(\mathrm{d}\vec\ell\wedge\overrightarrow{PM}=\vec 0\). Ce tronçon ne crée aucun champ en M, sans calcul. <i>Pourquoi c'est important :</i> repérer ces contributions nulles en un coup d'œil fait gagner la moitié du travail.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Tronçon vertical : champ élémentaire</div><div class="sd">
<p>Le courant monte le long de \(Oy\), de \(y=-\infty\) jusqu'à O (\(y=0\)). Un point P du tronçon est en \((0,y,0)\), avec \(y\lt0\) : \(\mathrm{d}\vec\ell=\mathrm{d}y\,\vec e_y\) et \(\overrightarrow{PM}=a\,\vec e_x-y\,\vec e_y\), de norme \(\sqrt{a^2+y^2}\). Le produit vectoriel : \(\vec e_y\wedge\vec e_x=-\vec e_z\) et \(\vec e_y\wedge\vec e_y=\vec0\), donc \(\mathrm{d}\vec\ell\wedge\overrightarrow{PM}=-a\,\mathrm{d}y\,\vec e_z\).</p>
<div class="mq">\[\mathrm{d}\vec B=-\frac{\mu_0I}{4\pi}\,\frac{a\,\mathrm{d}y}{(a^2+y^2)^{3/2}}\,\vec e_z\]</div>
<p>Le signe \(-\) dit que le champ <b>rentre</b> dans la feuille. Vérification par le tire-bouchon : on tourne \(\mathrm{d}\vec\ell\) (vers le haut) vers \(\overrightarrow{PM}\) (vers la droite) : rotation vers la droite, donc on visse, et le tire-bouchon s'enfonce dans la feuille ✓.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Intégration</div><div class="sd">
<p>Une primitive est \(\int\dfrac{a\,\mathrm{d}y}{(a^2+y^2)^{3/2}}=\dfrac{1}{a}\dfrac{y}{\sqrt{a^2+y^2}}\) (on peut le vérifier en dérivant, ou avec \(y=a\tan\alpha\) comme pour le fil infini). Entre \(-\infty\) et \(0\) : \(\dfrac1a\big(0-(-1)\big)=\dfrac1a\).</p>
<div class="mq">\[\vec B(M)=-\frac{\mu_0I}{4\pi a}\,\vec e_z\qquad\text{soit}\qquad B=\frac{\mu_0I}{4\pi a},\ \text{entrant}\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Application numérique</div><div class="sd">
<div class="mq">\[B=\frac{4\pi\times10^{-7}\times10}{4\pi\times0{,}05}=\frac{10^{-7}\times10}{0{,}05}=2{,}0\times10^{-5}\ \mathrm T=20\ \mu\mathrm T\]</div>
<p>C'est environ 43 % du champ terrestre.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Vérifications</div><div class="sd">
<p><b>Cohérence avec le fil infini :</b> un fil infini peut être vu comme deux demi-fils qui, en un point M situé en face de la jonction à la distance \(a\), créent des champs identiques (même sens, même norme). Chaque demi-fil donne donc la moitié de \(\frac{\mu_0I}{2\pi a}\), soit \(\frac{\mu_0I}{4\pi a}\) ✓ (c'est aussi \(\frac{\mu_0I}{4\pi a}\times\) la valeur de l'intégrale \(\int_0^{\pi/2}\cos\alpha\,\mathrm{d}\alpha=1\), contre 2 pour le fil entier). <b>Unités :</b> \(\mathrm T\) ✓. <b>Sens :</b> confirmé par le tire-bouchon et par la règle de la main droite (pouce vers le haut, à droite du fil les doigts rentrent dans la feuille). <b>Dépendance :</b> \(\propto\frac1a\) comme pour un fil.</p></div></div></li>
</ol>
<div class="cp-ret"><span class="cp-lab">À retenir</span><ul>
<li>Courant non rectiligne : on découpe en tronçons, on additionne les champs (vecteurs).</li>
<li>Si \(\mathrm{d}\vec\ell\parallel\overrightarrow{PM}\), la contribution est nulle (M sur le prolongement du tronçon).</li>
<li>Un demi-fil infini, vu depuis le pied de la perpendiculaire, crée la <b>moitié</b> du champ du fil infini : \(\frac{\mu_0I}{4\pi a}\).</li>
<li>Le sens se vérifie toujours deux fois : produit vectoriel, puis tire-bouchon ou main droite.</li>
</ul>
<a class="cp-link" href="corriges.html#td5-1">→ Voir le corrigé complet du TD5 ex. 1</a></div>
</div>

<h3 id="cp4-test">Test de compréhension</h3>
<details class="s4-qa"><summary>1. Deux fils infinis parallèles sont parcourus par des courants de même intensité et de même sens. Que peut-on dire de \(\vec B\) en un point du plan médiateur (plan équidistant des deux fils) ? Et pour deux charges linéiques égales, que dirait-on de \(\vec E\) ?</summary><div class="s4-ans">Le plan médiateur est un plan de <b>symétrie</b> de la distribution de courants, donc \(\vec B\) y est <b>perpendiculaire</b> au plan (les composantes de \(\vec B_1\) et \(\vec B_2\) qui sont perpendiculaires aux fils et contenues dans le plan se compensent ; les composantes perpendiculaires au plan s'ajoutent). Pour deux charges linéiques égales, le même plan est de symétrie des charges et \(\vec E\) est <b>dans</b> le plan : c'est la règle inversée pour \(\vec B\).</div></details>
<details class="s4-qa"><summary>2. Un électron entre dans un champ \(\vec B\) uniforme perpendiculaire à sa vitesse. Son énergie cinétique change-t-elle ? Dans quel sens tourne-t-il par rapport à un proton ?</summary><div class="s4-ans">Son énergie cinétique ne change pas : la force magnétique \(q\vec v\wedge\vec B\) est toujours perpendiculaire à \(\vec v\), sa puissance \(\vec f\cdot\vec v\) est nulle, donc \(|\vec v|\) est constante. Le mouvement est circulaire uniforme de rayon \(\frac{m_ev}{eB}\). La force dépend du signe de \(q\) : l'électron (\(q\lt0\)) tourne en sens <b>opposé</b> à un proton (\(q\gt0\)) dans le même champ. Et comme \(m_e\) est environ 1840 fois plus petite que \(m_p\), son rayon (à vitesse égale) est environ 1840 fois plus petit.</div></details>
<details class="s4-qa"><summary>3. Le champ à 5 cm d'un fil parcouru par 10 A vaut \(4\times10^{-5}\ \mathrm T\). Que vaut-il à 10 cm ? Avec un courant de 30 A à 5 cm ?</summary><div class="s4-ans">\(B=\frac{\mu_0I}{2\pi r}\) est proportionnel à \(I\) et inversement proportionnel à \(r\). À 10 cm (distance doublée) : \(B=2\times10^{-5}\ \mathrm T\). Avec \(I=30\ \mathrm A\) à 5 cm (courant triplé) : \(B=1{,}2\times10^{-4}\ \mathrm T\), soit environ 2,5 fois le champ terrestre. À retenir pour ne jamais se tromper : \(B\approx2\times10^{-7}\,I/r\) en unités SI.</div></details>
<a class="cp-back" href="#haut">↑ Retour au sommaire</a>
</div>
</article>
'''
