# MOMENTOS DE INERCIA - TI-Nspire CX II (Python)
# 1 Formulario  2 Figura compuesta (paso a paso)  3 Mohr directo
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
def esperar():
  while get_key()=="":
    pass

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
#  INTERFAZ TI-NSPIRE  (menus en la consola + dibujos con ti_draw)
# =============================================================================
def num(msg, defecto=None):
  while True:
    s = input(msg + ("" if defecto is None else " [" + str(defecto) + "]") + ": ")
    if s == "" and defecto is not None:
      return defecto
    try:
      return float(eval(s))
    except:
      print(" Numero no valido")

def opc(msg, n, defecto=None):
  # devuelve un entero entre 0 y n
  while True:
    s = input(msg + ("" if defecto is None else " [" + str(defecto) + "]") + ": ")
    if s == "" and defecto is not None:
      return defecto
    try:
      k = int(s)
      if 0 <= k <= n:
        return k
    except:
      pass
    print(" Opcion no valida (0-" + str(n) + ")")

def vista(piezas, cand=None, titulo="", numeros=True, res=None):
  G = [calcular(p) for p in piezas]
  gc = calcular(cand) if cand else None
  pts = []
  for g in G + ([gc] if gc else []):
    pts += g["P"]
  xs = [q[0] for q in pts]
  ys = [q[1] for q in pts]
  x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
  s = min(290.0 / max(x1 - x0, 1e-9), 170.0 / max(y1 - y0, 1e-9))
  ox = 14 + (290 - (x1 - x0) * s) / 2
  oy = 200 - (170 - (y1 - y0) * s) / 2

  def T(x, y):
    return int(ox + (x - x0) * s), int(oy - (y - y0) * s)

  def poly(P, rgb, relleno):
    X = [T(x, y)[0] for (x, y) in P]
    Y = [T(x, y)[1] for (x, y) in P]
    if relleno:
      set_color(rgb[0], rgb[1], rgb[2])
      fill_poly(X, Y)
    set_color(40, 80, 125)
    draw_poly(X, Y)

  clear()
  for i in range(len(piezas)):
    if not piezas[i]["hueco"]:
      poly(G[i]["P"], (150, 185, 230), True)
  for i in range(len(piezas)):
    if piezas[i]["hueco"]:
      poly(G[i]["P"], (255, 255, 255), True)
  ax, ay = T(0, 0)
  set_color(120, 120, 120)
  draw_line(0, ay, 318, ay)
  draw_line(ax, 0, ax, 212)
  if gc:
    poly(gc["P"], (240, 160, 90), True)
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
  set_color(0, 0, 150)
  draw_text(2, 14, titulo)
  set_color(0, 0, 0)
  draw_text(230, 211, "[tecla]")
  esperar()

def elegir_fig():
  print("--- FIGURA ---")
  for i in range(len(FIG)):
    print(i + 1, FIG[i][1], FIG[i][2])
  print("0 Cancelar")
  k = opc("Figura", len(FIG))
  return None if k == 0 else FIG[k - 1][0]

def medidas(clave):
  if clave == "poligono":
    n = int(num("Cuantos vertices"))
    return [(num(" v" + str(i + 1) + " x"), num(" v" + str(i + 1) + " y")) for i in range(n)]
  return [num(" " + AYUDA_PAR.get(q, q)) for q in params_fig(clave)]

def punto(p, msg):
  V = calcular(p)["V"]
  for j in range(len(V)):
    print(" ", j + 1, "p" + str(j + 1), V[j][0])
  return opc(msg, len(V), 1) - 1

def ajustar(piezas, p):
  while True:
    colocar(p)
    vista(piezas, p, "Vista previa (naranja)")
    print(describir(p))
    print("Enter=aceptar 1=espejo h 2=espejo v")
    print("3=girar 90  4=hueco si/no")
    print("5=otro punto  6=medidas  0=cancelar")
    k = opc("Opcion", 6, 9)
    if k == 9:
      return p
    if k == 0:
      return None
    if k == 1:
      p["eh"] = not p["eh"]
    elif k == 2:
      p["ev"] = not p["ev"]
    elif k == 3:
      p["giro"] = (p["giro"] + 90) % 360
    elif k == 4:
      p["hueco"] = not p["hueco"]
    elif k == 5 and p["ancla"] is not None:
      p["ancla"] = punto(p, "Punto")
    elif k == 6:
      p["d"] = medidas(p["clave"])
      if p["ancla"] is not None and p["ancla"] >= len(calcular(p)["V"]):
        p["ancla"] = 0

def nueva(piezas, modo, primera=False):
  if modo == 1 and not primera:
    V = lista_vertices(piezas)
    vista(piezas, None, "Vertices (numeros morados)")
    for k in range(len(V)):
      print(k + 1, "(" + f(V[k][0]) + "," + f(V[k][1]) + ")")
    k = opc("Vertice (0=cancelar)", len(V))
    if k == 0:
      return None
    dx = num("correr en x", 0)
    dy = num("correr en y", 0)
  cl = elegir_fig()
  if cl is None:
    return None
  p = nueva_pieza(cl, medidas(cl))
  if primera:
    p["ancla"], p["destino"] = None, (0.0, 0.0)
  elif modo == 1:
    p["ancla"], p["destino"] = 0, (V[k - 1][0] + dx, V[k - 1][1] + dy)
    colocar(p)
    vista(piezas, p, "Puntos de la figura nueva")
    p["ancla"] = punto(p, "Punto que va en el vertice " + str(k))
  else:
    colocar(p)
    vista(piezas, p, "Puntos de la figura nueva")
    p["ancla"] = punto(p, "Punto a ubicar")
    p["destino"] = (num("x"), num("y"))
  return ajustar(piezas, p)

def compuesta():
  print("1 Con vertices  2 A mano (x,y)")
  modo = opc("Modo (0=volver)", 2, 1)
  if modo == 0:
    return
  print("1a figura: esquina inf-izq en (0,0)")
  p = nueva([], modo, True)
  if p is None:
    return
  P = [p]
  while True:
    print("--- FIGURA COMPUESTA ---")
    for i in range(len(P)):
      print(i + 1, describir(P[i]))
    print("1 Agregar  2 Deshacer  3 RESOLVER")
    print("4 Ver dibujo  0 Volver")
    k = opc("Opcion", 4, 1)
    if k == 1:
      q = nueva(P, modo)
      if q:
        P.append(q)
    elif k == 2 and len(P) > 1:
      P.pop()
    elif k == 3:
      G, T = resolver(P)
      m = mohr(T["IX"], T["IY"], T["IXY"])
      vista(P, None, "X=" + f(T["X"]) + " Y=" + f(T["Y"]), False, (T["X"], T["Y"]))
      dib_mohr(T["IX"], T["IY"], T["IXY"], m)
      for s in pasos_compuesta(P):
        print(s)
      input("Fin. Enter...")
    elif k == 4:
      vista(P, None, "Figura compuesta")
    elif k == 0:
      if opc("Seguro? 1=si 0=no", 1, 0) == 1:
        return

def dib_mohr(Ix, Iy, Ixy, m):
  C, R = m["C"], m["R"]
  lo = min(0, C - R)
  s = min(280.0 / max(C + R - lo, 1e-9), 85.0 / max(R, 1e-9))
  def T(x, y):
    return int(20 + (x - lo) * s), int(110 - y * s)
  clear()
  set_color(120, 120, 120)
  draw_line(0, 110, 318, 110)
  draw_line(T(0, 0)[0], 15, T(0, 0)[0], 212)
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
  set_color(0, 0, 150)
  draw_text(2, 14, "Mohr C=" + f(C) + " R=" + f(R))
  set_color(0, 0, 0)
  draw_text(230, 211, "[tecla]")
  esperar()

def mohr_directo():
  print("MOHR DIRECTO")
  Ix = num("Ix")
  Iy = num("Iy")
  Ixy = num("Ixy")
  th = None
  if opc("Iu,Iv,Iuv para un angulo? 1=si 0=no", 1, 0) == 1:
    th = num("theta (grados)")
  m = mohr(Ix, Iy, Ixy, th)
  dib_mohr(Ix, Iy, Ixy, m)
  for s in pasos_mohr(Ix, Iy, Ixy, th):
    print(s)
  input("Enter...")

def formulario():
  while True:
    print("--- FORMULARIO ---")
    for i in range(len(L)):
      print(i + 1, L[i][0])
    k = opc("Figura (0=volver)", len(L))
    if k == 0:
      return
    t, d, fs = L[k - 1]
    clear()
    set_color(0, 0, 150)
    draw_text(5, 15, t)
    d()
    set_color(0, 0, 0)
    draw_text(230, 211, "[tecla]")
    esperar()
    texto(t, fs + ([] if k == len(L) else COM))
    esperar()

while True:
  print("=== MOMENTOS DE INERCIA ===")
  print("1 Formulario")
  print("2 Figura compuesta")
  print("3 Mohr directo")
  print("0 Salir")
  k = opc("Opcion", 3)
  if k == 1:
    formulario()
  elif k == 2:
    compuesta()
  elif k == 3:
    mohr_directo()
  else:
    break
