"""Resumen y gráficas de los resultados en el idioma y el sistema de unidades elegidos."""

from textos import tr
from unidades import a_mostrar, simbolo


def _valor(valor, magnitud, sistema, decimales):
    """Valor convertido y formateado con su unidad, p. ej. "1520 m" o "4987 ft"."""
    unidad = simbolo(magnitud, sistema)
    texto = f"{a_mostrar(valor, magnitud, sistema):.{decimales}f}"
    return f"{texto} {unidad}" if unidad else texto


def resumen(resultados, idioma="es", sistema="metrico"):
    m = resultados["metricas"]

    def v(clave, magnitud, decimales):
        return _valor(m[clave], magnitud, sistema, decimales)

    if m.get("aterriza", True):
        impacto = tr("r_impacto", idioma, t=v("tiempo_impacto", "tiempo", 1),
                     v=v("velocidad_impacto", "velocidad", 1),
                     x=v("x_impacto", "distancia", 0), y=v("y_impacto", "distancia", 0))
    else:
        impacto = tr("r_no_aterriza", idioma, t=v("tiempo_impacto", "tiempo", 0))
    return "\n".join([
        tr("r_margen", idioma, v=v("margen_estatico", "calibres", 2)),
        tr("r_rail", idioma, v=v("velocidad_salida_rail", "velocidad", 1)),
        tr("r_apogeo", idioma, h=v("apogeo", "distancia", 0), t=v("tiempo_apogeo", "tiempo", 1)),
        tr("r_vmax", idioma, v=v("velocidad_maxima", "velocidad", 1), m=f"{m['mach_maximo']:.2f}"),
        impacto,
    ])


def dibujar_graficas(resultados, fig, idioma="es", sistema="metrico"):
    """Dibuja altitud, velocidad, aceleración y trayectoria en la figura dada."""
    s = resultados["series"]

    def serie(clave, magnitud):
        return [a_mostrar(x, magnitud, sistema) for x in s[clave]]

    def u(magnitud):
        return f"[{simbolo(magnitud, sistema)}]"

    fig.clear()
    ejes = fig.subplots(2, 2)
    eje_t = "t [s]"
    ejes[0, 0].plot(s["t"], serie("altitud", "distancia"))
    ejes[0, 0].set(title=tr("g_altitud", idioma), xlabel=eje_t, ylabel=f"h {u('distancia')}")
    ejes[0, 1].plot(s["t"], serie("velocidad", "velocidad"))
    ejes[0, 1].set(title=tr("g_velocidad", idioma), xlabel=eje_t, ylabel=f"v {u('velocidad')}")
    ejes[1, 0].plot(s["t"], serie("aceleracion", "aceleracion"))
    ejes[1, 0].set(title=tr("g_aceleracion", idioma), xlabel=eje_t, ylabel=f"a {u('aceleracion')}")
    ejes[1, 1].plot(serie("x", "distancia"), serie("y", "distancia"))
    ejes[1, 1].set(title=tr("g_trayectoria", idioma), xlabel=f"{tr('eje_x', idioma)} {u('distancia')}",
                   ylabel=f"{tr('eje_y', idioma)} {u('distancia')}")
    for eje in ejes.flat:
        eje.grid(True)
    fig.tight_layout()
