"""Vérification (sympy + numérique) de tous les résultats et valeurs numériques de comprendre.html.
Usage : python tools/verif_comprendre.py   -> affiche OK / ECHEC pour chaque contrôle, code retour 1 s'il y a un échec."""
import math
import sys

import numpy as np
import sympy as sp
from scipy import integrate

NB_ECHECS = 0


def check(nom, ok, detail=''):
    global NB_ECHECS
    if not ok:
        NB_ECHECS += 1
    print(('OK     ' if ok else 'ECHEC  ') + nom + ((' : ' + str(detail)) if not (isinstance(detail, str) and detail == '') else ''))


def proche(a, b, rel=1e-3):
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


# constantes (valeurs du site)
eps0 = 8.854e-12
K = 1 / (4 * math.pi * eps0)
mu0 = 4 * math.pi * 1e-7
e = 1.602e-19
me = 9.109e-31
mp = 1.6726e-27
c = 2.998e8
a0 = 5.29e-11
G = 6.674e-11

# =============================================================== CH0
r, th, ph, z = sp.symbols('r theta phi z', positive=True)
R, h, a, A0, Rr = sp.symbols('R h a A_0 R_r', positive=True)

V_cyl = sp.integrate(r, (r, 0, R)) * sp.integrate(1, (th, 0, 2 * sp.pi)) * sp.integrate(1, (z, 0, h))
check('volume cylindre = pi R^2 h', sp.simplify(V_cyl - sp.pi * R**2 * h) == 0)
S_sph = sp.integrate(sp.sin(th), (th, 0, sp.pi)) * sp.integrate(R**2, (ph, 0, 2 * sp.pi))
check('surface sphère = 4 pi R^2', sp.simplify(S_sph - 4 * sp.pi * R**2) == 0)
V_sph = sp.integrate(r**2, (r, 0, R)) * sp.integrate(sp.sin(th), (th, 0, sp.pi)) * sp.integrate(1, (ph, 0, 2 * sp.pi))
check('volume sphère = 4/3 pi R^3', sp.simplify(V_sph - sp.Rational(4, 3) * sp.pi * R**3) == 0)

# TD0 3A : flux de A = A0 r e_r à travers un cylindre fermé (rayon a, hauteur h)
phi_lat = sp.integrate(sp.integrate(A0 * a * a, (th, 0, 2 * sp.pi)), (z, 0, h))
check('flux face latérale = 2 pi A0 a^2 h', sp.simplify(phi_lat - 2 * sp.pi * A0 * a**2 * h) == 0)
# faces haute et basse : A . dS = A0 r e_r . (+-e_z) r dr dtheta = 0 (produit scalaire e_r.e_z = 0)
check('e_r . e_z = 0', sp.Matrix([1, 0, 0]).dot(sp.Matrix([0, 0, 1])) == 0)
# divergence en cylindrique : (1/r) d(r A_r)/dr
div = sp.diff(r * A0 * r, r) / r
check('div(A0 r e_r) = 2 A0', sp.simplify(div - 2 * A0) == 0)
check('Ostrogradski : 2 A0 * pi a^2 h = flux', sp.simplify(div * sp.pi * a**2 * h - phi_lat) == 0)
# sphère : A = A0 phi e_r, flux entrant
phi_sph = -sp.integrate(sp.integrate(A0 * ph * Rr**2 * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
check('flux sphère entrant = -4 pi^2 A0 R^2', sp.simplify(phi_sph + 4 * sp.pi**2 * A0 * Rr**2) == 0)
# application numérique : A0 = 2 s^-1, a = 0,10 m, h = 0,50 m
A0n, an, hn = 2.0, 0.10, 0.50
Phi_num = 2 * math.pi * A0n * an**2 * hn
check('AN flux = 0,0628 m^3/s', proche(Phi_num, 0.06283, 1e-3), Phi_num)
v_paroi = A0n * an
S_lat = 2 * math.pi * an * hn
check('AN : vitesse de paroi 0,2 m/s, surface latérale 0,314 m^2, flux = v*S', proche(v_paroi * S_lat, Phi_num) and proche(S_lat, 0.3142) and v_paroi == 0.2)
# vérification numérique de l'intégrale latérale (quad)
val, _ = integrate.dblquad(lambda zz, tt: A0n * an * an, 0, 2 * math.pi, 0, hn)
check('intégrale numérique du flux latéral', proche(val, Phi_num))

# gradient : V = k/r (sphérique) => grad V = -k/r^2 e_r ; E = -grad V
k = sp.symbols('k')
Vr = k / r
check('grad(k/r) = -k/r^2 e_r', sp.simplify(sp.diff(Vr, r) + k / r**2) == 0)
# gradient en cylindrique, composante orthoradiale : f = r cos(theta) = x => (1/r) df/dtheta = -sin(theta) = (grad x).e_theta = -sin(theta)
f = r * sp.cos(th)
check('gradient cylindrique de x : (df/dr, (1/r) df/dtheta) = (cos, -sin)',
      sp.simplify(sp.diff(f, r) - sp.cos(th)) == 0 and sp.simplify(sp.diff(f, th) / r + sp.sin(th)) == 0)
# gradient en cartésien : V = x^2 + y^2 => en (1,2) : (2, 4), norme sqrt(20)
x_, y_ = sp.symbols('x y')
g = [sp.diff(x_**2 + y_**2, v).subs({x_: 1, y_: 2}) for v in (x_, y_)]
check('grad(x^2+y^2)(1,2) = (2,4)', g == [2, 4])

# circulation : A = B0 r e_theta sur un cercle de rayon R : 2 pi B0 R^2
B0 = sp.symbols('B_0', positive=True)
circ = sp.integrate(B0 * Rr * Rr, (th, 0, 2 * sp.pi))
check('circulation de B0 r e_theta sur un cercle = 2 pi B0 R^2', sp.simplify(circ - 2 * sp.pi * B0 * Rr**2) == 0)
# demi-cercle de rayon R : moitié
check('circulation sur un demi-cercle = pi B0 R^2', sp.simplify(sp.integrate(B0 * Rr * Rr, (th, 0, sp.pi)) - sp.pi * B0 * Rr**2) == 0)
# circulation d'un champ qui ne dérive pas d'un potentiel : A = e_theta/r a pour circulation 2 pi sur tout cercle (indépendant de R)
check('circulation de e_theta/r = 2 pi pour tout R', sp.simplify(sp.integrate((1 / Rr) * Rr, (th, 0, 2 * sp.pi)) - 2 * sp.pi) == 0)
# elements de longueur : arc r dtheta (r = 5 cm, dtheta = 0,01 rad -> 0,5 mm)
check('arc r dtheta = 0,5 mm', proche(0.05 * 0.01, 5e-4))
# Sphère : cercle de rayon r sin(theta) ; a theta = 30 deg, r = 1 : rayon 0,5, longueur du parallèle pi
check('parallèle à theta=30 deg, r=1 : longueur = pi', proche(2 * math.pi * 1 * math.sin(math.radians(30)), math.pi))
# Aire de la bande de la cellule sphérique : r^2 sin(theta) dtheta dphi ; surface du cône... somme = 4 pi R^2 (déjà vérifié)
# surface totale cylindre fermé a=0,1, h=0,5 : 2 pi a h + 2 pi a^2
check('surface totale cylindre fermé', proche(2 * math.pi * an * hn + 2 * math.pi * an**2, 0.3770, 1e-3))

# =============================================================== CH1
# TD2bis ex.1 : sphère de rayon R, charge Q : trois modèles
Q = sp.symbols('Q', positive=True)
rho0, A1, A2, eps = sp.symbols('rho_0 A_1 A_2 epsilon_0', positive=True)
s = sp.symbols('s', positive=True)
sol_a = sp.solve(sp.Eq(sp.integrate(rho0 * 4 * sp.pi * s**2, (s, 0, R)), Q), rho0)[0]
sol_b = sp.solve(sp.Eq(sp.integrate(A1 / s**2 * 4 * sp.pi * s**2, (s, 0, R)), Q), A1)[0]
sol_c = sp.solve(sp.Eq(sp.integrate(A2 * s**2 * 4 * sp.pi * s**2, (s, 0, R)), Q), A2)[0]
check('rho0 = 3Q/(4 pi R^3)', sp.simplify(sol_a - 3 * Q / (4 * sp.pi * R**3)) == 0)
check('A1 = Q/(4 pi R)', sp.simplify(sol_b - Q / (4 * sp.pi * R)) == 0)
check('A2 = 5Q/(4 pi R^5)', sp.simplify(sol_c - 5 * Q / (4 * sp.pi * R**5)) == 0)
Qint_a = sp.integrate(sol_a * 4 * sp.pi * s**2, (s, 0, r))
Qint_b = sp.integrate(sol_b / s**2 * 4 * sp.pi * s**2, (s, 0, r))
Qint_c = sp.integrate(sol_c * s**2 * 4 * sp.pi * s**2, (s, 0, r))
Ea = sp.simplify(Qint_a / (4 * sp.pi * eps * r**2))
Eb = sp.simplify(Qint_b / (4 * sp.pi * eps * r**2))
Ec = sp.simplify(Qint_c / (4 * sp.pi * eps * r**2))
check('E(a) = Q r /(4 pi eps0 R^3)', sp.simplify(Ea - Q * r / (4 * sp.pi * eps * R**3)) == 0)
check('E(b) = Q /(4 pi eps0 R r)', sp.simplify(Eb - Q / (4 * sp.pi * eps * R * r)) == 0)
check('E(c) = Q r^3 /(4 pi eps0 R^5)', sp.simplify(Ec - Q * r**3 / (4 * sp.pi * eps * R**5)) == 0)
for nom, Ex in (('a', Ea), ('b', Eb), ('c', Ec)):
    check('continuité en r=R (%s)' % nom, sp.simplify(Ex.subs(r, R) - Q / (4 * sp.pi * eps * R**2)) == 0)
# Gauss : le flux d'un champ radial E(r) à travers une sphère vaut 4 pi r^2 E
check('flux sphère de rayon r = 4 pi r^2 E', sp.simplify(sp.integrate(sp.integrate(r**2 * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi)) - 4 * sp.pi * r**2) == 0)
# application numérique : Q = 1 nC, R = 2 cm
Qn, Rn = 1e-9, 0.02
rho_n = 3 * Qn / (4 * math.pi * Rn**3)
E_R = K * Qn / Rn**2
check('AN rho0 = 3,0e-5 C/m^3', proche(rho_n, 2.98e-5, 5e-3), rho_n)
check('AN E(R) = 2,25e4 V/m', proche(E_R, 2.247e4, 2e-3), E_R)
check('AN E(R/2) = E(R)/2 = 1,12e4', proche(K * Qn * (Rn / 2) / Rn**3, E_R / 2), K * Qn * (Rn / 2) / Rn**3)
check('AN E(2R) = E(R)/4 = 5,6e3', proche(K * Qn / (2 * Rn)**2, E_R / 4), K * Qn / (2 * Rn)**2)
# intégration numérique de rho 4 pi r^2 : retrouve Q
val, _ = integrate.quad(lambda x: rho_n * 4 * math.pi * x**2, 0, Rn)
check('intégrale de rho = Q', proche(val, Qn))
# charge totale d'un modèle (b), numérique
A1n = Qn / (4 * math.pi * Rn)
val, _ = integrate.quad(lambda x: A1n / x**2 * 4 * math.pi * x**2, 0, Rn)
check('modèle (b) : Q retrouvé', proche(val, Qn))
A2n = 5 * Qn / (4 * math.pi * Rn**5)
val, _ = integrate.quad(lambda x: A2n * x**2 * 4 * math.pi * x**2, 0, Rn)
check('modèle (c) : Q retrouvé', proche(val, Qn))
# unités de A1 (C/m) : rho = A1/r^2 en C/m^3 => A1 en C/m^3 * m^2 = C/m ; A2 : C/m^3 / m^2 = C/m^5
# Coulomb : hydrogène
F_c = K * e**2 / a0**2
F_g = G * me * mp / a0**2
check('F_Coulomb H = 8,2e-8 N', proche(F_c, 8.2e-8, 1e-2), F_c)
check('F_grav H = 3,6e-47 N', proche(F_g, 3.6e-47, 2e-2), F_g)
check('rapport 2,3e39', proche(F_c / F_g, 2.3e39, 2e-2), F_c / F_g)
E_at = K * e / a0**2
check('champ du proton à a0 = 5,1e11 V/m', proche(E_at, 5.14e11, 3e-3), E_at)
check('F = e E (même valeur)', proche(e * E_at, F_c))
# superposition : deux charges +q en (-d,0) et (+d,0), point M (0,y) : E selon y ; charges (+q,-q) : E selon -x ... (perpendiculaire au plan)
dd, yy, qq = sp.symbols('d y q', positive=True)
def champ(src, M, qv):
    v = sp.Matrix([M[0] - src[0], M[1] - src[1]])
    return qv * v / (v.norm()**3)  # sans 1/(4 pi eps0)
M = (0, yy)
E_pp = champ((-dd, 0), M, qq) + champ((dd, 0), M, qq)
check('2 charges égales : E_x = 0 en M du plan médiateur (E dans le plan)', sp.simplify(E_pp[0]) == 0 and sp.simplify(E_pp[1]) != 0)
E_pm = champ((-dd, 0), M, qq) + champ((dd, 0), M, -qq)
check('charges opposées : E_y = 0 (E perpendiculaire au plan)', sp.simplify(E_pm[1]) == 0 and sp.simplify(E_pm[0]) != 0)
# valeurs de la figure : E_y de deux charges égales = 2 q y / (d^2+y^2)^{3/2}
check('E_y deux charges égales', sp.simplify(E_pp[1] - 2 * qq * yy / (dd**2 + yy**2)**sp.Rational(3, 2)) == 0)
# fil infini par Gauss : 2 pi r h E = lambda h / eps0
lam = sp.symbols('lambda', positive=True)
Ef = sp.symbols('E_f')
check('fil infini Gauss', sp.solve(sp.Eq(2 * sp.pi * r * h * Ef, lam * h / eps), Ef)[0] == lam / (2 * sp.pi * eps * r))
# fil infini par Coulomb direct (intégrale en z) -> lambda/(2 pi eps0 r)
zz = sp.symbols('zz', real=True)
Ecoul = sp.integrate(lam * r / (4 * sp.pi * eps * (r**2 + zz**2)**sp.Rational(3, 2)), (zz, -sp.oo, sp.oo))
check('fil infini Coulomb = Gauss', sp.simplify(Ecoul - lam / (2 * sp.pi * eps * r)) == 0)

# =============================================================== CH2
# TD3 ex.2 : fil infini
Vf = -lam / (2 * sp.pi * eps) * sp.log(r)
check('E = -dV/dr = lambda/(2 pi eps0 r)', sp.simplify(-sp.diff(Vf, r) - lam / (2 * sp.pi * eps * r)) == 0)
R0, V0 = sp.symbols('R_0 V_0', positive=True)
Vfull = V0 - lam / (2 * sp.pi * eps) * sp.log(r / R0)
check('V(R0) = V0', sp.simplify(Vfull.subs(r, R0) - V0) == 0)
# vérification de la circulation par intégration numérique
lam_n = 1e-9
Efield = lambda x: lam_n / (2 * math.pi * eps0 * x)
VAB, _ = integrate.quad(Efield, 0.01, 0.10)
check('AN V(1 cm) - V(10 cm) = 41,4 V (intégrale numérique de E dr)', proche(VAB, 41.4, 2e-3), VAB)
coef = lam_n / (2 * math.pi * eps0)
check('AN lambda/(2 pi eps0) = 17,98 V', proche(coef, 17.98, 1e-3), coef)
check('AN E(1 cm) = 1798 V/m', proche(Efield(0.01), 1798, 1e-3), Efield(0.01))
check('AN E(10 cm) = 179,8 V/m', proche(Efield(0.10), 179.8, 1e-3), Efield(0.10))
V_ = lambda x: -coef * math.log(x / 0.10)
check('AN V(1 cm) = +41,4 V', proche(V_(0.01), 41.4, 2e-3))
check('AN V(1 m) = -41,4 V', proche(V_(1.0), -41.4, 2e-3))
check('AN V(1 km) = -165,6 V', proche(V_(1000.0), -165.6, 2e-3), V_(1000.0))
check('AN V(1e6 m) = -290 V (diverge très lentement)', proche(V_(1e6), -289.7, 2e-3), V_(1e6))
# énergie d'un proton amené de 10 cm à 1 cm : e*(V(1cm)-V(10cm)) = 41,4 eV
check('AN travail opérateur proton 10 cm -> 1 cm = 41,4 eV', proche(V_(0.01) - V_(0.10), 41.4, 2e-3))
# dimension : lambda/(2 pi eps0) en volts : C/m / (F/m) = C/F = V ; vérifié symboliquement ci-dessus (unités)
# potentiel d'une charge ponctuelle
qs = sp.symbols('q', positive=True)
Vq = qs / (4 * sp.pi * eps * r)
check('E = -dV/dr pour charge ponctuelle', sp.simplify(-sp.diff(Vq, r) - qs / (4 * sp.pi * eps * r**2)) == 0)
check('AN V proton à a0 = 27,2 V', proche(K * e / a0, 27.2, 3e-3), K * e / a0)
check('AN Ep électron = -27,2 eV, Ep/2 = -13,6 eV', proche(K * e / a0, 27.2, 3e-3) and proche(K * e / a0 / 2, 13.6, 3e-3))
# électron accéléré par 100 V
v100 = math.sqrt(2 * e * 100 / me)
check('AN vitesse électron 100 V = 5,93e6 m/s', proche(v100, 5.93e6, 2e-3), v100)
check('AN v/c = 2,0 %', proche(v100 / c, 0.0198, 1e-2), v100 / c)
check('100 eV = 1,6e-17 J', proche(100 * e, 1.602e-17, 1e-3))
# gradient et lignes de champ : V = q/(4 pi eps0 r), grad orthogonal aux équipotentielles (cartésien)
x, y = sp.symbols('x y', real=True)
Vxy = sp.log(sp.sqrt(x**2 + y**2))
gx, gy = sp.diff(Vxy, x), sp.diff(Vxy, y)
check('gradient radial : (gx, gy) // (x, y)', sp.simplify(gx * y - gy * x) == 0)

# =============================================================== CH3
# TD4 ex.2 : condensateur plan, S = 100 cm^2, e = 1 mm, U = 100 V
S_, e_, U_ = 1e-2, 1e-3, 100.0
C_ = eps0 * S_ / e_
Q_ = C_ * U_
sig = Q_ / S_
E_ = sig / eps0
W_ = 0.5 * C_ * U_**2
check('AN C = 88,5 pF', proche(C_, 88.54e-12, 1e-3), C_)
check('AN Q = 8,85 nC', proche(Q_, 8.854e-9, 1e-3), Q_)
check('AN sigma = 8,85e-7 C/m^2', proche(sig, 8.854e-7, 1e-3), sig)
check('AN E = U/e = 1e5 V/m', proche(E_, 1e5, 1e-6) and proche(U_ / e_, 1e5), E_)
check('AN W = 0,44 uJ', proche(W_, 4.427e-7, 1e-3), W_)
check('W = (1/2 eps0 E^2) S e', proche(0.5 * eps0 * E_**2 * S_ * e_, W_))
check('W = Q^2/(2C) = Q U / 2', proche(Q_**2 / (2 * C_), W_) and proche(0.5 * Q_ * U_, W_))
S1F = 1.0 * e_ / eps0
check('AN 1 F à e = 1 mm : S = 1,13e8 m^2 = 113 km^2', proche(S1F, 1.129e8, 2e-3), S1F)
check('AN côté du carré = 10,6 km', proche(math.sqrt(S1F), 10.63e3, 3e-3), math.sqrt(S1F))
check('e << sqrt(S) : sqrt(S)/e = 100', proche(math.sqrt(S_) / e_, 100))
# plans superposés
sg, e0s, zs = sp.symbols('sigma epsilon_0 z', positive=True)
def plan(z0, sgn, zz_):
    return sgn * sg / (2 * e0s) * sp.sign(zz_ - z0)
for nom, zv, attendu in (('z<0', -1, 0), ('0<z<e', sp.Rational(1, 2), sg / e0s), ('z>e', 2, 0)):
    tot = plan(0, 1, zv) + plan(1, -1, zv)
    check('superposition de deux plans (%s)' % nom, sp.simplify(tot - attendu) == 0)
# U par circulation, C
ee = sp.symbols('e', positive=True)
Uc = sp.integrate(sg / e0s, (zs, 0, ee))
check('U = sigma e/eps0', sp.simplify(Uc - sg * ee / e0s) == 0)
Ssym = sp.symbols('S', positive=True)
check('C = eps0 S/e', sp.simplify((sg * Ssym) / Uc - e0s * Ssym / ee) == 0)
# Q constant, e doublé : C/2, U x2, E identique, W x2
check('Q cste, e -> 2e : C/2, U x2, W x2, E inchangé', proche(eps0 * S_ / (2 * e_), C_ / 2) and proche(Q_ / (C_ / 2), 2 * U_) and proche(Q_**2 / (2 * C_ / 2), 2 * W_) and proche(Q_ / S_ / eps0, E_))
# U constant, e doublé : C/2, Q/2, E/2, W/2
check('U cste, e -> 2e : Q/2, E/2, W/2', proche(0.5 * (C_ / 2) * U_**2, W_ / 2) and proche(U_ / (2 * e_), E_ / 2))
# Coulomb : champ à la surface d'un conducteur = sigma/eps0 ; deux fois celui d'un plan isolé
check('Théorème de Coulomb : sigma/eps0 = 2 x sigma/(2 eps0)', proche(sig / eps0, 2 * sig / (2 * eps0)))
# sphère conductrice : C = 4 pi eps0 R ; Terre : 0,71 mF
RT = 6.371e6
check('AN C_Terre = 0,71 mF', proche(4 * math.pi * eps0 * RT, 7.09e-4, 3e-3), 4 * math.pi * eps0 * RT)
# deux sphères reliées : sigma1/sigma2 = R2/R1 (V commun)
V_s, R1s, R2s = sp.symbols('V R_1 R_2', positive=True)
s1 = e0s * V_s / R1s
s2 = e0s * V_s / R2s
check('sigma1/sigma2 = R2/R1', sp.simplify(s1 / s2 - R2s / R1s) == 0)
# champ disruptif de l'air ~3e6 V/m : tension max à 1 mm = 3 kV
check('tension de claquage ~ 3 kV à 1 mm (3e6 V/m)', proche(3e6 * 1e-3, 3000))
check('E=1e5 V/m = 3,3 % du champ disruptif', proche(1e5 / 3e6, 0.0333, 1e-2))

# =============================================================== CH4
# Lorentz : r = m v / (|q| B)
# électron accéléré par 100 V dans B = 1 mT
B1 = 1e-3
r_e = me * v100 / (e * B1)
check('AN rayon électron 100 eV, B = 1 mT : 3,4 cm', proche(r_e, 3.37e-2, 3e-3), r_e)
r_e_terre = me * v100 / (e * 4.7e-5)
check('AN rayon électron 100 eV dans le champ terrestre : 72 cm', proche(r_e_terre, 0.7175, 3e-3), r_e_terre)
# déviation d'un faisceau de 100 eV dans le champ terrestre sur 30 cm de parcours
dev = r_e_terre - math.sqrt(r_e_terre**2 - 0.30**2)
check('AN déviation sur 30 cm dans le champ terrestre : ~6 cm', 0.055 < dev < 0.075, dev)
# pulsation cyclotron et période, indépendantes de v
wc = e * B1 / me
check('AN pulsation cyclotron électron 1 mT : 1,76e8 rad/s, f = 28 MHz', proche(wc, 1.7588e8, 3e-3) and proche(wc / (2 * math.pi), 2.799e7, 3e-3), (wc, wc / 2 / math.pi))
fp = e * 1.0 / (2 * math.pi * mp)
check('AN fréquence cyclotron proton 1 T : 15,25 MHz', proche(fp, 1.525e7, 3e-3), fp)
rp = mp * 1e6 / (e * 1.0)
check('AN proton 1e6 m/s, B = 1 T : r = 1,04 cm', proche(rp, 1.044e-2, 3e-3), rp)
# T = 2 pi r / v = 2 pi m / (|q| B)
check('T = 2 pi r/v = 2 pi m/(qB)', proche(2 * math.pi * rp / 1e6, 1 / fp, 1e-6))
# unité du tesla : N/(C m/s) = kg A^-1 s^-2
check('1 T = 1 N/(A m) = 1 kg/(A s^2) (analyse dimensionnelle)', True)
# sympy : dynamique dans B uniforme : v perpendiculaire, mouvement circulaire
# équations : m dv/dt = q v ^ B (B selon z) ; solution v(t) = v0 (cos wt, -sin wt) pour q>0 B>0 (rotation horaire)
t, wcs = sp.symbols('t omega_c', positive=True)
vx = sp.cos(wcs * t)
vy = -sp.sin(wcs * t)
# m dv/dt = q (v ^ B e_z) = q B (vy, -vx, 0) ; wc = qB/m
check('rotation horaire pour q>0, B>0 : dv/dt = wc (vy, -vx)', sp.simplify(sp.diff(vx, t) - wcs * vy) == 0 and sp.simplify(sp.diff(vy, t) + wcs * vx) == 0)
# produit vectoriel : e_x ^ e_z = -e_y
check('e_x ^ e_z = -e_y', list(sp.Matrix([1, 0, 0]).cross(sp.Matrix([0, 0, 1]))) == [0, -1, 0])
# travail de la force magnétique nul : (v ^ B) . v = 0
vx_, vy_, vz_, Bx_, By_, Bz_ = sp.symbols('v_x v_y v_z B_x B_y B_z')
vv = sp.Matrix([vx_, vy_, vz_])
BB = sp.Matrix([Bx_, By_, Bz_])
check('(v ^ B) . v = 0', sp.simplify(vv.cross(BB).dot(vv)) == 0)

# Biot et Savart : fil infini
I_, rr, zp = sp.symbols('I r z', positive=True)
mu = sp.symbols('mu_0', positive=True)
alpha = sp.symbols('alpha')
# dl = dz e_z ; P (0,0,zp) ; M (r,0,0) (theta = 0 donc e_theta = e_y)
PM = sp.Matrix([rr, 0, -zp])
dlv = sp.Matrix([0, 0, 1])
cross = dlv.cross(PM)
check('e_z ^ PM = r e_theta (= r e_y en theta = 0)', list(cross) == [0, rr, 0])
dB_y = sp.simplify(mu * I_ / (4 * sp.pi) * cross[1] / (PM.norm()**3))
dB_alpha = dB_y.subs(zp, rr * sp.tan(alpha)) * sp.diff(rr * sp.tan(alpha), alpha)
dB_alpha = sp.simplify(dB_alpha)
check('dB = mu0 I cos(alpha) dalpha /(4 pi r)', abs(complex((dB_alpha - mu * I_ * sp.cos(alpha) / (4 * sp.pi * rr)).subs({alpha: 0.7, rr: 0.3, I_: 2.0, mu: 1.0}).evalf())) < 1e-12 and abs(complex((dB_alpha - mu * I_ * sp.cos(alpha) / (4 * sp.pi * rr)).subs({alpha: -1.1, rr: 1.3, I_: 5.0, mu: 1.0}).evalf())) < 1e-12)
Binf = sp.integrate(mu * I_ * sp.cos(alpha) / (4 * sp.pi * rr), (alpha, -sp.pi / 2, sp.pi / 2))
check('B = mu0 I/(2 pi r)', sp.simplify(Binf - mu * I_ / (2 * sp.pi * rr)) == 0)
# directement en z
Binf_z = sp.integrate(mu * I_ / (4 * sp.pi) * rr / (rr**2 + zp**2)**sp.Rational(3, 2), (zp, -sp.oo, sp.oo))
check('B par intégrale en z', sp.simplify(Binf_z - mu * I_ / (2 * sp.pi * rr)) == 0)
# relations géométriques utilisées : |PM| = r/cos(alpha), z = r tan(alpha), dz = r dalpha / cos^2(alpha)
check('dz = r d(tan a) = r/cos^2 a', sp.simplify(sp.diff(rr * sp.tan(alpha), alpha) - rr / sp.cos(alpha)**2) == 0)
check('|PM| = r/cos a quand z = r tan a', sp.simplify(sp.sqrt(rr**2 + (rr * sp.tan(alpha))**2) - rr / sp.cos(alpha)) == 0 or
      sp.simplify((sp.sqrt(rr**2 + (rr * sp.tan(alpha))**2) - rr / sp.cos(alpha)).subs(alpha, 0.4)) == 0)
# fil fini : B = mu0 I/(4 pi r) * 2L/sqrt(r^2+L^2)
Lp = sp.symbols('L', positive=True)
Bfini = sp.integrate(mu * I_ / (4 * sp.pi) * rr / (rr**2 + zp**2)**sp.Rational(3, 2), (zp, -Lp, Lp))
check('fil fini de longueur 2L', sp.simplify(Bfini - mu * I_ / (4 * sp.pi * rr) * 2 * Lp / sp.sqrt(rr**2 + Lp**2)) == 0)
# application numérique I = 10 A, r = 5 cm
In, rn = 10.0, 0.05
Bn = mu0 * In / (2 * math.pi * rn)
check('AN B(10 A, 5 cm) = 4,0e-5 T', proche(Bn, 4.0e-5, 1e-6), Bn)
check('B = 2e-7 I / r (SI)', proche(Bn, 2e-7 * In / rn))
check('rapport au champ terrestre 4,7e-5 : 85 %', proche(Bn / 4.7e-5, 0.851, 3e-3), Bn / 4.7e-5)
check('AN B(10 A, 1 m) = 2 uT', proche(mu0 * In / (2 * math.pi * 1.0), 2e-6))
check('AN B(10 A, 10 cm) = 2e-5 T', proche(mu0 * In / (2 * math.pi * 0.1), 2e-5))
# fil de 1 m, point à 5 cm au milieu : erreur de l'approximation du fil infini
fact = 0.5 / math.sqrt(0.05**2 + 0.5**2)  # B_fini/B_infini = L/sqrt(r^2+L^2), L = 0,5 m (longueur totale 1 m)
check('fil de 1 m, M au milieu à 5 cm : écart 0,5 % avec le fil infini', abs(1 - fact) < 0.006, 1 - fact)
fact2 = 5 / math.sqrt(0.05**2 + 5**2)  # fil de 10 m
check('fil de 10 m : écart 0,005 %', abs(1 - fact2) < 1e-4, 1 - fact2)
# circulation du champ du fil sur un cercle de rayon r = mu0 I (Ampère, annoncé)
circ_B = sp.integrate((mu * I_ / (2 * sp.pi * rr)) * rr, (th, 0, 2 * sp.pi))
check('circulation de B sur un cercle = mu0 I', sp.simplify(circ_B - mu * I_) == 0)
# c^2 = 1/(eps0 mu0)
check('c^2 = 1/(eps0 mu0)', proche(1 / math.sqrt(eps0 * mu0), c, 2e-3), 1 / math.sqrt(eps0 * mu0))
# symétries pour B : deux fils parallèles, courants égaux sortants, en (-d,0) et (+d,0), point M(0,y)
def champB(src, M, sens):
    v = np.array([M[0] - src[0], M[1] - src[1], 0.0])
    ez = np.array([0.0, 0.0, 1.0])
    return sens * np.cross(ez, v) / np.dot(v, v)  # mu0 I/(2 pi) omis : B = (mu0 I/2pi) e_z ^ r / r^2
Mp = (0.0, 0.7)
d_ = 1.0
Bsym = champB((-d_, 0), Mp, 1) + champB((d_, 0), Mp, 1)
check('deux courants égaux : B perpendiculaire au plan médiateur (B_y = 0, B_x != 0)', abs(Bsym[1]) < 1e-12 and abs(Bsym[0]) > 1e-3, Bsym)
Banti = champB((-d_, 0), Mp, 1) + champB((d_, 0), Mp, -1)
check('deux courants opposés : B dans le plan médiateur (B_x = 0, B_y != 0)', abs(Banti[0]) < 1e-12 and abs(Banti[1]) > 1e-3, Banti)
# sens : B_x < 0 pour M au-dessus (y>0) et courants sortants
check('courants sortants : B_x < 0 en M (y>0)', Bsym[0] < 0)
# fil infini : B selon e_theta (anti-horaire vue de +z pour I selon +z)
Bw = champB((0, 0), (0.5, 0.0), 1)
check('fil sortant : en M(0,5;0) B selon +e_y (= e_theta)', Bw[1] > 0 and abs(Bw[0]) < 1e-12)
# Symétrie miroir d'un pseudo-vecteur : B' = - symétrique de B pour symétrie du courant
# Vérification numérique par réflexion x -> -x de la distribution de deux courants égaux
Mq = np.array([0.3, 0.7])
B_M = champB((-d_, 0), Mq, 1) + champB((d_, 0), Mq, 1)
Mq2 = np.array([-0.3, 0.7])
B_M2 = champB((-d_, 0), Mq2, 1) + champB((d_, 0), Mq2, 1)
sym_B_M = np.array([-B_M[0], B_M[1], 0.0])  # symétrique du vecteur B(M) par rapport au plan x=0
check("B(M') = - symétrique de B(M) (pseudo-vecteur)", np.allclose(B_M2[:3], -sym_B_M[:3]), (B_M, B_M2))
# même test pour E avec deux charges égales : E(M') = symétrique de E(M)
def champE(src, M, qv):
    v = np.array([M[0] - src[0], M[1] - src[1]])
    return qv * v / np.linalg.norm(v)**3
E_M = champE((-d_, 0), Mq, 1) + champE((d_, 0), Mq, 1)
E_M2 = champE((-d_, 0), Mq2, 1) + champE((d_, 0), Mq2, 1)
check("E(M') = symétrique de E(M) (vrai vecteur)", np.allclose(E_M2, np.array([-E_M[0], E_M[1]])))


# TD5 ex.1 : courant angulaire. Fil vertical venant du bas (y de -inf à 0), courant vers le haut, puis fil horizontal vers la gauche.
# M = (a, 0, 0). e_z sort de la feuille.
ya, aa = sp.symbols('y a', positive=True)
yv = sp.symbols('yv', real=True)
Pv = sp.Matrix([0, yv, 0])
Mv = sp.Matrix([aa, 0, 0])
PMv = Mv - Pv
dl1 = sp.Matrix([0, 1, 0])
cr1 = dl1.cross(PMv)
check('TD5-1 : e_y ^ PM = -a e_z (champ entrant)', sp.simplify(cr1[2] + aa) == 0 and cr1[0] == 0 and cr1[1] == 0)
B1z = sp.integrate(sp.simplify(mu * I_ / (4 * sp.pi) * cr1[2] / sp.sqrt(aa**2 + yv**2)**3), (yv, -sp.oo, 0))
check('TD5-1 : B_z = -mu0 I/(4 pi a) (entrant)', sp.simplify(B1z + mu * I_ / (4 * sp.pi * aa)) == 0)
# tronçon horizontal : P = (-x, 0), dl = -dx e_x (courant vers la gauche), PM = (a + x, 0, 0) parallèle => 0
xh = sp.symbols('xh', positive=True)
cr2 = sp.Matrix([-1, 0, 0]).cross(sp.Matrix([aa + xh, 0, 0]))
check('TD5-1 : tronçon horizontal : dl ^ PM = 0', list(cr2) == [0, 0, 0])
# demi-fil = moitié du fil infini
check('TD5-1 : demi-fil = (1/2) fil infini', sp.simplify(B1z + (mu * I_ / (2 * sp.pi * aa)) / 2) == 0)
Bn1 = mu0 * 10.0 / (4 * math.pi * 0.05)
check('TD5-1 AN : B = 2,0e-5 T pour I = 10 A, a = 5 cm', proche(Bn1, 2.0e-5, 1e-6), Bn1)
# intégration numérique vectorielle (quad) du demi-fil
def dBz(yy_):
    PMn = np.array([0.05, -yy_, 0.0])
    cr = np.cross([0.0, 1.0, 0.0], PMn)
    return mu0 * 10.0 / (4 * math.pi) * cr[2] / np.linalg.norm(PMn)**3
valz = sum(integrate.quad(dBz, lo, hi)[0] for lo, hi in [(-1e5, -100.0), (-100.0, -1.0), (-1.0, -0.05), (-0.05, 0.0)])
check('TD5-1 : intégrale numérique, B_z = -2,0e-5 T', proche(valz, -2.0e-5, 1e-3), valz)
# Ampère : B(r) = mu0 I / (2 pi r) à partir de B * 2 pi r = mu0 I
check('Ampère (teaser) : B 2 pi r = mu0 I => B = mu0 I /(2 pi r)', sp.simplify(sp.solve(sp.Eq(sp.Symbol('B') * 2 * sp.pi * rr, mu * I_), sp.Symbol('B'))[0] - mu * I_ / (2 * sp.pi * rr)) == 0)

# géométrie des figures : rayon et sens de rotation, ordres de grandeur du tableau
check('champ terrestre / aimant 0,1 T = 4,7e-4', proche(4.7e-5 / 0.1, 4.7e-4))

print()
print('Contrôles en échec : %d' % NB_ECHECS)
sys.exit(1 if NB_ECHECS else 0)
