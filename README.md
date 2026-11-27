# Centroides y momentos de inercia — Mecánica racional I

Programa para estudiar y resolver momentos de inercia de áreas:

1. **Formulario**: eliges una figura y ves su dibujo con sus fórmulas.
2. **Figura compuesta**: la armas pieza por pieza (pegando figuras a los vértices o con coordenadas),
   con vista previa, y la resuelve paso a paso: centroide, Steiner, momentos y círculo de Mohr.
3. **Mohr directo**: ingresas Ix, Iy, Ixy y obtienes el círculo y sus resultados.

## Computador (`computador/momentos_inercia.py`)

```
python -m pip install matplotlib numpy
python computador/momentos_inercia.py
```

## Calculadora TI-Nspire CX II / CX II CAS (`calculadora/inercia_nspire.py`)

Requiere OS 5.2 o superior (Python).

1. Pestaña **Actions** → último proceso "Generar inercia.tns" → sección **Artifacts** → descargar `inercia-tns`.
2. Descomprimir el .zip: adentro está `inercia.tns`.
3. Pasarlo a la calculadora con **TI-Nspire CX II Connect** (carpeta *Mis documentos*).
4. En la calculadora: abrir `inercia.tns` y ejecutar el programa con **Ctrl + R**.

Cada vez que se cambia `calculadora/inercia_nspire.py`, la acción genera un `inercia.tns` nuevo.
La conversión usa [Luna](https://github.com/ndless-nspire/Luna) (licencia MPL 1.1).
