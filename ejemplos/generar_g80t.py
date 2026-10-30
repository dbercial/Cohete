"""Genera las configuraciones del cohete G80T (modelo base + iteraciones) para importar.

Datos originales y suposiciones en g80t_modelo.md. Uso, desde la carpeta del proyecto:
    .\\.venv\\Scripts\\python.exe ejemplos\\generar_g80t.py [--todas]
"""

import math
import sys
from pathlib import Path

PROYECTO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROYECTO))
from presentacion import resumen  # noqa: E402
from simulacion import (exportar_biblioteca, extraer_resultados, guardar_json,  # noqa: E402
                        parametros_por_defecto, simular, PARAMETROS)

# Densidades [g/cm³] y espesores [mm] supuestos por material
MATERIALES = {
    "cartón": {"tubo_rho": 0.8, "tubo_pared": 1.0, "aleta_rho": 0.7},
    "fibra de vidrio": {"tubo_rho": 1.85, "tubo_pared": 1.0, "aleta_rho": 1.85},
}


def cohete(masa_g=300, diametro=38, ojiva_len=190, cuerpo_len=370, ojiva_tipo="von karman",
           raiz=90, punta=40, altura=50, barrido=50, espesor=2.0, material="cartón"):
    """Devuelve los parámetros de la pestaña Cohete. Medidas en mm, eje x desde la cola hacia la ojiva."""
    mat = MATERIALES[material]
    r = diametro / 2
    piezas = []  # (masa g, x del centro de masas mm, inercia lateral propia g·mm², inercia axial g·mm²)

    # Tubo del cuerpo (cilindro hueco de pared fina)
    m = math.pi * diametro * cuerpo_len * mat["tubo_pared"] * mat["tubo_rho"] / 1000
    piezas.append((m, cuerpo_len / 2, m * (cuerpo_len ** 2 / 12 + r ** 2 / 2), m * r ** 2))

    # Ojiva de plástico hueca: 30 g para 190 mm × Ø38, escalada por superficie; CdM a 0,4 L de la base
    m = 30 * (ojiva_len * diametro) / (190 * 38)
    piezas.append((m, cuerpo_len + 0.4 * ojiva_len, m * ojiva_len ** 2 / 18, m * r ** 2 / 2))

    # Aletas: raíz enrasada con la cola (borde de salida de la raíz en x = 0)
    area = (raiz + punta) / 2 * altura
    m_aleta = area * espesor * mat["aleta_rho"] / 1000
    # Centroide del trapecio medido desde el borde de ataque de la raíz hacia la cola
    x_c = ((raiz ** 2 + raiz * punta + punta ** 2) + barrido * (raiz + 2 * punta)) / (3 * (raiz + punta))
    radial = r + altura * (raiz + 2 * punta) / (3 * (raiz + punta))
    m = 3 * m_aleta
    piezas.append((m, raiz - x_c, m * (raiz ** 2 / 12 + radial ** 2 / 2), m * radial ** 2))

    # Tubo interior del motor (140 mm × Ø29,5, cartón 0,5 mm) + 2 anillos de centrado (3 g)
    m = math.pi * 29.5 * 140 * 0.5 * 0.8 / 1000 + 6
    piezas.append((m, 70, m * (140 ** 2 / 12 + 14.75 ** 2 / 2), m * 14.75 ** 2))

    # Componente de masa (altímetro, paracaídas...) en la parte alta del cuerpo hasta completar la masa
    m = masa_g - sum(p[0] for p in piezas)
    assert m > 0, f"las piezas ya pesan más de {masa_g} g"
    rc = 0.8 * r
    piezas.append((m, cuerpo_len - 60, m * (50 ** 2 / 12 + rc ** 2 / 4), m * rc ** 2 / 2))

    masa = sum(p[0] for p in piezas)
    cdm = sum(p[0] * p[1] for p in piezas) / masa
    i_lat = sum(p[2] + p[0] * (p[1] - cdm) ** 2 for p in piezas)
    i_ax = sum(p[3] for p in piezas)

    def pos(x_mm):  # posición en el sistema de la app: m desde el CdM sin motor, + hacia la ojiva
        return round((x_mm - cdm) / 1000, 4)

    return {
        "diametro": float(diametro),
        "masa": round(masa / 1000, 4),
        "inercia_lateral": round(i_lat * 1e-9, 6),
        "inercia_axial": round(i_ax * 1e-9, 7),
        "posicion_motor": pos(0),
        "boton_superior": pos(cuerpo_len - 40),
        "boton_inferior": pos(raiz / 2),
        "cd_subsonico": 0.45,
        "aumento_transonico": 40.0,
        "ojiva_longitud": ojiva_len / 1000,
        "ojiva_tipo": ojiva_tipo,
        "ojiva_posicion": pos(cuerpo_len + ojiva_len),
        "aletas_numero": 3,
        "aletas_cuerda_raiz": raiz / 1000,
        "aletas_cuerda_punta": punta / 1000,
        "aletas_envergadura": altura / 1000,
        "aletas_barrido": barrido / 1000,
        "aletas_posicion": pos(raiz),
        "cola_radio_inferior": round(r / 1000, 4),
        "cola_longitud": 0.0,
        "cola_posicion": pos(0),
    }


def entorno(viento):
    p = parametros_por_defecto()
    datos = {k: p[k] for k in PARAMETROS["Entorno"]}
    datos["viento_velocidad"] = float(viento)
    return datos


# AeroTech G80T (29 × 124 mm, Blue Thunder), datos certificados NAR según thrustcurve.org:
# 136,6 N·s, 1,7 s, 127,9 g en total, 62,5 g de propelente -> 65,4 g de carcasa.
# La forma "regresiva" queda a ~1,5 % en apogeo de la curva real (meseta de ~105 N y cola larga).
MOTOR = {
    "impulso_total": 136.6,
    "tiempo_combustion": 1.7,
    "forma_empuje": "regresiva",
    "masa_seca_motor": 0.0654,
    "radio_tobera": 6.0,
    "radio_garganta": 3.0,
    "num_granos": 2,
    "densidad_grano": 1727.0,  # ajustada para que los granos sumen 62,5 g
    "radio_exterior_grano": 12.0,
    "radio_interior_grano": 4.0,
    "altura_grano": 45.0,
    "separacion_granos": 2.0,
}
LANZAMIENTO = {"longitud_rail": 1.5, "inclinacion": 85.0, "rumbo": 0.0}
PARACAIDAS = {k: parametros_por_defecto()[k] for k in PARAMETROS["Paracaídas"]}

COHETES = {
    "G80T · Base Ø38 300 g": cohete(),
    "G80T · Masa 280 g": cohete(masa_g=280),
    "G80T · Masa 380 g": cohete(masa_g=380),
    "G80T · Ø30 500 mm": cohete(diametro=30, cuerpo_len=310),
    "G80T · Aletas raíz 70": cohete(raiz=70),
    "G80T · Aletas raíz 110": cohete(raiz=110),
    "G80T · Aletas altura 40": cohete(altura=40),
    "G80T · Aletas altura 60": cohete(altura=60),
    "G80T · Aletas espesor 1,5": cohete(espesor=1.5),
    "G80T · Ojiva tangente": cohete(ojiva_tipo="tangent"),
    "G80T · Ojiva 150 mm": cohete(ojiva_len=150),
    "G80T · Ojiva 250 mm": cohete(ojiva_len=250),
    "G80T · Fibra de vidrio": cohete(material="fibra de vidrio"),
}

biblioteca = {
    "Entorno": {f"Campo · viento {v} m/s": entorno(v) for v in (0, 3, 5, 8)},
    "Motor": {"AeroTech G80T": MOTOR},
    "Cohete": COHETES,
    "Paracaídas": {
        "Por defecto": PARACAIDAS,
        # Cúpula redonda de 45 cm: Cd·S ≈ 0,8 × π × 0,225² ≈ 0,13 m², abierta en el apogeo
        "Único 45 cm en apogeo": {**PARACAIDAS, "drogue_cds": 0.13, "principal_cds": 0.0},
    },
    "Lanzamiento": {"Carril 1,5 m a 5°": LANZAMIENTO},
}

salida = PROYECTO / "ejemplos"
salida.mkdir(exist_ok=True)
exportar_biblioteca(salida / "g80t_configuraciones.json", biblioteca)

# Simulación del modelo base (condiciones comunes), con resultados
base = parametros_por_defecto()
for datos in (entorno(3), MOTOR, COHETES["G80T · Base Ø38 300 g"], PARACAIDAS, LANZAMIENTO):
    base.update(datos)
resultados = extraer_resultados(*simular(base))
guardar_json(salida / "g80t_base.json", base, resultados)

print("Base:", {k: COHETES["G80T · Base Ø38 300 g"][k] for k in
                ("masa", "inercia_lateral", "inercia_axial", "posicion_motor", "ojiva_posicion",
                 "aletas_posicion", "boton_superior", "boton_inferior")})
print(resumen(resultados))

if "--todas" in sys.argv:
    print(f"\n{'Cohete':28s} {'margen':>6s} {'v_rail':>6s} {'apogeo':>7s} {'vmax':>6s}")
    for nombre, datos in COHETES.items():
        p = {**base, **datos}
        m = extraer_resultados(*simular(p))["metricas"]
        print(f"{nombre:28s} {m['margen_estatico']:6.2f} {m['velocidad_salida_rail']:6.1f} "
              f"{m['apogeo']:7.0f} {m['velocidad_maxima']:6.1f}")
    for nombre, datos in biblioteca["Paracaídas"].items():
        print(f"\nParacaídas «{nombre}»:", resumen(extraer_resultados(*simular({**base, **datos}))).splitlines()[-1])
