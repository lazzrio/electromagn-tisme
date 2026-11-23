TOC = [('cp3-comp', 'Pour comprendre'), ('cp3-ex', 'Exemple guidé (TD4)'), ('cp3-test', 'Test de compréhension')]

CH = r'''<!-- ============ CH 3 ============ -->
<article class="chapter cp-chap" id="cp3">
<div class="chapter-hd">
<span class="cn">CH 3</span>
<h2>Conducteurs à l'équilibre et condensateurs</h2>
</div>
<div class="prose">
<div class="cp-idea"><span class="cp-k">L'idée en une phrase</span><p>Dans un métal, les charges libres se déplacent jusqu'à ce qu'il n'y ait plus aucun champ à l'intérieur ; cette règle simple fixe où sont les charges, donne le champ juste à l'extérieur, et permet de calculer la capacité \(C=Q/U\) d'un condensateur, c'est-à-dire sa « contenance » en charge.</p></div>

<h3 id="cp3-comp">Pour comprendre</h3>

<h4>Pourquoi \(\vec E=\vec 0\) dans un conducteur à l'équilibre</h4>
<p>Un métal contient des électrons libres qui n'attendent qu'une force pour bouger. <b>Si</b> un champ existait dans le métal, il pousserait ces charges, donc il y aurait un courant. « À l'équilibre » signifie justement : plus de courant, plus de mouvement d'ensemble. La seule façon que ça tienne : \(\vec E_{int}=\vec 0\). Tout le reste en découle :</p>
<ul>
<li>\(\vec E=-\overrightarrow{\mathrm{grad}}V=\vec0\) : le potentiel est <b>le même</b> partout dans le conducteur (c'est un volume équipotentiel, comme la surface d'une eau au repos est horizontale) ;</li>
<li>Gauss sur n'importe quelle petite surface fermée à l'intérieur : flux nul, donc \(Q_{int}=0\) : <b>pas de charge dans le volume</b>. Les charges en excès sont forcément sur la <b>surface</b>, avec une densité \(\sigma\) ;</li>
<li>la surface est une équipotentielle, et les lignes de champ coupent les équipotentielles à angle droit : à l'extérieur, \(\vec E\) est <b>normal</b> à la surface.</li>
</ul>

<h4>Le théorème de Coulomb : \(E=\sigma/\varepsilon_0\), et pourquoi pas \(\sigma/2\varepsilon_0\)</h4>
<div class="mq">\[\vec E_{ext}=\frac{\sigma}{\varepsilon_0}\,\vec n_{ext}\]</div>
<p>Il y a un piège classique : un plan chargé isolé crée \(\frac{\sigma}{2\varepsilon_0}\) <i>de chaque côté</i>, mais à la surface d'un conducteur on trouve \(\frac{\sigma}{\varepsilon_0}\) d'<i>un seul</i> côté. Explication : près du point P, le champ est la somme du champ du petit morceau de surface (qui vaut \(\pm\frac{\sigma}{2\varepsilon_0}\), signe selon le côté) et du champ \(\vec E_2\) créé par tout le reste, qui est continu à la traversée. Dedans, le total est nul : \(0=-\frac{\sigma}{2\varepsilon_0}+E_2\), donc \(E_2=\frac{\sigma}{2\varepsilon_0}\). Dehors, les deux contributions s'ajoutent : \(\frac{\sigma}{2\varepsilon_0}+\frac{\sigma}{2\varepsilon_0}=\frac{\sigma}{\varepsilon_0}\). Le conducteur « arrange » ses charges pour annuler exactement le champ dedans, ce qui double le champ dehors.</p>

<h4>Effet de pointe</h4>
<p>Deux sphères conductrices de rayons \(R_1\) et \(R_2\), très éloignées et reliées par un fil, forment un seul conducteur : même potentiel \(V\). Or le potentiel d'une sphère est \(V=\frac{\sigma R}{\varepsilon_0}\) (car \(Q=4\pi R^2\sigma\) et \(V=\frac{Q}{4\pi\varepsilon_0R}\)). Donc \(\sigma_1R_1=\sigma_2R_2\), soit \(\frac{\sigma_1}{\sigma_2}=\frac{R_2}{R_1}\) : <b>la plus petite sphère porte la plus grande densité de charge</b>, et le champ \(\frac{\sigma}{\varepsilon_0}\) y est le plus fort. Une pointe est un rayon de courbure minuscule : le champ y devient énorme (paratonnerre, décharge par effet de pointe).</p>

<h4>Influence totale : la cavité</h4>
<p>Une charge \(+q\) dans une cavité d'un conducteur neutre : une surface de Gauss dans le métal (où \(E=0\)) qui entoure la cavité a un flux nul, donc contient une charge totale nulle : la face interne porte \(-q\). Conducteur neutre oblige, la face externe porte \(+q\). Cavité <i>vide</i> : la face interne ne porte rien et le champ y est nul : une « cage de Faraday » protège l'intérieur de tout champ extérieur.</p>

<h4>Capacité : combien de charge pour un volt ?</h4>
<p>Si on porte un conducteur seul au potentiel \(V\) (référence à l'infini), il se charge de \(Q=CV\), où \(C\) ne dépend <b>que de la géométrie</b>. Pourquoi une relation linéaire ? Parce que si on multiplie \(V\) par 2, toutes les densités \(\sigma\) doublent (le champ et le potentiel sont proportionnels aux charges). Pour une sphère, \(C=4\pi\varepsilon_0R\) : plus elle est grosse, plus elle « contient » de charge à \(V\) donné. L'unité est le farad, \(1\ \mathrm F=1\ \mathrm{C\cdot V^{-1}}\) ; c'est une unité gigantesque (la Terre, \(R=6400\ \mathrm{km}\), n'a que \(0{,}7\ \mathrm{mF}\)), d'où les \(\mathrm{pF}\), \(\mathrm{nF}\), \(\mu\mathrm F\).</p>

<h4>Condensateur : deux conducteurs en influence totale</h4>
<p>Pour stocker beaucoup de charge avec peu de tension, on rapproche deux conducteurs en influence totale : quand l'armature 1 porte \(+Q\), l'armature 2 qui lui fait face porte \(-Q\). La tension entre elles est proportionnelle à \(Q\) :</p>
<div class="mq">\[Q=C\,U\qquad U=V_1-V_2\qquad C\ \text{ne dépend que de la géométrie (et du vide ou du diélectrique)}\]</div>
<p>Analogie hydraulique : un réservoir cylindrique. \(Q\) est le volume d'eau, \(U\) la hauteur d'eau, et \(C\) la <b>section</b> du réservoir : plus elle est large, plus il faut de volume pour monter d'un mètre. De même, pour un condensateur plan, \(C=\frac{\varepsilon_0S}{e}\) augmente avec la surface \(S\) des armatures, et quand on rapproche les armatures (\(e\) petit) il faut moins de tension pour la même charge.</p>
<div class="box method"><div class="bt">▹ Méthode : calculer une capacité</div><p>1) Schéma, armatures chargées \(+Q\) et \(-Q\). 2) Champ entre les armatures (Gauss ou superposition) en fonction de \(Q\) ou \(\sigma\), nul à l'extérieur. 3) \(U=V_1-V_2=\int_1^2\vec E\cdot\mathrm{d}\vec\ell\) le long d'une ligne de champ. 4) \(C=\frac{Q}{U}\) : <b>\(Q\) doit se simplifier</b>. S'il reste, c'est qu'il y a une erreur.</p></div>
{{FIG:superpo}}
<p>Superposition de deux plans : chaque plan crée \(\frac{\sigma}{2\varepsilon_0}\) de chaque côté. Entre les plans les deux champs sont <b>dans le même sens</b> (le plan \(+\sigma\) repousse, le plan \(-\sigma\) attire) et s'ajoutent ; à l'extérieur ils sont opposés et s'annulent. Voilà pourquoi tout le champ est enfermé entre les armatures : \(E=\frac{\sigma}{\varepsilon_0}\).</p>

<h4>Énergie stockée</h4>
<p>Pourquoi \(\frac12\) dans \(W=\frac12QU\) ? Parce qu'on charge progressivement : quand la charge déjà transférée est \(q\), la tension vaut \(\frac qC\), et amener \(\mathrm{d}q\) de plus coûte \(\frac qC\mathrm{d}q\). Au total \(W=\int_0^Q\frac{q}{C}\mathrm{d}q=\frac{Q^2}{2C}=\frac12CU^2=\frac12QU\). Cette énergie est dans le <b>champ</b> : pour le condensateur plan, \(W=\frac12\varepsilon_0E^2\times(Se)\), soit une densité d'énergie \(\frac12\varepsilon_0E^2\) dans le volume entre les armatures.</p>
<div class="box warn"><div class="bt">⚠ Charge constante ou tension constante ?</div><p>Condensateur <b>isolé</b> : \(Q\) est fixée. On écarte les armatures : \(C\) diminue, \(U=\frac QC\) et \(W=\frac{Q^2}{2C}\) augmentent (c'est l'opérateur qui fournit l'énergie), et le champ \(\frac{\sigma}{\varepsilon_0}\) <i>ne change pas</i>. Condensateur <b>branché</b> sur un générateur : c'est \(U\) qui est fixée, \(Q\) et \(E=\frac Ue\) diminuent. Dis toujours quelle grandeur est imposée avant de calculer.</p></div>

<h3 id="cp3-ex">Exemple guidé avec le TD</h3>
<div class="cp-td">
<p class="s4-small">TD4, exercice 2 (corrigé complet : <a href="corriges.html#td4-2">corriges.html#td4-2</a>)</p>
<div class="cp-enonce"><span class="cp-lab">Énoncé</span>Deux armatures métalliques parallèles à l'équilibre, de même surface \(S\) très grande devant l'épaisseur \(e\), chargées uniformément, dans le vide. Champ d'un plan infini chargé (calculé), champ du condensateur partout, circulation entre les armatures, tension \(U=V_1-V_2\), capacité en fonction de \(S\) et \(e\).</div>
<div class="cp-q"><span class="cp-lab">Ce qu'on cherche</span><p>La capacité \(C=Q/U\) : il faut donc \(Q\) et \(U\) en fonction de la géométrie. Valeurs réalistes : \(S=100\ \mathrm{cm^2}=10^{-2}\ \mathrm{m^2}\), \(e=1\ \mathrm{mm}\), \(U=100\ \mathrm V\).</p></div>
<div class="cp-q"><span class="cp-lab">Quel outil, et pourquoi</span><p>On connaît (ou on calcule par Gauss) le champ d'un <b>plan infini</b>. Le condensateur est deux plans de charges opposées : on <b>superpose</b>. On intègre ensuite le champ le long d'une ligne de champ pour avoir \(U\) (on va de \(\vec E\) à une tension), puis \(C=Q/U\).</p></div>
{{FIG:cond_ex}}
<ol class="steps">
<li class="step"><span class="sn"></span><div><div class="st">Repère et charges</div><div class="sd">
<p>Axe \(Oz\) perpendiculaire aux armatures : armature 1 (\(+Q\), densité \(+\sigma\)) en \(z=0\), armature 2 (\(-Q\), \(-\sigma\)) en \(z=e\). Les charges sont sur les faces en regard (influence totale) et \(Q=\sigma S\).</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Champ d'un plan infini par Gauss</div><div class="sd">
<p>Symétries : \(\vec E=E(z)\vec e_z\), impair en \(z\). Gauss avec un cylindre de base \(S_0\), d'axe \(Oz\), à cheval sur le plan : flux \(2S_0E\) (deux bases, rien sur la face latérale), charge intérieure \(\sigma S_0\) :</p>
<div class="mq">\[2S_0E=\frac{\sigma S_0}{\varepsilon_0}\ \Longrightarrow\ \vec E=\pm\frac{\sigma}{2\varepsilon_0}\vec e_z\quad(+\text{ pour }z\gt0)\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Superposition des deux plans</div><div class="sd">
<div class="mq">\[\begin{gathered}z\lt0:\ \ -\frac{\sigma}{2\varepsilon_0}+\frac{\sigma}{2\varepsilon_0}=0\\[4pt] 0\lt z\lt e:\ \ \frac{\sigma}{2\varepsilon_0}+\frac{\sigma}{2\varepsilon_0}=\frac{\sigma}{\varepsilon_0}\\[4pt] z\gt e:\ \ \frac{\sigma}{2\varepsilon_0}-\frac{\sigma}{2\varepsilon_0}=0\end{gathered}\]</div>
<p>Le champ est <b>uniforme</b> entre les armatures, nul dehors : \(\vec E=\dfrac{\sigma}{\varepsilon_0}\vec e_z\) pour \(0\lt z\lt e\).</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Tension : la circulation de \(0\) à \(e\)</div><div class="sd">
<p>On choisit le chemin le plus simple : le segment de droite le long d'une ligne de champ, \(\mathrm{d}\vec\ell=\mathrm{d}z\,\vec e_z\) (le résultat ne dépend pas du chemin, c'est un champ conservatif).</p>
<div class="mq">\[U=V_1-V_2=\int_0^e\frac{\sigma}{\varepsilon_0}\mathrm{d}z=\frac{\sigma e}{\varepsilon_0}=\frac{Qe}{\varepsilon_0S}\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Capacité</div><div class="sd">
<div class="mq">\[C=\frac QU=\frac{\sigma S}{\sigma e/\varepsilon_0}=\frac{\varepsilon_0S}{e}\]</div>
<p>\(\sigma\) (donc \(Q\)) s'est simplifié : la capacité ne dépend que de la géométrie ✓.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Application numérique</div><div class="sd">
<div class="mq">\[C=\frac{8{,}85\times10^{-12}\times10^{-2}}{10^{-3}}\approx8{,}85\times10^{-11}\ \mathrm F=88{,}5\ \mathrm{pF}\]</div>
<p>Avec \(U=100\ \mathrm V\) : \(Q=CU\approx8{,}85\ \mathrm{nC}\), \(\sigma=\frac QS\approx8{,}85\times10^{-7}\ \mathrm{C\cdot m^{-2}}\), \(E=\frac{\sigma}{\varepsilon_0}=\frac Ue=10^5\ \mathrm{V\cdot m^{-1}}\) (ce sont bien les deux expressions de \(E\) qui coïncident), énergie \(\frac12CU^2\approx4{,}4\times10^{-7}\ \mathrm J\) (identique à \(\frac12\varepsilon_0E^2\times Se\)). Ordres de grandeur : \(E\) vaut 3 % du champ de claquage de l'air (\(\approx3\times10^6\ \mathrm{V\cdot m^{-1}}\)) ; et pour fabriquer <b>1 farad</b> avec \(e=1\ \mathrm{mm}\), il faudrait \(S=\frac{Ce}{\varepsilon_0}\approx1{,}1\times10^8\ \mathrm{m^2}\), soit un carré de plus de 10 km de côté : le farad est une unité immense.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Vérifications</div><div class="sd">
<p><b>Unités :</b> \(\mathrm{F\cdot m^{-1}}\cdot\frac{\mathrm m^2}{\mathrm m}=\mathrm F\) ✓. <b>Tendances :</b> \(C\propto S\) (plus de place) et \(C\propto\frac1e\) (si \(e\to0\), \(U\to0\) pour la même charge) ✓. <b>Hypothèse :</b> \(\sqrt S=10\ \mathrm{cm}\gg e=1\ \mathrm{mm}\) : on peut négliger les effets de bord, la formule du plan infini est valable. <b>Piège évité :</b> le champ est \(\frac{\sigma}{\varepsilon_0}\) et non \(\frac{\sigma}{2\varepsilon_0}\) car il vient de la <i>somme</i> des deux plans.</p></div></div></li>
</ol>
<div class="cp-ret"><span class="cp-lab">À retenir</span><ul>
<li>Capacité en 4 temps : champ en fonction de \(Q\), tension par circulation, \(C=Q/U\), vérifier que \(Q\) a disparu.</li>
<li>Plan : \(E=\frac{\sigma}{\varepsilon_0}\) entre les armatures (somme de deux plans), \(C=\frac{\varepsilon_0S}{e}\), \(W=\frac12CU^2=\frac12\varepsilon_0E^2\,Se\).</li>
<li>Toujours préciser : \(Q\) constante (isolé) ou \(U\) constante (branché).</li>
</ul>
<a class="cp-link" href="corriges.html#td4-2">→ Voir le corrigé complet du TD4 ex. 2</a></div>
</div>

<h3 id="cp3-test">Test de compréhension</h3>
<details class="s4-qa"><summary>1. Pourquoi le champ est-il nul à l'intérieur d'un conducteur à l'équilibre, et que peut-on en déduire sur les charges ?</summary><div class="s4-ans">S'il y avait un champ dans le métal, il mettrait les charges libres en mouvement : ce ne serait pas un équilibre. Donc \(\vec E_{int}=\vec0\), le potentiel y est constant, et par Gauss toute surface fermée à l'intérieur a un flux nul donc ne contient aucune charge : les charges en excès sont uniquement sur la surface.</div></details>
<details class="s4-qa"><summary>2. Un condensateur plan isolé (charge \(Q\) fixée) voit son écartement doubler. Que deviennent \(C\), \(U\), \(E\) et l'énergie ?</summary><div class="s4-ans">\(C=\frac{\varepsilon_0S}{e}\) est divisée par 2. \(U=\frac QC\) est multipliée par 2. \(E=\frac{\sigma}{\varepsilon_0}=\frac{Q}{\varepsilon_0S}\) ne change pas (ni \(Q\) ni \(S\) n'ont bougé). L'énergie \(\frac{Q^2}{2C}\) est multipliée par 2 : le surcroît vient du travail fourni par l'opérateur pour écarter les armatures qui s'attirent. (Si le condensateur était resté branché à \(U\), ce serait \(C\), \(Q\), \(E\) et \(W\) divisés par 2.)</div></details>
<details class="s4-qa"><summary>3. Pourquoi les paratonnerres sont-ils des pointes ?</summary><div class="s4-ans">Un conducteur est à un potentiel uniforme, et le potentiel local est de l'ordre de \(\frac{\sigma R}{\varepsilon_0}\) avec \(R\) le rayon de courbure : à \(V\) fixé, \(\sigma\propto\frac1R\). Une pointe (très petit \(R\)) concentre donc une très grande densité de charge, et le champ juste à l'extérieur \(E=\frac{\sigma}{\varepsilon_0}\) y est très intense : c'est là que l'air s'ionise en premier, ce qui permet de canaliser la décharge.</div></details>
<a class="cp-back" href="#haut">↑ Retour au sommaire</a>
</div>
</article>
'''
