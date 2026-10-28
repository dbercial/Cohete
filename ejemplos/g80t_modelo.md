# Cohete de 38 mm con AeroTech G80T

Datos originales del modelo, tal como se definieron. A partir de ellos `generar_g80t.py` crea
`g80t_base.json` y `g80t_configuraciones.json`.

## Modelo base

- **Ojiva:** Haack C=0 (Von Kármán), 190 mm, Ø38 mm, hombro 40 mm
- **Tubo del cuerpo:** 370 mm, Ø38 mm (incluye la sección del altímetro)
- **Tubo interior:** 140 mm, Ø29,5 mm, marcado como motor mount
- **Aletas:** 3, trapezoidales, raíz 90 / punta 40 / altura 50 / barrido 50 mm, espesor 2 mm
- **Componente de masa** para que la masa seca total (sin motor) sea 300 g
- **Motor:** AeroTech G80T

## Condiciones comunes

- Carril de 1,5 m a 5°
- Viento de 3 m/s
- Altitud del campo: la misma para todos
- El resto, por defecto

## Ideas para iteraciones

- **Masa:** masa seca de 280 / 300 / 380 g
- **Diámetro:** Ø38 mm (base) frente a Ø30 mm con ~500 mm de longitud total, misma masa
- **Aletas:** raíz 70/90/110 mm, altura 40/50/60 mm, espesor 1,5 frente a 2 mm
- **Ojiva y viento:** Von Kármán frente a tangente, longitud 150/190/250 mm, viento 0/3/5/8 m/s
- **Materiales:** fibra de vidrio o cartón

## Motor AeroTech G80T

Datos certificados (NAR) según [ThrustCurve.org](https://www.thrustcurve.org/motors/AeroTech/G80T/):

| Dato | Valor |
|---|---|
| Dimensiones | 29 × 124 mm, un solo uso |
| Propelente | Blue Thunder, 62,5 g |
| Masa total | 127,9 g (carcasa ≈ 65,4 g) |
| Impulso total | 136,6 N·s |
| Tiempo de combustión | 1,7 s |
| Empuje medio / máximo | 77,6 N / 108,5 N |
| Retardos | 6 a 14 s |

Curva real: meseta de ~105 N hasta 0,85 s, baja a ~88 N a 1,2 s y cola de ~20 N hasta 1,7 s.
En la aplicación se usa la forma «regresiva» con 1,7 s, que da un apogeo un 1,5 % mayor que la
curva real en el modelo base.

## Cómo se han traducido los datos

La aplicación no tiene campos para todas las medidas, así que algunas se convierten:

- **Medidas directas:** diámetro, longitud y tipo de ojiva, aletas (número, raíz, punta, altura,
  barrido), masa sin motor, carril, inclinación (85° = 5° respecto a la vertical) y viento.
- **Convertidas en posiciones:** la longitud del cuerpo, la de la ojiva y la raíz de las aletas
  fijan dónde quedan la punta de la ojiva, las aletas, el motor (enrasado con la cola) y los
  botones del raíl, medidos desde el centro de masas sin motor.
- **Convertidas en centro de masas e inercias:** el tubo interior, el espesor de las aletas, el
  material y el componente de masa.
- **No representado:** el hombro de la ojiva (va dentro del tubo y no cambia la forma exterior).

### Suposiciones

- Ojiva de plástico hueca de 30 g (para 190 mm × Ø38), con su centro de masas a 0,4 L de la base.
- Tubo de cartón de 1 mm (0,8 g/cm³) o de fibra de vidrio de 1 mm (1,85 g/cm³).
- Aletas de 0,7 g/cm³ (cartón) o 1,85 g/cm³ (fibra de vidrio), enrasadas con la cola.
- Tubo interior de cartón de 0,5 mm y dos anillos de centrado de 3 g.
- El componente de masa completa la masa total y va 60 mm por debajo de lo alto del cuerpo.
  Por eso, cambiar material o espesor no cambia la masa total, solo su reparto.
- Variante Ø30: ojiva de 190 mm y cuerpo de 310 mm (500 mm en total).
- Botones del raíl: uno entre las aletas y otro a 40 mm de lo alto del cuerpo.
- Cd 0,45 y dirección del viento 0° (del norte), por defecto.

## Regenerar los JSON

Cambia los datos en `generar_g80t.py` (en mm) y ejecuta desde la carpeta del proyecto:

```powershell
.\.venv\Scripts\python.exe ejemplos\generar_g80t.py
```

Con `--todas` también simula cada variante y muestra una tabla comparativa.
