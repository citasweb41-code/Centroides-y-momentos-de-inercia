# MOMENTOS DE INERCIA - TI-Nspire CX II (Python)
# 1 Formulario  2 Figura compuesta (paso a paso)  3 Mohr directo
# Se maneja con flechas + enter; esc = volver
from ti_draw import *
from ti_system import *
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


# ---------- formulario (dibujos de la hoja) ----------

def ejes(ox,oy):
  set_color(0,0,0)
  draw_line(ox,oy,300,oy)
  draw_line(ox,oy,ox,20)
  draw_text(300,oy+14,"x")
  draw_text(ox-12,24,"y")

def c(x,y):
  set_color(200,0,0)
  fill_circle(x,y,3)
  draw_text(x+5,y+14,"C")
  set_color(0,0,0)

def az():
  set_color(150,185,230)

def bd():
  set_color(40,80,125)

def par(f,n=20):
  return [f(i/n) for i in range(n+1)]

def d_rect():
  az();fill_rect(60,60,160,100);bd();draw_rect(60,60,160,100)
  ejes(60,160);c(140,110)
  draw_text(135,185,"b");draw_text(40,115,"h")

def d_circ():
  az();fill_circle(160,110,70);bd();draw_circle(160,110,70)
  set_color(0,0,0);draw_line(80,110,250,110);draw_line(160,190,160,30)
  draw_text(250,128,"x");draw_text(165,35,"y");c(160,110)
  draw_line(160,110,111,159);draw_text(122,150,"R")

def d_spandrel():
  p=par(lambda t:(60+160*t,170-100*t*t))
  xs=[q[0] for q in p]+[220];ys=[q[1] for q in p]+[170]
  az();fill_poly(xs,ys);bd();draw_poly(xs,ys)
  ejes(60,170);c(180,140)
  draw_text(135,195,"b");draw_text(228,125,"h");draw_text(90,120,"y=kx^2")

def d_trir():
  xs=[60,240,60];ys=[170,170,70]
  az();fill_poly(xs,ys);bd();draw_poly(xs,ys)
  ejes(60,170);c(120,137)
  draw_text(145,195,"b");draw_text(40,125,"h")

def d_semi():
  az();fill_arc(80,40,160,160,0,180);bd();draw_arc(80,40,160,160,0,180)
  ejes(160,120);draw_line(60,120,160,120);c(160,86)
  draw_text(200,145,"4R/(3pi)")

def d_mpar():
  p=par(lambda t:(60+150*t,170-110*t*t))
  xs=[q[0] for q in p]+[60];ys=[q[1] for q in p]+[60]
  az();fill_poly(xs,ys);bd();draw_poly(xs,ys)
  ejes(60,170);c(116,104)
  draw_text(130,55,"b");draw_text(40,120,"h");draw_text(190,150,"y=kx^2")

def d_iso():
  xs=[80,240,160];ys=[170,170,40]
  az();fill_poly(xs,ys);bd();draw_poly(xs,ys)
  ejes(160,170);draw_line(60,170,160,170);c(160,127)
  draw_text(110,195,"b/2");draw_text(190,195,"b/2");draw_text(60,110,"h")

def d_cc():
  az();fill_arc(-60,50,240,240,0,90);bd();draw_arc(-60,50,240,240,0,90)
  ejes(60,170);c(111,119)
  draw_text(115,195,"R");draw_text(150,90,"xc=yc=4R/(3pi)")

def d_sector():
  az();fill_arc(-80,10,320,320,-30,60);bd();draw_arc(-80,10,320,320,-30,60)
  set_color(0,0,0);draw_line(80,90,219,170);draw_line(80,250,219,170)
  draw_line(80,170,300,170);draw_line(80,60,80,200)
  c(162,170);draw_text(110,160,"a");draw_text(110,195,"a");draw_text(180,130,"R")

def d_tri():
  xs=[60,240,180];ys=[170,170,60]
  az();fill_poly(xs,ys);bd();draw_poly(xs,ys)
  ejes(60,170);c(160,133)
  draw_text(145,195,"b");draw_text(115,55,"a");draw_text(250,120,"h")

def d_elip():
  p=par(lambda t:(60+180*(1-t*t)**0.5,170-100*t))
  xs=[60]+[q[0] for q in p];ys=[170]+[q[1] for q in p]
  az();fill_poly(xs,ys);bd();draw_poly(xs,ys)
  ejes(60,170);c(136,128)
  draw_text(145,195,"a");draw_text(40,125,"b")

def d_mohr():
  set_color(0,0,0);draw_line(20,110,300,110);draw_line(30,20,30,200)
  draw_text(290,128,"I");draw_text(35,30,"Ixy")
  bd();draw_circle(170,110,80)
  set_color(0,0,0);draw_line(234,62,106,158)
  draw_text(238,60,"X(Ix,Ixy)");draw_text(40,178,"Y(Iy,-Ixy)")
  c(170,110);draw_text(255,130,"Imax");draw_text(60,130,"Imin")
  draw_text(205,100,"2tp")

L=[
("Rectangulo",d_rect,["A=bh  xc=b/2  yc=h/2",
 "Ixc=bh^3/12  Iyc=b^3h/12  Ixyc=0",
 "Ix=bh^3/3   Iy=b^3h/3",
 "Ixy=b^2h^2/4","Jc=bh(b^2+h^2)/12"]),
("Circulo",d_circ,["A=pi R^2  C en el centro",
 "Ix=Iy=pi R^4/4   Ixy=0","Jc=pi R^4/2"]),
("Media parab. compl.",d_spandrel,["y=kx^2   A=bh/3",
 "xc=3b/4   yc=3h/10",
 "Ixc=37bh^3/2100  Iyc=b^3h/80",
 "Ixyc=b^2h^2/120",
 "Ix=bh^3/21  Iy=b^3h/5","Ixy=b^2h^2/12"]),
("Triangulo rectangulo",d_trir,["A=bh/2  xc=b/3  yc=h/3",
 "Ixc=bh^3/36  Iyc=b^3h/36",
 "Ixyc=-b^2h^2/72",
 "Ix=bh^3/12  Iy=b^3h/12","Ixy=b^2h^2/24"]),
("Semicirculo",d_semi,["A=pi R^2/2  xc=0  yc=4R/(3pi)",
 "Ixc=0.1098 R^4   Ixyc=0",
 "Ix=Iy=Iyc=pi R^4/8   Ixy=0"]),
("Media parabola",d_mpar,["y=kx^2   A=2bh/3",
 "xc=3b/8   yc=3h/5",
 "Ixc=8bh^3/175  Iyc=19b^3h/480",
 "Ixyc=b^2h^2/60",
 "Ix=2bh^3/7  Iy=2b^3h/15","Ixy=b^2h^2/6"]),
("Triangulo isosceles",d_iso,["A=bh/2  xc=0  yc=h/3",
 "Ixc=bh^3/36  Iyc=b^3h/48",
 "Ixyc=0","Ix=bh^3/12  Ixy=0"]),
("Cuarto de circulo",d_cc,["A=pi R^2/4  xc=yc=4R/(3pi)",
 "Ixc=Iyc=0.05488 R^4",
 "Ixyc=-0.01647 R^4",
 "Ix=Iy=pi R^4/16  Ixy=R^4/8"]),
("Sector circular",d_sector,["A=a R^2 (a=medio ang, rad)",
 "xc=2R sin(a)/(3a)  yc=0",
 "Ix=Ixc=R^4/8 (2a-sin2a)",
 "Iy=R^4/8 (2a+sin2a)  Ixy=0",
 "Iyc=Iy-A xc^2"]),
("Triangulo",d_tri,["A=bh/2  xc=(a+b)/3  yc=h/3",
 "Ixc=bh^3/36   Ix=bh^3/12",
 "Iyc=bh/36 (a^2-ab+b^2)",
 "Iy=bh/12 (a^2+ab+b^2)",
 "Ixyc=bh^2/72 (2a-b)",
 "Ixy=bh^2/24 (2a+b)"]),
("Cuarto de elipse",d_elip,["A=pi ab/4",
 "xc=4a/(3pi)  yc=4b/(3pi)",
 "Ixc=0.05488 ab^3",
 "Iyc=0.05488 a^3b",
 "Ixyc=-0.01647 a^2b^2",
 "Ix=pi ab^3/16  Iy=pi a^3b/16","Ixy=a^2b^2/8"]),
("Circulo de Mohr",d_mohr,["C=(Ix+Iy)/2",
 "R=sqrt(((Ix-Iy)/2)^2+Ixy^2)",
 "Imax,min=C+-R",
 "tan2tp=-2Ixy/(Ix-Iy)",
 "Iu=C+(Ix-Iy)/2 cos2t-Ixy sin2t",
 "Iv=C-(Ix-Iy)/2 cos2t+Ixy sin2t",
 "Iuv=(Ix-Iy)/2 sin2t+Ixy cos2t",
 "Steiner: I=Ic+A d^2",
 "Ixy=Ixyc+A dx dy"])]

COM=["J=Ix+Iy  k=sqrt(I/A)","Steiner: I=Ic+A d^2","Ixy=Ixyc+A xc yc","(c = respecto al centroide)"]

def texto(tit,ls):
  clear();set_color(0,0,150);draw_text(5,18,tit);set_color(0,0,0)
  y=40
  for s in ls:
    draw_text(5,y,s);y+=19
    if y>205:
      draw_text(220,210,"[tecla]");esperar()
      clear();y=20




# =============================================================================
#  INTERFAZ TI-NSPIRE: todo dentro de la pantalla grafica
#  flechas + enter para elegir, esc para volver
# =============================================================================
def esperar():
  return get_key(1)

def cab(t):
  clear()
  set_color(0, 0, 150)
  draw_text(4, 16, t)
  set_color(0, 0, 0)

def pie(t):
  set_color(110, 110, 110)
  draw_text(4, 210, t)
  set_color(0, 0, 0)

def elegir(tit, items, sel=0):
  # menu con flechas; devuelve el indice o -1 (esc)
  top = 0
  N = 9
  while True:
    cab(tit)
    if sel < top:
      top = sel
    if sel >= top + N:
      top = sel - N + 1
    for i in range(top, min(len(items), top + N)):
      y = 40 + (i - top) * 18
      if i == sel:
        set_color(200, 220, 255)
        fill_rect(0, y - 14, 318, 18)
        set_color(0, 0, 0)
      draw_text(6, y, str(i + 1) + ". " + items[i])
    pie("flechas + enter    esc = volver")
    k = get_key(1)
    if k == "up":
      sel = (sel - 1) % len(items)
    elif k == "down":
      sel = (sel + 1) % len(items)
    elif k == "enter":
      return sel
    elif k == "esc":
      return -1
    elif len(k) == 1 and k in "123456789" and int(k) <= len(items):
      return int(k) - 1

def leer(msg, defecto=None):
  # escribe un numero (se permiten + - * / ^ ( ) pi); None si esc
  s = ""
  err = ""
  ult = ""
  while True:
    cab(msg)
    draw_rect(8, 50, 300, 28)
    draw_text(14, 70, s + "_")
    set_color(200, 0, 0)
    draw_text(8, 100, err)
    set_color(0, 0, 0)
    if defecto is not None:
      draw_text(8, 125, "Enter vacio = " + f(defecto))
    set_color(110, 110, 110)
    draw_text(8, 185, "tecla: " + ult)
    pie("enter=ok  del=borrar  esc=cancelar")
    k = get_key(1)
    ult = k
    err = ""
    if k == "enter":
      if s == "" and defecto is not None:
        return defecto
      try:
        return float(eval(s.replace("^", "**")))
      except:
        err = "No es un numero valido"
    elif k == "del" or k == "clear":
      s = s[:-1]
    elif k == "esc":
      return None
    elif k in ("−", "(-)", "neg", "-"):
      s += "-"
    elif k in ("π", "pi"):
      s += "pi"
    elif k in ("EE", "ee", "E"):
      s += "e"
    elif k in ("×", "*"):
      s += "*"
    elif k in ("÷", "/"):
      s += "/"
    elif k == "^":
      s += "^"
    elif len(k) == 1 and k in "0123456789.+()":
      s += k

def partir(t, n=40):
  out = []
  while len(t) > n:
    out.append(t[:n])
    t = "  " + t[n:]
  out.append(t)
  return out

def ver_texto(tit, lineas):
  L = []
  for s in lineas:
    if len(s) > 30 and s.strip("=") == "":
      s = "-" * 30
    L += partir(s)
  N = 10
  pag = 0
  tot = max(1, (len(L) + N - 1) // N)
  while True:
    cab(tit + "  (" + str(pag + 1) + "/" + str(tot) + ")")
    for i in range(N):
      j = pag * N + i
      if j < len(L):
        draw_text(4, 38 + i * 17, L[j])
    pie("abajo/enter=sigue  arriba=atras  esc=salir")
    k = get_key(1)
    if k in ("down", "enter", "right"):
      if pag + 1 < tot:
        pag += 1
      elif k == "enter":
        return
    elif k in ("up", "left"):
      pag = max(0, pag - 1)
    elif k == "esc":
      return

def vista(piezas, cand=None, titulo="", numeros=True, res=None, abajo="[tecla]"):
  G = [calcular(p) for p in piezas]
  gc = calcular(cand) if cand else None
  pts = []
  for g in G + ([gc] if gc else []):
    pts += g["P"]
  xs = [q[0] for q in pts]
  ys = [q[1] for q in pts]
  x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
  s = min(280.0 / max(x1 - x0, 1e-9), 150.0 / max(y1 - y0, 1e-9))
  ox = 19 + (280 - (x1 - x0) * s) / 2
  oy = 185 - (150 - (y1 - y0) * s) / 2

  def T(x, y):
    return int(ox + (x - x0) * s), int(oy - (y - y0) * s)

  def poly(P, rgb):
    X = [T(x, y)[0] for (x, y) in P]
    Y = [T(x, y)[1] for (x, y) in P]
    set_color(rgb[0], rgb[1], rgb[2])
    fill_poly(X, Y)
    set_color(40, 80, 125)
    draw_poly(X, Y)

  cab(titulo)
  for i in range(len(piezas)):
    if not piezas[i]["hueco"]:
      poly(G[i]["P"], (150, 185, 230))
  for i in range(len(piezas)):
    if piezas[i]["hueco"]:
      poly(G[i]["P"], (255, 255, 255))
  ax, ay = T(0, 0)
  set_color(150, 150, 150)
  draw_line(0, ay, 318, ay)
  draw_line(ax, 22, ax, 196)
  if gc:
    poly(gc["P"], (240, 160, 90))
    set_color(200, 90, 0)
    for j in range(len(gc["V"])):
      px, py = T(gc["V"][j][1][0], gc["V"][j][1][1])
      fill_rect(px - 2, py - 2, 5, 5)
      draw_text(px + 3, py + 14, "p" + str(j + 1))
  if numeros:
    V = lista_vertices(piezas)
    for k in range(len(V)):
      px, py = T(V[k][0], V[k][1])
      set_color(0, 0, 0)
      fill_circle(px, py, 2)
      set_color(150, 0, 150)
      draw_text(px + 3, py - 2, str(k + 1))
  if res:
    px, py = T(res[0], res[1])
    set_color(200, 0, 0)
    fill_circle(px, py, 4)
    draw_text(px + 6, py - 4, "C")
  pie(abajo)

def elegir_fig():
  k = elegir("Que figura agregas?", [q[1] + "  (" + q[2] + ")" if q[2] else q[1] for q in FIG])
  return None if k < 0 else FIG[k][0]

def medidas(clave):
  if clave == "poligono":
    n = leer("Cuantos vertices tiene?")
    if n is None or n < 3:
      return None
    P = []
    for i in range(int(n)):
      x = leer("Vertice " + str(i + 1) + ": x")
      if x is None:
        return None
      y = leer("Vertice " + str(i + 1) + ": y")
      if y is None:
        return None
      P.append((x, y))
    return P
  d = []
  for q in params_fig(clave):
    v = leer(nombre_fig(clave) + ": " + AYUDA_PAR.get(q, q))
    if v is None:
      return None
    d.append(v)
  return d

def punto(piezas, p, msg):
  colocar(p)
  vista(piezas, p, "Puntos naranja de la figura nueva")
  esperar()
  V = calcular(p)["V"]
  k = elegir(msg, ["p" + str(j + 1) + " = " + V[j][0] for j in range(len(V))])
  return k

def ajustar(piezas, p):
  while True:
    colocar(p)
    vista(piezas, p, describir(p)[:44], abajo="ent=OK 1=esp.h 2=esp.v 3=gira 4=hueco")
    set_color(110, 110, 110)
    draw_text(4, 196, "5=otro punto 6=medidas esc=cancelar")
    k = get_key(1)
    if k == "enter":
      return p
    if k == "esc":
      return None
    if k == "1":
      p["eh"] = not p["eh"]
    elif k == "2":
      p["ev"] = not p["ev"]
    elif k == "3":
      p["giro"] = (p["giro"] + 90) % 360
    elif k == "4":
      p["hueco"] = not p["hueco"]
    elif k == "5" and p["ancla"] is not None:
      a = punto(piezas, p, "Que punto va ahi?")
      if a >= 0:
        p["ancla"] = a
    elif k == "6":
      d = medidas(p["clave"])
      if d is not None:
        p["d"] = d
        if p["ancla"] is not None and p["ancla"] >= len(calcular(p)["V"]):
          p["ancla"] = 0

def nueva(piezas, modo, primera=False):
  if modo == 0 and not primera:
    V = lista_vertices(piezas)
    vista(piezas, None, "Mira el numero del vertice", abajo="[tecla] para elegirlo")
    esperar()
    k = elegir("En que vertice va?", ["(" + f(V[i][0]) + ", " + f(V[i][1]) + ")"
                                      for i in range(len(V))])
    if k < 0:
      return None
    dx = leer("Correr desde el vertice en x", 0.0)
    if dx is None:
      return None
    dy = leer("Correr desde el vertice en y", 0.0)
    if dy is None:
      return None
  cl = elegir_fig()
  if cl is None:
    return None
  d = medidas(cl)
  if d is None:
    return None
  p = nueva_pieza(cl, d)
  if primera:
    p["ancla"], p["destino"] = None, (0.0, 0.0)
  elif modo == 0:
    p["ancla"], p["destino"] = 0, (V[k][0] + dx, V[k][1] + dy)
    a = punto(piezas, p, "Que punto va en el vertice " + str(k + 1) + "?")
    if a < 0:
      return None
    p["ancla"] = a
  else:
    a = punto(piezas, p, "Que punto vas a ubicar?")
    if a < 0:
      return None
    p["ancla"] = a
    x = leer("Coordenada x de ese punto")
    if x is None:
      return None
    y = leer("Coordenada y de ese punto")
    if y is None:
      return None
    p["destino"] = (x, y)
  return ajustar(piezas, p)

def compuesta():
  modo = elegir("Figura compuesta", ["Con vertices (pegar figuras)", "A mano (coordenadas x, y)"])
  if modo < 0:
    return
  p = nueva([], modo, True)
  if p is None:
    return
  P = [p]
  while True:
    k = elegir("Figura compuesta: " + str(len(P)) + " pieza(s)",
               ["Agregar figura", "Deshacer la ultima", "RESOLVER paso a paso", "Ver dibujo",
                "Ver lista de piezas", "Volver al menu"])
    if k == 0:
      como = elegir("Como ubicas la figura nueva?",
                    ["En un vertice de la figura", "Con coordenadas (x, y)"], modo)
      if como >= 0:
        modo = como
        q = nueva(P, como)
        if q:
          P.append(q)
    elif k == 1 and len(P) > 1:
      P.pop()
    elif k == 2:
      G, T = resolver(P)
      if abs(T["A"]) < 1e-12:
        ver_texto("Error", ["El area total es 0. Revisa los huecos."])
        continue
      resultados(P)
    elif k == 3:
      vista(P, None, "Figura compuesta")
      esperar()
    elif k == 4:
      ver_texto("Piezas", [str(i + 1) + ". " + describir(P[i]) for i in range(len(P))])
    elif k in (5, -1):
      if elegir("Salir? Se pierde el dibujo", ["No, seguir", "Si, salir"]) == 1:
        return

def dib_mohr(Ix, Iy, Ixy, m):
  C, R = m["C"], m["R"]
  lo = min(0, C - R)
  s = min(280.0 / max(C + R - lo, 1e-9), 80.0 / max(R, 1e-9))

  def T(x, y):
    return int(20 + (x - lo) * s), int(112 - y * s)

  cab("Mohr  C=" + f(C) + "  R=" + f(R))
  set_color(150, 150, 150)
  draw_line(0, 112, 318, 112)
  draw_line(T(0, 0)[0], 22, T(0, 0)[0], 200)
  cx, cy = T(C, 0)
  set_color(40, 80, 125)
  draw_circle(cx, cy, max(int(R * s), 1))
  set_color(0, 0, 0)
  a, b = T(Ix, Ixy)
  c2, d2 = T(Iy, -Ixy)
  draw_line(a, b, c2, d2)
  set_color(200, 0, 0)
  fill_circle(a, b, 3)
  draw_text(a + 4, b - 2, "X")
  fill_circle(c2, d2, 3)
  draw_text(c2 + 4, d2 + 12, "Y")
  set_color(0, 140, 60)
  e, g2 = T(C + R, 0)
  fill_rect(e - 2, g2 - 2, 5, 5)
  draw_text(e - 30, g2 + 14, "Imax")
  e, g2 = T(C - R, 0)
  fill_rect(e - 2, g2 - 2, 5, 5)
  draw_text(e + 2, g2 + 14, "Imin")
  if "Iu" in m:
    set_color(200, 90, 0)
    a, b = T(m["Iu"], m["Iuv"])
    fill_circle(a, b, 3)
    draw_text(a + 4, b - 2, "U")
  pie("Imax=" + f(m["Imax"]) + " Imin=" + f(m["Imin"]) + " tp=" + f(m["tp"]))

def mohr_directo():
  Ix = leer("Mohr directo: Ix")
  if Ix is None:
    return
  Iy = leer("Mohr directo: Iy")
  if Iy is None:
    return
  Ixy = leer("Mohr directo: Ixy")
  if Ixy is None:
    return
  th = None
  if elegir("Calcular Iu, Iv, Iuv para un angulo?", ["No", "Si"]) == 1:
    th = leer("Angulo theta en grados (antihorario)")
  m = mohr(Ix, Iy, Ixy, th)
  sel = 0
  while True:
    k = elegir("MOHR: que quieres ver?", ["Dibujo del circulo", "Paso a paso", "Resumen", "Volver"], sel)
    if k < 0 or k == 3:
      return
    sel = k
    if k == 0:
      dib_mohr(Ix, Iy, Ixy, m)
      esperar()
    elif k == 1:
      pantalla_pasos("Mohr", pasos_mohr_calc(Ix, Iy, Ixy, m))
    else:
      R = [("C", f(m["C"])), ("R", f(m["R"])), ("Imax", f(m["Imax"])), ("Imin", f(m["Imin"])),
           ("tp (grados)", f(m["tp"])), ("eje Imin", f(m["tp2"]))]
      if th is not None:
        R += [("Iu", f(m["Iu"])), ("Iv", f(m["Iv"])), ("Iuv", f(m["Iuv"]))]
      resumen("Mohr directo", R)

def formulario():
  sel = 0
  while True:
    k = elegir("Formulario", [q[0] for q in L], sel)
    if k < 0:
      return
    sel = k
    t, d, fs = L[k]
    cab(t)
    d()
    pie("[tecla] = ver formulas")
    esperar()
    ver_texto(t, fs + ([] if k == len(L) - 1 else COM))


# =============================================================================
#  RESULTADOS (calculadora): menu, tablas con cuadricula y paso a paso
# =============================================================================
CW = 7  # ancho aproximado de un caracter en pantalla (px)

def tabla(tit, enc, filas, nfijas=1):
  W = []
  for j in range(len(enc)):
    w = len(enc[j])
    for r in filas:
      w = max(w, len(r[j]))
    W.append(w * CW + 8)
  c0 = 0
  r0 = 0
  NR = 8
  while True:
    cab(tit)
    cols = list(range(nfijas))
    x = sum(W[:nfijas])
    j = nfijas + c0
    while j < len(enc) and x + W[j] <= 316:
      cols.append(j)
      x += W[j]
      j += 1
    hay_mas = j < len(enc)
    ancho = x
    y0 = 24
    set_color(200, 220, 255)
    fill_rect(1, y0, ancho, 18)
    vis = filas[r0:r0 + NR]
    for i in range(len(vis)):
      if vis[i][0] in ("SUMA", "TOTAL"):
        set_color(225, 240, 225)
        fill_rect(1, y0 + 18 * (i + 1), ancho, 18)
    set_color(0, 0, 0)
    xx = 1
    for j in cols:
      draw_text(xx + 4, y0 + 14, enc[j])
      for i in range(len(vis)):
        t = vis[i][j]
        if t[:1] == "-":
          set_color(190, 0, 0)
        draw_text(xx + 4, y0 + 18 * (i + 1) + 14, t)
        set_color(0, 0, 0)
      xx += W[j]
    set_color(120, 120, 120)
    for i in range(len(vis) + 2):
      draw_line(1, y0 + 18 * i, ancho, y0 + 18 * i)
    xx = 1
    for j in cols + [None]:
      draw_line(xx, y0, xx, y0 + 18 * (len(vis) + 1))
      if j is not None:
        xx += W[j]
    flechas = ""
    if c0 > 0:
      flechas += "<- "
    if hay_mas:
      flechas += "-> mas columnas "
    if r0 > 0 or r0 + NR < len(filas):
      flechas += "arriba/abajo filas "
    pie(flechas + "esc=volver")
    k = get_key(1)
    if k == "right" and hay_mas:
      c0 += 1
    elif k == "left" and c0 > 0:
      c0 -= 1
    elif k == "down" and r0 + NR < len(filas):
      r0 += 1
    elif k == "up" and r0 > 0:
      r0 -= 1
    elif k in ("esc", "enter"):
      return

def pantalla_pasos(tit, lineas):
  # cada linea ya viene corta; las paginas no parten bloques si se puede
  N = 10
  pags = []
  act = []
  bloque = []
  for s in lineas + [""]:
    if s == "":
      if len(act) + len(bloque) > N and act:
        pags.append(act)
        act = []
      act += bloque + ([""] if bloque else [])
      bloque = []
    else:
      bloque.append(s)
  while len(act) > N:
    pags.append(act[:N])
    act = act[N:]
  if act:
    pags.append(act)
  p = 0
  while True:
    cab(tit + "  (" + str(p + 1) + "/" + str(len(pags)) + ")")
    for i in range(len(pags[p])):
      s = pags[p][i]
      if s[:1] == "#":
        set_color(0, 0, 150)
        s = s[1:]
      elif s[:2] == "  ":
        set_color(60, 60, 60)
      draw_text(6, 38 + i * 17, s)
      set_color(0, 0, 0)
    pie("abajo/enter=sigue  arriba=atras  esc")
    k = get_key(1)
    if k in ("down", "right", "enter"):
      if p + 1 < len(pags):
        p += 1
      elif k == "enter":
        return
    elif k in ("up", "left"):
      p = max(0, p - 1)
    elif k == "esc":
      return

def nombre_corto(p):
  return nombre_fig(p["clave"]).split(" (")[0]

def pasos_piezas(P):
  L = []
  for i in range(len(P)):
    p = P[i]
    g = calcular(p)
    A, xc, yc, Ix, Iy, Ixy, Pl, V = forma(p["clave"], p["d"])
    fo = FORM[p["clave"]]
    L.append("#Pieza " + str(i + 1) + ": " + nombre_corto(p))
    if p["clave"] != "poligono":
      L.append("  " + ", ".join(n + "=" + f(v) for n, v in zip(params_fig(p["clave"]), p["d"])))
    ex = []
    if p["giro"] % 360:
      ex.append("giro " + f(p["giro"] % 360))
    if p["eh"]:
      ex.append("espejo h")
    if p["ev"]:
      ex.append("espejo v")
    if p["hueco"]:
      ex.append("HUECO (resta)")
    if ex:
      L.append("  " + ", ".join(ex))
    L.append("")
    if p["clave"] != "poligono":
      for nom, k, val in (("A", 0, A), ("Ixc", 3, Ix), ("Iyc", 4, Iy), ("Ixyc", 5, Ixy)):
        L.append(nom + " = " + fo[k])
        L.append("  = " + f(val))
        L.append("")
    else:
      L += ["A, Ixc, Iyc, Ixyc con la", "formula de Gauss", ""]
    if p["giro"] % 180 == 90:
      L += ["Girada 90: Ixc <-> Iyc", "y Ixyc cambia de signo", ""]
    if p["eh"] != p["ev"]:
      L += ["Un espejo: Ixyc cambia", "de signo", ""]
    if p["hueco"]:
      L += ["Hueco: A e I van negativas", ""]
    L += ["Centroide en la figura:", "  x = " + f(g["x"]) + "   y = " + f(g["y"]), "",
          "Valores para la tabla:", "  A = " + f(g["A"]), "  Ixc = " + f(g["Ix"]),
          "  Iyc = " + f(g["Iy"]), "  Ixyc = " + f(g["Ixy"]), ""]
  return L

def pasos_centroide(T):
  return ["#Centroide de la figura", "",
          "X = Suma(A*x) / Suma(A)", "  = " + f(T["SAx"]) + " / " + f(T["A"]), "  = " + f(T["X"]), "",
          "Y = Suma(A*y) / Suma(A)", "  = " + f(T["SAy"]) + " / " + f(T["A"]), "  = " + f(T["Y"])]

def pasos_steiner(G, T):
  L = []
  for i in range(len(G)):
    g = G[i]
    L += ["#Pieza " + str(i + 1),
          "dx = x - X = " + f(g["x"]) + " - " + f(T["X"]), "  = " + f(g["dx"]),
          "dy = y - Y = " + f(g["y"]) + " - " + f(T["Y"]), "  = " + f(g["dy"]), "",
          "IX = Ixc + A*dy^2",
          "  = " + f(g["Ix"]) + " + " + f(g["A"]) + "*(" + f(g["dy"]) + ")^2", "  = " + f(g["IX"]), "",
          "IY = Iyc + A*dx^2",
          "  = " + f(g["Iy"]) + " + " + f(g["A"]) + "*(" + f(g["dx"]) + ")^2", "  = " + f(g["IY"]), "",
          "IXY = Ixyc + A*dx*dy",
          "  = " + f(g["Ixy"]) + " + " + f(g["A"]), "    *(" + f(g["dx"]) + ")*(" + f(g["dy"]) + ")",
          "  = " + f(g["IXY"]), ""]
  L += ["#Sumas", "IX  = " + f(T["IX"]), "IY  = " + f(T["IY"]), "IXY = " + f(T["IXY"]),
        "J = IX + IY = " + f(T["IX"] + T["IY"])]
  return L

def pasos_origen(T):
  A, X, Y = T["A"], T["X"], T["Y"]
  return ["#Respecto al origen (0, 0)", "",
          "Ix = IX + A*Y^2", "  = " + f(T["IX"]) + " + " + f(A) + "*(" + f(Y) + ")^2",
          "  = " + f(T["IX"] + A * Y * Y), "",
          "Iy = IY + A*X^2", "  = " + f(T["IY"]) + " + " + f(A) + "*(" + f(X) + ")^2",
          "  = " + f(T["IY"] + A * X * X), "",
          "Ixy = IXY + A*X*Y", "  = " + f(T["IXY"]) + " + " + f(A), "    *(" + f(X) + ")*(" + f(Y) + ")",
          "  = " + f(T["IXY"] + A * X * Y)]

def pasos_mohr_calc(Ix, Iy, Ixy, m):
  L = ["#Datos", "Ix = " + f(Ix), "Iy = " + f(Iy), "Ixy = " + f(Ixy), "",
       "#Centro", "C = (Ix + Iy) / 2", "  = (" + f(Ix) + " + " + f(Iy) + ")/2", "  = " + f(m["C"]), "",
       "#Radio", "R = sqrt( ((Ix-Iy)/2)^2 + Ixy^2 )",
       "(Ix-Iy)/2 = " + f(m["D"]), "R = sqrt((" + f(m["D"]) + ")^2 + (" + f(Ixy) + ")^2)", "  = " + f(m["R"]), "",
       "#Momentos principales", "Imax = C + R", "  = " + f(m["C"]) + " + " + f(m["R"]), "  = " + f(m["Imax"]),
       "", "Imin = C - R", "  = " + f(m["C"]) + " - " + f(m["R"]), "  = " + f(m["Imin"]), "",
       "#Angulo principal", "tan(2tp) = -2*Ixy / (Ix - Iy)", "  = -2*(" + f(Ixy) + ") / (" + f(Ix - Iy) + ")",
       "tp = " + f(m["tp"]) + " grados -> eje Imax", "eje Imin: " + f(m["tp2"]) + " grados", "",
       "#Comprobacion", "Imax + Imin = Ix + Iy", "  = " + f(Ix + Iy)]
  if "Iu" in m:
    L += ["", "#Ejes girados t = " + f(m["th"]) + " grados",
          "Iu = C + (Ix-Iy)/2*cos2t", "     - Ixy*sin2t", "  = " + f(m["Iu"]), "",
          "Iv = C - (Ix-Iy)/2*cos2t", "     + Ixy*sin2t", "  = " + f(m["Iv"]), "",
          "Iuv = (Ix-Iy)/2*sin2t", "     + Ixy*cos2t", "  = " + f(m["Iuv"])]
  return L

def resumen(tit, filas):
  cab(tit)
  for i in range(len(filas)):
    draw_text(10, 40 + i * 17, filas[i][0])
    draw_text(120, 40 + i * 17, "= " + filas[i][1])
  pie("[tecla] = volver")
  esperar()

def resultados(P):
  G, T = resolver(P)
  m = mohr(T["IX"], T["IY"], T["IXY"])
  ops = ["Resumen", "Dibujo con centroide", "Datos de cada pieza", "Tabla: A, x, y, A*x, A*y",
         "Calculo del centroide", "Tabla Steiner IX", "Tabla Steiner IY", "Tabla Steiner IXY",
         "Steiner paso a paso", "Momentos respecto al origen", "Circulo de Mohr (dibujo)",
         "Mohr paso a paso", "Volver"]
  sel = 0
  n = [str(i + 1) for i in range(len(G))]
  while True:
    k = elegir("RESULTADOS", ops, sel)
    if k < 0 or k == len(ops) - 1:
      return
    sel = k
    if k == 0:
      resumen("Resumen", [("X", f(T["X"])), ("Y", f(T["Y"])), ("Area", f(T["A"])), ("IX", f(T["IX"])),
                          ("IY", f(T["IY"])), ("IXY", f(T["IXY"])), ("J", f(T["IX"] + T["IY"])),
                          ("Imax", f(m["Imax"])), ("Imin", f(m["Imin"])), ("tp (grados)", f(m["tp"]))])
    elif k == 1:
      vista(P, None, "X=" + f(T["X"]) + "  Y=" + f(T["Y"]), False, (T["X"], T["Y"]))
      esperar()
    elif k == 2:
      pantalla_pasos("Datos de cada pieza", pasos_piezas(P))
    elif k == 3:
      F = [[n[i], f(G[i]["A"]), f(G[i]["x"]), f(G[i]["y"]), f(G[i]["A"] * G[i]["x"]),
            f(G[i]["A"] * G[i]["y"])] for i in range(len(G))]
      F.append(["SUMA", f(T["A"]), "", "", f(T["SAx"]), f(T["SAy"])])
      tabla("Tabla de centroide", ["Pz", "A", "x", "y", "A*x", "A*y"], F)
    elif k == 4:
      pantalla_pasos("Centroide", pasos_centroide(T))
    elif k == 5:
      F = [[n[i], f(G[i]["Ix"]), f(G[i]["A"]), f(G[i]["dy"]), f(G[i]["A"] * G[i]["dy"] ** 2), f(G[i]["IX"])]
           for i in range(len(G))]
      F.append(["SUMA", "", "", "", "", f(T["IX"])])
      tabla("Steiner IX", ["Pz", "Ixc", "A", "dy", "A*dy^2", "IX"], F)
    elif k == 6:
      F = [[n[i], f(G[i]["Iy"]), f(G[i]["A"]), f(G[i]["dx"]), f(G[i]["A"] * G[i]["dx"] ** 2), f(G[i]["IY"])]
           for i in range(len(G))]
      F.append(["SUMA", "", "", "", "", f(T["IY"])])
      tabla("Steiner IY", ["Pz", "Iyc", "A", "dx", "A*dx^2", "IY"], F)
    elif k == 7:
      F = [[n[i], f(G[i]["Ixy"]), f(G[i]["A"]), f(G[i]["dx"]), f(G[i]["dy"]),
            f(G[i]["A"] * G[i]["dx"] * G[i]["dy"]), f(G[i]["IXY"])] for i in range(len(G))]
      F.append(["SUMA", "", "", "", "", "", f(T["IXY"])])
      tabla("Steiner IXY", ["Pz", "Ixyc", "A", "dx", "dy", "A*dx*dy", "IXY"], F)
    elif k == 8:
      pantalla_pasos("Steiner", pasos_steiner(G, T))
    elif k == 9:
      pantalla_pasos("Respecto al origen", pasos_origen(T))
    elif k == 10:
      dib_mohr(T["IX"], T["IY"], T["IXY"], m)
      esperar()
    elif k == 11:
      pantalla_pasos("Mohr", pasos_mohr_calc(T["IX"], T["IY"], T["IXY"], m))

sel = 0
while True:
  k = elegir("MOMENTOS DE INERCIA", ["Formulario", "Figura compuesta (paso a paso)",
                                     "Mohr directo", "Salir"], sel)
  if k < 0 or k == 3:
    break
  sel = k
  if k == 0:
    formulario()
  elif k == 1:
    compuesta()
  else:
    mohr_directo()
