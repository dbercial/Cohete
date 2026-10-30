"""Textos de la interfaz en español e inglés."""

IDIOMAS = {"es": "Español", "en": "English"}

TEXTOS = {
    # Ventana y menús
    "titulo_ventana": {"es": "Simulador de cohete — RocketPy", "en": "Rocket simulator — RocketPy"},
    "menu_ayuda": {"es": "Ayuda", "en": "Help"},
    "menu_manual": {"es": "Manual de uso", "en": "User manual"},
    "menu_idioma": {"es": "Idioma", "en": "Language"},
    "menu_unidades": {"es": "Unidades", "en": "Units"},
    "metrico": {"es": "Métrico (SI)", "en": "Metric (SI)"},
    "imperial": {"es": "Imperial (ft, in, lb)", "en": "Imperial (ft, in, lb)"},
    # Botones
    "simular": {"es": "Simular", "en": "Simulate"},
    "por_defecto": {"es": "Valores por defecto", "en": "Default values"},
    "importar": {"es": "Importar JSON…", "en": "Import JSON…"},
    "exportar": {"es": "Exportar JSON…", "en": "Export JSON…"},
    "guardadas": {"es": "Configuraciones guardadas", "en": "Saved configurations"},
    "cargar": {"es": "Cargar", "en": "Load"},
    "guardar": {"es": "Guardar…", "en": "Save…"},
    "eliminar": {"es": "Eliminar", "en": "Delete"},
    "cancelar": {"es": "Cancelar", "en": "Cancel"},
    # Estado
    "inicio": {"es": "Pulsa «Simular» para lanzar el vuelo.", "en": "Press “Simulate” to launch the flight."},
    "simulando": {"es": "Simulando…", "en": "Simulating…"},
    "sim_fallo": {"es": "La simulación ha fallado.", "en": "The simulation failed."},
    "importados_sin_resultados": {"es": "Parámetros importados (sin resultados). Pulsa «Simular».",
                                  "en": "Parameters imported (no results). Press “Simulate”."},
    # Diálogos
    "t_parametros": {"es": "Parámetros", "en": "Parameters"},
    "valor_no_valido": {"es": "Valor no válido en «{etiqueta}»: {texto!r}",
                        "en": "Invalid value in “{etiqueta}”: {texto!r}"},
    "t_biblioteca": {"es": "Configuraciones guardadas", "en": "Saved configurations"},
    "error_leer_biblioteca": {"es": "No se pudo leer biblioteca.json:\n{error}",
                              "en": "Could not read biblioteca.json:\n{error}"},
    "error_guardar_biblioteca": {"es": "No se pudo guardar biblioteca.json:\n{error}",
                                 "en": "Could not save biblioteca.json:\n{error}"},
    "t_guardar": {"es": "Guardar — {seccion}", "en": "Save — {seccion}"},
    "nombre_config": {"es": "Nombre de la configuración:", "en": "Configuration name:"},
    "sobrescribir": {"es": "Ya existe «{nombre}» en {seccion}. ¿Sobrescribir?",
                     "en": "“{nombre}” already exists in {seccion}. Overwrite?"},
    "t_cargar": {"es": "Cargar", "en": "Load"},
    "elige_config": {"es": "Elige una configuración de {seccion} en la lista.",
                     "en": "Choose a {seccion} configuration from the list."},
    "t_eliminar": {"es": "Eliminar", "en": "Delete"},
    "confirmar_eliminar": {"es": "¿Eliminar «{nombre}» de {seccion}?",
                           "en": "Delete “{nombre}” from {seccion}?"},
    "t_importar": {"es": "Importar", "en": "Import"},
    "t_importar_sim": {"es": "Importar simulación", "en": "Import simulation"},
    "todos_archivos": {"es": "Todos", "en": "All files"},
    "error_leer_archivo": {"es": "No se pudo leer el archivo:\n{error}", "en": "Could not read the file:\n{error}"},
    "t_importar_configs": {"es": "Importar configuraciones", "en": "Import configurations"},
    "importar_configs": {
        "es": "El archivo contiene {total} configuraciones guardadas.\n\n"
              "«Añadir»: se suman a las que ya tienes.{aviso}\n"
              "«Reemplazar»: se borran las tuyas y quedan solo las del archivo.",
        "en": "The file contains {total} saved configurations.\n\n"
              "“Add”: they are added to the ones you already have.{aviso}\n"
              "“Replace”: yours are deleted and only the file's remain."},
    "aviso_repetidas": {"es": "\n{n} tienen el mismo nombre que alguna tuya y la sustituirán.",
                        "en": "\n{n} have the same name as one of yours and will replace it."},
    "anadir": {"es": "Añadir", "en": "Add"},
    "reemplazar": {"es": "Reemplazar", "en": "Replace"},
    "importadas": {"es": "Importadas {total} configuraciones.", "en": "{total} configurations imported."},
    "t_exportar": {"es": "Exportar", "en": "Export"},
    "exportar_que": {
        "es": "¿Qué quieres exportar?\n\n"
              "«Simulación actual»: los valores de las pestañas y sus resultados.\n"
              "«Todas las guardadas»: todas tus configuraciones guardadas de cada sección.",
        "en": "What do you want to export?\n\n"
              "“Current simulation”: the values in the tabs and their results.\n"
              "“All saved”: all your saved configurations from every section."},
    "sim_actual": {"es": "Simulación actual", "en": "Current simulation"},
    "todas_guardadas": {"es": "Todas las guardadas", "en": "All saved"},
    "sin_guardadas": {"es": "No tienes ninguna configuración guardada todavía.",
                      "en": "You have no saved configurations yet."},
    "t_exportar_configs": {"es": "Exportar configuraciones guardadas", "en": "Export saved configurations"},
    "t_exportar_sim": {"es": "Exportar simulación", "en": "Export simulation"},
    "sin_simular": {"es": "Los parámetros actuales no se han simulado todavía.\n"
                          "¿Exportar solo los parámetros, sin resultados?",
                    "en": "The current parameters have not been simulated yet.\n"
                          "Export only the parameters, without results?"},
    "t_error_sim": {"es": "Error en la simulación", "en": "Simulation error"},
    "t_error_inesperado": {"es": "Error inesperado", "en": "Unexpected error"},
    # Resumen de resultados
    "r_margen": {"es": "Margen estático inicial: {v}", "en": "Initial static margin: {v}"},
    "r_rail": {"es": "Velocidad al salir del raíl: {v}", "en": "Rail departure speed: {v}"},
    "r_apogeo": {"es": "Apogeo: {h} sobre el suelo (t = {t})", "en": "Apogee: {h} above ground (t = {t})"},
    "r_vmax": {"es": "Velocidad máxima: {v} (Mach {m})", "en": "Maximum speed: {v} (Mach {m})"},
    "r_impacto": {"es": "Impacto: t = {t}, a {v}, en x = {x}, y = {y}",
                  "en": "Landing: t = {t}, at {v}, at x = {x}, y = {y}"},
    "r_no_aterriza": {"es": "Impacto: no llega al suelo en los {t} simulados",
                      "en": "Landing: does not reach the ground within the {t} simulated"},
    # Gráficas
    "g_altitud": {"es": "Altitud sobre el suelo", "en": "Altitude above ground"},
    "g_velocidad": {"es": "Velocidad", "en": "Speed"},
    "g_aceleracion": {"es": "Aceleración", "en": "Acceleration"},
    "g_trayectoria": {"es": "Trayectoria horizontal", "en": "Ground track"},
    "eje_x": {"es": "x (Este)", "en": "x (East)"},
    "eje_y": {"es": "y (Norte)", "en": "y (North)"},
}

# Nombres visibles de las secciones (las claves internas no cambian, se usan en los JSON)
SECCIONES = {
    "Entorno": {"es": "Entorno", "en": "Environment"},
    "Motor": {"es": "Motor", "en": "Motor"},
    "Cohete": {"es": "Cohete", "en": "Rocket"},
    "Paracaídas": {"es": "Paracaídas", "en": "Parachutes"},
    "Lanzamiento": {"es": "Lanzamiento", "en": "Launch"},
}

# Etiquetas de los parámetros, sin unidades (se añaden según el sistema elegido)
ETIQUETAS = {
    "latitud": {"es": "Latitud", "en": "Latitude"},
    "longitud": {"es": "Longitud", "en": "Longitude"},
    "elevacion": {"es": "Elevación del lugar", "en": "Site elevation"},
    "temperatura_suelo": {"es": "Temperatura en el suelo", "en": "Ground temperature"},
    "viento_velocidad": {"es": "Velocidad del viento", "en": "Wind speed"},
    "viento_direccion": {"es": "Dirección de procedencia del viento", "en": "Wind direction (from)"},
    "impulso_total": {"es": "Impulso total", "en": "Total impulse"},
    "tiempo_combustion": {"es": "Tiempo de combustión", "en": "Burn time"},
    "forma_empuje": {"es": "Forma de la curva de empuje", "en": "Thrust curve shape"},
    "masa_seca_motor": {"es": "Masa seca del motor", "en": "Motor dry mass"},
    "radio_tobera": {"es": "Radio de la tobera", "en": "Nozzle radius"},
    "radio_garganta": {"es": "Radio de la garganta", "en": "Throat radius"},
    "num_granos": {"es": "Número de granos", "en": "Number of grains"},
    "densidad_grano": {"es": "Densidad del propelente", "en": "Propellant density"},
    "radio_exterior_grano": {"es": "Radio exterior del grano", "en": "Grain outer radius"},
    "radio_interior_grano": {"es": "Radio interior inicial del grano", "en": "Grain initial inner radius"},
    "altura_grano": {"es": "Altura del grano", "en": "Grain height"},
    "separacion_granos": {"es": "Separación entre granos", "en": "Grain separation"},
    "diametro": {"es": "Diámetro", "en": "Diameter"},
    "masa": {"es": "Masa sin motor", "en": "Mass without motor"},
    "inercia_lateral": {"es": "Inercia lateral", "en": "Lateral inertia"},
    "inercia_axial": {"es": "Inercia axial", "en": "Axial inertia"},
    "posicion_motor": {"es": "Posición de la tobera", "en": "Nozzle position"},
    "boton_superior": {"es": "Posición del botón de raíl superior", "en": "Upper rail button position"},
    "boton_inferior": {"es": "Posición del botón de raíl inferior", "en": "Lower rail button position"},
    "cd_subsonico": {"es": "Coeficiente de arrastre subsónico (Cd)", "en": "Subsonic drag coefficient (Cd)"},
    "aumento_transonico": {"es": "Aumento del Cd cerca de Mach 1", "en": "Cd increase near Mach 1"},
    "ojiva_longitud": {"es": "Longitud de la ojiva", "en": "Nose cone length"},
    "ojiva_tipo": {"es": "Tipo de ojiva", "en": "Nose cone shape"},
    "ojiva_posicion": {"es": "Posición de la punta de la ojiva", "en": "Nose cone tip position"},
    "aletas_numero": {"es": "Número de aletas", "en": "Number of fins"},
    "aletas_cuerda_raiz": {"es": "Cuerda en la raíz", "en": "Root chord"},
    "aletas_cuerda_punta": {"es": "Cuerda en la punta", "en": "Tip chord"},
    "aletas_envergadura": {"es": "Envergadura de las aletas", "en": "Fin span"},
    "aletas_barrido": {"es": "Barrido de las aletas", "en": "Fin sweep length"},
    "aletas_posicion": {"es": "Posición de las aletas", "en": "Fin position"},
    "cola_radio_inferior": {"es": "Radio inferior de la cola", "en": "Tail bottom radius"},
    "cola_longitud": {"es": "Longitud de la cola (0 = sin cola)", "en": "Tail length (0 = no tail)"},
    "cola_posicion": {"es": "Posición de la cola", "en": "Tail position"},
    "drogue_cds": {"es": "Cd·S del drogue (0 = sin él)", "en": "Drogue Cd·S (0 = none)"},
    "principal_cds": {"es": "Cd·S del principal (0 = sin él)", "en": "Main Cd·S (0 = none)"},
    "principal_altura": {"es": "Apertura del principal sobre el suelo", "en": "Main deployment altitude"},
    "retardo": {"es": "Retardo de apertura", "en": "Deployment lag"},
    "longitud_rail": {"es": "Longitud del raíl", "en": "Rail length"},
    "inclinacion": {"es": "Inclinación (90 = vertical)", "en": "Inclination (90 = vertical)"},
    "rumbo": {"es": "Rumbo (0 = Norte)", "en": "Heading (0 = North)"},
}

# Nombres visibles de las opciones de los desplegables (los valores internos no cambian)
OPCIONES = {
    "constante": {"es": "constante", "en": "constant"},
    "progresiva": {"es": "progresiva", "en": "progressive"},
    "regresiva": {"es": "regresiva", "en": "regressive"},
    "pico inicial": {"es": "pico inicial", "en": "initial peak"},
    "von karman": {"es": "Von Kármán (Haack C=0)", "en": "Von Kármán (Haack C=0)"},
    "ogive": {"es": "ojiva", "en": "ogive"},
    "conical": {"es": "cónica", "en": "conical"},
    "elliptical": {"es": "elíptica", "en": "elliptical"},
    "tangent": {"es": "tangente", "en": "tangent"},
    "lvhaack": {"es": "LV-Haack", "en": "LV-Haack"},
    "powerseries": {"es": "serie de potencias", "en": "power series"},
}


def tr(clave, idioma, **datos):
    texto = TEXTOS[clave][idioma]
    return texto.format(**datos) if datos else texto


MANUAL = {
    "es": """\
# Manual de uso

Esta aplicación simula el vuelo completo de un cohete de modelismo (despegue, ascenso, apogeo, \
descenso con paracaídas y aterrizaje) con el motor de simulación RocketPy, en 6 grados de libertad.

## Uso rápido

- Ajusta los parámetros en las pestañas de la izquierda.
- Pulsa «Simular». En unos segundos aparecen el resumen y las gráficas a la derecha.
- «Valores por defecto» devuelve todas las pestañas a la configuración inicial.

Los campos numéricos tienen flechas para subir y bajar el valor; también se puede escribir \
directamente (se admite coma o punto decimal).

## Pestañas

Entorno: lugar de lanzamiento, temperatura en el suelo y viento. La dirección del viento es de \
dónde viene: 0 = Norte, 90 = Este. Un viento del oeste (270) desplaza el cohete hacia el Este.

Motor: motor de propelente sólido. La curva de empuje se genera a partir del impulso total, el \
tiempo de combustión y la forma (constante, progresiva, regresiva o pico inicial). El resto de \
campos describen la masa y los granos de propelente.

Cohete: dimensiones, masa, inercias, arrastre, ojiva, aletas y cola. Todas las posiciones se miden \
a lo largo del eje desde el centro de masas del cohete sin motor, positivas hacia la ojiva y \
negativas hacia la cola. La posición de la ojiva es la de su punta; la de las aletas, el borde \
de ataque de la raíz; la de la cola, su parte superior. Con longitud de cola 0 no hay cola.

Paracaídas: un drogue que se abre en el apogeo y un principal que se abre a la altura indicada. \
Un Cd·S de 0 significa que no se lleva ese paracaídas. Para una cúpula redonda, Cd·S ≈ 0,8 × área.

Lanzamiento: longitud del raíl, inclinación (90 = vertical) y rumbo (0 = Norte).

## Resultados

- Margen estático (en calibres): entre 1 y 3 el cohete es estable. Por debajo de 1 puede ser \
inestable; muy por encima tiende a girarse contra el viento.
- Velocidad al salir del raíl: conviene que supere unos 15–20 m/s (50–65 ft/s).
- Apogeo: altura máxima sobre el suelo.
- Velocidad máxima y número de Mach.
- Impacto: tiempo de vuelo, velocidad de aterrizaje y punto de caída (x hacia el Este, y hacia el \
Norte, desde la rampa). Si el cohete no aterriza en el tiempo simulado, se indica.

Las gráficas muestran altitud, velocidad y aceleración frente al tiempo, y la trayectoria vista \
desde arriba. La barra bajo las gráficas permite hacer zoom y guardarlas como imagen.

## Configuraciones guardadas

Cada pestaña tiene arriba una lista de configuraciones guardadas:

- «Guardar…» pide un nombre y guarda los valores de esa pestaña.
- «Cargar» aplica la configuración elegida solo a esa pestaña.
- «Eliminar» la borra.

Así puedes combinar, por ejemplo, un motor con distintos cohetes y entornos. Se guardan en \
biblioteca.json y se conservan entre sesiones.

## Importar y exportar

«Exportar JSON…» permite exportar la simulación actual (valores de las pestañas y resultados) o \
todas las configuraciones guardadas. «Importar JSON…» reconoce el tipo de archivo: una simulación \
rellena las pestañas y muestra sus resultados; unas configuraciones se pueden añadir a las tuyas \
o reemplazarlas.

## Idioma y unidades

En el menú «Idioma» puedes cambiar entre español e inglés, y en «Unidades» entre el sistema \
métrico y el imperial. Las unidades solo cambian lo que se muestra: los archivos y las \
configuraciones se guardan siempre en el sistema métrico, así que sirven con cualquier elección. \
Ambas preferencias se recuerdan al cerrar la aplicación.

## Consejos

- El arrastre depende solo del Cd: la forma de la ojiva y el tamaño de las aletas cambian la \
estabilidad, pero no el arrastre. Para comparar diseños, ajusta también el Cd.
- Si cambias el diámetro o la longitud del cohete, revisa las posiciones, la masa y las inercias.
- En la carpeta «ejemplos» hay un cohete de 38 mm con motor AeroTech G80T listo para importar.
""",
    "en": """\
# User manual

This application simulates the complete flight of a model rocket (lift-off, ascent, apogee, \
parachute descent and landing) with the RocketPy simulation engine, in 6 degrees of freedom.

## Quick start

- Adjust the parameters in the tabs on the left.
- Press “Simulate”. After a few seconds the summary and the plots appear on the right.
- “Default values” resets every tab to the initial configuration.

Numeric fields have arrows to increase and decrease the value; you can also type directly \
(comma or dot decimal separators are accepted).

## Tabs

Environment: launch site, ground temperature and wind. The wind direction is where the wind comes \
from: 0 = North, 90 = East. A west wind (270) drifts the rocket eastwards.

Motor: solid propellant motor. The thrust curve is generated from the total impulse, the burn \
time and the shape (constant, progressive, regressive or initial peak). The other fields describe \
the mass and the propellant grains.

Rocket: dimensions, mass, inertias, drag, nose cone, fins and tail. All positions are measured \
along the axis from the centre of mass of the rocket without motor, positive towards the nose and \
negative towards the tail. The nose cone position is its tip; the fin position is the root \
leading edge; the tail position is its top. A tail length of 0 means no tail.

Parachutes: a drogue that opens at apogee and a main that opens at the given altitude. A Cd·S of 0 \
means that parachute is not carried. For a round canopy, Cd·S ≈ 0.8 × area.

Launch: rail length, inclination (90 = vertical) and heading (0 = North).

## Results

- Static margin (in calibers): between 1 and 3 the rocket is stable. Below 1 it may be unstable; \
far above it tends to weathercock into the wind.
- Rail departure speed: it should exceed about 15–20 m/s (50–65 ft/s).
- Apogee: maximum height above ground.
- Maximum speed and Mach number.
- Landing: flight time, landing speed and landing point (x towards East, y towards North, from the \
launch pad). If the rocket does not land within the simulated time, it is reported.

The plots show altitude, speed and acceleration versus time, and the ground track seen from \
above. The toolbar below the plots lets you zoom and save them as an image.

## Saved configurations

Each tab has a list of saved configurations at the top:

- “Save…” asks for a name and saves the values of that tab.
- “Load” applies the chosen configuration to that tab only.
- “Delete” removes it.

This way you can combine, for example, one motor with different rockets and environments. They \
are stored in biblioteca.json and kept between sessions.

## Import and export

“Export JSON…” exports either the current simulation (tab values and results) or all saved \
configurations. “Import JSON…” recognises the file type: a simulation fills the tabs and shows its \
results; saved configurations can be added to yours or replace them.

## Language and units

Use the “Language” menu to switch between Spanish and English, and the “Units” menu to switch \
between metric and imperial units. Units only change what is displayed: files and saved \
configurations are always stored in metric units, so they work with either choice. Both \
preferences are remembered when the application is closed.

## Tips

- Drag depends only on Cd: the nose cone shape and fin size change stability, but not drag. To \
compare designs, adjust Cd as well.
- If you change the rocket's diameter or length, check the positions, mass and inertias.
- The “ejemplos” folder contains a 38 mm rocket with an AeroTech G80T motor, ready to import.
""",
}
