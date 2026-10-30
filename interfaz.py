"""Interfaz gráfica para editar los parámetros y lanzar la simulación."""

import json
import math
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from presentacion import dibujar_graficas, resumen
from simulacion import (PARAMETROS, RESULTADOS, biblioteca_desde, cargar_biblioteca, es_biblioteca,
                        exportar_biblioteca, extraer_resultados, guardar_biblioteca, guardar_json,
                        leer_json, parametros_por_defecto, simular, simulacion_desde)
from textos import ETIQUETAS, IDIOMAS, MANUAL, OPCIONES, SECCIONES, tr
from unidades import SISTEMAS, a_interno, a_mostrar, formatear, paso_redondo, simbolo

PREFERENCIAS = Path(__file__).parent / "preferencias.json"
SPECS = {clave: spec for seccion in PARAMETROS.values() for clave, spec in seccion.items()}


def cargar_preferencias():
    """Idioma y sistema de unidades de la última sesión."""
    try:
        datos = json.loads(PREFERENCIAS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        datos = {}
    idioma = datos.get("idioma") if datos.get("idioma") in IDIOMAS else "es"
    sistema = datos.get("unidades") if datos.get("unidades") in SISTEMAS else "metrico"
    return idioma, sistema


def guardar_preferencias(idioma, sistema):
    try:
        PREFERENCIAS.write_text(json.dumps({"idioma": idioma, "unidades": sistema}), encoding="utf-8")
    except OSError:
        pass  # no es grave: la próxima vez se abrirá con los valores por defecto


def elegir(padre, titulo, mensaje, opciones, cancelar):
    """Diálogo modal con un botón por opción. Devuelve la opción pulsada o None si se cancela."""
    dialogo = tk.Toplevel(padre)
    dialogo.title(titulo)
    dialogo.resizable(False, False)
    dialogo.transient(padre)
    eleccion = tk.StringVar()
    ttk.Label(dialogo, text=mensaje, justify="left", padding=(16, 16, 16, 8)).pack()
    botones = ttk.Frame(dialogo, padding=(16, 0, 16, 16))
    botones.pack()
    for opcion in opciones + [cancelar]:
        ttk.Button(botones, text=opcion, command=lambda o=opcion: (eleccion.set(o), dialogo.destroy())
                   ).pack(side="left", padx=4)
    dialogo.grab_set()
    padre.wait_window(dialogo)
    return eleccion.get() if eleccion.get() in opciones else None


class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x820")
        self.idioma, self.sistema = cargar_preferencias()
        self.var_idioma = tk.StringVar(value=self.idioma)
        self.var_sistema = tk.StringVar(value=self.sistema)

        self.campos = {}  # clave -> (variable, spec, etiqueta visible)
        self.mostrado = {}  # clave -> (texto mostrado, valor interno exacto)
        self.opciones = {}  # clave -> {texto visible: valor interno}
        self.selectores = {}  # sección -> Combobox con las configuraciones guardadas
        self.ultima_simulacion = None  # (parámetros usados, resultados)
        self.ventana_manual = None
        self.contenido = None
        try:
            self.biblioteca = cargar_biblioteca()
        except (OSError, ValueError) as error:
            messagebox.showerror(self.t("t_biblioteca"), self.t("error_leer_biblioteca", error=error))
            self.biblioteca = {seccion: {} for seccion in PARAMETROS}

        self._construir()
        self.rellenar(parametros_por_defecto())

    def t(self, clave, **datos):
        return tr(clave, self.idioma, **datos)

    def nombre_seccion(self, seccion):
        return SECCIONES[seccion][self.idioma]

    # --- Construcción de la ventana ---

    def _construir(self):
        self.title(self.t("titulo_ventana"))
        self.config(menu=self._crear_menu())
        self.campos, self.opciones, self.selectores, self.mostrado = {}, {}, {}, {}

        self.contenido = ttk.Frame(self)
        self.contenido.pack(fill="both", expand=True)
        izquierda = ttk.Frame(self.contenido, padding=8)
        izquierda.pack(side="left", fill="y")
        derecha = ttk.Frame(self.contenido, padding=8)
        derecha.pack(side="left", fill="both", expand=True)

        pestanas = ttk.Notebook(izquierda, width=500)
        pestanas.pack(fill="both", expand=True)
        for seccion, parametros in PARAMETROS.items():
            pestanas.add(self._crear_pestana(pestanas, seccion, parametros), text=self.nombre_seccion(seccion))

        botones = ttk.Frame(izquierda)
        botones.pack(fill="x", pady=(8, 0))
        self.boton_simular = ttk.Button(botones, text=self.t("simular"), command=self.simular)
        self.boton_simular.pack(side="left", expand=True, fill="x")
        ttk.Button(botones, text=self.t("por_defecto"), command=self.restablecer).pack(
            side="left", expand=True, fill="x", padx=(8, 0))

        archivos = ttk.Frame(izquierda)
        archivos.pack(fill="x", pady=(8, 0))
        ttk.Button(archivos, text=self.t("importar"), command=self.importar).pack(
            side="left", expand=True, fill="x")
        ttk.Button(archivos, text=self.t("exportar"), command=self.exportar).pack(
            side="left", expand=True, fill="x", padx=(8, 0))

        self.texto_resumen = tk.StringVar(value=self.t("inicio"))
        ttk.Label(derecha, textvariable=self.texto_resumen, justify="left",
                  font=("Consolas", 10)).pack(anchor="w", pady=(0, 8))

        self.figura = Figure(figsize=(9, 6.5))
        self.lienzo = FigureCanvasTkAgg(self.figura, master=derecha)
        NavigationToolbar2Tk(self.lienzo, derecha).update()
        self.lienzo.get_tk_widget().pack(fill="both", expand=True)

    def _crear_menu(self):
        barra = tk.Menu(self)
        idioma = tk.Menu(barra, tearoff=False)
        for codigo, nombre in IDIOMAS.items():
            idioma.add_radiobutton(label=nombre, value=codigo, variable=self.var_idioma,
                                   command=self._cambiar_preferencias)
        barra.add_cascade(label=self.t("menu_idioma"), menu=idioma)
        unidades = tk.Menu(barra, tearoff=False)
        for sistema in SISTEMAS:
            unidades.add_radiobutton(label=self.t(sistema), value=sistema, variable=self.var_sistema,
                                     command=self._cambiar_preferencias)
        barra.add_cascade(label=self.t("menu_unidades"), menu=unidades)
        ayuda = tk.Menu(barra, tearoff=False)
        ayuda.add_command(label=self.t("menu_manual"), command=self.mostrar_manual, accelerator="F1")
        barra.add_cascade(label=self.t("menu_ayuda"), menu=ayuda)
        self.bind("<F1>", lambda evento: self.mostrar_manual())
        return barra

    def _crear_pestana(self, padre, seccion, parametros):
        marco = ttk.Frame(padre, padding=8)

        # Barra de configuraciones guardadas de esta sección
        barra = ttk.LabelFrame(marco, text=self.t("guardadas"), padding=6)
        barra.pack(fill="x")
        selector = ttk.Combobox(barra, state="readonly", width=22)
        selector.pack(side="left", fill="x", expand=True)
        self.selectores[seccion] = selector
        self._actualizar_selector(seccion)
        ttk.Button(barra, text=self.t("cargar"),
                   command=lambda: self.cargar_configuracion(seccion)).pack(side="left", padx=(6, 0))
        ttk.Button(barra, text=self.t("guardar"),
                   command=lambda: self.guardar_configuracion(seccion)).pack(side="left", padx=(6, 0))
        ttk.Button(barra, text=self.t("eliminar"),
                   command=lambda: self.eliminar_configuracion(seccion)).pack(side="left", padx=(6, 0))

        formulario = ttk.Frame(marco)
        formulario.pack(fill="both", expand=True, pady=(8, 0))
        formulario.columnconfigure(1, weight=1)
        for fila, (clave, spec) in enumerate(parametros.items()):
            magnitud = spec[0]
            etiqueta = ETIQUETAS[clave][self.idioma]
            unidad = simbolo(magnitud, self.sistema) if magnitud != "opcion" else ""
            if unidad:
                etiqueta = f"{etiqueta} [{unidad}]"
            ttk.Label(formulario, text=etiqueta).grid(row=fila, column=0, sticky="nw", pady=3, padx=(0, 8))
            variable = tk.StringVar()
            if magnitud == "opcion":
                self.opciones[clave] = {OPCIONES[o][self.idioma]: o for o in spec[2]}
                widget = ttk.Combobox(formulario, textvariable=variable, values=list(self.opciones[clave]),
                                      state="readonly", width=16)
            else:
                paso, minimo, maximo = spec[2:]
                paso = paso_redondo(paso, magnitud, self.sistema)
                decimales = max(0, -math.floor(math.log10(paso)))
                widget = ttk.Spinbox(formulario, textvariable=variable,
                                     from_=a_mostrar(minimo, magnitud, self.sistema),
                                     to=a_mostrar(maximo, magnitud, self.sistema),
                                     increment=paso, format=f"%.{decimales}f", width=16)
            self.campos[clave] = (variable, spec, etiqueta)
            widget.grid(row=fila, column=1, sticky="ew", pady=3)
        return marco

    # --- Idioma, unidades y manual ---

    def _cambiar_preferencias(self):
        try:
            p = self.leer_parametros()
        except ValueError as error:
            messagebox.showerror(self.t("t_parametros"), str(error))
            self.var_idioma.set(self.idioma)
            self.var_sistema.set(self.sistema)
            return
        selecciones = {seccion: selector.get() for seccion, selector in self.selectores.items()}
        texto_resumen = self.texto_resumen.get()
        manual_abierto = self.ventana_manual is not None and self.ventana_manual.winfo_exists()

        self.idioma, self.sistema = self.var_idioma.get(), self.var_sistema.get()
        guardar_preferencias(self.idioma, self.sistema)
        self.contenido.destroy()
        self._construir()
        self.rellenar(p)
        for seccion, nombre in selecciones.items():
            self.selectores[seccion].set(nombre)
        if self.ultima_simulacion and self.ultima_simulacion[0] == p:
            self._mostrar(self.ultima_simulacion[1])
        elif texto_resumen not in (tr("inicio", "es"), tr("inicio", "en")):
            self.texto_resumen.set(self.t("importados_sin_resultados"))
        if manual_abierto:
            self.mostrar_manual()

    def mostrar_manual(self):
        if self.ventana_manual is not None and self.ventana_manual.winfo_exists():
            self.ventana_manual.destroy()
        ventana = tk.Toplevel(self)
        ventana.title(self.t("menu_manual"))
        ventana.geometry("780x700")
        self.ventana_manual = ventana

        texto = tk.Text(ventana, wrap="word", padx=20, pady=14, relief="flat", font=("Segoe UI", 10))
        barra = ttk.Scrollbar(ventana, command=texto.yview)
        texto.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        texto.pack(fill="both", expand=True)
        texto.tag_configure("h1", font=("Segoe UI", 16, "bold"), spacing3=10)
        texto.tag_configure("h2", font=("Segoe UI", 12, "bold"), spacing1=14, spacing3=6)
        texto.tag_configure("parrafo", spacing3=8)
        texto.tag_configure("vineta", lmargin1=14, lmargin2=30, spacing3=4)
        texto.tag_configure("negrita", font=("Segoe UI", 10, "bold"))

        # Formato mínimo: "# " título, "## " sección, "- " viñeta; "Pestaña: …" con la pestaña en negrita
        pestanas = {nombres[self.idioma] for nombres in SECCIONES.values()}
        for linea in MANUAL[self.idioma].splitlines():
            if linea.startswith("# "):
                texto.insert("end", linea[2:] + "\n", "h1")
            elif linea.startswith("## "):
                texto.insert("end", linea[3:] + "\n", "h2")
            elif linea.startswith("- "):
                texto.insert("end", "•  " + linea[2:] + "\n", "vineta")
            elif linea.split(":")[0] in pestanas:
                nombre, resto = linea.split(":", 1)
                texto.insert("end", nombre + ":", ("parrafo", "negrita"))
                texto.insert("end", resto + "\n", "parrafo")
            elif linea.strip():
                texto.insert("end", linea + "\n", "parrafo")
        texto.configure(state="disabled")

    # --- Lectura y escritura de los campos ---

    def leer_parametros(self, claves=None):
        """Valores internos (SI) de los campos. Si un campo no se ha tocado, devuelve el valor exacto."""
        p = {}
        for clave in claves or self.campos:
            variable, spec, etiqueta = self.campos[clave]
            texto = variable.get().strip()
            mostrado, interno = self.mostrado.get(clave, (None, None))
            if texto == mostrado:
                p[clave] = interno
                continue
            magnitud = spec[0]
            try:
                if magnitud == "opcion":
                    p[clave] = self.opciones[clave][texto]
                else:
                    valor = a_interno(float(texto.replace(",", ".")), magnitud, self.sistema)
                    p[clave] = int(round(valor)) if magnitud == "entero" else valor
            except (ValueError, KeyError):
                raise ValueError(self.t("valor_no_valido", etiqueta=etiqueta, texto=texto)) from None
        return p

    def rellenar(self, p):
        for clave, valor in p.items():
            if clave not in self.campos:
                continue
            variable, spec, _ = self.campos[clave]
            magnitud = spec[0]
            if magnitud == "opcion":
                texto = OPCIONES.get(valor, {}).get(self.idioma, valor)
            elif magnitud == "entero":
                texto = str(int(valor))
            else:
                texto = formatear(a_mostrar(valor, magnitud, self.sistema))
            variable.set(texto)
            self.mostrado[clave] = (texto, valor)

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
            messagebox.showerror(self.t("t_biblioteca"), self.t("error_guardar_biblioteca", error=error))

    def guardar_configuracion(self, seccion):
        try:
            valores = self.leer_parametros(PARAMETROS[seccion])
        except ValueError as error:
            messagebox.showerror(self.t("t_parametros"), str(error))
            return
        nombre = simpledialog.askstring(self.t("t_guardar", seccion=self.nombre_seccion(seccion)),
                                        self.t("nombre_config"),
                                        initialvalue=self.selectores[seccion].get(), parent=self)
        nombre = (nombre or "").strip()
        if not nombre:
            return
        if nombre in self.biblioteca[seccion] and not messagebox.askyesno(
                self.t("t_guardar", seccion=self.nombre_seccion(seccion)),
                self.t("sobrescribir", nombre=nombre, seccion=self.nombre_seccion(seccion))):
            return
        self.biblioteca[seccion][nombre] = valores
        self._persistir_biblioteca()
        self._actualizar_selector(seccion, nombre)

    def cargar_configuracion(self, seccion):
        nombre = self.selectores[seccion].get()
        if not nombre:
            messagebox.showinfo(self.t("t_cargar"), self.t("elige_config", seccion=self.nombre_seccion(seccion)))
            return
        # Los parámetros que no estén guardados (p. ej. añadidos más tarde) toman su valor por defecto
        valores = {clave: spec[1] for clave, spec in PARAMETROS[seccion].items()}
        valores.update({k: v for k, v in self.biblioteca[seccion][nombre].items() if k in valores})
        self.rellenar(valores)

    def eliminar_configuracion(self, seccion):
        nombre = self.selectores[seccion].get()
        if not nombre or not messagebox.askyesno(
                self.t("t_eliminar"), self.t("confirmar_eliminar", nombre=nombre,
                                             seccion=self.nombre_seccion(seccion))):
            return
        del self.biblioteca[seccion][nombre]
        self._persistir_biblioteca()
        self._actualizar_selector(seccion)

    # --- Importar / exportar ---

    def importar(self):
        ruta = filedialog.askopenfilename(title=self.t("t_importar_sim"), initialdir=RESULTADOS,
                                          filetypes=[("JSON", "*.json"), (self.t("todos_archivos"), "*.*")])
        if not ruta:
            return
        try:
            datos = leer_json(ruta)
        except (OSError, ValueError) as error:
            messagebox.showerror(self.t("t_importar"), self.t("error_leer_archivo", error=error))
            return
        if es_biblioteca(datos):
            self._importar_biblioteca(biblioteca_desde(datos.get("biblioteca", {})))
            return

        p, resultados = simulacion_desde(datos)
        self.rellenar(p)
        if resultados:
            self.ultima_simulacion = (self.leer_parametros(), resultados)
            self._mostrar(resultados)
        else:
            self.ultima_simulacion = None
            self.figura.clear()
            self.lienzo.draw()
            self.texto_resumen.set(self.t("importados_sin_resultados"))

    def _importar_biblioteca(self, importada):
        total = sum(len(configs) for configs in importada.values())
        repetidas = sum(len(configs.keys() & self.biblioteca[s].keys()) for s, configs in importada.items())
        aviso = self.t("aviso_repetidas", n=repetidas) if repetidas else ""
        modo = elegir(self, self.t("t_importar_configs"), self.t("importar_configs", total=total, aviso=aviso),
                      [self.t("anadir"), self.t("reemplazar")], self.t("cancelar"))
        if modo is None:
            return
        for seccion, configs in importada.items():
            if modo == self.t("reemplazar"):
                self.biblioteca[seccion].clear()
            self.biblioteca[seccion].update(configs)
            self._actualizar_selector(seccion)
        self._persistir_biblioteca()
        messagebox.showinfo(self.t("t_importar"), self.t("importadas", total=total))

    def exportar(self):
        que = elegir(self, self.t("t_exportar"), self.t("exportar_que"),
                     [self.t("sim_actual"), self.t("todas_guardadas")], self.t("cancelar"))
        if que == self.t("sim_actual"):
            self._exportar_simulacion()
        elif que == self.t("todas_guardadas"):
            self._exportar_biblioteca()

    def _exportar_biblioteca(self):
        if not any(self.biblioteca.values()):
            messagebox.showinfo(self.t("t_exportar"), self.t("sin_guardadas"))
            return
        RESULTADOS.mkdir(exist_ok=True)
        ruta = filedialog.asksaveasfilename(title=self.t("t_exportar_configs"), initialdir=RESULTADOS,
                                            initialfile="configuraciones.json", defaultextension=".json",
                                            filetypes=[("JSON", "*.json")])
        if ruta:
            exportar_biblioteca(ruta, self.biblioteca)

    def _exportar_simulacion(self):
        try:
            p = self.leer_parametros()
        except ValueError as error:
            messagebox.showerror(self.t("t_parametros"), str(error))
            return
        # Solo se incluyen los resultados si corresponden a los parámetros actuales
        resultados = None
        if self.ultima_simulacion and self.ultima_simulacion[0] == p:
            resultados = self.ultima_simulacion[1]
        elif not messagebox.askyesno(self.t("t_exportar"), self.t("sin_simular")):
            return

        RESULTADOS.mkdir(exist_ok=True)
        ruta = filedialog.asksaveasfilename(title=self.t("t_exportar_sim"), initialdir=RESULTADOS,
                                            defaultextension=".json", filetypes=[("JSON", "*.json")])
        if ruta:
            guardar_json(ruta, p, resultados)

    # --- Simulación ---

    def simular(self):
        try:
            p = self.leer_parametros()
        except ValueError as error:
            messagebox.showerror(self.t("t_parametros"), str(error))
            return

        self.boton_simular.state(["disabled"])
        self.texto_resumen.set(self.t("simulando"))

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
        dibujar_graficas(resultados, self.figura, self.idioma, self.sistema)
        self.lienzo.draw()
        self.texto_resumen.set(resumen(resultados, self.idioma, self.sistema))

    def report_callback_exception(self, tipo, valor, traza):
        # Sin consola (pythonw) los errores no se verían: se muestran en una ventana
        messagebox.showerror(self.t("t_error_inesperado"), f"{tipo.__name__}: {valor}")

    def _error(self, error):
        self.texto_resumen.set(self.t("sim_fallo"))
        self.boton_simular.state(["!disabled"])
        messagebox.showerror(self.t("t_error_sim"), f"{type(error).__name__}: {error}")


if __name__ == "__main__":
    Interfaz().mainloop()
