# Cohete

Simulador de vuelo de un cohete de modelismo de alta potencia, con interfaz gráfica, basado en
[RocketPy](https://rocketpy.org/).

Defines el lugar de lanzamiento, el motor, el cohete, los paracaídas y el raíl; la aplicación
simula el vuelo completo en 6 grados de libertad (despegue, ascenso, apogeo, descenso con
paracaídas y aterrizaje) y muestra el resultado en números y gráficas. Cada parte se puede
guardar con un nombre para combinar motores, cohetes, entornos, etc. y comparar resultados.

## Ejecución

**Doble clic en `Cohete.bat`.**

- La primera vez crea un entorno virtual (`.venv`) e instala las dependencias de
  `requirements.txt`. Tarda unos minutos y necesita **Python 3.10 o superior** instalado y en
  el `PATH`.
- Las siguientes veces abre directamente la interfaz.

Alternativa desde una terminal en la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe interfaz.py
```

## Uso

La ventana tiene los parámetros a la izquierda, organizados en pestañas, y los resultados a la
derecha.

1. **Ajusta los parámetros** de cada pestaña. Los campos numéricos tienen flechas para subir o
   bajar el valor (o se puede escribir directamente).
2. Pulsa **Simular**. En unos segundos aparecen el resumen y las gráficas.
3. **Valores por defecto** devuelve todas las pestañas a la configuración inicial.

### Resultados

- **Margen estático inicial** (en calibres): distancia entre el centro de presiones y el centro
  de masas dividida por el diámetro. Entre 1 y 3 el cohete es estable; por debajo de 1 puede
  volar de forma inestable, y muy por encima tiende a girarse contra el viento.
- **Velocidad al salir del raíl**: conviene que supere unos 15–20 m/s para que las aletas ya
  estabilicen el cohete.
- **Apogeo**: altura máxima sobre el suelo y el instante en que se alcanza.
- **Velocidad máxima** y su número de Mach.
- **Impacto**: tiempo total de vuelo, velocidad de aterrizaje y punto de caída (x hacia el Este,
  y hacia el Norte, en metros desde la rampa).

Gráficas: altitud, velocidad y aceleración frente al tiempo, y trayectoria vista desde arriba.
La barra de herramientas bajo las gráficas permite hacer zoom y guardarlas como imagen.

### Configuraciones guardadas

Arriba de cada pestaña hay una barra para guardar los valores **de esa pestaña** con un nombre:

- **Guardar…** pide un nombre y guarda los valores actuales de la pestaña.
- **Cargar** aplica la configuración elegida en la lista (solo a esa pestaña).
- **Eliminar** la borra.

Así se pueden combinar, por ejemplo, el motor «M grande» con el cohete «Ligero» y el entorno
«Viento oeste». Las configuraciones se guardan en `biblioteca.json` y se conservan entre
sesiones.

### Importar y exportar

**Exportar JSON…** pregunta qué exportar:

- **Simulación actual**: los valores de todas las pestañas y, si ya se ha simulado con ellos,
  los resultados (métricas y series de las gráficas).
- **Todas las guardadas**: todas las configuraciones guardadas de todas las pestañas, para
  llevarlas a otro ordenador o compartirlas.

**Importar JSON…** reconoce el tipo de archivo. Una simulación rellena las pestañas y muestra
sus resultados sin volver a simular; unas configuraciones guardadas se pueden **añadir** a las
tuyas o **reemplazarlas**. Si a un archivo le faltan valores, se usan los de por defecto.

## Parámetros

### Entorno

| Parámetro | Descripción |
|---|---|
| Latitud / Longitud [°] | Situación del lugar de lanzamiento. Afecta a la gravedad. Por defecto, Oviedo. |
| Elevación del lugar [m] | Altitud del suelo sobre el nivel del mar. Las alturas de los resultados se dan sobre el suelo. |
| Temperatura en el suelo [°C] | La temperatura baja 6,5 °C por km hasta la tropopausa. Afecta a la densidad del aire y a la velocidad del sonido. La presión sigue la atmósfera estándar. |
| Velocidad del viento [m/s] | Viento constante con la altura. |
| Dirección de procedencia del viento [°] | De dónde **viene** el viento: 0 = Norte, 90 = Este, 180 = Sur, 270 = Oeste. Un viento de 270° desplaza el cohete hacia el Este. |

### Motor

Motor de propelente sólido. La curva de empuje se genera a partir del impulso total, el tiempo y
la forma.

| Parámetro | Descripción |
|---|---|
| Impulso total [N·s] | Empuje total entregado (área bajo la curva de empuje). Determina la clase del motor: H 160–320, I –640, J –1280, K –2560, L –5120, M –10240 N·s. |
| Tiempo de combustión [s] | Duración del empuje. Empuje medio = impulso / tiempo. |
| Forma de la curva de empuje | **constante**: empuje plano. **progresiva**: crece durante la combustión. **regresiva**: decrece. **pico inicial**: arranque fuerte y luego empuje sostenido. Todas incluyen un arranque y apagado suaves. |
| Masa seca del motor [kg] | Masa de la carcasa sin propelente. |
| Radio de la tobera / garganta [mm] | Radio de la salida de la tobera y de su parte más estrecha. |
| Número de granos | Bloques cilíndricos de propelente apilados. |
| Densidad del propelente [kg/m³] | Junto con el tamaño de los granos, fija la masa de propelente. |
| Radio exterior / interior inicial del grano [mm] | El grano es un tubo: arde desde el hueco interior hacia fuera. |
| Altura del grano / Separación entre granos [mm] | Longitud de cada grano y hueco entre ellos. |

### Cohete

**Criterio de posiciones:** todas las posiciones se miden en metros a lo largo del eje del
cohete, desde su **centro de masas sin motor**, con valores **positivos hacia la ojiva** y
negativos hacia la cola.

| Parámetro | Descripción |
|---|---|
| Diámetro [mm] | Diámetro del fuselaje. Es también la referencia del margen estático. |
| Masa sin motor [kg] | Masa del cohete completo (incluidos paracaídas y electrónica) sin el motor. |
| Inercia lateral / axial [kg·m²] | Momentos de inercia sin motor: respecto a un eje perpendicular al cohete (cabeceo) y respecto a su eje longitudinal (alabeo). |
| Posición de la tobera [m] | Dónde queda la salida del motor. |
| Coeficiente de arrastre subsónico (Cd) | Cd del cohete a baja velocidad. Valores típicos: 0,35–0,6. |
| Aumento del Cd cerca de Mach 1 [%] | Cuánto sube el Cd al acercarse a la velocidad del sonido. El Cd es constante hasta Mach 0,8, máximo en Mach 1,05 y baja después. Con 0 % el Cd es constante. |
| Longitud / Tipo / Posición de la ojiva | Forma del morro y dónde está su base. |
| Número de aletas | Aletas trapezoidales repartidas alrededor del fuselaje. |
| Cuerda en la raíz / en la punta [m] | Longitud de la aleta junto al fuselaje y en su extremo. |
| Envergadura de las aletas [m] | Cuánto sobresale cada aleta del fuselaje. |
| Posición de las aletas [m] | Posición del borde de ataque de la raíz. |
| Radio inferior / Longitud / Posición de la cola | Estrechamiento cónico al final del fuselaje. El radio superior es el del fuselaje. |

### Paracaídas

Hay dos paracaídas: un **drogue** (pequeño) que se abre en el apogeo para bajar rápido sin
desviarse mucho, y un **principal** que se abre cerca del suelo para aterrizar despacio.

| Parámetro | Descripción |
|---|---|
| Cd·S del drogue / principal [m²] | Coeficiente de arrastre por área del paracaídas. Cuanto mayor, más lento cae. Para una cúpula redonda, Cd·S ≈ 0,8 × área. |
| Apertura del principal [m sobre el suelo] | Altura a la que se despliega el principal. |
| Retardo de apertura [s] | Tiempo entre la orden de apertura y el despliegue efectivo. |

### Lanzamiento

| Parámetro | Descripción |
|---|---|
| Longitud del raíl [m] | Guía por la que desliza el cohete al despegar. Más largo = más velocidad al salir. |
| Inclinación [°] | Ángulo del raíl respecto al suelo: 90 = vertical. |
| Rumbo [°] | Hacia dónde apunta el raíl: 0 = Norte, 90 = Este. |

### Valores fijos

Algunos valores no son editables desde la interfaz y están en `simulacion.py`: la inercia del
motor seco, la posición de su centro de masas, la posición de los botones del raíl
(0,082 m y −0,618 m) y el ángulo de inclinación de las aletas (0,5°).

## Archivos

| Archivo | Contenido |
|---|---|
| `Cohete.bat` | Lanzador. |
| `interfaz.py` | Interfaz gráfica (tkinter). |
| `simulacion.py` | Definición de parámetros, construcción del modelo en RocketPy, simulación y lectura/escritura de JSON. |
| `biblioteca.json` | Configuraciones guardadas (se crea al guardar la primera). |
| `resultados/` | Carpeta propuesta por defecto para exportar simulaciones. |
| `requirements.txt` | Dependencias de Python. |
