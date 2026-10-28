"""Definición de un cohete y simulación de su vuelo con RocketPy."""

import json
import math
from pathlib import Path

from rocketpy import Environment, Flight, Function, Rocket, SolidMotor

RESULTADOS = Path(__file__).parent / "resultados"
BIBLIOTECA = Path(__file__).parent / "biblioteca.json"
TIEMPO_MAXIMO = 3600  # s de vuelo simulado como máximo (descensos lentos con paracaídas grandes)

TIPOS_OJIVA = ["von karman", "ogive", "conical", "elliptical", "tangent", "lvhaack", "powerseries"]
FORMAS_EMPUJE = ["constante", "progresiva", "regresiva", "pico inicial"]

# Parámetros de entrada agrupados por sección.
# Numéricos: clave -> (etiqueta, valor por defecto, paso, mínimo, máximo).
# Opciones: clave -> (etiqueta, valor por defecto, lista de opciones).
PARAMETROS = {
    "Entorno": {
        "latitud": ("Latitud [°]", 43.36, 0.01, -90, 90),
        "longitud": ("Longitud [°]", -5.85, 0.01, -180, 180),
        "elevacion": ("Elevación del lugar [m]", 230.0, 10, -500, 9000),
        "temperatura_suelo": ("Temperatura en el suelo [°C]", 15.0, 1, -60, 60),
        "viento_velocidad": ("Velocidad del viento [m/s]", 0.0, 0.5, 0, 50),
        "viento_direccion": ("Dirección de procedencia del viento [°]", 0.0, 15, 0, 360),
    },
    "Motor": {
        "impulso_total": ("Impulso total [N·s]", 6200.0, 100, 1, 1000000),
        "tiempo_combustion": ("Tiempo de combustión [s]", 3.9, 0.1, 0.1, 300),
        "forma_empuje": ("Forma de la curva de empuje", "regresiva", FORMAS_EMPUJE),
        "masa_seca_motor": ("Masa seca del motor [kg]", 1.815, 0.001, 0, 1000),
        "radio_tobera": ("Radio de la tobera [mm]", 33.0, 1, 1, 1000),
        "radio_garganta": ("Radio de la garganta [mm]", 11.0, 1, 1, 1000),
        "num_granos": ("Número de granos", 5, 1, 1, 50),
        "densidad_grano": ("Densidad del propelente [kg/m³]", 1815.0, 10, 1, 10000),
        "radio_exterior_grano": ("Radio exterior del grano [mm]", 33.0, 1, 1, 1000),
        "radio_interior_grano": ("Radio interior inicial del grano [mm]", 15.0, 1, 0, 1000),
        "altura_grano": ("Altura del grano [mm]", 120.0, 5, 1, 5000),
        "separacion_granos": ("Separación entre granos [mm]", 5.0, 1, 0, 1000),
    },
    "Cohete": {
        "diametro": ("Diámetro [mm]", 127.0, 1, 1, 2000),
        "masa": ("Masa sin motor [kg]", 14.426, 0.01, 0.001, 10000),
        "inercia_lateral": ("Inercia lateral [kg·m²]", 6.321, 0.0001, 0, 10000),
        "inercia_axial": ("Inercia axial [kg·m²]", 0.034, 0.00001, 0, 1000),
        "posicion_motor": ("Posición de la tobera [m]", -1.255, 0.01, -50, 50),
        "boton_superior": ("Posición del botón de raíl superior [m]", 0.082, 0.01, -50, 50),
        "boton_inferior": ("Posición del botón de raíl inferior [m]", -0.618, 0.01, -50, 50),
        "cd_subsonico": ("Coeficiente de arrastre subsónico (Cd)", 0.45, 0.01, 0.01, 5),
        "aumento_transonico": ("Aumento del Cd cerca de Mach 1 [%]", 40.0, 5, 0, 300),
        "ojiva_longitud": ("Longitud de la ojiva [m]", 0.558, 0.01, 0.01, 10),
        "ojiva_tipo": ("Tipo de ojiva", "von karman", TIPOS_OJIVA),
        "ojiva_posicion": ("Posición de la ojiva [m]", 1.278, 0.01, -50, 50),
        "aletas_numero": ("Número de aletas", 4, 1, 1, 12),
        "aletas_cuerda_raiz": ("Cuerda en la raíz [m]", 0.120, 0.005, 0.001, 10),
        "aletas_cuerda_punta": ("Cuerda en la punta [m]", 0.060, 0.005, 0, 10),
        "aletas_envergadura": ("Envergadura de las aletas [m]", 0.110, 0.005, 0.001, 10),
        "aletas_barrido": ("Barrido de las aletas [m]", 0.060, 0.005, -10, 10),
        "aletas_posicion": ("Posición de las aletas [m]", -1.04956, 0.01, -50, 50),
        "cola_radio_inferior": ("Radio inferior de la cola [m]", 0.0435, 0.001, 0, 10),
        "cola_longitud": ("Longitud de la cola [m] (0 = sin cola)", 0.060, 0.005, 0, 10),
        "cola_posicion": ("Posición de la cola [m]", -1.194656, 0.01, -50, 50),
    },
    "Paracaídas": {
        "drogue_cds": ("Cd·S del drogue [m²]", 1.0, 0.01, 0, 1000),
        "principal_cds": ("Cd·S del principal [m²]", 10.0, 0.5, 0, 1000),
        "principal_altura": ("Apertura del principal [m sobre el suelo]", 500.0, 50, 0, 100000),
        "retardo": ("Retardo de apertura [s]", 1.5, 0.1, 0, 60),
    },
    "Lanzamiento": {
        "longitud_rail": ("Longitud del raíl [m]", 5.2, 0.1, 0.1, 100),
        "inclinacion": ("Inclinación [°]", 85.0, 1, 0, 90),
        "rumbo": ("Rumbo [°] (0 = Norte)", 0.0, 5, 0, 360),
    },
}

def parametros_por_defecto():
    return {clave: spec[1] for seccion in PARAMETROS.values() for clave, spec in seccion.items()}


def curva_empuje(impulso_total, tiempo, forma, puntos=60):
    """Curva (t [s], F [N]) con la forma indicada, escalada para dar el impulso total pedido."""
    perfiles = {
        "constante": lambda x: 1.0,
        "progresiva": lambda x: 0.6 + 0.8 * x,
        "regresiva": lambda x: 1.4 - 0.8 * x,
        "pico inicial": lambda x: 1.0 + 1.5 * math.exp(-x / 0.06),
    }
    perfil = perfiles[forma]

    # Arranque y apagado suaves durante el 3 % inicial y final de la combustión
    def rampa(x):
        return min(1.0, x / 0.03, (1 - x) / 0.03)

    tiempos = [tiempo * i / (puntos - 1) for i in range(puntos)]
    empujes = [perfil(t / tiempo) * rampa(t / tiempo) for t in tiempos]
    impulso = sum((empujes[i] + empujes[i + 1]) / 2 * (tiempos[i + 1] - tiempos[i])
                  for i in range(puntos - 1))
    escala = impulso_total / impulso
    return [(t, f * escala) for t, f in zip(tiempos, empujes)]


def curva_arrastre(cd, aumento_transonico):
    """Curva (Mach, Cd): plana en subsónico, con un pico cerca de Mach 1 y bajada posterior."""
    a = aumento_transonico / 100
    factores = [(0.0, 0), (0.8, 0), (0.95, 0.7), (1.05, 1), (1.2, 0.85), (1.5, 0.6), (2.5, 0.35), (5.0, 0.2)]
    return [(mach, cd * (1 + a * factor)) for mach, factor in factores]


def crear_entorno(p):
    env = Environment(latitude=p["latitud"], longitude=p["longitud"], elevation=p["elevacion"])

    # Temperatura: gradiente estándar de -6,5 K/km desde el suelo hasta la tropopausa (216,65 K)
    t_suelo = p["temperatura_suelo"] + 273.15
    elevacion = p["elevacion"]

    def temperatura(h):
        return max(t_suelo - 0.0065 * (h - elevacion), 216.65)

    # El viento "procede de" la dirección indicada; u apunta al Este y v al Norte
    direccion = math.radians(p["viento_direccion"])
    env.set_atmospheric_model(
        type="custom_atmosphere",
        temperature=temperatura,
        wind_u=-p["viento_velocidad"] * math.sin(direccion),
        wind_v=-p["viento_velocidad"] * math.cos(direccion),
    )
    return env


def crear_motor(p):
    """Motor sólido con curva de empuje generada a partir del impulso total y su forma."""
    curva = curva_empuje(p["impulso_total"], p["tiempo_combustion"], p["forma_empuje"])
    num_granos = int(p["num_granos"])
    altura_grano = p["altura_grano"] / 1000
    separacion = p["separacion_granos"] / 1000
    longitud_granos = num_granos * altura_grano + (num_granos - 1) * separacion
    # Geometría aproximada de la carcasa: los granos empiezan a 2 radios de la tobera y la
    # carcasa se trata como un tubo delgado centrado en ellos
    radio_carcasa = p["radio_exterior_grano"] / 1000
    inicio_granos = 2 * radio_carcasa
    centro_granos = inicio_granos + longitud_granos / 2
    longitud_carcasa = inicio_granos + longitud_granos
    masa_seca = p["masa_seca_motor"]
    inercia_lateral = masa_seca * (radio_carcasa ** 2 / 2 + longitud_carcasa ** 2 / 12)
    return SolidMotor(
        thrust_source=curva,
        dry_mass=masa_seca,
        dry_inertia=(inercia_lateral, inercia_lateral, masa_seca * radio_carcasa ** 2),
        nozzle_radius=p["radio_tobera"] / 1000,
        grain_number=num_granos,
        grain_density=p["densidad_grano"],
        grain_outer_radius=p["radio_exterior_grano"] / 1000,
        grain_initial_inner_radius=p["radio_interior_grano"] / 1000,
        grain_initial_height=altura_grano,
        grain_separation=separacion,
        grains_center_of_mass_position=centro_granos,
        center_of_dry_mass_position=centro_granos,
        nozzle_position=0,
        burn_time=p["tiempo_combustion"],
        throat_radius=p["radio_garganta"] / 1000,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )


def crear_cohete(p, motor):
    """Posiciones en metros desde el centro de masas sin motor, positivas hacia la ojiva."""
    # Interpolación lineal: con la spline por defecto la curva oscila y hunde el Cd subsónico
    arrastre = Function(curva_arrastre(p["cd_subsonico"], p["aumento_transonico"]), "Mach", "Cd",
                        interpolation="linear", extrapolation="constant")
    radio = p["diametro"] / 2000

    cohete = Rocket(
        radius=radio,
        mass=p["masa"],
        inertia=(p["inercia_lateral"], p["inercia_lateral"], p["inercia_axial"]),
        power_off_drag=arrastre,
        power_on_drag=arrastre,
        center_of_mass_without_motor=0,
        coordinate_system_orientation="tail_to_nose",
    )
    cohete.add_motor(motor, position=p["posicion_motor"])
    cohete.set_rail_buttons(upper_button_position=p["boton_superior"],
                            lower_button_position=p["boton_inferior"])

    cohete.add_nose(length=p["ojiva_longitud"], kind=p["ojiva_tipo"], position=p["ojiva_posicion"])
    cohete.add_trapezoidal_fins(
        n=int(p["aletas_numero"]),
        root_chord=p["aletas_cuerda_raiz"],
        tip_chord=p["aletas_cuerda_punta"],
        span=p["aletas_envergadura"],
        position=p["aletas_posicion"],
        sweep_length=p["aletas_barrido"],
        cant_angle=0.5,
    )
    if p["cola_longitud"] > 0:  # longitud 0 = cohete sin cola
        cohete.add_tail(top_radius=radio, bottom_radius=p["cola_radio_inferior"],
                        length=p["cola_longitud"], position=p["cola_posicion"])

    # Drogue en el apogeo y paracaídas principal a cierta altura sobre el suelo (Cd·S = 0: no lo lleva)
    if p["drogue_cds"] > 0:
        cohete.add_parachute("Drogue", cd_s=p["drogue_cds"], trigger="apogee",
                             sampling_rate=105, lag=p["retardo"])
    if p["principal_cds"] > 0:
        cohete.add_parachute("Principal", cd_s=p["principal_cds"], trigger=p["principal_altura"],
                             sampling_rate=105, lag=p["retardo"])
    return cohete


def simular(p):
    """Construye entorno, motor y cohete con los parámetros dados y simula el vuelo."""
    env = crear_entorno(p)
    cohete = crear_cohete(p, crear_motor(p))
    vuelo = Flight(rocket=cohete, environment=env, rail_length=p["longitud_rail"],
                   inclination=p["inclinacion"], heading=p["rumbo"], max_time=TIEMPO_MAXIMO,
                   max_time_step=1)  # sin límite de paso el integrador se pierde en vuelos largos
    return cohete, vuelo


def extraer_resultados(cohete, vuelo):
    """Métricas y series temporales del vuelo como tipos simples (serializables a JSON)."""
    elevacion = vuelo.env.elevation
    t = vuelo.time
    metricas = {
        "margen_estatico": float(cohete.static_margin(0)),
        "velocidad_salida_rail": float(vuelo.out_of_rail_velocity),
        "apogeo": float(vuelo.apogee - elevacion),
        "tiempo_apogeo": float(vuelo.apogee_time),
        "velocidad_maxima": float(vuelo.max_speed),
        "mach_maximo": float(vuelo.max_mach_number),
        "aterriza": bool(vuelo.z(vuelo.t_final) - elevacion < 1),
        "tiempo_impacto": float(vuelo.t_final),
        "velocidad_impacto": float(abs(vuelo.impact_velocity)),
        "x_impacto": float(vuelo.x_impact),
        "y_impacto": float(vuelo.y_impact),
    }
    series = {
        "t": t,
        "altitud": vuelo.z(t) - elevacion,
        "velocidad": vuelo.speed(t),
        "aceleracion": vuelo.acceleration(t),
        "x": vuelo.x(t),
        "y": vuelo.y(t),
    }
    return {"metricas": metricas, "series": {k: [float(v) for v in vals] for k, vals in series.items()}}


def resumen(resultados):
    m = resultados["metricas"]
    if m.get("aterriza", True):
        impacto = (f"Impacto: t = {m['tiempo_impacto']:.1f} s, a {m['velocidad_impacto']:.1f} m/s, "
                   f"en x = {m['x_impacto']:.0f} m, y = {m['y_impacto']:.0f} m")
    else:
        impacto = f"Impacto: no llega al suelo en los {m['tiempo_impacto']:.0f} s simulados"
    return "\n".join([
        f"Margen estático inicial: {m['margen_estatico']:.2f} calibres",
        f"Velocidad al salir del raíl: {m['velocidad_salida_rail']:.1f} m/s",
        f"Apogeo: {m['apogeo']:.0f} m sobre el suelo (t = {m['tiempo_apogeo']:.1f} s)",
        f"Velocidad máxima: {m['velocidad_maxima']:.1f} m/s (Mach {m['mach_maximo']:.2f})",
        impacto,
    ])


def dibujar_graficas(resultados, fig):
    """Dibuja altitud, velocidad, aceleración y trayectoria en la figura dada."""
    s = resultados["series"]
    fig.clear()
    ejes = fig.subplots(2, 2)
    ejes[0, 0].plot(s["t"], s["altitud"])
    ejes[0, 0].set(title="Altitud sobre el suelo", xlabel="t [s]", ylabel="h [m]")
    ejes[0, 1].plot(s["t"], s["velocidad"])
    ejes[0, 1].set(title="Velocidad", xlabel="t [s]", ylabel="v [m/s]")
    ejes[1, 0].plot(s["t"], s["aceleracion"])
    ejes[1, 0].set(title="Aceleración", xlabel="t [s]", ylabel="a [m/s²]")
    ejes[1, 1].plot(s["x"], s["y"])
    ejes[1, 1].set(title="Trayectoria horizontal", xlabel="x (Este) [m]", ylabel="y (Norte) [m]")
    for eje in ejes.flat:
        eje.grid(True)
    fig.tight_layout()


def escribir_json(ruta, datos):
    Path(ruta).write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")


def leer_json(ruta):
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


# Archivos exportados: {"version": 1, "tipo": "simulacion" | "biblioteca", ...}

def guardar_json(ruta, parametros, resultados=None):
    escribir_json(ruta, {"version": 1, "tipo": "simulacion",
                         "parametros": parametros, "resultados": resultados})


def exportar_biblioteca(ruta, biblioteca):
    escribir_json(ruta, {"version": 1, "tipo": "biblioteca", "biblioteca": biblioteca})


def es_biblioteca(datos):
    return datos.get("tipo") == "biblioteca"


def simulacion_desde(datos):
    """Devuelve (parametros, resultados). Los parámetros que falten toman su valor por defecto."""
    parametros = parametros_por_defecto()
    parametros.update({k: v for k, v in datos.get("parametros", {}).items() if k in parametros})
    return parametros, datos.get("resultados")


def biblioteca_desde(datos):
    """Normaliza una biblioteca: todas las secciones presentes y solo las conocidas."""
    return {seccion: dict(datos.get(seccion, {})) for seccion in PARAMETROS}


def cargar_biblioteca():
    """Configuraciones guardadas con nombre: {sección: {nombre: {clave: valor}}}."""
    if BIBLIOTECA.exists():
        return biblioteca_desde(leer_json(BIBLIOTECA))
    return biblioteca_desde({})


def guardar_biblioteca(biblioteca):
    escribir_json(BIBLIOTECA, biblioteca)


if __name__ == "__main__":
    # La aplicación se usa siempre desde la interfaz gráfica
    from interfaz import Interfaz

    Interfaz().mainloop()
