"""Interfaz gráfica sencilla para editar los parámetros y lanzar la simulación."""

import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from simulacion import (PARAMETROS, RESULTADOS, biblioteca_desde, cargar_biblioteca,
                        dibujar_graficas, es_biblioteca, exportar_biblioteca, extraer_resultados,
                        guardar_biblioteca, guardar_json, leer_json, parametros_por_defecto,
                        resumen, simular, simulacion_desde)


def elegir(padre, titulo, mensaje, opciones):
    """Diálogo modal con un botón por opción. Devuelve la opción pulsada o None si se cierra."""
    dialogo = tk.Toplevel(padre)
    dialogo.title(titulo)
    dialogo.resizable(False, False)
    dialogo.transient(padre)
    eleccion = tk.StringVar()
    ttk.Label(dialogo, text=mensaje, justify="left", padding=(16, 16, 16, 8)).pack()
    botones = ttk.Frame(dialogo, padding=(16, 0, 16, 16))
    botones.pack()
    for opcion in opciones + ["Cancelar"]:
        ttk.Button(botones, text=opcion, command=lambda o=opcion: (eleccion.set(o), dialogo.destroy())
                   ).pack(side="left", padx=4)
    dialogo.grab_set()
    padre.wait_window(dialogo)
    return eleccion.get() if eleccion.get() in opciones else None


class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de cohete — RocketPy")
        self.geometry("1400x820")

        self.campos = {}  # clave -> (widget o variable, tipo del valor por defecto, etiqueta)
        self.selectores = {}  # sección -> Combobox con las configuraciones guardadas
        self.ultima_simulacion = None  # (parámetros usados, resultados)
        try:
            self.biblioteca = cargar_biblioteca()
        except (OSError, ValueError) as error:
            messagebox.showerror("Biblioteca", f"No se pudo leer biblioteca.json:\n{error}")
            self.biblioteca = {seccion: {} for seccion in PARAMETROS}

        izquierda = ttk.Frame(self, padding=8)
        izquierda.pack(side="left", fill="y")
        derecha = ttk.Frame(self, padding=8)
        derecha.pack(side="left", fill="both", expand=True)

        pestanas = ttk.Notebook(izquierda, width=470)
        pestanas.pack(fill="both", expand=True)
        for seccion, parametros in PARAMETROS.items():
            pestanas.add(self._crear_pestana(pestanas, seccion, parametros), text=seccion)

        botones = ttk.Frame(izquierda)
        botones.pack(fill="x", pady=(8, 0))
        self.boton_simular = ttk.Button(botones, text="Simular", command=self.simular)
        self.boton_simular.pack(side="left", expand=True, fill="x")
        ttk.Button(botones, text="Valores por defecto", command=self.restablecer).pack(
            side="left", expand=True, fill="x", padx=(8, 0))

        archivos = ttk.Frame(izquierda)
        archivos.pack(fill="x", pady=(8, 0))
        ttk.Button(archivos, text="Importar JSON…", command=self.importar).pack(
            side="left", expand=True, fill="x")
        ttk.Button(archivos, text="Exportar JSON…", command=self.exportar).pack(
            side="left", expand=True, fill="x", padx=(8, 0))

        self.texto_resumen = tk.StringVar(value="Pulsa «Simular» para lanzar el vuelo.")
        ttk.Label(derecha, textvariable=self.texto_resumen, justify="left",
                  font=("Consolas", 10)).pack(anchor="w", pady=(0, 8))

        self.figura = Figure(figsize=(9, 6.5))
        self.lienzo = FigureCanvasTkAgg(self.figura, master=derecha)
        NavigationToolbar2Tk(self.lienzo, derecha).update()
        self.lienzo.get_tk_widget().pack(fill="both", expand=True)

    # --- Construcción de las pestañas ---

    def _crear_pestana(self, padre, seccion, parametros):
        marco = ttk.Frame(padre, padding=8)

        # Barra de configuraciones guardadas de esta sección
        barra = ttk.LabelFrame(marco, text=f"{seccion} guardados", padding=6)
        barra.pack(fill="x")
        selector = ttk.Combobox(barra, state="readonly", width=22)
        selector.pack(side="left", fill="x", expand=True)
        self.selectores[seccion] = selector
        self._actualizar_selector(seccion)
        ttk.Button(barra, text="Cargar", width=7,
                   command=lambda: self.cargar_configuracion(seccion)).pack(side="left", padx=(6, 0))
        ttk.Button(barra, text="Guardar…", width=9,
                   command=lambda: self.guardar_configuracion(seccion)).pack(side="left", padx=(6, 0))
        ttk.Button(barra, text="Eliminar", width=8,
                   command=lambda: self.eliminar_configuracion(seccion)).pack(side="left", padx=(6, 0))

        formulario = ttk.Frame(marco)
        formulario.pack(fill="both", expand=True, pady=(8, 0))
        formulario.columnconfigure(1, weight=1)
        for fila, (clave, spec) in enumerate(parametros.items()):
            etiqueta, defecto = spec[:2]
            ttk.Label(formulario, text=etiqueta).grid(row=fila, column=0, sticky="nw", pady=3, padx=(0, 8))
            variable = tk.StringVar(value=str(defecto))
            if isinstance(defecto, str):
                widget = ttk.Combobox(formulario, textvariable=variable, values=spec[2],
                                      state="readonly", width=16)
            else:
                paso, minimo, maximo = spec[2:]
                decimales = len(f"{paso:g}".partition(".")[2])
                widget = ttk.Spinbox(formulario, textvariable=variable, from_=minimo, to=maximo,
                                     increment=paso, format=f"%.{decimales}f", width=16)
            self.campos[clave] = (variable, type(defecto), etiqueta)
            widget.grid(row=fila, column=1, sticky="ew", pady=3)
        return marco

    # --- Lectura y escritura de los campos ---

    def leer_parametros(self, claves=None):
        p = {}
        for clave in claves or self.campos:
            campo, tipo, etiqueta = self.campos[clave]
            texto = campo.get().strip()
            try:
                p[clave] = int(float(texto)) if tipo is int else tipo(texto)
            except ValueError:
                raise ValueError(f"Valor no válido en «{etiqueta}»: {texto!r}") from None
        return p

    def rellenar(self, p):
        for clave, valor in p.items():
            self.campos[clave][0].set(str(valor))

    def restablecer(self):
        self.rellenar(parametros_por_defecto())

    # --- Configuraciones guardadas por sección ---

    def _actualizar_selector(self, seccion, seleccion=""):
        selector = self.selectores[seccion]
        selector["values"] = sorted(self.biblioteca[seccion], key=str.lower)
        selector.set(seleccion)

    def _persistir_biblioteca(self):
        try:
            guardar_biblioteca(self.biblioteca)
        except OSError as error:
            messagebox.showerror("Biblioteca", f"No se pudo guardar biblioteca.json:\n{error}")

    def guardar_configuracion(self, seccion):
        try:
            valores = self.leer_parametros(PARAMETROS[seccion])
        except ValueError as error:
            messagebox.showerror("Parámetros", str(error))
            return
        nombre = simpledialog.askstring(f"Guardar {seccion.lower()}", "Nombre de la configuración:",
                                        initialvalue=self.selectores[seccion].get(), parent=self)
        nombre = (nombre or "").strip()
        if not nombre:
            return
        if nombre in self.biblioteca[seccion] and not messagebox.askyesno(
                "Guardar", f"Ya existe «{nombre}» en {seccion}. ¿Sobrescribir?"):
            return
        self.biblioteca[seccion][nombre] = valores
        self._persistir_biblioteca()
        self._actualizar_selector(seccion, nombre)

    def cargar_configuracion(self, seccion):
        nombre = self.selectores[seccion].get()
        if not nombre:
            messagebox.showinfo("Cargar", f"Elige una configuración de {seccion} en la lista.")
            return
        # Los parámetros que no estén guardados (p. ej. añadidos más tarde) toman su valor por defecto
        valores = {clave: spec[1] for clave, spec in PARAMETROS[seccion].items()}
        valores.update({k: v for k, v in self.biblioteca[seccion][nombre].items() if k in valores})
        self.rellenar(valores)

    def eliminar_configuracion(self, seccion):
        nombre = self.selectores[seccion].get()
        if not nombre or not messagebox.askyesno("Eliminar", f"¿Eliminar «{nombre}» de {seccion}?"):
            return
        del self.biblioteca[seccion][nombre]
        self._persistir_biblioteca()
        self._actualizar_selector(seccion)

    # --- Importar / exportar simulaciones completas ---

    def importar(self):
        ruta = filedialog.askopenfilename(title="Importar simulación", initialdir=RESULTADOS,
                                          filetypes=[("JSON", "*.json"), ("Todos", "*.*")])
        if not ruta:
            return
        try:
            datos = leer_json(ruta)
        except (OSError, ValueError) as error:
            messagebox.showerror("Importar", f"No se pudo leer el archivo:\n{error}")
            return
        if es_biblioteca(datos):
            self._importar_biblioteca(biblioteca_desde(datos.get("biblioteca", {})))
            return

        p, resultados = simulacion_desde(datos)
        self.rellenar(p)
        if resultados:
            # Se guarda con los parámetros tal y como los lee el formulario para poder compararlos
            self.ultima_simulacion = (self.leer_parametros(), resultados)
            self._mostrar(resultados)
        else:
            self.ultima_simulacion = None
            self.figura.clear()
            self.lienzo.draw()
            self.texto_resumen.set("Parámetros importados (sin resultados). Pulsa «Simular».")

    def _importar_biblioteca(self, importada):
        total = sum(len(configs) for configs in importada.values())
        repetidas = sum(len(configs.keys() & self.biblioteca[s].keys()) for s, configs in importada.items())
        aviso = f"\n{repetidas} tienen el mismo nombre que alguna tuya y la sustituirán." if repetidas else ""
        modo = elegir(self, "Importar configuraciones",
                      f"El archivo contiene {total} configuraciones guardadas.\n\n"
                      f"«Añadir»: se suman a las que ya tienes.{aviso}\n"
                      "«Reemplazar»: se borran las tuyas y quedan solo las del archivo.",
                      ["Añadir", "Reemplazar"])
        if modo is None:
            return
        for seccion, configs in importada.items():
            if modo == "Reemplazar":
                self.biblioteca[seccion].clear()
            self.biblioteca[seccion].update(configs)
            self._actualizar_selector(seccion)
        self._persistir_biblioteca()
        messagebox.showinfo("Importar", f"Importadas {total} configuraciones.")

    def exportar(self):
        que = elegir(self, "Exportar", "¿Qué quieres exportar?\n\n"
                     "«Simulación actual»: los valores de las pestañas y sus resultados.\n"
                     "«Todas las guardadas»: todas tus configuraciones guardadas de cada sección.",
                     ["Simulación actual", "Todas las guardadas"])
        if que == "Simulación actual":
            self._exportar_simulacion()
        elif que == "Todas las guardadas":
            self._exportar_biblioteca()

    def _exportar_biblioteca(self):
        if not any(self.biblioteca.values()):
            messagebox.showinfo("Exportar", "No tienes ninguna configuración guardada todavía.")
            return
        RESULTADOS.mkdir(exist_ok=True)
        ruta = filedialog.asksaveasfilename(title="Exportar configuraciones guardadas",
                                            initialdir=RESULTADOS, initialfile="configuraciones.json",
                                            defaultextension=".json", filetypes=[("JSON", "*.json")])
        if ruta:
            exportar_biblioteca(ruta, self.biblioteca)

    def _exportar_simulacion(self):
        try:
            p = self.leer_parametros()
        except ValueError as error:
            messagebox.showerror("Parámetros", str(error))
            return
        # Solo se incluyen los resultados si corresponden a los parámetros actuales
        resultados = None
        if self.ultima_simulacion and self.ultima_simulacion[0] == p:
            resultados = self.ultima_simulacion[1]
        elif not messagebox.askyesno(
                "Exportar", "Los parámetros actuales no se han simulado todavía.\n"
                            "¿Exportar solo los parámetros, sin resultados?"):
            return

        RESULTADOS.mkdir(exist_ok=True)
        ruta = filedialog.asksaveasfilename(title="Exportar simulación", initialdir=RESULTADOS,
                                            defaultextension=".json", filetypes=[("JSON", "*.json")])
        if ruta:
            guardar_json(ruta, p, resultados)

    # --- Simulación ---

    def simular(self):
        try:
            p = self.leer_parametros()
        except ValueError as error:
            messagebox.showerror("Parámetros", str(error))
            return

        self.boton_simular.state(["disabled"])
        self.texto_resumen.set("Simulando…")

        # La simulación tarda unos segundos: se hace en otro hilo para no congelar la ventana
        def tarea():
            try:
                resultados = extraer_resultados(*simular(p))
                self.after(0, self._terminar, p, resultados)
            except Exception as error:
                self.after(0, self._error, error)

        threading.Thread(target=tarea, daemon=True).start()

    def _terminar(self, p, resultados):
        self.ultima_simulacion = (p, resultados)
        self._mostrar(resultados)
        self.boton_simular.state(["!disabled"])

    def _mostrar(self, resultados):
        dibujar_graficas(resultados, self.figura)
        self.lienzo.draw()
        self.texto_resumen.set(resumen(resultados))

    def report_callback_exception(self, tipo, valor, traza):
        # Sin consola (pythonw) los errores no se verían: se muestran en una ventana
        messagebox.showerror("Error inesperado", f"{tipo.__name__}: {valor}")

    def _error(self, error):
        self.texto_resumen.set("La simulación ha fallado.")
        self.boton_simular.state(["!disabled"])
        messagebox.showerror("Error en la simulación", f"{type(error).__name__}: {error}")


if __name__ == "__main__":
    Interfaz().mainloop()
