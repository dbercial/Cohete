"""Sistemas de unidades. Los valores internos (simulación, JSON) están siempre en SI, salvo las
magnitudes "longitud_mm", que se guardan en mm. Aquí solo se convierte lo que se muestra."""

import math

SISTEMAS = ["metrico", "imperial"]

# magnitud -> sistema -> (símbolo, factor): valor mostrado = valor interno × factor (+ desplazamiento)
UNIDADES = {
    "distancia": {"metrico": ("m", 1), "imperial": ("ft", 3.28084)},
    "longitud": {"metrico": ("m", 1), "imperial": ("in", 39.3701)},
    "longitud_mm": {"metrico": ("mm", 1), "imperial": ("in", 1 / 25.4)},
    "velocidad": {"metrico": ("m/s", 1), "imperial": ("ft/s", 3.28084)},
    "velocidad_viento": {"metrico": ("m/s", 1), "imperial": ("mph", 2.23694)},
    "aceleracion": {"metrico": ("m/s²", 1), "imperial": ("ft/s²", 3.28084)},
    "masa": {"metrico": ("kg", 1), "imperial": ("lb", 2.20462)},
    "impulso": {"metrico": ("N·s", 1), "imperial": ("lbf·s", 0.224809)},
    "densidad": {"metrico": ("kg/m³", 1), "imperial": ("lb/ft³", 0.0624280)},
    "inercia": {"metrico": ("kg·m²", 1), "imperial": ("lb·ft²", 23.7304)},
    "area": {"metrico": ("m²", 1), "imperial": ("ft²", 10.7639)},
    "temperatura": {"metrico": ("°C", 1), "imperial": ("°F", 1.8)},
    "grados": {"metrico": ("°", 1), "imperial": ("°", 1)},
    "angulo": {"metrico": ("°", 1), "imperial": ("°", 1)},
    "tiempo": {"metrico": ("s", 1), "imperial": ("s", 1)},
    "porcentaje": {"metrico": ("%", 1), "imperial": ("%", 1)},
    "calibres": {"metrico": ("cal", 1), "imperial": ("cal", 1)},
    "adimensional": {"metrico": ("", 1), "imperial": ("", 1)},
    "entero": {"metrico": ("", 1), "imperial": ("", 1)},
}
DESPLAZAMIENTO = {("temperatura", "imperial"): 32}


def simbolo(magnitud, sistema):
    return UNIDADES[magnitud][sistema][0]


def a_mostrar(valor, magnitud, sistema):
    return valor * UNIDADES[magnitud][sistema][1] + DESPLAZAMIENTO.get((magnitud, sistema), 0)


def a_interno(valor, magnitud, sistema):
    return (valor - DESPLAZAMIENTO.get((magnitud, sistema), 0)) / UNIDADES[magnitud][sistema][1]


def paso_redondo(paso, magnitud, sistema):
    """Convierte el paso de las flechas y lo redondea a 1, 2 o 5 × 10ⁿ."""
    paso = paso * UNIDADES[magnitud][sistema][1]
    exponente = math.floor(math.log10(paso))
    base = paso / 10 ** exponente
    redondo = 1 if base < 1.5 else 2 if base < 3.5 else 5 if base < 7.5 else 10
    return round(redondo * 10 ** exponente, max(0, -exponente))


def formatear(valor, cifras=6):
    """Número con hasta `cifras` cifras significativas y sin notación científica."""
    if valor == 0:
        return "0"
    decimales = max(0, cifras - 1 - math.floor(math.log10(abs(valor))))
    texto = f"{valor:.{decimales}f}"
    return texto.rstrip("0").rstrip(".") if "." in texto else texto
