A = r'''<!-- ============ CH 4 ============ -->
<article class="chapter cp-chap" id="cp4">
<div class="chapter-hd">
<span class="cn">CH 4</span>
<h2>Champ magnétique (début du chapitre)</h2>
</div>
<div class="prose">
<div class="cp-idea"><span class="cp-k">L'idée en une phrase</span><p>Les charges <i>en mouvement</i> (les courants) créent un champ magnétique \(\vec B\) qui tourne autour d'elles, et ce champ n'agit que sur les charges <i>en mouvement</i> ; le chapitre se construit comme l'électrostatique, mais avec un produit vectoriel qui retourne presque tous les raisonnements de symétrie.</p></div>

<h3 id="cp4-comp">Pour comprendre</h3>

<h4>Ce qui ressemble à l'électrostatique, et ce qui change</h4>
<p>Tu connais déjà la méthode : une source crée un champ, on l'obtient en additionnant les contributions de petits morceaux, on gagne du temps avec les symétries et les invariances. Ici, tout est pareil dans l'esprit, mais avec trois grandes différences à garder en tête dès le début :</p>
<div class="tbl-wrap"><table>
<thead><tr><th></th><th>Électrostatique (\(\vec E\))</th><th>Magnétostatique (\(\vec B\))</th></tr></thead>
<tbody>
<tr><td>Sources</td><td>charges \(q\), \(\lambda\), \(\sigma\), \(\rho\)</td><td>courants \(I\), de densité \(\vec j=\rho_d\vec v\)</td></tr>
<tr><td>Élément source</td><td>\(\mathrm{d}q\) (scalaire)</td><td>\(I\,\mathrm{d}\vec\ell\) (vecteur, sens du courant)</td></tr>
<tr><td>Loi élémentaire</td><td>\(\mathrm{d}\vec E=\dfrac{\mathrm{d}q}{4\pi\varepsilon_0}\dfrac{\overrightarrow{PM}}{PM^3}\)</td><td>\(\mathrm{d}\vec B=\dfrac{\mu_0I}{4\pi}\dfrac{\mathrm{d}\vec\ell\wedge\overrightarrow{PM}}{PM^3}\)</td></tr>
<tr><td>Direction du champ</td><td>le long de \(\overrightarrow{PM}\) (radiale)</td><td><b>perpendiculaire</b> à \(\mathrm{d}\vec\ell\) et à \(\overrightarrow{PM}\) (produit vectoriel)</td></tr>
<tr><td>Lignes de champ</td><td>partent des \(+\), arrivent sur les \(-\)</td><td><b>se referment</b> autour des courants</td></tr>
<tr><td>Nature</td><td>vrai vecteur</td><td><b>pseudo-vecteur</b></td></tr>
<tr><td>Plan de symétrie des sources</td><td>\(\vec E\) <i>dans</i> le plan</td><td>\(\vec B\) <i>perpendiculaire</i> au plan</td></tr>
<tr><td>Plan d'antisymétrie</td><td>\(\vec E\) perpendiculaire au plan</td><td>\(\vec B\) <i>dans</i> le plan</td></tr>
<tr><td>Isoler un morceau de source ?</td><td>oui (une charge isolée existe)</td><td>non (un morceau de circuit n'existe pas seul : \(\mathrm{d}\vec B\) est un artifice de calcul)</td></tr>
</tbody></table></div>
<p>Ce chapitre ne traite que des champs <b>magnétostatiques</b> : créés par des courants qui ne dépendent pas du temps.</p>

<h4>Aimants, boussole, champ terrestre : comment « voir » un champ</h4>
<p>Un aimant a toujours deux pôles (nord et sud) : deux pôles de même nature se repoussent, de natures différentes s'attirent. Mais le plus important est ceci : <b>l'aimant modifie les propriétés de l'espace autour de lui</b>. On le détecte avec une boussole, qui s'oriente dans une direction, avec un sens (de son sud vers son nord) : c'est exactement la définition d'un champ de vecteurs. Si on écarte l'aiguille, elle oscille autour de cette direction, d'autant plus vite que le champ est intense. La limaille de fer saupoudrée autour d'un aimant s'aimante et se transforme en milliers de petites boussoles : elle dessine les <b>lignes de champ</b> (le « spectre magnétique »). Sans aimant, la boussole s'oriente quand même vers le nord : la Terre elle-même crée un champ magnétique, de l'ordre de \(4{,}7\times10^{-5}\ \mathrm T\).</p>
<div class="tbl-wrap"><table>
<thead><tr><th>Ordre de grandeur de \(B\)</th><th>Valeur</th></tr></thead>
<tbody>
<tr><td>champ magnétique terrestre</td><td>\(4{,}7\times10^{-5}\ \mathrm T\) (47 \(\mu\)T)</td></tr>
<tr><td>aimant permanent</td><td>\(0{,}1\ \mathrm T\)</td></tr>
<tr><td>électroaimant</td><td>\(10\ \mathrm T\)</td></tr>
</tbody></table></div>

<h4>La force de Lorentz : comment on <i>définit</i> et on mesure \(\vec B\)</h4>
<p>Une charge \(q\) qui se déplace à la vitesse \(\vec v\) dans un champ électrique \(\vec E\) et un champ magnétique \(\vec B\) subit :</p>
<div class="mq">\[\vec f=q\,\vec E+q\,\vec v\wedge\vec B\]</div>
<p>Le premier terme est la force électrique que tu connais déjà. Le second est la force magnétique, et elle a trois caractéristiques surprenantes :</p>
<ul>
<li>elle est nulle si la charge est <b>immobile</b> (\(\vec v=\vec0\)) ou si \(\vec v\parallel\vec B\) : le champ magnétique n'agit que sur des charges <i>en mouvement</i> ;</li>
<li>elle est <b>perpendiculaire à la fois à \(\vec v\) et à \(\vec B\)</b> (produit vectoriel), et non dans la direction de \(\vec B\) comme on pourrait s'y attendre ;</li>
<li>comme elle est toujours perpendiculaire à \(\vec v\), sa puissance \(\vec f_m\cdot\vec v\) est nulle : <b>elle ne travaille pas</b> et ne change jamais la norme de la vitesse, seulement sa direction.</li>
</ul>
<p><b>Unité du tesla.</b> De \(f_m=|q|\,v\,B\) (si \(\vec v\perp\vec B\)) : \([B]=\dfrac{\mathrm N}{\mathrm C\cdot\mathrm{m\cdot s^{-1}}}=\dfrac{\mathrm N}{\mathrm{A\cdot m}}=\mathrm{kg\cdot A^{-1}\cdot s^{-2}}\). Voilà pourquoi le courant électrique est la clé du chapitre : l'ampère est dans l'unité de \(B\). 1 tesla (T) est le nom de cette unité.</p>

<h4>Mouvement d'une particule chargée : pourquoi un cercle, et de quel rayon</h4>
{{FIG:lorentz}}
<p>Cas simple : champ \(\vec B\) uniforme, vitesse initiale perpendiculaire à \(\vec B\). La force est perpendiculaire à \(\vec v\) donc \(|\vec v|\) est constante ; la force est donc de norme constante \(|q|vB\), toujours perpendiculaire à la trajectoire et dirigée vers le même côté : c'est exactement la situation d'une masse au bout d'un fil (force centripète). La trajectoire est un <b>cercle</b>. On écrit la deuxième loi de Newton avec l'accélération centripète \(\frac{v^2}{r}\) :</p>
<div class="mq">\[m\frac{v^2}{r}=|q|\,v\,B\ \Longrightarrow\ \boxed{\,r=\frac{m\,v}{|q|\,B}\,}\qquad\omega_c=\frac vr=\frac{|q|B}{m}\qquad T=\frac{2\pi m}{|q|B}\]</div>
<p>Lecture : une particule plus lourde ou plus rapide a plus d'inertie, donc elle tourne sur un plus grand cercle ; un champ plus fort ou une charge plus grande courbe davantage, donc un plus petit cercle. Remarque capitale : la <b>période</b> \(T\) ne dépend pas de la vitesse, c'est le principe du cyclotron. Si \(q\gt0\) et \(\vec B\) sort de la feuille, la rotation est horaire ; pour \(q\lt0\) elle est antihoraire. Dans le cas général, la trajectoire est une hélice (cercle + dérive uniforme le long de \(\vec B\)).</p>
<div class="cp-an"><span class="cp-lab">Exemple numérique : électron et proton</span>
<p><b>Un électron accéléré par 100 V</b> (chapitre 2 : \(v=\sqrt{2eU/m_e}\approx5{,}9\times10^6\ \mathrm{m\cdot s^{-1}}\)) entre dans un champ \(B=1\ \mathrm{mT}\) perpendiculaire à sa vitesse :</p>
<div class="mq">\[r=\frac{m_ev}{eB}=\frac{9{,}1\times10^{-31}\times5{,}9\times10^{6}}{1{,}6\times10^{-19}\times10^{-3}}\approx3{,}4\times10^{-2}\ \mathrm m=3{,}4\ \mathrm{cm}\]</div>
<p>Dans le seul champ terrestre (\(4{,}7\times10^{-5}\ \mathrm T\)), le même électron décrirait un cercle de rayon \(\approx72\ \mathrm{cm}\) : sur 30 cm de parcours, un faisceau de ce type est dévié d'environ 6 cm par le seul champ terrestre (c'est pourquoi on blinde les tubes cathodiques). <b>Un proton</b> dans \(B=1\ \mathrm T\), à \(v=10^6\ \mathrm{m\cdot s^{-1}}\) : \(r=\frac{m_pv}{eB}\approx1{,}0\ \mathrm{cm}\), et la fréquence de rotation \(\frac{eB}{2\pi m_p}\approx15\ \mathrm{MHz}\) est la même quelle que soit la vitesse : c'est ce qui permet au cyclotron d'accélérer les particules avec une tension alternative de fréquence fixe.</p></div>
<p>Applications : le cyclotron (accélérateur dont les « dees » baignent dans un champ magnétique uniforme) et le spectromètre de masse (des ions de même vitesse, mais de masses différentes, décrivent des cercles de rayons différents : on lit la masse sur le rayon).</p>
'''
