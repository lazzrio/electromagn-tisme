"""Vérifications numériques / symboliques des corrigés du TD5 (magnétostatique).
Usage : python tools/verif_td5.py   (affiche OK/ECART pour chaque résultat).
Biot et Savart exact pour des segments rectilignes, B en unités de mu0 I / (4 pi) puis converti."""
import math
import numpy as np
import sympy as sp

MU0 = 4e-7 * math.pi
E_CHARGE = 1.602176634e-19


def seg_B(p1, p2, P, I=1.0):
    """champ (T) d'un segment de p1 à p2 parcouru par I, au point P (formule exacte, vectorisée sur les segments)"""
    p1 = np.atleast_2d(p1).astype(float)
    p2 = np.atleast_2d(p2).astype(float)
    P = np.asarray(P, float)
    d = p2 - p1
    L = np.linalg.norm(d, axis=1)
    u = d / L[:, None]
    w = P - p1
    s1 = -np.einsum('ij,ij->i', w, u)  # abscisse de p1 par rapport au pied de la perpendiculaire
    s2 = s1 + L
    perp = w - np.einsum('ij,ij->i', w, u)[:, None] * u
    rho = np.linalg.norm(perp, axis=1)
    # sinus des angles : s / sqrt(s^2+rho^2)
    f = s2 / np.sqrt(s2 ** 2 + rho ** 2) - s1 / np.sqrt(s1 ** 2 + rho ** 2)
    n = np.cross(u, perp)
    nn = np.linalg.norm(n, axis=1)
    ok = rho > 1e-12 * (1 + L)  # point sur la droite support : dl // r, donc dB = 0
    coef = np.zeros_like(rho)
    coef[ok] = f[ok] / rho[ok] / nn[ok]
    B = (MU0 * I / (4 * math.pi)) * coef[:, None] * n
    return B.sum(axis=0)


def rep(nom, val, ref, tol=1e-3):
    ok = abs(val - ref) <= tol * max(abs(ref), 1e-30) if ref != 0 else abs(val) < tol
    print('%-62s calcul=% .6g  théorie=% .6g  %s' % (nom, val, ref, 'OK' if ok else 'ECART'))
    return ok


tout = True
a = 0.7
# ---------------------------------------------------------------- Ex 1 : fil coudé
y = sp.symbols('y', real=True)
a_s = sp.symbols('a', positive=True)
integ = sp.integrate(a_s / (a_s ** 2 + y ** 2) ** sp.Rational(3, 2), (y, -sp.oo, 0))
print('Ex1 : intégrale symbolique =', sp.simplify(integ), "(attendu 1/a)")
big = 1e5
# courant : monte le long de y (x=0) de -big à 0, puis repart vers la gauche de (0,0) à (-big,0) ; M=(a,0,0)
B = seg_B([0, -big, 0], [0, 0, 0], [a, 0, 0]) + seg_B([0, 0, 0], [-big, 0, 0], [a, 0, 0])
tout &= rep('Ex1 Bz (z sortant) = -mu0 I/(4 pi a)', B[2], -MU0 / (4 * math.pi * a))
tout &= rep('Ex1 Bx, By = 0', abs(B[0]) + abs(B[1]), 0, 1e-9)
tout &= rep('Ex1 branche horizontale seule = 0', np.linalg.norm(seg_B([0, 0, 0], [-big, 0, 0], [a, 0, 0])), 0, 1e-9)
# angle : dB = mu0 I/(4 pi a) cos(alpha) d alpha
al = sp.symbols('alpha')
print('Ex1 : int_0^{pi/2} cos = ', sp.integrate(sp.cos(al), (al, 0, sp.pi / 2)))

# ---------------------------------------------------------------- Ex 2 : 4 fils
b = 0.4
pos = [(b, b), (-b, b), (-b, -b), (b, -b)]
Btot = np.zeros(3)
for (x0, y0) in pos:
    Btot += seg_B([x0, y0, big], [x0, y0, -big], [0, 0, 0])  # courant -e_z (entrant)
tout &= rep('Ex2 |B(O)| = 0', np.linalg.norm(Btot), 0, 1e-6)
# champ d'un fil seul au centre
B1 = seg_B([b, b, big], [b, b, -big], [0, 0, 0])
tout &= rep('Ex2 |B| un fil = mu0 I/(2 pi b sqrt2)', np.linalg.norm(B1), MU0 / (2 * math.pi * b * math.sqrt(2)), 1e-4)
print('Ex2 B un fil en (b,b) (unités mu0 I/(2 pi b sqrt2)) =', np.round(B1 / (MU0 / (2 * math.pi * b * math.sqrt(2))), 4), '  -> direction (-1,+1)/sqrt2 attendue pour (b,b)')
# un point hors centre : le champ n'est pas nul (preuve que la compensation est bien spécifique au centre)
Bp = sum(seg_B([x0, y0, big], [x0, y0, -big], [0.1, 0.05, 0]) for (x0, y0) in pos)
print('Ex2 |B| en un point voisin (0.1,0.05) =', np.linalg.norm(Bp), '(non nul, linéaire en la distance)')

# ---------------------------------------------------------------- Ex 3 : spire
R = 0.5
N = 4000
th = np.linspace(0, 2 * math.pi, N + 1)
loop = np.stack([R * np.cos(th), R * np.sin(th), np.zeros_like(th)], axis=1)  # courant dans le sens +e_theta


def B_spire(P):
    return seg_B(loop[:-1], loop[1:], P)


for z in (0.0, 0.3, 1.0, -0.6):
    Bz = B_spire([0, 0, z])
    th_ = MU0 * R ** 2 / (2 * (R ** 2 + z ** 2) ** 1.5)
    sa = R / math.hypot(R, z)
    ok = rep('Ex3 B axe z=%.1f  Bz = mu0 I R^2/(2(R^2+z^2)^1.5)' % z, Bz[2], th_)
    ok &= rep('Ex3     idem en sin^3(alpha) mu0/(2R)', Bz[2], MU0 * sa ** 3 / (2 * R))
    tout &= ok
    tout &= rep('Ex3     Bx, By = 0 sur l\'axe', abs(Bz[0]) + abs(Bz[1]), 0, 1e-9)
tout &= rep('Ex3 B(centre) = mu0 I/(2R)', B_spire([0, 0, 0])[2], MU0 / (2 * R))
# hors axe : plan theta=0 (plan xz), B_y = 0 (antisymétrie), B_r et B_z ; indépendance de theta
P = np.array([0.2, 0.0, 0.3])
B0 = B_spire(P)
print('Ex3 hors axe, theta=0 : B =', B0, ' (By=0 attendu)')
c, s = math.cos(1.1), math.sin(1.1)
P2 = np.array([0.2 * c, 0.2 * s, 0.3])
B2 = B_spire(P2)
er = np.array([c, s, 0])
et = np.array([-s, c, 0])
print('Ex3 theta=1.1 rad : B_r=%.6e B_theta=%.2e B_z=%.6e  | theta=0 : B_r=%.6e B_z=%.6e' % (B2 @ er, B2 @ et, B2[2], B0[0], B0[2]))
tout &= rep('Ex3 B_r indépendant de theta', B2 @ er, B0[0], 1e-4)
tout &= rep('Ex3 B_z indépendant de theta', B2[2], B0[2], 1e-4)
# développement près de l'axe : B_r ~ (r/2) * 3 mu0 I R^2 z /(2 (R^2+z^2)^(5/2))
z = 0.3
r = 0.02
Br_num = B_spire([r, 0, z])[0]
Br_th = 0.5 * r * 3 * MU0 * R ** 2 * z / (2 * (R ** 2 + z ** 2) ** 2.5)
tout &= rep('Ex3 B_r proche axe = (3 mu0 I R^2 z r)/(4 (R^2+z^2)^(5/2))', Br_num, Br_th, 5e-3)

# ---------------------------------------------------------------- Ex 4 : point d'arrêt fil + champ uniforme
I = 3.0
B0u = 0.002
r0 = MU0 * I / (2 * math.pi * B0u)
print('Ex4 r0 = mu0 I/(2 pi B0) =', r0, 'm')
# fil le long de +e_z en (0,0), champ uniforme B0 e_x ; point (0, r0)
Bw = seg_B([0, 0, -big], [0, 0, big], [0, r0, 0], I) + np.array([B0u, 0, 0])
tout &= rep('Ex4 |B| au point (0, r0) = 0', np.linalg.norm(Bw), 0, 1e-4)
Bw2 = seg_B([0, 0, -big], [0, 0, big], [0, -r0, 0], I) + np.array([B0u, 0, 0])
print('Ex4 en (0,-r0) : B_x =', Bw2[0], '= 2 B0 =', 2 * B0u)
# deux fils de même sens : B(milieu)=0 ; trois fils en triangle : B(centre)=0
d = 1.0
Bm = seg_B([-d / 2, 0, -big], [-d / 2, 0, big], [0, 0, 0]) + seg_B([d / 2, 0, -big], [d / 2, 0, big], [0, 0, 0])
tout &= rep('Ex4a B(milieu) = 0', np.linalg.norm(Bm), 0, 1e-9)
tri = [(d * math.cos(t), d * math.sin(t)) for t in (math.pi / 2, math.pi / 2 + 2 * math.pi / 3, math.pi / 2 + 4 * math.pi / 3)]
Bc = sum(seg_B([x0, y0, -big], [x0, y0, big], [0, 0, 0]) for x0, y0 in tri)
tout &= rep('Ex4c B(centre) = 0', np.linalg.norm(Bc), 0, 1e-9)
# deux fils opposés : entre les fils, les champs s'additionnent
Bo = seg_B([-d / 2, 0, -big], [-d / 2, 0, big], [0, 0, 0]) + seg_B([d / 2, 0, big], [d / 2, 0, -big], [0, 0, 0])
tout &= rep('Ex4b B(milieu) = 2 mu0 I/(pi d)... |B|', np.linalg.norm(Bo), 2 * MU0 / (math.pi * d), 1e-6)

# ---------------------------------------------------------------- Ex 5 : solénoïde (spires jointives, n par unité de longueur)
Rs = 1.0
L = 80.0
n = 25
nseg = 90
tt = np.linspace(0, 2 * math.pi, nseg + 1)
zs = (np.arange(int(n * L)) + 0.5) / n - L / 2
p1 = []
p2 = []
for zk in zs:
    pts = np.stack([Rs * np.cos(tt), Rs * np.sin(tt), np.full_like(tt, zk)], axis=1)
    p1.append(pts[:-1])
    p2.append(pts[1:])
p1 = np.vstack(p1)
p2 = np.vstack(p2)
for r_ in (0.0, 0.5, 0.9):
    Bz = seg_B(p1, p2, [r_, 0, 0])
    tout &= rep('Ex5 B_z intérieur r=%.1f = mu0 n I' % r_, Bz[2], MU0 * n, 2e-3)
for r_ in (1.3, 2.0, 5.0):
    Bz = seg_B(p1, p2, [r_, 0, 0])
    print('Ex5 extérieur r=%.1f : |B|/(mu0 n I) = %.2e (attendu ~ 0)' % (r_, np.linalg.norm(Bz) / (MU0 * n)))
    tout &= np.linalg.norm(Bz) / (MU0 * n) < 5e-3

# ---------------------------------------------------------------- Ex 6 : cylindre plein, j uniforme
Rc = 0.5
Lc = 400.0
fil_n = 60000
rng = np.random.default_rng(1)
# points de la section : grille polaire à aires égales
ks = (np.arange(fil_n) + 0.5) / fil_n
rr = Rc * np.sqrt(ks)
ang = np.arange(fil_n) * 2.399963229728653  # angle d'or
xs, ys = rr * np.cos(ang), rr * np.sin(ang)
Itot = 1.0
for r_ in (0.2, 0.4, 0.5001, 0.8, 3.0):
    P = np.array([r_, 0, 0])
    Bv = seg_B(np.stack([xs, ys, np.full_like(xs, -Lc / 2)], 1), np.stack([xs, ys, np.full_like(xs, Lc / 2)], 1), P, Itot / fil_n)
    th_ = MU0 * Itot * r_ / (2 * math.pi * Rc ** 2) if r_ < Rc else MU0 * Itot / (2 * math.pi * r_)
    tout &= rep('Ex6 r=%.4f : B_theta' % r_, Bv[1], th_, 1.5e-2)  # bruit d'échantillonnage des 60000 filaments
Rs_ = sp.symbols('R', positive=True)
r_s, I_s, mu = sp.symbols('r I mu0', positive=True)
print('Ex6 continuité en r=R : int =', sp.simplify((mu * I_s * r_s / (2 * sp.pi * Rs_ ** 2)).subs(r_s, Rs_) - (mu * I_s / (2 * sp.pi * r_s)).subs(r_s, Rs_)))

# ---------------------------------------------------------------- Ex 7 : coaxial
R1, R2, R3 = 0.3, 0.6, 0.9
sp_r, spI = sp.symbols('r I', positive=True)
B1 = mu * spI * sp_r / (2 * sp.pi * R1 ** 2)
B2 = mu * spI / (2 * sp.pi * sp_r)
B3 = mu * spI / (2 * sp.pi * sp_r) * (R3 ** 2 - sp_r ** 2) / (R3 ** 2 - R2 ** 2)
print('Ex7 continuité R1 :', sp.simplify(B1.subs(sp_r, R1) - B2.subs(sp_r, R1)),
      ' R2 :', sp.simplify(B2.subs(sp_r, R2) - B3.subs(sp_r, R2)), ' R3 :', sp.simplify(B3.subs(sp_r, R3)))
# vérification numérique de Biot et Savart : cœur I (+z) uniforme, couronne -I uniforme
pts = []
for (rmin, rmax, sgn) in ((0, R1, +1), (R2, R3, -1)):
    ks = (np.arange(fil_n) + 0.5) / fil_n
    rr = np.sqrt(rmin ** 2 + ks * (rmax ** 2 - rmin ** 2))
    ang = np.arange(fil_n) * 2.399963229728653
    pts.append((rr * np.cos(ang), rr * np.sin(ang), sgn))
for r_ in (0.15, 0.45, 0.75, 0.85, 1.2):
    Bv = np.zeros(3)
    P = np.array([r_, 0, 0])
    for (xx, yy, sg) in pts:
        Bv += seg_B(np.stack([xx, yy, np.full_like(xx, -Lc / 2)], 1), np.stack([xx, yy, np.full_like(xx, Lc / 2)], 1), P, sg * 1.0 / fil_n)
    if r_ < R1:
        th_ = MU0 * r_ / (2 * math.pi * R1 ** 2)
    elif r_ < R2:
        th_ = MU0 / (2 * math.pi * r_)
    elif r_ < R3:
        th_ = MU0 / (2 * math.pi * r_) * (R3 ** 2 - r_ ** 2) / (R3 ** 2 - R2 ** 2)
    else:
        th_ = 0.0
    if th_ == 0:
        ok = abs(Bv[1]) < 5e-3 * MU0 / (2 * math.pi * R1)
        print('Ex7 r=%.2f : B_theta = %.3e (attendu 0)  %s' % (r_, Bv[1], 'OK' if ok else 'ECART'))
        tout &= ok
    else:
        tout &= rep('Ex7 r=%.2f : B_theta' % r_, Bv[1], th_, 1.5e-2)

# ---------------------------------------------------------------- Ex 8 : tore
Ro, aw, bh = 3.0, 1.0, 1.0
Nt = 240
p1 = []
p2 = []
for k in range(Nt):
    t = 2 * math.pi * (k + 0.5) / Nt
    c_, s_ = math.cos(t), math.sin(t)

    def P3(rad, z):
        return [rad * c_, rad * s_, z]
    ro, ri = Ro + aw / 2, Ro - aw / 2
    # extérieur vers le haut, dessus vers l'intérieur, intérieur vers le bas, dessous vers l'extérieur
    chain = [P3(ro, -bh / 2), P3(ro, bh / 2), P3(ri, bh / 2), P3(ri, -bh / 2), P3(ro, -bh / 2)]
    for q in range(4):
        p1.append(chain[q])
        p2.append(chain[q + 1])
p1 = np.array(p1)
p2 = np.array(p2)
for r_ in (2.7, 3.0, 3.4):
    Bv = seg_B(p1, p2, [r_, 0, 0.1])  # theta = 0 : e_theta = +e_y
    th_ = -MU0 * Nt / (2 * math.pi * r_)
    tout &= rep('Ex8 r=%.1f (dans le tore) : B_theta = -mu0 N I/(2 pi r)' % r_, Bv[1], th_, 8e-3)
for r_ in (1.0, 2.0, 4.2, 6.0):
    Bv = seg_B(p1, p2, [r_, 0, 0.1])
    ok = np.linalg.norm(Bv) < 1e-2 * MU0 * Nt / (2 * math.pi * Ro)
    print('Ex8 r=%.1f (hors tore) : |B|/(mu0 N I/(2 pi Ro)) = %.2e  %s' % (r_, np.linalg.norm(Bv) / (MU0 * Nt / (2 * math.pi * Ro)), 'OK' if ok else 'ECART'))
    tout &= ok
Bv = seg_B(p1, p2, [0, 0, 0.0])
print('Ex8 sur l\'axe : |B| / B_ref = %.2e' % (np.linalg.norm(Bv) / (MU0 * Nt / (2 * math.pi * Ro))))
Bv = seg_B(p1, p2, [0, 0, 3.0])
print('Ex8 au-dessus du tore : |B| / B_ref = %.2e' % (np.linalg.norm(Bv) / (MU0 * Nt / (2 * math.pi * Ro))))
# indépendance en z à l'intérieur
for zz in (-0.4, 0.0, 0.4):
    Bv = seg_B(p1, p2, [3.2, 0, zz])
    tout &= rep('Ex8 z=%.1f : B_theta' % zz, Bv[1], -MU0 * Nt / (2 * math.pi * 3.2), 8e-3)

# ---------------------------------------------------------------- Ex 9 : Hall
e = E_CHARGE
I_, B_, h_, CH = 0.1, 1.0, 0.3e-3, 385e-6
UH = CH * I_ * B_ / h_
n_ = 1 / (e * CH)
print('Ex9 U_H = C_H I B / h = %.4f V ;  n = 1/(e C_H) = %.3e m^-3' % (UH, n_))
tout &= rep('Ex9 U_H ~ 0,128 V', UH, 0.12833, 1e-3)
tout &= rep('Ex9 n ~ 1,62e22 m^-3', n_, 1.6218e22, 1e-3)
# cohérence : IB/(n e h) = C_H I B / h
tout &= rep('Ex9 I B /(n e h) = C_H I B / h', I_ * B_ / (n_ * e * h_), UH, 1e-9)
# signe : v = -(j/(ne)) e_x ; F = -e v ^ B  doit être selon -e_y
j = 1.0
v = np.array([-j / (n_ * e), 0, 0])
F = -e * np.cross(v, np.array([0, 0, B_]))
print('Ex9 force magnétique (direction) :', np.sign(F), ' -> -e_y attendu')
EH = -np.cross(v, np.array([0, 0, B_]))
print('Ex9 E_H = -v ^ B  =', EH, ' -> selon -e_y, module jB/(ne) =', j * B_ / (n_ * e))


# figure ex.3 : formules elliptiques (champ d'une spire hors axe) comparées à Biot et Savart numérique
from scipy.special import ellipe, ellipk


def loop_field(r, z, R=1.0):
    d1 = (R + r) ** 2 + z ** 2
    d2 = (R - r) ** 2 + z ** 2
    m = 4 * R * r / d1
    K, E = ellipk(m), ellipe(m)
    Bz = (K + (R * R - r * r - z * z) / d2 * E) / math.sqrt(d1)
    Br = (z / (r * math.sqrt(d1))) * (-K + (R * R + r * r + z * z) / d2 * E)
    return Br, Bz


for (r_, z_) in ((0.8 * R, 0.5 * R), (1.7 * R, -0.4 * R), (0.3 * R, 1.2 * R)):
    Bnum = B_spire([r_, 0, z_])
    Br_f, Bz_f = loop_field(r_ / R, z_ / R, 1.0)
    unit = MU0 / (2 * math.pi * R)  # mu0 I /(2 pi R)
    tout &= rep('Ex3 elliptique B_r en (%.2f,%.2f)' % (r_, z_), Bnum[0], Br_f * unit, 1e-3)
    tout &= rep('Ex3 elliptique B_z en (%.2f,%.2f)' % (r_, z_), Bnum[2], Bz_f * unit, 1e-3)

# figure ex.4d : la séparatrice A = B0 y - K ln r passe par le point d'arrêt (0, r0) ; K = 1, B0 = 1 (r0 = 1)
A = lambda x, y: y - math.log(math.hypot(x, y))
tout &= rep('Ex4d A(0, r0) = 1 (niveau de la séparatrice)', A(0, 1.0), 1.0, 1e-12)
tout &= rep('Ex4d point bas de l\'oeuf : A(0, -0.2784) = 1', A(0, -0.2784), 1.0, 2e-3)
# Hall : ordre de grandeur pour le cuivre
CuCH = 1 / (8.5e28 * E_CHARGE)
UCu = CuCH * 0.1 * 1 / 0.3e-3
print('Ex9 cuivre : C_H = %.3e m^3/C, U_H = %.2e V (rapport InSb/Cu = %.1e)' % (CuCH, UCu, UH / UCu))

print('\nBILAN : ', 'tout est OK' if tout else 'AU MOINS UN ECART')
