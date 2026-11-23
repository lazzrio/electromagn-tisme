TOC = [('cp0-comp', 'Pour comprendre'), ('cp0-ex', 'Exemple guidé (TD0)'), ('cp0-test', 'Test de compréhension')]

CH = r'''<!-- ============ CH 0 ============ -->
<article class="chapter cp-chap" id="cp0">
<div class="chapter-hd">
<span class="cn">CH 0</span>
<h2>Outils mathématiques</h2>
</div>
<div class="prose">
<div class="cp-idea"><span class="cp-k">L'idée en une phrase</span><p>Presque tout le cours se résume à « découper en petits morceaux, multiplier par une densité ou un champ, puis sommer » : ce chapitre t'apprend à écrire proprement les petits morceaux (\(\mathrm{d}\ell\), \(\mathrm{d}S\), \(\mathrm{d}\tau\)) et les deux façons de sommer un champ (flux et circulation).</p></div>

<h3 id="cp0-comp">Pour comprendre</h3>

<h4>Pourquoi trois repères ?</h4>
<p>Pour donner l'adresse d'un point, on peut dire « 3 rues à l'est, 2 au nord » (cartésien) ou « à 3,6 rues de la gare, dans la direction nord-est » (polaire). Les deux disent la même chose ; le second est bien plus naturel si tout ce qui t'intéresse est <b>autour de la gare</b>. En physique, c'est pareil : on choisit le repère qui épouse la <b>forme de l'objet</b>, de sorte que les bornes des intégrales soient des constantes et que les expressions restent simples.</p>
<ul>
<li>pavé, plan, plaque : <b>cartésien</b> \((x,y,z)\) ;</li>
<li>fil, cylindre, disque : <b>cylindrique</b> \((r,\theta,z)\), \(r\) est la distance à l'axe ;</li>
<li>boule, coquille : <b>sphérique</b> \((r,\theta,\varphi)\), \(r\) est la distance au centre.</li>
</ul>

<h4>Le petit morceau : d'où sortent \(\mathrm{d}\ell\), \(\mathrm{d}S\), \(\mathrm{d}\tau\)</h4>
<p>Imagine que tu découpes un objet en minuscules « briques » en faisant varier chaque coordonnée d'un tout petit peu. La brique est presque un pavé droit, et il suffit de trouver <b>la longueur de chacun de ses côtés</b>. Le piège : une coordonnée qui n'est pas une longueur (un angle) ne donne pas directement un côté.</p>
<div class="mq">\[\text{côté} \;=\; \text{(de combien on bouge)}\ \times\ \text{(rayon du cercle qu'on parcourt)}\]</div>
<p>C'est tout simplement la définition de l'angle en radians : un arc vaut <b>rayon × angle</b>. Voilà pourquoi \(\mathrm{d}\theta\) (sans dimension) devient une longueur \(r\,\mathrm{d}\theta\) (en mètres) et pourquoi les facteurs \(r\) et \(r\sin\theta\) apparaissent.</p>
{{FIG:cyl}}
<p>En <b>cylindrique</b>, les trois côtés de la brique sont \(\mathrm{d}r\), \(r\,\mathrm{d}\theta\), \(\mathrm{d}z\), d'où \(\mathrm{d}\tau=r\,\mathrm{d}r\,\mathrm{d}\theta\,\mathrm{d}z\). Sur la figure, les deux cellules ont le même \(\mathrm{d}\theta\) mais celle qui est loin de l'axe est plus large : c'est exactement ce que dit le facteur \(r\).</p>
{{FIG:sph}}
<p>En <b>sphérique</b>, deux angles. Quand \(\theta\) varie, M suit un grand cercle de rayon \(r\) : côté \(r\,\mathrm{d}\theta\). Quand \(\varphi\) varie, M tourne autour de l'axe \(Oz\), sur un cercle de rayon \(r\sin\theta\) (sa distance à l'axe, pas \(r\)) : côté \(r\sin\theta\,\mathrm{d}\varphi\). Donc :</p>
<div class="mq">\[\mathrm{d}\vec\ell=\mathrm{d}r\,\vec e_r+r\,\mathrm{d}\theta\,\vec e_\theta+r\sin\theta\,\mathrm{d}\varphi\,\vec e_\varphi\qquad\mathrm{d}\tau=r^2\sin\theta\,\mathrm{d}r\,\mathrm{d}\theta\,\mathrm{d}\varphi\]</div>
<p>Contrôle express : intègre \(\mathrm{d}\tau\) sur une boule de rayon \(R\) et tu dois retrouver \(\frac43\pi R^3\). Pour la surface d'une sphère (\(r=R\) fixé, on garde les deux côtés \(R\,\mathrm{d}\theta\) et \(R\sin\theta\,\mathrm{d}\varphi\)) : \(\int_0^\pi\sin\theta\,\mathrm{d}\theta\int_0^{2\pi}R^2\mathrm{d}\varphi=2\times2\pi R^2=4\pi R^2\).</p>
<div class="box warn"><div class="bt">⚠ Erreurs typiques</div><p>Oublier le facteur \(r\) (ou \(r^2\sin\theta\)) dans \(\mathrm{d}\tau\) ; confondre le \(\theta\) cylindrique (angle dans le plan \(xOy\), de \(0\) à \(2\pi\)) avec le \(\theta\) sphérique (angle depuis l'axe \(Oz\), de \(0\) à \(\pi\)) ; croire que \(\overrightarrow{OM}\) a une composante sur \(\vec e_\theta\) (il n'en a jamais : \(\overrightarrow{OM}=r\vec e_r+z\vec e_z\) en cylindrique, \(r\vec e_r\) en sphérique).</p></div>

<h4>Le gradient : la « pente » d'un champ scalaire</h4>
<p>Pense à une carte topographique : les courbes de niveau relient les points de même altitude. À chaque endroit, le <b>gradient</b> est la flèche qui indique <b>dans quelle direction ça monte le plus vite</b>, et sa longueur dit à quel point c'est raide. Conséquences immédiates :</p>
{{FIG:grad}}
<ul>
<li>le gradient est <b>perpendiculaire</b> aux courbes (surfaces) de niveau : en les suivant, la valeur ne change pas ;</li>
<li>il pointe vers les valeurs <b>croissantes</b> ;</li>
<li>unité : celle du champ divisée par un mètre (pour \(V\) en volts : \(\mathrm{V\cdot m^{-1}}\), c'est bien l'unité d'un champ électrique).</li>
</ul>
<p>D'où viennent les \(\frac1r\) dans les autres repères ? Le gradient est défini par : « si je me déplace de \(\mathrm{d}\vec\ell\), la valeur change de \(\mathrm{d}f=\overrightarrow{\mathrm{grad}}f\cdot\mathrm{d}\vec\ell\) ». Dans la direction \(\vec e_\theta\), le déplacement réel est \(r\,\mathrm{d}\theta\) (et pas \(\mathrm{d}\theta\)), donc la composante du gradient est la variation \(\frac{\partial f}{\partial\theta}\mathrm{d}\theta\) divisée par \(r\,\mathrm{d}\theta\) :</p>
<div class="mq">\[(\overrightarrow{\mathrm{grad}}f)_\theta=\frac{1}{r}\frac{\partial f}{\partial\theta}\qquad(\overrightarrow{\mathrm{grad}}f)_\varphi=\frac{1}{r\sin\theta}\frac{\partial f}{\partial\varphi}\]</div>
<p>Un exemple qui servira partout : \(V(r)=k/r\) (en sphérique, ne dépend que de \(r\)). Alors \(\overrightarrow{\mathrm{grad}}V=\frac{\mathrm{d}V}{\mathrm{d}r}\vec e_r=-\frac{k}{r^2}\vec e_r\) : le gradient pointe vers le centre (là où \(V\) est le plus grand), et \(-\overrightarrow{\mathrm{grad}}V=\frac{k}{r^2}\vec e_r\) est un champ « en \(1/r^2\) » qui s'éloigne du centre. Tu viens de retrouver la forme du champ de Coulomb à partir du potentiel de Coulomb.</p>

<h4>Le flux : « combien traverse cette surface ? »</h4>
<p>Imagine un champ de vitesses d'eau et un filet tendu : le <b>flux</b> est le débit d'eau qui traverse le filet (en \(\mathrm{m^3\cdot s^{-1}}\) si \(\vec A\) est une vitesse). Une petite maille de surface \(\mathrm{d}S\) laisse passer \(\vec A\cdot\mathrm{d}\vec S\), où \(\mathrm{d}\vec S=\mathrm{d}S\,\vec n\) est un vecteur de norme \(\mathrm{d}S\) <b>perpendiculaire</b> à la maille.</p>
<div class="mq">\[\mathrm{d}\Phi=\vec A\cdot\mathrm{d}\vec S=A\,\mathrm{d}S\cos\alpha\qquad\Phi=\iint_\Sigma\vec A\cdot\mathrm{d}\vec S\]</div>
<ul>
<li>\(\alpha=0\) (le courant arrive de face) : le débit est maximal ; \(\alpha=90^\circ\) (le courant glisse le long du filet) : rien ne passe ;</li>
<li>le <b>signe</b> dépend du sens choisi pour \(\vec n\) : pour une surface fermée, on prend toujours la normale <b>sortante</b>. Flux positif = ça sort plus que ça n'entre ;</li>
<li>le flux est un <b>scalaire</b> : on calcule d'abord \(\vec A\cdot\mathrm{d}\vec S\) face par face, puis on intègre.</li>
</ul>
<p>Le plus gros gain de temps en pratique : sur beaucoup de faces, \(\vec A\) est <b>soit parallèle soit perpendiculaire</b> à \(\mathrm{d}\vec S\), et \(A\) est constant sur la face. L'intégrale devient alors « valeur du champ × aire » ou bien simplement zéro.</p>

<h4>La circulation : « le champ pousse-t-il dans le sens de ma balade ? »</h4>
<p>C'est l'analogue du travail d'une force : tu te promènes le long d'une courbe, et à chaque pas tu comptes la part du champ qui est dans le sens du pas, \(\mathrm{d}C=\vec A\cdot\mathrm{d}\vec\ell\) (vent dans le dos : positif ; vent de face : négatif).</p>
<div class="mq">\[C_{M_1\to M_2}=\int_{M_1}^{M_2}\vec A\cdot\mathrm{d}\vec\ell\qquad C=\oint_\Gamma\vec A\cdot\mathrm{d}\vec\ell\ \ (\text{contour fermé})\]</div>
<p>Sur un cercle d'axe \(Oz\) et de rayon \(R\), parcouru dans le sens trigonométrique, \(\mathrm{d}\vec\ell=R\,\mathrm{d}\theta\,\vec e_\theta\) : <b>seule la composante \(A_\theta\)</b> compte. Par exemple pour \(\vec A=B_0\,r\,\vec e_\theta\), \(C=\int_0^{2\pi}B_0R\cdot R\,\mathrm{d}\theta=2\pi B_0R^2\) (sur un demi-cercle, la moitié).</p>
<p>Deux comportements très différents à bien distinguer :</p>
<ul>
<li>si \(\vec A=\overrightarrow{\mathrm{grad}}F\), la circulation entre deux points vaut \(F(B)-F(A)\) : elle ne dépend pas du chemin et elle est nulle sur un contour fermé (comme le travail du poids). C'est le cas du champ électrostatique ;</li>
<li>si ce n'est pas un gradient, une boucle peut rapporter quelque chose. Exemple : \(\vec A=\dfrac{1}{r}\vec e_\theta\) a une circulation égale à \(2\pi\) sur <b>tout</b> cercle autour de l'axe. Garde cette idée en tête : le champ magnétique d'un fil (Ch4) est exactement de cette forme.</li>
</ul>

<div class="box method"><div class="bt">▹ Le réflexe pour tout calcul d'intégrale</div><p>1) Dessiner. 2) Choisir le repère selon la symétrie de l'objet. 3) Écrire le petit morceau (\(\mathrm{d}\ell\), \(\mathrm{d}S\) ou \(\mathrm{d}\tau\)) avec <i>tous</i> ses facteurs. 4) Lire les bornes sur le dessin. 5) Séparer les variables. 6) Contrôler : unité, signe, cas particulier connu.</p></div>

<h3 id="cp0-ex">Exemple guidé avec le TD</h3>
<div class="cp-td">
<p class="s4-small">TD0, exercice 3 A (corrigé complet : <a href="corriges.html#td0-3a">corriges.html#td0-3a</a>)</p>
<div class="cp-enonce"><span class="cp-lab">Énoncé (partie 1)</span>Cylindre d'axe \(Oz\), de rayon \(a\) et de hauteur \(h\), et le champ \(\vec A=A_0\,r\,\vec e_r\). Calculer le flux de \(\vec A\) à travers chaque face, puis le flux sortant total.</div>
<div class="cp-q"><span class="cp-lab">Ce qu'on cherche</span><p>Un flux à travers une surface <b>fermée</b> : normale sortante. Pour donner du sens, imagine que \(\vec A\) est une vitesse d'écoulement (en \(\mathrm{m\cdot s^{-1}}\)), qui s'écarte de l'axe en accélérant : \(A_0\) est alors en \(\mathrm{s^{-1}}\) et le flux sera un débit en \(\mathrm{m^3\cdot s^{-1}}\). Valeurs réalistes : \(A_0=2\ \mathrm{s^{-1}}\), \(a=10\ \mathrm{cm}\), \(h=50\ \mathrm{cm}\).</p></div>
<div class="cp-q"><span class="cp-lab">Quel outil, et pourquoi</span><p>La définition du flux, en coordonnées <b>cylindriques</b> (l'objet est un cylindre : les bornes seront des constantes). La surface fermée a trois morceaux (latérale, haut, bas) : on calcule un flux par morceau.</p></div>
{{FIG:flux_cyl}}
<ol class="steps">
<li class="step"><span class="sn"></span><div><div class="st">Face latérale : \(r=a\), \(\mathrm{d}\vec S=a\,\mathrm{d}\theta\,\mathrm{d}z\ \vec e_r\)</div><div class="sd">
<p><i>Pourquoi cette expression ?</i> On fait varier \(\theta\) et \(z\) en restant à \(r=a\) : les côtés sont \(a\,\mathrm{d}\theta\) et \(\mathrm{d}z\), la normale sortante est \(\vec e_r\). Sur cette face, \(r\) vaut \(a\) <i>partout</i> : \(\vec A=A_0a\,\vec e_r\) est constant et parallèle à \(\mathrm{d}\vec S\).</p>
<div class="mq">\[\Phi_{lat}=\int_0^{2\pi}\!\!\int_0^h A_0a\cdot a\,\mathrm{d}z\,\mathrm{d}\theta=A_0a^2\cdot 2\pi h=2\pi A_0\,a^2h\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Faces haute et basse : \(\mathrm{d}\vec S=\pm\,r\,\mathrm{d}r\,\mathrm{d}\theta\ \vec e_z\)</div><div class="sd">
<p>La normale est verticale, alors que \(\vec A\) est horizontal (radial) : \(\vec e_r\cdot\vec e_z=0\), donc \(\vec A\cdot\mathrm{d}\vec S=0\) en tout point. Le champ « glisse » le long de ces faces sans les traverser : \(\Phi_{haut}=\Phi_{bas}=0\).</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Total</div><div class="sd">
<div class="mq">\[\Phi=\Phi_{lat}+\Phi_{haut}+\Phi_{bas}=2\pi A_0\,a^2h\]</div></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Application numérique</div><div class="sd">
<div class="mq">\[\Phi=2\pi\times2\times(0{,}10)^2\times0{,}50\approx6{,}3\times10^{-2}\ \mathrm{m^3\cdot s^{-1}}\]</div>
<p>Soit environ 63 litres par seconde. Ordre de grandeur : à la paroi, la vitesse vaut \(A_0a=0{,}2\ \mathrm{m\cdot s^{-1}}\) et l'aire latérale \(2\pi ah\approx0{,}31\ \mathrm{m^2}\). Or \(0{,}2\times0{,}31\approx0{,}063\) : on retrouve la même valeur avec « vitesse × aire », ce qui est exactement ce que fait l'intégrale quand \(\vec A\) est constant et normal à la surface.</p></div></div></li>
<li class="step"><span class="sn"></span><div><div class="st">Vérifications</div><div class="sd">
<p><b>Unités :</b> \(\mathrm{s^{-1}}\times\mathrm{m^3}=\mathrm{m^3\cdot s^{-1}}\), un débit. <b>Dépendances :</b> doubler \(a\) multiplie le flux par 4 (\(a^2\)) ; doubler \(h\) le double (plus de surface) ; si \(h\to0\), \(\Phi\to0\). <b>Second calcul :</b> la divergence de \(\vec A\) en cylindrique est \(\frac1r\frac{\partial(r\cdot A_0r)}{\partial r}=2A_0\), uniforme ; « ce qui sort = divergence × volume » (théorème d'Ostrogradski, vu plus tard) donne \(2A_0\times\pi a^2h=2\pi A_0a^2h\). Même résultat.</p></div></div></li>
</ol>
<div class="cp-an"><span class="cp-lab">Pour t'entraîner (question 2 du même exercice)</span>Sphère de rayon \(R\) et \(\vec A=A_0\,\varphi\,\vec e_r\) : flux de l'extérieur vers l'intérieur. Ici \(\vec A\) est parallèle à \(\mathrm{d}\vec S=R^2\sin\theta\,\mathrm{d}\theta\,\mathrm{d}\varphi\,\vec e_r\) partout, mais sa norme dépend de l'angle \(\varphi\) : on ne peut plus écrire « valeur × aire », il faut intégrer. Le signe \(-\) vient de la normale rentrante. Réponse : \(-4\pi^2A_0R^2\) (détail dans le corrigé).</div>
<div class="cp-ret"><span class="cp-lab">À retenir</span><ul>
<li>Pour un flux : décomposer en faces, écrire \(\mathrm{d}\vec S\) avec sa normale, faire le produit scalaire <b>sur chaque face</b> en remplaçant \(r\) par sa valeur sur cette face.</li>
<li>Champ parallèle à la face \(\Rightarrow\) flux nul ; champ normal et constant \(\Rightarrow\) flux = champ × aire.</li>
<li>Le contrôle « vitesse × aire » et le contrôle des unités prennent 10 secondes et évitent la plupart des erreurs de facteur.</li>
</ul>
<a class="cp-link" href="corriges.html#td0-3a">→ Voir le corrigé complet du TD0 3 A</a></div>
</div>

<h3 id="cp0-test">Test de compréhension</h3>
<details class="s4-qa"><summary>1. Pourquoi l'élément de longueur selon \(\vec e_\theta\) vaut-il \(r\,\mathrm{d}\theta\) et pas \(\mathrm{d}\theta\) ?</summary><div class="s4-ans">Parce que \(\mathrm{d}\theta\) est un angle (sans dimension) et que \(\mathrm{d}\ell\) doit être une longueur. Un arc de cercle vaut rayon \(\times\) angle : à la distance \(r\) de l'axe, tourner de \(\mathrm{d}\theta\) fait avancer de \(r\,\mathrm{d}\theta\). Plus on est loin de l'axe, plus le même angle correspond à une grande distance. C'est aussi pour cela que \((\overrightarrow{\mathrm{grad}}f)_\theta=\frac1r\frac{\partial f}{\partial\theta}\).</div></details>
<details class="s4-qa"><summary>2. Au point P, \(\overrightarrow{\mathrm{grad}}V\) est-il tangent ou perpendiculaire à la surface équipotentielle ? Et le champ \(\vec E=-\overrightarrow{\mathrm{grad}}V\) ?</summary><div class="s4-ans">Perpendiculaire : le long de la surface, \(V\) ne change pas, donc \(\overrightarrow{\mathrm{grad}}V\cdot\mathrm{d}\vec\ell=\mathrm{d}V=0\) pour tout déplacement \(\mathrm{d}\vec\ell\) tangent. Le gradient pointe vers les \(V\) croissants, et \(\vec E\), qui est son opposé, est lui aussi perpendiculaire aux équipotentielles mais pointe vers les \(V\) décroissants.</div></details>
<details class="s4-qa"><summary>3. Quel est le flux du champ uniforme \(\vec A=A_0\,\vec e_z\) à travers une sphère fermée de rayon \(R\) ?</summary><div class="s4-ans">Zéro. Sur l'hémisphère nord \(\vec A\cdot\mathrm{d}\vec S\gt0\) (le champ sort), sur l'hémisphère sud \(\vec A\cdot\mathrm{d}\vec S\lt0\) (il rentre), et les deux se compensent : \(\int_0^\pi A_0\cos\theta\,R^2\sin\theta\,\mathrm{d}\theta\int_0^{2\pi}\mathrm{d}\varphi=0\) car \(\int_0^\pi\cos\theta\sin\theta\,\mathrm{d}\theta=0\). Tout ce qui entre ressort : un champ sans source à l'intérieur a un flux sortant nul.</div></details>
<a class="cp-back" href="#haut">↑ Retour au sommaire</a>
</div>
</article>
'''
