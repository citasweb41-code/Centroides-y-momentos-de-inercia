"""
MOMENTOS DE INERCIA DE ÁREAS — Mecánica racional I
==================================================
Menú principal:
  1. Formulario ............ eliges una figura y ves su dibujo con SUS fórmulas
  2. Figura compuesta ...... la armas pieza por pieza (por vértices o por coordenadas),
                             con vista previa, y la resuelve paso a paso
                             (centroide, Steiner, momentos y círculo de Mohr)
  3. Mohr directo .......... ingresas Ix, Iy, Ixy y obtienes el círculo y sus resultados

Instalar una sola vez:   pip install matplotlib numpy
Ejecutar:                python momentos_inercia.py
Todo se maneja escribiendo números en la terminal; la ventana muestra los dibujos.
En los datos puedes escribir operaciones: 240/2, 3*pi, sqrt(2).
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge, Rectangle

AZUL = "#a9c4e4"
BORDE = "#2c4f7c"

# ----------------------------------------------------------------- utilidades de dibujo
def ejes(ax, x0, x1, y0, y1, ox=0, oy=0):
    flecha = dict(arrowstyle="->", lw=1.3, color="k")
    ax.plot([x0, x1 + 0.3], [y0, y1 + 0.3], alpha=0)  # para que los ejes entren en el encuadre
    ax.annotate("", (x1, oy), (x0, oy), arrowprops=flecha)
    ax.annotate("", (ox, y1), (ox, y0), arrowprops=flecha)
    ax.text(x1, oy - 0.25, "x", fontsize=13, ha="center")
    ax.text(ox - 0.25, y1, "y", fontsize=13, va="center")


def centroide(ax, x, y, guias=False):
    ax.plot(x, y, "ko", ms=6, zorder=5)
    ax.text(x + 0.1, y - 0.3, "C", fontsize=13, weight="bold")
    if guias:
        ax.plot([x, x], [0, y], "k:", lw=0.8)
        ax.plot([0, x], [y, y], "k:", lw=0.8)


def cota(ax, p1, p2, texto, off=(0, 0)):
    ax.annotate("", p2, p1, arrowprops=dict(arrowstyle="<->", lw=1, color="k"))
    xm, ym = (p1[0] + p2[0]) / 2 + off[0], (p1[1] + p2[1]) / 2 + off[1]
    ax.text(xm, ym, texto, fontsize=13, ha="center", va="center",
            bbox=dict(fc="white", ec="none", pad=1))


def area(ax, patch):
    patch.set_facecolor(AZUL)
    patch.set_edgecolor(BORDE)
    patch.set_linewidth(1.6)
    ax.add_patch(patch)


# ----------------------------------------------------------------- figuras
def d_rectangulo(ax):
    b, h = 4, 2.5
    area(ax, Rectangle((0, 0), b, h))
    ejes(ax, -0.5, b + 1, -0.5, h + 1)
    centroide(ax, b / 2, h / 2)
    cota(ax, (0, -0.6), (b, -0.6), "$b$")
    cota(ax, (-0.6, 0), (-0.6, h), "$h$")
    ax.plot([b / 2, b / 2], [h / 2, h + 0.3], "k:", lw=0.8)
    cota(ax, (0, h + 0.3), (b / 2, h + 0.3), "$b/2$", (0, 0.25))


def d_circulo(ax):
    R = 2
    area(ax, Circle((0, 0), R))
    ejes(ax, -R - 0.6, R + 1, -R - 0.6, R + 1)
    centroide(ax, 0, 0)
    ax.annotate("", (R * np.cos(np.pi / 4 * 5), R * np.sin(np.pi / 4 * 5)), (0, 0),
                arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(-0.95, -0.5, "$R$", fontsize=13)


def d_spandrel(ax):
    b, h = 4, 2.5
    x = np.linspace(0, b, 80)
    y = h * (x / b) ** 2
    area(ax, Polygon(np.r_[np.c_[x, y], [[b, 0]]]))
    ejes(ax, -0.5, b + 1, -0.5, h + 1)
    centroide(ax, 3 * b / 4, 3 * h / 10)
    cota(ax, (0, -0.6), (b, -0.6), "$b$")
    cota(ax, (b + 0.4, 0), (b + 0.4, h), "$h$")
    ax.text(1.2, 1.3, "$y = kx^2$", fontsize=13)


def d_tri_rect(ax):
    b, h = 4.5, 2.5
    area(ax, Polygon([(0, 0), (b, 0), (0, h)]))
    ejes(ax, -0.5, b + 1, -0.5, h + 1)
    centroide(ax, b / 3, h / 3, guias=True)
    cota(ax, (0, -0.6), (b, -0.6), "$b$")
    cota(ax, (-0.6, 0), (-0.6, h), "$h$")
    ax.text(b / 3, -0.25, "$b/3$", fontsize=11, ha="center")
    ax.text(0.1, h / 3 + 0.05, "$h/3$", fontsize=11)


def d_semicirculo(ax):
    R = 2.2
    area(ax, Wedge((0, 0), R, 0, 180))
    ejes(ax, -R - 0.5, R + 1, -0.6, R + 1)
    yc = 4 * R / (3 * np.pi)
    centroide(ax, 0, yc)
    cota(ax, (0.6, 0), (0.6, yc), r"$\frac{4R}{3\pi}$", (0.45, 0))
    ax.annotate("", (-R * np.cos(0.8), R * np.sin(0.8)), (0, 0),
                arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(-1.1, 0.95, "$R$", fontsize=13)


def d_media_parabola(ax):
    b, h = 3.5, 3
    yy = np.linspace(0, h, 80)
    xx = b * np.sqrt(yy / h)
    area(ax, Polygon(np.r_[np.c_[xx, yy], [[0, h]]]))
    ejes(ax, -0.5, b + 1, -0.5, h + 1)
    centroide(ax, 3 * b / 8, 3 * h / 5)
    cota(ax, (0, h + 0.4), (b, h + 0.4), "$b$")
    cota(ax, (-0.6, 0), (-0.6, h), "$h$")
    ax.text(2.4, 0.9, "$y = kx^2$", fontsize=13)


def d_isosceles(ax):
    b, h = 4, 3.5
    area(ax, Polygon([(-b / 2, 0), (b / 2, 0), (0, h)]))
    ejes(ax, -b / 2 - 0.5, b / 2 + 1, -0.8, h + 0.8)
    centroide(ax, 0, h / 3)
    cota(ax, (-b / 2, -0.55), (0, -0.55), "$b/2$")
    cota(ax, (0, -0.55), (b / 2, -0.55), "$b/2$")
    cota(ax, (-b / 2 - 0.4, 0), (-b / 2 - 0.4, h), "$h$")
    cota(ax, (b / 2 - 0.3, 0), (b / 2 - 0.3, h / 3), "$h/3$", (0.45, 0))


def d_cuarto_circulo(ax):
    R = 3
    area(ax, Wedge((0, 0), R, 0, 90))
    ejes(ax, -0.5, R + 1, -0.5, R + 1)
    c = 4 * R / (3 * np.pi)
    centroide(ax, c, c, guias=True)
    cota(ax, (0, -0.5), (R, -0.5), "$R$")
    ax.text(c / 2, c + 0.15, r"$\frac{4R}{3\pi}$", fontsize=12, ha="center")


def d_sector(ax):
    R, a = 3.2, np.radians(30)
    area(ax, Wedge((0, 0), R, -30, 30))
    ejes(ax, -0.5, R + 1, -R * np.sin(a) - 0.8, R * np.sin(a) + 0.9)
    xc = 2 * R * np.sin(a) / (3 * a)
    centroide(ax, xc, 0)
    ax.text(0.9, 0.18, r"$\alpha$", fontsize=13)
    ax.text(0.9, -0.45, r"$\alpha$", fontsize=13)
    ax.text(1.5, -1.45, "$R$", fontsize=13)
    cota(ax, (0, -0.25), (xc, -0.25), r"$\bar{x}$", (0, -0.25))


def d_triangulo(ax):
    a, b, h = 3, 4.5, 2.8
    area(ax, Polygon([(0, 0), (b, 0), (a, h)]))
    ejes(ax, -0.5, b + 1, -0.5, h + 1)
    centroide(ax, (a + b) / 3, h / 3)
    cota(ax, (0, -0.6), (b, -0.6), "$b$")
    ax.plot([a, a], [h, h + 0.4], "k:", lw=0.8)
    cota(ax, (0, h + 0.4), (a, h + 0.4), "$a$", (0, 0.25))
    cota(ax, (b + 0.4, 0), (b + 0.4, h), "$h$")


def d_cuarto_elipse(ax):
    a, b = 4, 2.5
    t = np.linspace(0, np.pi / 2, 80)
    area(ax, Polygon(np.r_[[[0, 0]], np.c_[a * np.cos(t), b * np.sin(t)]]))
    ejes(ax, -0.5, a + 1, -0.5, b + 1)
    centroide(ax, 4 * a / (3 * np.pi), 4 * b / (3 * np.pi), guias=True)
    cota(ax, (0, -0.55), (a, -0.55), "$a$")
    cota(ax, (-0.55, 0), (-0.55, b), "$b$")
    ax.text(2.6, 2.4, r"$\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$", fontsize=13)


def d_mohr(ax):
    Ix, Iy, Ixy = 5.0, 2.0, 1.5
    C = (Ix + Iy) / 2
    R = np.hypot((Ix - Iy) / 2, Ixy)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(C + R * np.cos(t), R * np.sin(t), color=BORDE, lw=1.8)
    ejes(ax, -0.3, C + R + 1, -R - 0.6, R + 0.8)
    ax.text(C + R + 1, -0.35, "$I$", fontsize=13, ha="center")
    ax.text(-0.75, R + 0.8, "$I_{xy}$", fontsize=13)
    ax.plot([Ix, Iy], [Ixy, -Ixy], "k-", lw=1)
    for (px, py, s) in [(Ix, Ixy, "X$(I_x,\\,I_{xy})$"), (Iy, -Ixy, "Y$(I_y,\\,-I_{xy})$")]:
        ax.plot(px, py, "o", color="#c0392b")
        ax.text(px + 0.1, py + (0.2 if py > 0 else -0.45), s, fontsize=11)
    ax.plot(C, 0, "ko")
    ax.text(C - 0.1, 0.15, "C", fontsize=12, ha="right")
    for v, s in [(C + R, r"$I_{max}$"), (C - R, r"$I_{min}$")]:
        ax.plot(v, 0, "s", color="#27ae60")
        ax.text(v, -0.45, s, fontsize=12, ha="center")
    ang = np.degrees(np.arctan2(Ixy, Ix - C))
    ax.add_patch(Wedge((C, 0), 0.7, 0, ang, fill=False, lw=1, color="k"))
    ax.text(C + 0.8, 0.25, r"$2\theta_p$", fontsize=12)
    ax.text(C + 0.15, -R / 2, "$R$", fontsize=12)
    ax.plot([C, C], [0, -R], "k:", lw=0.8)


# ----------------------------------------------------------------- fórmulas
F = r"\frac"
FIGURAS = {
    "Rectángulo": (d_rectangulo, [
        r"$A = bh \qquad \bar{x} = b/2 \qquad \bar{y} = h/2$",
        r"$\bar{I}_x = \frac{bh^3}{12} \qquad \bar{I}_y = \frac{b^3h}{12} \qquad \bar{I}_{xy} = 0$",
        r"$I_x = \frac{bh^3}{3} \qquad I_y = \frac{b^3h}{3} \qquad I_{xy} = \frac{b^2h^2}{4}$",
        r"$\bar{J}_C = \frac{bh}{12}\,(b^2 + h^2)$",
    ]),
    "Círculo": (d_circulo, [
        r"$A = \pi R^2 \qquad C$ en el centro",
        r"$I_x = I_y = \frac{\pi R^4}{4} \qquad I_{xy} = 0$",
        r"$J_C = \frac{\pi R^4}{2}$",
        r"$I_{tangente} = \frac{5\pi R^4}{4}$",
    ]),
    "Media parábola compl.": (d_spandrel, [
        r"$y = kx^2 \qquad A = \frac{1}{3}bh$",
        r"$\bar{x} = \frac{3b}{4} \qquad \bar{y} = \frac{3h}{10}$",
        r"$\bar{I}_x = \frac{37bh^3}{2100} \qquad \bar{I}_y = \frac{b^3h}{80} \qquad \bar{I}_{xy} = \frac{b^2h^2}{120}$",
        r"$I_x = \frac{bh^3}{21} \qquad I_y = \frac{b^3h}{5} \qquad I_{xy} = \frac{b^2h^2}{12}$",
    ]),
    "Triángulo rectángulo": (d_tri_rect, [
        r"$A = \frac{1}{2}bh \qquad \bar{x} = \frac{b}{3} \qquad \bar{y} = \frac{h}{3}$",
        r"$\bar{I}_x = \frac{bh^3}{36} \qquad \bar{I}_y = \frac{b^3h}{36} \qquad \bar{I}_{xy} = -\frac{b^2h^2}{72}$",
        r"$I_x = \frac{bh^3}{12} \qquad I_y = \frac{b^3h}{12} \qquad I_{xy} = \frac{b^2h^2}{24}$",
        r"(el signo de $\bar{I}_{xy}$ cambia si la hipotenusa va al otro lado)",
    ]),
    "Semicírculo": (d_semicirculo, [
        r"$A = \frac{\pi R^2}{2} \qquad \bar{x} = 0 \qquad \bar{y} = \frac{4R}{3\pi}$",
        r"$\bar{I}_x = 0.1098\,R^4 \qquad \bar{I}_y = \frac{\pi R^4}{8} \qquad \bar{I}_{xy} = 0$",
        r"$I_x = I_y = \frac{\pi R^4}{8} \qquad I_{xy} = 0$",
        r"$J_O = \frac{\pi R^4}{4}$",
    ]),
    "Media parábola": (d_media_parabola, [
        r"$y = kx^2 \qquad A = \frac{2}{3}bh$",
        r"$\bar{x} = \frac{3b}{8} \qquad \bar{y} = \frac{3h}{5}$",
        r"$\bar{I}_x = \frac{8bh^3}{175} \qquad \bar{I}_y = \frac{19b^3h}{480} \qquad \bar{I}_{xy} = \frac{b^2h^2}{60}$",
        r"$I_x = \frac{2bh^3}{7} \qquad I_y = \frac{2b^3h}{15} \qquad I_{xy} = \frac{b^2h^2}{6}$",
    ]),
    "Triángulo isósceles": (d_isosceles, [
        r"$A = \frac{1}{2}bh \qquad \bar{x} = 0 \qquad \bar{y} = \frac{h}{3}$",
        r"$\bar{I}_x = \frac{bh^3}{36} \qquad \bar{I}_y = \frac{b^3h}{48} \qquad \bar{I}_{xy} = 0$",
        r"$I_x = \frac{bh^3}{12} \qquad I_{xy} = 0$",
        r"(eje $x$ en la base)",
    ]),
    "Cuarto de círculo": (d_cuarto_circulo, [
        r"$A = \frac{\pi R^2}{4} \qquad \bar{x} = \bar{y} = \frac{4R}{3\pi}$",
        r"$\bar{I}_x = \bar{I}_y = 0.05488\,R^4 \qquad \bar{I}_{xy} = -0.01647\,R^4$",
        r"$I_x = I_y = \frac{\pi R^4}{16} \qquad I_{xy} = \frac{R^4}{8}$",
        r"$J_O = \frac{\pi R^4}{8}$",
    ]),
    "Sector circular": (d_sector, [
        r"$A = \alpha R^2 \quad (\alpha$ = medio ángulo, en radianes$)$",
        r"$\bar{x} = \frac{2R\,\sin\alpha}{3\alpha} \qquad \bar{y} = 0$",
        r"$I_x = \bar{I}_x = \frac{R^4}{8}\,(2\alpha - \sin 2\alpha)$",
        r"$I_y = \frac{R^4}{8}\,(2\alpha + \sin 2\alpha) \qquad I_{xy} = 0$",
        r"$\bar{I}_y = I_y - A\,\bar{x}^2$",
    ]),
    "Triángulo": (d_triangulo, [
        r"$A = \frac{1}{2}bh \qquad \bar{x} = \frac{a+b}{3} \qquad \bar{y} = \frac{h}{3}$",
        r"$\bar{I}_x = \frac{bh^3}{36} \qquad I_x = \frac{bh^3}{12}$",
        r"$\bar{I}_y = \frac{bh}{36}\,(a^2 - ab + b^2) \qquad I_y = \frac{bh}{12}\,(a^2 + ab + b^2)$",
        r"$\bar{I}_{xy} = \frac{bh^2}{72}\,(2a - b) \qquad I_{xy} = \frac{bh^2}{24}\,(2a + b)$",
    ]),
    "Cuarto de elipse": (d_cuarto_elipse, [
        r"$A = \frac{\pi ab}{4} \qquad \bar{x} = \frac{4a}{3\pi} \qquad \bar{y} = \frac{4b}{3\pi}$",
        r"$\bar{I}_x = 0.05488\,ab^3 \qquad \bar{I}_y = 0.05488\,a^3b$",
        r"$\bar{I}_{xy} = -0.01647\,a^2b^2$",
        r"$I_x = \frac{\pi ab^3}{16} \qquad I_y = \frac{\pi a^3b}{16} \qquad I_{xy} = \frac{a^2b^2}{8}$",
    ]),
    "Círculo de Mohr": (d_mohr, [
        r"Centro: $C = \frac{I_x + I_y}{2}$",
        r"Radio: $R = \sqrt{\left(\frac{I_x - I_y}{2}\right)^2 + I_{xy}^2}$",
        r"$I_{max,\,min} = C \pm R \qquad \tan 2\theta_p = -\frac{2I_{xy}}{I_x - I_y}$",
        r"$I_u = C + \frac{I_x - I_y}{2}\cos 2\theta - I_{xy}\sin 2\theta$",
        r"$I_v = C - \frac{I_x - I_y}{2}\cos 2\theta + I_{xy}\sin 2\theta$",
        r"$I_{uv} = \frac{I_x - I_y}{2}\sin 2\theta + I_{xy}\cos 2\theta$",
        r"$I_u + I_v = I_x + I_y = J_O$ (invariante)",
        r"Steiner: $I_x = \bar{I}_x + A\,d_y^2 \qquad I_{xy} = \bar{I}_{xy} + A\,d_x d_y$",
    ]),
}

# ----------------------------------------------------------------- tabla de áreas compuestas
EJEMPLO = [  # (figura, x̄, ȳ, A)  -> A negativa = hueco que se resta
    ("Rectángulo 240x120", 120, 60, 240 * 120),
    ("Semicírculo R=90 (hueco)", 120, 120 - 4 * 90 / (3 * np.pi), -np.pi * 90**2 / 2),
]


def tabla_compuesta(filas):
    """Devuelve filas con A·x̄, A·ȳ, las sumas y el centroide X̄, Ȳ."""
    res = [(n, x, y, A, A * x, A * y) for n, x, y, A in filas]
    SA = sum(r[3] for r in res)
    SAx = sum(r[4] for r in res)
    SAy = sum(r[5] for r in res)
    return res, SA, SAx, SAy, SAx / SA, SAy / SA


def d_tabla(ax, filas=None):
    res, SA, SAx, SAy, X, Y = tabla_compuesta(filas or EJEMPLO)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    enc = ["Fig", r"$\bar{x}$", r"$\bar{y}$", "$A$", r"$A\bar{x}$", r"$A\bar{y}$"]
    cols = [0.0, 0.36, 0.46, 0.59, 0.76, 0.93]
    fmt = lambda v: f"{v:,.0f}" if abs(v) >= 1000 else f"{v:,.4g}"
    y = 0.92
    for c, t in zip(cols, enc):
        ax.text(c, y, t, fontsize=13, weight="bold", ha="left" if c == 0 else "center")
    ax.plot([0, 1], [y - 0.04, y - 0.04], "k-", lw=1)
    for r in res:
        y -= 0.09
        ax.text(0, y, r[0], fontsize=8.5)
        for c, v in zip(cols[1:], r[1:]):
            ax.text(c, y, fmt(v), fontsize=9,
                    ha="center", color="#c0392b" if v < 0 and c > 0.6 else "k")
    y -= 0.06
    ax.plot([0.58, 1], [y, y], "k-", lw=1)
    y -= 0.06
    ax.text(0, y, r"$\Sigma$", fontsize=14)
    for c, v in zip(cols[3:], (SA, SAx, SAy)):
        ax.text(c, y, fmt(v), fontsize=9, ha="center", weight="bold")
    ax.text(0, y - 0.16, rf"$\bar{{X}} = \frac{{\Sigma A\bar{{x}}}}{{\Sigma A}} = {X:.3f}$", fontsize=15)
    ax.text(0, y - 0.30, rf"$\bar{{Y}} = \frac{{\Sigma A\bar{{y}}}}{{\Sigma A}} = {Y:.3f}$", fontsize=15)


FIGURAS["Tabla área compuesta"] = (d_tabla, [
    "Pasos para un área compuesta:",
    "1. Divide en figuras simples (los huecos con $A$ negativa)",
    r"2. Para cada una anota $\bar{x},\ \bar{y}$ (desde ejes comunes) y $A$",
    r"3. Multiplica: $A\bar{x}$ y $A\bar{y}$;  suma columnas",
    r"4. $\bar{X} = \frac{\Sigma A\bar{x}}{\Sigma A} \qquad \bar{Y} = \frac{\Sigma A\bar{y}}{\Sigma A}$",
    r"5. Inercia: $\bar{I}_X = \Sigma\,[\bar{I}_{x,i} + A_i(\bar{y}_i - \bar{Y})^2]$",
    r"$\quad\ \bar{I}_Y = \Sigma\,[\bar{I}_{y,i} + A_i(\bar{x}_i - \bar{X})^2]$",
    r"$\quad\ \bar{I}_{XY} = \Sigma\,[\bar{I}_{xy,i} + A_i(\bar{x}_i-\bar{X})(\bar{y}_i-\bar{Y})]$",
    "Ejemplo: rectángulo 240×120 menos semicírculo R = 90",
    "Para resolver la tuya: menú 2 → Dibujar figura compuesta",
])



COMUNES = [
    r"$J_O = I_x + I_y \qquad k_x = \sqrt{I_x/A} \qquad k_y = \sqrt{I_y/A}$",
    r"Steiner: $I = \bar{I} + A\,d^2 \qquad I_{xy} = \bar{I}_{xy} + A\,\bar{x}\,\bar{y}$",
]


# =============================================================================
#  NUCLEO DE CALCULO  (Python puro: funciona igual en el PC y en la TI-Nspire)
# =============================================================================
from math import pi, sin, cos, sqrt, atan2

FIG = [
    ("rect", "Rectangulo", "b h"),
    ("circulo", "Circulo", "R"),
    ("semicirculo", "Semicirculo", "R"),
    ("tri_rect", "Triangulo rectangulo", "b h"),
    ("tri_iso", "Triangulo isosceles", "b h"),
    ("triangulo", "Triangulo general", "a b h"),
    ("cuarto_circ", "Cuarto de circulo", "R"),
    ("cuarto_elipse", "Cuarto de elipse", "a b"),
    ("sector", "Sector circular", "R alfa"),
    ("parab_compl", "Media parabola complementaria", "b h"),
    ("media_parab", "Media parabola", "b h"),
    ("poligono", "Poligono libre (escribes los vertices)", ""),
]

AYUDA_PAR = {
    "b": "base b", "h": "altura h", "R": "radio R",
    "a": "a = distancia horizontal al vertice de arriba",
    "alfa": "alfa = MEDIO angulo del sector, en grados",
}

# formulas (ejes locales, respecto al centroide): A, xc, yc, Ixc, Iyc, Ixyc
FORM = {
    "rect": ["b*h", "b/2", "h/2", "b*h^3/12", "b^3*h/12", "0"],
    "circulo": ["pi*R^2", "0 (centro)", "0 (centro)", "pi*R^4/4", "pi*R^4/4", "0"],
    "semicirculo": ["pi*R^2/2", "0", "4R/(3pi)", "pi*R^4/8 - 8R^4/(9pi)", "pi*R^4/8", "0"],
    "tri_rect": ["b*h/2", "b/3", "h/3", "b*h^3/36", "b^3*h/36", "-b^2*h^2/72"],
    "tri_iso": ["b*h/2", "0 (centro base)", "h/3", "b*h^3/36", "b^3*h/48", "0"],
    "triangulo": ["b*h/2", "(a+b)/3", "h/3", "b*h^3/36", "b*h*(a^2-ab+b^2)/36", "b*h^2*(2a-b)/72"],
    "cuarto_circ": ["pi*R^2/4", "4R/(3pi)", "4R/(3pi)", "0.05488*R^4", "0.05488*R^4", "-0.01647*R^4"],
    "cuarto_elipse": ["pi*a*b/4", "4a/(3pi)", "4b/(3pi)", "0.05488*a*b^3", "0.05488*a^3*b",
                      "-0.01647*a^2*b^2"],
    "sector": ["alfa*R^2 (alfa en rad)", "2R*sin(alfa)/(3alfa)", "0", "R^4/8*(2alfa - sin2alfa)",
               "R^4/8*(2alfa + sin2alfa) - A*xc^2", "0"],
    "parab_compl": ["b*h/3", "3b/4", "3h/10", "37*b*h^3/2100", "b^3*h/80", "b^2*h^2/120"],
    "media_parab": ["2*b*h/3", "3b/8", "3h/5", "8*b*h^3/175", "19*b^3*h/480", "b^2*h^2/60"],
    "poligono": ["formula de Gauss (shoelace)"] * 6,
}


def f(v):
    """Formato corto de numeros."""
    if abs(v) < 1e-9:
        return "0"
    if 1e5 <= abs(v) < 1e13:
        return "%.0f" % v
    return "%.6g" % v


def nombre_fig(clave):
    for k, n, p in FIG:
        if k == clave:
            return n
    return clave


def params_fig(clave):
    for k, n, p in FIG:
        if k == clave:
            return p.split()
    return []


def arco(cx, cy, rx, ry, a0, a1, n):
    return [(cx + rx * cos(a0 + (a1 - a0) * i / n), cy + ry * sin(a0 + (a1 - a0) * i / n))
            for i in range(n + 1)]


def props_poligono(P):
    A = cx = cy = ix = iy = ixy = 0.0
    n = len(P)
    for i in range(n):
        x0, y0 = P[i]
        x1, y1 = P[(i + 1) % n]
        c = x0 * y1 - x1 * y0
        A += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
        ix += (y0 * y0 + y0 * y1 + y1 * y1) * c
        iy += (x0 * x0 + x0 * x1 + x1 * x1) * c
        ixy += (x0 * y1 + 2 * x0 * y0 + 2 * x1 * y1 + x1 * y0) * c
    A /= 2.0
    cx /= 6.0 * A
    cy /= 6.0 * A
    ix /= 12.0
    iy /= 12.0
    ixy /= 24.0
    if A < 0:
        A, ix, iy, ixy = -A, -ix, -iy, -ixy
    return A, cx, cy, ix - A * cy * cy, iy - A * cx * cx, ixy - A * cx * cy


def forma(clave, d, n=24):
    """Propiedades en ejes locales + contorno P + puntos notables V=[(nombre,x,y)]."""
    if clave == "rect":
        b, h = d
        P = [(0, 0), (b, 0), (b, h), (0, h)]
        V = [("esquina inf-izq", 0, 0), ("esquina inf-der", b, 0), ("esquina sup-der", b, h),
             ("esquina sup-izq", 0, h), ("centro", b / 2.0, h / 2.0)]
        return b * h, b / 2.0, h / 2.0, b * h ** 3 / 12.0, b ** 3 * h / 12.0, 0.0, P, V
    if clave == "circulo":
        R = d[0]
        P = arco(0, 0, R, R, 0, 2 * pi, 2 * n)[:-1]
        V = [("centro", 0, 0), ("izquierda", -R, 0), ("derecha", R, 0), ("abajo", 0, -R), ("arriba", 0, R)]
        return pi * R * R, 0.0, 0.0, pi * R ** 4 / 4, pi * R ** 4 / 4, 0.0, P, V
    if clave == "semicirculo":
        R = d[0]
        P = arco(0, 0, R, R, 0, pi, n)
        V = [("extremo izq del diametro", -R, 0), ("extremo der del diametro", R, 0),
             ("centro del diametro", 0, 0), ("punto mas alto", 0, R)]
        return (pi * R * R / 2, 0.0, 4 * R / (3 * pi), pi * R ** 4 / 8 - 8 * R ** 4 / (9 * pi),
                pi * R ** 4 / 8, 0.0, P, V)
    if clave in ("tri_rect", "tri_iso", "triangulo"):
        if clave == "tri_rect":
            a = 0.0
            b, h = d
        elif clave == "tri_iso":
            b, h = d
            a = b / 2.0
        else:
            a, b, h = d
        dx = -b / 2.0 if clave == "tri_iso" else 0.0
        P = [(dx, 0), (b + dx, 0), (a + dx, h)]
        if clave == "tri_rect":
            V = [("angulo recto", 0, 0), ("esquina der (base)", b, 0), ("vertice de arriba", 0, h)]
        else:
            V = [("esquina izq (base)", dx, 0), ("esquina der (base)", b + dx, 0),
                 ("vertice de arriba", a + dx, h)]
            if clave == "tri_iso":
                V.append(("centro de la base", 0, 0))
        return (b * h / 2.0, (a + b) / 3.0 + dx, h / 3.0, b * h ** 3 / 36.0,
                b * h * (a * a - a * b + b * b) / 36.0, b * h * h * (2 * a - b) / 72.0, P, V)
    if clave == "cuarto_circ":
        R = d[0]
        k = 4 * R / (3 * pi)
        I = pi * R ** 4 / 16 - 4 * R ** 4 / (9 * pi)
        P = [(0, 0)] + arco(0, 0, R, R, 0, pi / 2, n)
        V = [("centro (esquina)", 0, 0), ("extremo derecho", R, 0), ("extremo de arriba", 0, R)]
        return pi * R * R / 4, k, k, I, I, R ** 4 / 8 - 4 * R ** 4 / (9 * pi), P, V
    if clave == "cuarto_elipse":
        a, b = d
        P = [(0, 0)] + arco(0, 0, a, b, 0, pi / 2, n)
        V = [("centro (esquina)", 0, 0), ("extremo derecho", a, 0), ("extremo de arriba", 0, b)]
        return (pi * a * b / 4, 4 * a / (3 * pi), 4 * b / (3 * pi),
                pi * a * b ** 3 / 16 - 4 * a * b ** 3 / (9 * pi),
                pi * a ** 3 * b / 16 - 4 * a ** 3 * b / (9 * pi),
                a * a * b * b / 8 - 4 * a * a * b * b / (9 * pi), P, V)
    if clave == "sector":
        R, al = d
        al = al * pi / 180
        A = al * R * R
        xc = 2 * R * sin(al) / (3 * al)
        P = [(0, 0)] + arco(0, 0, R, R, -al, al, n)
        V = [("vertice", 0, 0), ("punta (eje)", R, 0), ("extremo inferior", R * cos(al), -R * sin(al)),
             ("extremo superior", R * cos(al), R * sin(al))]
        return (A, xc, 0.0, R ** 4 / 8 * (2 * al - sin(2 * al)),
                R ** 4 / 8 * (2 * al + sin(2 * al)) - A * xc * xc, 0.0, P, V)
    if clave == "parab_compl":
        b, h = d
        P = [(b * i / n, h * (i / float(n)) ** 2) for i in range(n + 1)] + [(b, 0)]
        V = [("vertice de la parabola", 0, 0), ("esquina inf-der", b, 0), ("esquina sup-der", b, h)]
        return (b * h / 3.0, 3 * b / 4.0, 3 * h / 10.0, 37 * b * h ** 3 / 2100.0, b ** 3 * h / 80.0,
                b * b * h * h / 120.0, P, V)
    if clave == "media_parab":
        b, h = d
        P = [(b * i / n, h * (i / float(n)) ** 2) for i in range(n + 1)] + [(0, h)]
        V = [("vertice de la parabola", 0, 0), ("esquina sup-der", b, h), ("esquina sup-izq", 0, h)]
        return (2 * b * h / 3.0, 3 * b / 8.0, 3 * h / 5.0, 8 * b * h ** 3 / 175.0, 19 * b ** 3 * h / 480.0,
                b * b * h * h / 60.0, P, V)
    if clave == "poligono":
        P = [tuple(q) for q in d]
        A, xc, yc, Ix, Iy, Ixy = props_poligono(P)
        V = [("vertice %d" % (i + 1), P[i][0], P[i][1]) for i in range(len(P))]
        return A, xc, yc, Ix, Iy, Ixy, P, V
    raise ValueError("Figura desconocida: " + str(clave))


def nueva_pieza(clave, d):
    return {"clave": clave, "d": d, "eh": False, "ev": False, "giro": 0, "hueco": False,
            "tx": 0.0, "ty": 0.0, "ancla": None, "destino": (0.0, 0.0)}


def _cs(giro):
    g = giro % 360
    tabla = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}
    if g in tabla:
        return tabla[g]
    t = giro * pi / 180
    return cos(t), sin(t)


def calcular(p):
    """Aplica espejo -> giro -> traslacion. Devuelve propiedades GLOBALES de la pieza."""
    A, xc, yc, Ix, Iy, Ixy, P, V = forma(p["clave"], p["d"])
    c, s = _cs(p["giro"])

    def tr(x, y):
        if p["eh"]:
            x = -x
        if p["ev"]:
            y = -y
        return (c * x - s * y + p["tx"], s * x + c * y + p["ty"])

    if p["eh"]:
        xc, Ixy = -xc, -Ixy
    if p["ev"]:
        yc, Ixy = -yc, -Ixy
    xg, yg = c * xc - s * yc + p["tx"], s * xc + c * yc + p["ty"]
    C, D = (Ix + Iy) / 2.0, (Ix - Iy) / 2.0
    c2, s2 = c * c - s * s, 2 * s * c
    Ix, Iy, Ixy = C + D * c2 + Ixy * s2, C - D * c2 - Ixy * s2, -D * s2 + Ixy * c2
    esc = abs(Ix) + abs(Iy)
    if abs(Ixy) < 1e-12 * esc:
        Ixy = 0.0
    k = -1 if p["hueco"] else 1
    return {"A": k * A, "x": xg, "y": yg, "Ix": k * Ix, "Iy": k * Iy, "Ixy": k * Ixy,
            "P": [tr(x, y) for (x, y) in P], "V": [(n, tr(x, y)) for (n, x, y) in V]}


def colocar(p):
    """Mueve la pieza para que su punto de anclaje quede en p['destino'].
    ancla = None -> la esquina inferior izquierda del rectangulo que la encierra."""
    p["tx"], p["ty"] = 0.0, 0.0
    g = calcular(p)
    if p["ancla"] is None:
        ax = min(q[0] for q in g["P"])
        ay = min(q[1] for q in g["P"])
    else:
        ax, ay = g["V"][p["ancla"]][1]
    p["tx"] = p["destino"][0] - ax
    p["ty"] = p["destino"][1] - ay


def describir(p):
    nom = nombre_fig(p["clave"])
    if p["clave"] == "poligono":
        txt = nom.split(" (")[0] + " de %d vertices" % len(p["d"])
    else:
        txt = nom + " " + " ".join("%s=%s" % (n, f(v)) for n, v in zip(params_fig(p["clave"]), p["d"]))
    extra = []
    if p["giro"] % 360:
        extra.append("girada %g grados" % (p["giro"] % 360))
    if p["eh"]:
        extra.append("espejo horizontal")
    if p["ev"]:
        extra.append("espejo vertical")
    if p["hueco"]:
        extra.append("HUECO")
    if extra:
        txt += " (" + ", ".join(extra) + ")"
    return txt


def lista_vertices(piezas):
    """Todos los puntos notables de todas las piezas, sin repetir."""
    out = []
    for i in range(len(piezas)):
        for (n, (x, y)) in calcular(piezas[i])["V"]:
            rep = False
            for q in out:
                if abs(q[0] - x) < 1e-7 and abs(q[1] - y) < 1e-7:
                    rep = True
                    break
            if not rep:
                out.append((x, y, "pieza %d: %s" % (i + 1, n)))
    return out


def resolver(piezas):
    G = [calcular(p) for p in piezas]
    SA = sum(g["A"] for g in G)
    SAx = sum(g["A"] * g["x"] for g in G)
    SAy = sum(g["A"] * g["y"] for g in G)
    X, Y = SAx / SA, SAy / SA
    for g in G:
        g["dx"], g["dy"] = g["x"] - X, g["y"] - Y
        g["IX"] = g["Ix"] + g["A"] * g["dy"] ** 2
        g["IY"] = g["Iy"] + g["A"] * g["dx"] ** 2
        g["IXY"] = g["Ixy"] + g["A"] * g["dx"] * g["dy"]
    IX = sum(g["IX"] for g in G)
    IY = sum(g["IY"] for g in G)
    IXY = sum(g["IXY"] for g in G)
    if abs(IXY) < 1e-9 * (abs(IX) + abs(IY)):
        IXY = 0.0
    return G, {"A": SA, "SAx": SAx, "SAy": SAy, "X": X, "Y": Y, "IX": IX, "IY": IY, "IXY": IXY}


def mohr(Ix, Iy, Ixy, th=None):
    C = (Ix + Iy) / 2.0
    D = (Ix - Iy) / 2.0
    R = sqrt(D * D + Ixy * Ixy)
    tp = 0.5 * atan2(-2 * Ixy, Ix - Iy) * 180 / pi
    if tp <= -89.999:
        tp += 180
    r = {"C": C, "D": D, "R": R, "Imax": C + R, "Imin": C - R, "tp": tp, "tp2": tp + 90 if tp <= 0 else tp - 90}
    if th is not None:
        t = 2 * th * pi / 180
        r["th"] = th
        r["Iu"] = C + D * cos(t) - Ixy * sin(t)
        r["Iv"] = C - D * cos(t) + Ixy * sin(t)
        r["Iuv"] = D * sin(t) + Ixy * cos(t)
    return r


def pasos_mohr(Ix, Iy, Ixy, th=None):
    m = mohr(Ix, Iy, Ixy, th)
    L = ["CIRCULO DE MOHR",
         "Datos: Ix = %s   Iy = %s   Ixy = %s" % (f(Ix), f(Iy), f(Ixy)),
         "1) Centro  C = (Ix+Iy)/2 = (%s + %s)/2 = %s" % (f(Ix), f(Iy), f(m["C"])),
         "2) (Ix-Iy)/2 = (%s - %s)/2 = %s" % (f(Ix), f(Iy), f(m["D"])),
         "3) Radio  R = sqrt( ((Ix-Iy)/2)^2 + Ixy^2 )",
         "         = sqrt( (%s)^2 + (%s)^2 ) = %s" % (f(m["D"]), f(Ixy), f(m["R"])),
         "4) Imax = C + R = %s + %s = %s" % (f(m["C"]), f(m["R"]), f(m["Imax"])),
         "   Imin = C - R = %s - %s = %s" % (f(m["C"]), f(m["R"]), f(m["Imin"])),
         "5) tan(2 tp) = -2 Ixy/(Ix-Iy) = -2(%s)/(%s)" % (f(Ixy), f(Ix - Iy)),
         "   tp = %s grados (antihorario desde x) -> eje de Imax" % f(m["tp"]),
         "   el eje de Imin esta a %s grados" % f(m["tp2"]),
         "   Comprobacion: Imax + Imin = Ix + Iy = %s" % f(Ix + Iy)]
    if th is not None:
        L += ["6) Ejes girados theta = %s grados:" % f(th),
              "   Iu  = C + (Ix-Iy)/2 cos2t - Ixy sin2t = %s" % f(m["Iu"]),
              "   Iv  = C - (Ix-Iy)/2 cos2t + Ixy sin2t = %s" % f(m["Iv"]),
              "   Iuv = (Ix-Iy)/2 sin2t + Ixy cos2t   = %s" % f(m["Iuv"])]
    return L


def pasos_compuesta(piezas):
    G, T = resolver(piezas)
    L = ["=" * 60, "PASO 1. Propiedades de cada pieza (respecto a SU centroide)", "=" * 60]
    for i in range(len(piezas)):
        p, g = piezas[i], G[i]
        fo = FORM[p["clave"]]
        L.append("Pieza %d: %s" % (i + 1, describir(p)))
        if p["clave"] != "poligono":
            L.append("   A = %s = %s%s" % (fo[0], f(abs(g["A"])), "  -> negativa por ser hueco" if p["hueco"] else ""))
            L.append("   formulas: Ixc = %s,  Iyc = %s,  Ixyc = %s" % (fo[3], fo[4], fo[5]))
        else:
            L.append("   A = %s (formula de Gauss con los vertices)" % f(abs(g["A"])))
        L.append("   centroide en la figura: x = %s   y = %s" % (f(g["x"]), f(g["y"])))
        g90 = p["giro"] % 180 == 90
        if g90:
            L.append("   girada 90/270: se intercambian Ixc <-> Iyc y Ixyc cambia de signo")
        if p["eh"] != p["ev"]:
            L.append("   un espejo: Ixyc cambia de signo")
        L.append("   Ixc = %s   Iyc = %s   Ixyc = %s" % (f(g["Ix"]), f(g["Iy"]), f(g["Ixy"])))
    L += ["", "=" * 60, "PASO 2. Tabla y centroide de la figura completa", "=" * 60,
          "Pz |      A      |    x    |    y    |     A*x     |     A*y"]
    for i in range(len(G)):
        g = G[i]
        L.append("%2d | %11s | %7s | %7s | %11s | %11s" % (i + 1, f(g["A"]), f(g["x"]), f(g["y"]),
                                                          f(g["A"] * g["x"]), f(g["A"] * g["y"])))
    L.append("SUMA %11s |         |         | %11s | %11s" % (f(T["A"]), f(T["SAx"]), f(T["SAy"])))
    L += ["X = SUMA(A*x)/SUMA(A) = %s / %s = %s" % (f(T["SAx"]), f(T["A"]), f(T["X"])),
          "Y = SUMA(A*y)/SUMA(A) = %s / %s = %s" % (f(T["SAy"]), f(T["A"]), f(T["Y"])),
          "", "=" * 60, "PASO 3. Steiner: llevar cada pieza al centroide (X, Y)", "=" * 60,
          "dx = x - X     dy = y - Y"]
    for i in range(len(G)):
        g = G[i]
        L += ["Pieza %d:  dx = %s - %s = %s    dy = %s - %s = %s" % (
            i + 1, f(g["x"]), f(T["X"]), f(g["dx"]), f(g["y"]), f(T["Y"]), f(g["dy"])),
            "   IX  = Ixc + A dy^2   = %s + (%s)(%s)^2 = %s" % (f(g["Ix"]), f(g["A"]), f(g["dy"]), f(g["IX"])),
            "   IY  = Iyc + A dx^2   = %s + (%s)(%s)^2 = %s" % (f(g["Iy"]), f(g["A"]), f(g["dx"]), f(g["IY"])),
            "   IXY = Ixyc + A dx dy = %s + (%s)(%s)(%s) = %s" % (
                f(g["Ixy"]), f(g["A"]), f(g["dx"]), f(g["dy"]), f(g["IXY"]))]
    L += ["", "=" * 60, "PASO 4. Sumas (respecto a los ejes centroidales de la figura)", "=" * 60,
          "IX  = %s" % f(T["IX"]), "IY  = %s" % f(T["IY"]), "IXY = %s" % f(T["IXY"]),
          "J   = IX + IY = %s" % f(T["IX"] + T["IY"]),
          "Respecto al origen (0,0):  Ix = IX + A Y^2 = %s" % f(T["IX"] + T["A"] * T["Y"] ** 2),
          "                           Iy = IY + A X^2 = %s" % f(T["IY"] + T["A"] * T["X"] ** 2),
          "                           Ixy = IXY + A X Y = %s" % f(T["IXY"] + T["A"] * T["X"] * T["Y"]),
          "", "=" * 60, "PASO 5. " + pasos_mohr(T["IX"], T["IY"], T["IXY"])[0], "=" * 60]
    L += pasos_mohr(T["IX"], T["IY"], T["IXY"])[1:]
    return L

# =============================================================================
#  INTERFAZ PARA EL COMPUTADOR  (menús en la terminal + ventana de vista previa)
# =============================================================================
MAPA = {"rect": "Rectángulo", "circulo": "Círculo", "semicirculo": "Semicírculo",
        "tri_rect": "Triángulo rectángulo", "tri_iso": "Triángulo isósceles", "triangulo": "Triángulo",
        "cuarto_circ": "Cuarto de círculo", "cuarto_elipse": "Cuarto de elipse",
        "sector": "Sector circular", "parab_compl": "Media parábola compl.",
        "media_parab": "Media parábola"}
NARANJA = "#e67e22"
ROJO = "#c0392b"
VERDE = "#27ae60"
FIGV = None
plt.ion()


# ----------------------------------------------------------------- entrada de datos
def linea(t=""):
    print("\n" + "─" * 64 + ("\n " + t + "\n" + "─" * 64 if t else ""))


def leer_num(msg, defecto=None, positivo=False):
    while True:
        extra = f" [Enter = {defecto}]" if defecto is not None else ""
        s = input(f"{msg}{extra}: ").strip()
        if s == "" and defecto is not None:
            return defecto
        try:
            v = float(eval(s, {"__builtins__": {}}, {"pi": pi, "sqrt": sqrt, "sin": sin, "cos": cos}))
            if positivo and v <= 0:
                print("   ✗ Debe ser mayor que 0.")
                continue
            return v
        except Exception:
            print("   ✗ Escribe un número (puedes usar operaciones: 240/2, 3*pi, sqrt(2)).")


def leer_opcion(msg, validas, defecto=None):
    validas = [str(v) for v in validas]
    while True:
        extra = f" [Enter = {defecto}]" if defecto is not None else ""
        s = input(f"{msg}{extra}: ").strip()
        if s == "" and defecto is not None:
            return str(defecto)
        if s in validas:
            return s
        print("   ✗ Opción no válida. Escribe uno de: " + ", ".join(validas))


def pausa(msg="Presiona Enter para continuar"):
    input(f"\n   {msg}...")


# ----------------------------------------------------------------- ventana
def ventana():
    global FIGV
    if FIGV is None or not plt.fignum_exists(FIGV.number):
        FIGV = plt.figure("Momentos de inercia", figsize=(15, 8.2))
    return FIGV


def refrescar():
    FIGV.canvas.draw_idle()
    plt.pause(0.2)


def hoja_formulas(ax_dib, ax_txt, nombre, grande=True):
    """Dibujo de referencia + fórmulas de UNA figura (de la hoja de fórmulas)."""
    dibujar, formulas = FIGURAS[nombre]
    dibujar(ax_dib)
    if dibujar is not d_tabla:
        ax_dib.set_aspect("equal")
        ax_dib.autoscale_view()
    ax_dib.axis("off")
    ax_dib.set_title(nombre, fontsize=15 if grande else 12, weight="bold")
    ax_txt.axis("off")
    extra = [] if nombre in ("Círculo de Mohr", "Tabla área compuesta") or not grande else [""] + COMUNES
    lineas = formulas + extra
    paso = min(0.12 if grande else 0.16, 0.97 / max(len(lineas), 1))
    for i, s in enumerate(lineas):
        ax_txt.text(0, 0.97 - i * paso, s, va="top",
                    fontsize=(15 if grande else 12.5) if i < len(formulas) else 11,
                    color="k" if i < len(formulas) else "#555")


def dibujar_compuesta(ax, piezas, cand=None, vertices=True, res=None):
    todos = [calcular(p) for p in piezas]
    gc = calcular(cand) if cand else None
    pts = [q for g in todos + ([gc] if gc else []) for q in g["P"]] or [(0, 0), (1, 1)]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    L = max(max(xs) - min(xs), max(ys) - min(ys), 1e-9)
    for p, g in sorted(zip(piezas, todos), key=lambda t: t[0]["hueco"]):
        ax.add_patch(Polygon(g["P"], closed=True, fc="white" if p["hueco"] else AZUL,
                             ec=BORDE, lw=1.5, ls="--" if p["hueco"] else "-", zorder=2))
    for i, g in enumerate(todos):
        ax.plot(g["x"], g["y"], "x", color="#777", zorder=3)
        ax.text(g["x"], g["y"], f" c{i+1}", color="#777", fontsize=9, zorder=3)
    if vertices:
        for k, (x, y, _) in enumerate(lista_vertices(piezas)):
            ax.plot(x, y, "o", color="k", ms=5, zorder=4)
            ax.text(x + 0.015 * L, y + 0.015 * L, str(k + 1), fontsize=11, weight="bold", zorder=6,
                    bbox=dict(fc="#fff7c2", ec="k", lw=0.6, boxstyle="round,pad=0.2"))
    if gc:
        ax.add_patch(Polygon(gc["P"], closed=True, fc="white" if cand["hueco"] else NARANJA,
                             alpha=0.55, ec=NARANJA, lw=2.2, ls="--" if cand["hueco"] else "-", zorder=5))
        for j, (n, (x, y)) in enumerate(gc["V"]):
            ax.plot(x, y, "s", color=NARANJA, ms=6, zorder=7)
            ax.text(x - 0.012 * L, y - 0.03 * L, f"p{j+1}", color=NARANJA, fontsize=11,
                    weight="bold", ha="right", zorder=7)
    if res:
        X, Y = res["X"], res["Y"]
        ax.plot(X, Y, "o", color=ROJO, ms=9, zorder=8)
        ax.text(X, Y, f"  C ({f(X)}, {f(Y)})", color=ROJO, fontsize=12, weight="bold", zorder=8)
        for (ux, uy, est, col) in [(1, 0, ":", ROJO), (0, 1, ":", ROJO)]:
            ax.plot([X - ux * L * .6, X + ux * L * .6], [Y - uy * L * .6, Y + uy * L * .6], est, color=col, lw=1)
        t = np.radians(res["tp"])
        ax.plot([X - np.cos(t) * L * .6, X + np.cos(t) * L * .6],
                [Y - np.sin(t) * L * .6, Y + np.sin(t) * L * .6], "-", color=VERDE, lw=1.4)
        ax.text(X + np.cos(t) * L * .6, Y + np.sin(t) * L * .6, " eje Imax", color=VERDE)
    ax.axhline(0, color="k", lw=0.8, zorder=1)
    ax.axvline(0, color="k", lw=0.8, zorder=1)
    ax.set_xlim(min(xs) - 0.12 * L, max(xs) + 0.12 * L)
    ax.set_ylim(min(ys) - 0.12 * L, max(ys) + 0.12 * L)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.3)


def pantalla(piezas, cand=None, titulo="", vertices=True):
    fig = ventana()
    fig.clf()
    ax = fig.add_axes([0.03, 0.05, 0.56, 0.86])
    dibujar_compuesta(ax, piezas, cand, vertices)
    ax.set_title(titulo, fontsize=13)
    if cand:
        if cand["clave"] in MAPA:
            hoja_formulas(fig.add_axes([0.63, 0.52, 0.35, 0.40]), fig.add_axes([0.63, 0.03, 0.36, 0.45]),
                          MAPA[cand["clave"]], grande=False)
        else:
            a = fig.add_axes([0.63, 0.3, 0.35, 0.5])
            a.axis("off")
            a.text(0, 0.8, "Polígono libre", fontsize=15, weight="bold")
            a.text(0, 0.6, "Área, centroide e inercias con la\nfórmula de Gauss (shoelace)\n"
                   "a partir de los vértices.", fontsize=12, va="top")
    else:
        a = fig.add_axes([0.63, 0.05, 0.35, 0.86])
        a.axis("off")
        a.set_title("Piezas", fontsize=13, weight="bold", loc="left")
        for i, p in enumerate(piezas):
            a.text(0, 0.95 - i * 0.07, f"{i+1}. {describir(p)}", fontsize=10.5, va="top", wrap=True)
    refrescar()


# ----------------------------------------------------------------- 1. formulario
def menu_formulario():
    nombres = list(FIGURAS)
    while True:
        linea("FORMULARIO — elige una figura")
        for i, n in enumerate(nombres):
            print(f"  {i+1:>2}. {n}")
        print("   0. Volver")
        o = int(leer_opcion("Figura", range(len(nombres) + 1)))
        if o == 0:
            return
        fig = ventana()
        fig.clf()
        hoja_formulas(fig.add_axes([0.03, 0.08, 0.42, 0.82]), fig.add_axes([0.50, 0.04, 0.49, 0.88]),
                      nombres[o - 1])
        fig.text(0.5, 0.965, "Barra = respecto al centroide C;  sin barra = respecto a los ejes x, y",
                 ha="center", fontsize=10, color="#555")
        refrescar()
        print(f"\n   → Mira la ventana: {nombres[o-1]}")
        pausa("Enter para elegir otra figura")


# ----------------------------------------------------------------- 2. figura compuesta
def elegir_figura():
    linea("¿Qué figura vas a agregar?")
    for i, (k, n, par) in enumerate(FIG):
        print(f"  {i+1:>2}. {n:<40} {('datos: ' + par) if par else ''}")
    print("   0. Cancelar")
    o = int(leer_opcion("Figura", range(len(FIG) + 1)))
    return None if o == 0 else FIG[o - 1][0]


def pedir_medidas(clave):
    if clave == "poligono":
        n = int(leer_num("¿Cuántos vértices tiene?", positivo=True))
        print("   Escribe los vértices en orden (siguiendo el borde). El primero puede ser (0, 0).")
        P = []
        for i in range(n):
            P.append((leer_num(f"   Vértice {i+1}  x"), leer_num(f"   Vértice {i+1}  y")))
        return P
    d = []
    for par in params_fig(clave):
        d.append(leer_num(f"   {AYUDA_PAR.get(par, par)}", positivo=(par != "a")))
    return d


def elegir_punto(p, msg):
    V = calcular(p)["V"]
    print("\n   Puntos de la figura nueva (en NARANJA en la ventana):")
    for j, (n, _) in enumerate(V):
        print(f"     {j+1}. p{j+1} = {n}")
    return int(leer_opcion(msg, range(1, len(V) + 1), 1)) - 1


def ajustar(piezas, p, titulo):
    """Vista previa + girar / espejo / hueco antes de aceptar la pieza."""
    while True:
        colocar(p)
        pantalla(piezas, p, titulo)
        linea("VISTA PREVIA (figura en naranja)  →  " + describir(p))
        print("  [Enter] Aceptar así")
        print("   1. Espejo horizontal (izquierda ↔ derecha)")
        print("   2. Espejo vertical   (arriba ↔ abajo)")
        print("   3. Girar 90° (antihorario)")
        print(f"   4. Hueco: {'SÍ → cambiar a NO' if p['hueco'] else 'NO → cambiar a SÍ (se resta)'}")
        if p["ancla"] is not None:
            print("   5. Cambiar el punto de la figura que va en ese lugar")
        print("   6. Cambiar medidas")
        print("   0. Cancelar esta figura")
        o = leer_opcion("Opción", ["0", "1", "2", "3", "4", "5", "6"], "aceptar")
        if o == "aceptar":
            return p
        if o == "0":
            return None
        if o == "1":
            p["eh"] = not p["eh"]
        elif o == "2":
            p["ev"] = not p["ev"]
        elif o == "3":
            p["giro"] = (p["giro"] + 90) % 360
        elif o == "4":
            p["hueco"] = not p["hueco"]
        elif o == "5" and p["ancla"] is not None:
            p["ancla"] = elegir_punto(p, "¿Qué punto va ahí?")
        elif o == "6":
            p["d"] = pedir_medidas(p["clave"])
            if p["ancla"] is not None and p["ancla"] >= len(calcular(p)["V"]):
                p["ancla"] = 0


def agregar_en_vertice(piezas):
    verts = lista_vertices(piezas)
    pantalla(piezas, None, "Vértices disponibles (números amarillos)")
    linea("¿En qué vértice va la nueva figura?")
    for k, (x, y, d) in enumerate(verts):
        print(f"  {k+1:>2}. ({f(x)}, {f(y)})   {d}")
    print("   0. Cancelar")
    k = int(leer_opcion("Vértice", range(len(verts) + 1)))
    if k == 0:
        return None
    x, y, _ = verts[k - 1]
    print("   Si la figura no va exactamente en el vértice, córrela (si no, Enter):")
    dx = leer_num("   correr en x", 0.0)
    dy = leer_num("   correr en y", 0.0)
    clave = elegir_figura()
    if clave is None:
        return None
    p = nueva_pieza(clave, [1] * len(params_fig(clave)) if clave != "poligono" else [(0, 0), (1, 0), (0, 1)])
    p["ancla"], p["destino"] = 0, (x + dx, y + dy)
    colocar(p)
    pantalla(piezas, p, "Mira la hoja de la figura para saber qué es cada medida")
    p["d"] = pedir_medidas(clave)
    colocar(p)
    pantalla(piezas, p, f"¿Qué punto naranja va en el vértice {k}?")
    p["ancla"] = elegir_punto(p, f"¿Qué punto de la figura nueva va en el vértice {k}?")
    return ajustar(piezas, p, f"Figura nueva en el vértice {k}")


def agregar_en_coordenadas(piezas, primera=False):
    clave = elegir_figura()
    if clave is None:
        return None
    p = nueva_pieza(clave, [1] * len(params_fig(clave)) if clave != "poligono" else [(0, 0), (1, 0), (0, 1)])
    colocar(p)
    pantalla(piezas, p, "Mira la hoja de la figura para saber qué es cada medida")
    p["d"] = pedir_medidas(clave)
    if primera:
        p["ancla"], p["destino"] = None, (0.0, 0.0)
        return ajustar(piezas, p, "Primera figura: su esquina inferior izquierda en (0, 0)")
    colocar(p)
    pantalla(piezas, p, "Elige qué punto de la figura vas a ubicar")
    p["ancla"] = elegir_punto(p, "¿Qué punto vas a ubicar con coordenadas?")
    print("   ¿Dónde va ese punto?")
    p["destino"] = (leer_num("   x"), leer_num("   y"))
    return ajustar(piezas, p, "Figura nueva ubicada por coordenadas")


def menu_compuesta():
    linea("DIBUJAR FIGURA COMPUESTA")
    print("   1. Dibujar con vértices  (cada figura nueva se pega a un vértice)")
    print("   2. Dibujar a mano        (ubicas cada figura con coordenadas x, y)")
    print("   0. Volver")
    modo = leer_opcion("Opción", ["0", "1", "2"], 1)
    if modo == "0":
        return
    linea("PRIMERA FIGURA: queda con su esquina inferior izquierda en (0, 0)")
    p = agregar_en_coordenadas([], primera=True)
    if p is None:
        return
    piezas = [p]
    while True:
        pantalla(piezas, None, "Figura compuesta (números amarillos = vértices)")
        linea(f"FIGURA COMPUESTA — {len(piezas)} pieza(s)")
        for i, q in enumerate(piezas):
            print(f"   {i+1}. {describir(q)}")
        print()
        a, b = ("1", "2") if modo == "1" else ("2", "1")
        print(f"   {a}. Agregar figura en un VÉRTICE")
        print(f"   {b}. Agregar figura en COORDENADAS (x, y)")
        print("   3. Deshacer la última figura")
        print("   4. ✔ RESOLVER (paso a paso)")
        print("   0. Volver al menú principal")
        o = leer_opcion("Opción", ["0", "1", "2", "3", "4"], 1)
        en_vertice = "1" if modo == "1" else "2"
        if o == en_vertice:
            nueva = agregar_en_vertice(piezas)
        elif o in ("1", "2"):
            nueva = agregar_en_coordenadas(piezas)
        elif o == "3":
            if len(piezas) > 1:
                print("   Eliminada: " + describir(piezas.pop()))
            else:
                print("   ✗ No puedes borrar la única figura.")
            continue
        elif o == "4":
            mostrar_resultado(piezas)
            continue
        else:
            if leer_opcion("¿Seguro? Se pierde el dibujo (1 = sí, 0 = no)", ["0", "1"], 0) == "1":
                return
            continue
        if nueva is not None:
            piezas.append(nueva)


def mostrar_resultado(piezas):
    G, T = resolver(piezas)
    if abs(T["A"]) < 1e-12:
        print("   ✗ El área total es 0: revisa los huecos.")
        return
    L = pasos_compuesta(piezas)
    print()
    print("\n".join(L))
    m = mohr(T["IX"], T["IY"], T["IXY"])
    fig = ventana()
    fig.clf()
    a1 = fig.add_axes([0.03, 0.38, 0.40, 0.56])
    a2 = fig.add_axes([0.46, 0.38, 0.27, 0.56])
    a3 = fig.add_axes([0.76, 0.38, 0.23, 0.56])
    a4 = fig.add_axes([0.02, 0.01, 0.96, 0.32])
    dibujar_compuesta(a1, piezas, None, vertices=False, res={"X": T["X"], "Y": T["Y"], "tp": m["tp"]})
    a1.set_title("Figura (· · ejes centroidales)", fontsize=12)
    dibujar_mohr(a2, T["IX"], T["IY"], T["IXY"], m)
    a3.axis("off")
    res = [rf"$\bar{{X}} = {f(T['X'])}$", rf"$\bar{{Y}} = {f(T['Y'])}$", rf"$\Sigma A = {f(T['A'])}$",
           rf"$\bar{{I}}_X = {f(T['IX'])}$", rf"$\bar{{I}}_Y = {f(T['IY'])}$",
           rf"$\bar{{I}}_{{XY}} = {f(T['IXY'])}$", rf"$J_C = {f(T['IX'] + T['IY'])}$",
           rf"$I_{{max}} = {f(m['Imax'])}$", rf"$I_{{min}} = {f(m['Imin'])}$",
           rf"$\theta_p = {f(m['tp'])}^\circ$"]
    for i, t in enumerate(res):
        a3.text(0, 1 - i * 0.1, t, fontsize=13, va="top")
    a4.axis("off")
    cab = ["#", "Figura", "A", "x̄", "ȳ", "A·x̄", "A·ȳ", "Īx", "Īy", "Īxy", "dx", "dy",
           "Īx+A·dy²", "Īy+A·dx²", "Īxy+A·dx·dy"]
    filas = [[str(i + 1), nombre_fig(p["clave"])[:18] + (" (−)" if p["hueco"] else ""),
              f(g["A"]), f(g["x"]), f(g["y"]), f(g["A"] * g["x"]), f(g["A"] * g["y"]), f(g["Ix"]),
              f(g["Iy"]), f(g["Ixy"]), f(g["dx"]), f(g["dy"]), f(g["IX"]), f(g["IY"]), f(g["IXY"])]
             for i, (p, g) in enumerate(zip(piezas, G))]
    filas.append(["", "Σ", f(T["A"]), "", "", f(T["SAx"]), f(T["SAy"]), "", "", "", "", "",
                  f(T["IX"]), f(T["IY"]), f(T["IXY"])])
    tb = a4.table(cellText=filas, colLabels=cab, loc="upper center", cellLoc="center")
    tb.auto_set_font_size(False)
    tb.set_fontsize(8.5)
    tb.scale(1, 1.35)
    for (fi, co), cell in tb.get_celld().items():
        if fi == 0 or fi == len(filas):
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#e8eef7")
    refrescar()
    print("\n   → La ventana muestra la figura, el círculo de Mohr y la tabla.")
    if leer_opcion("¿Guardar el paso a paso en un archivo .txt? (1 = sí, 0 = no)", ["0", "1"], 0) == "1":
        nom = input("   Nombre del archivo [Enter = solucion.txt]: ").strip() or "solucion.txt"
        if not nom.endswith(".txt"):
            nom += ".txt"
        with open(nom, "w", encoding="utf-8") as fh:
            fh.write("PIEZAS:\n" + "\n".join(f"{i+1}. {describir(p)}" for i, p in enumerate(piezas)))
            fh.write("\n\n" + "\n".join(L) + "\n")
        print(f"   Guardado en {nom}")
    pausa("Enter para volver al dibujo")


# ----------------------------------------------------------------- 3. Mohr directo
def dibujar_mohr(ax, Ix, Iy, Ixy, m):
    C, R = m["C"], m["R"]
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(C + R * np.cos(t), R * np.sin(t), color=BORDE, lw=1.8)
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)
    ax.plot([Ix, Iy], [Ixy, -Ixy], "k-", lw=1)
    ax.plot(Ix, Ixy, "o", color=ROJO)
    ax.text(Ix, Ixy, "  X", fontsize=12, color=ROJO, weight="bold")
    ax.plot(Iy, -Ixy, "o", color=ROJO)
    ax.text(Iy, -Ixy, "  Y", fontsize=12, color=ROJO, weight="bold")
    ax.plot([C - R, C, C + R], [0, 0, 0], "s", color=VERDE)
    ax.text(C + R, 0, f"  Imax\n  {f(m['Imax'])}", fontsize=9, va="bottom")
    ax.text(C - R, 0, f"Imin  \n{f(m['Imin'])}  ", fontsize=9, va="bottom", ha="right")
    ax.text(C, 0, "C", fontsize=11, va="top", ha="center")
    if R > 0:
        a0 = np.degrees(np.arctan2(Ixy, Ix - C))
        ax.add_patch(Wedge((C, 0), R * 0.3, min(0, a0), max(0, a0), fill=False, lw=1.2, color=VERDE))
        ax.text(C + R * 0.35 * np.cos(np.radians(a0 / 2)), R * 0.35 * np.sin(np.radians(a0 / 2)),
                r"$2\theta_p$", fontsize=11, color=VERDE)
    if "Iu" in m:
        ax.plot([m["Iu"], m["Iv"]], [m["Iuv"], -m["Iuv"]], "--", color=NARANJA, lw=1.2)
        ax.plot(m["Iu"], m["Iuv"], "D", color=NARANJA)
        ax.text(m["Iu"], m["Iuv"], "  U", color=NARANJA, fontsize=12, weight="bold")
        ax.plot(m["Iv"], -m["Iuv"], "D", color=NARANJA)
        ax.text(m["Iv"], -m["Iuv"], "  V", color=NARANJA, fontsize=12, weight="bold")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.3)
    ax.set_xlabel("$I$")
    ax.set_ylabel("$I_{xy}$")
    ax.set_title("Círculo de Mohr", fontsize=12)


def menu_mohr():
    linea("MOHR DIRECTO — ingresa los momentos respecto a unos ejes x, y")
    Ix = leer_num("   Ix")
    Iy = leer_num("   Iy")
    Ixy = leer_num("   Ixy")
    th = None
    if leer_opcion("¿Quieres también Iu, Iv, Iuv para un ángulo θ? (1 = sí, 0 = no)", ["0", "1"], 0) == "1":
        th = leer_num("   θ en grados (antihorario desde x)")
    m = mohr(Ix, Iy, Ixy, th)
    print()
    print("\n".join(pasos_mohr(Ix, Iy, Ixy, th)))
    fig = ventana()
    fig.clf()
    ax = fig.add_axes([0.05, 0.08, 0.55, 0.84])
    dibujar_mohr(ax, Ix, Iy, Ixy, m)
    a = fig.add_axes([0.64, 0.05, 0.35, 0.88])
    a.axis("off")
    res = [rf"$C = \frac{{I_x+I_y}}{{2}} = {f(m['C'])}$",
           rf"$R = \sqrt{{\left(\frac{{I_x-I_y}}{{2}}\right)^2 + I_{{xy}}^2}} = {f(m['R'])}$",
           rf"$I_{{max}} = C + R = {f(m['Imax'])}$", rf"$I_{{min}} = C - R = {f(m['Imin'])}$",
           rf"$\tan 2\theta_p = -\frac{{2I_{{xy}}}}{{I_x - I_y}}$",
           rf"$\theta_p = {f(m['tp'])}^\circ$  (eje de $I_{{max}}$)",
           rf"eje de $I_{{min}}$: ${f(m['tp2'])}^\circ$"]
    if th is not None:
        res += [rf"Para $\theta = {f(th)}^\circ$:", rf"$I_u = {f(m['Iu'])}$", rf"$I_v = {f(m['Iv'])}$",
                rf"$I_{{uv}} = {f(m['Iuv'])}$"]
    res += ["", "X = (Ix, Ixy),  Y = (Iy, −Ixy)", "Girar los ejes θ antihorario =",
            "girar 2θ antihorario en el círculo"]
    for i, t in enumerate(res):
        a.text(0, 0.98 - i * 0.07, t, fontsize=13 if "$" in t else 11, va="top")
    refrescar()
    pausa("Enter para volver al menú")


# ----------------------------------------------------------------- menú principal
def principal():
    print("\n  MOMENTOS DE INERCIA DE ÁREAS — Mecánica racional I")
    print("  (deja abierta la ventana que aparece: ahí se ve todo)")
    while True:
        linea("MENÚ PRINCIPAL")
        print("   1. Formulario (dibujo + fórmulas de una figura)")
        print("   2. Dibujar figura compuesta (con paso a paso)")
        print("   3. Mohr directo (Ix, Iy, Ixy)")
        print("   0. Salir")
        o = leer_opcion("Opción", ["0", "1", "2", "3"])
        if o == "1":
            menu_formulario()
        elif o == "2":
            menu_compuesta()
        elif o == "3":
            menu_mohr()
        else:
            plt.close("all")
            print("  ¡Éxitos en el parcial!")
            return


if __name__ == "__main__":
    principal()
