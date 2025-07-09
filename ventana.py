import gi
import os 
import csv 
from gi.repository import Gtk, GLib, Gio

gi.require_version("Gtk", "4.0")

QUIT = False

def quit_(window):
    global QUIT
    QUIT = True

class Ventana(Gtk.Window):
    def __init__(self):
        super().__init__(title="Simulador Placa Petri")
        self.connect("close-request", quit_)

        # ---- Lógica para la simulación ----
        self.paso_actual = 0
        self.datos_csv = self.cargar_datos_csv("historial_colonia.csv")
        self.pasos_max = len(self.datos_csv) - 1

        # Layout horizontal
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_child(main_box)

        self.picture = Gtk.Picture()
        self.picture.set_content_fit(Gtk.ContentFit.CONTAIN)  # Ajusta la imagen
        self.picture.set_can_shrink(True)
        main_box.append(self.picture)
        self.actualizar_imagen()

        # Columna derecha: Datos y botones
        side_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.append(side_box)

    def cargar_datos_csv(self, archivo):
        datos = []
        if not os.path.exists(archivo):
            print(f"No se encontró el archivo {archivo}")
            return datos
        with open(archivo, newline="", encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                datos.append(row)
        return datos
    
    def cargar_eventos_txt(self, archivo):
        eventos_por_paso = {}
        if not os.path.exists(archivo):
            print(f"No se encontró el archivo {archivo}")
            return eventos_por_paso
        
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        paso_actual = None
        eventos_paso = []
        
        for linea in lineas:
            linea = linea.strip()
            if linea.startswith("Paso ") and linea.endswith(":"):
                if paso_actual is not None:
                    eventos_por_paso[paso_actual] = eventos_paso
                paso_actual = int(linea.split()[1][:-1])
                eventos_paso = []
            elif linea.startswith("  - "):
                eventos_paso.append(linea[4:])
        
        # Agregar último paso
        if paso_actual is not None:
            eventos_por_paso[paso_actual] = eventos_paso
            
        return eventos_por_paso
    
    def actualizar_imagen(self):
        img_path = f"imagenes_generadas/grilla_paso_{self.paso_actual}.png"
        if not os.path.exists(img_path):
            img_path = "imagenes_generadas/grilla_paso_0.png"
        self.picture.set_file(Gio.File.new_for_path(img_path))

    def actualizar_info_csv(self):
        if self.paso_actual < 0 or self.paso_actual > self.pasos_max:
            self.label_info.set_label("No hay datos para este paso")
            return
        row = self.datos_csv[self.paso_actual]
        texto = (
            f"<b>Paso:</b> {row['paso']}\n"
            f"<b>Bacterias activas:</b> {row['bacterias_activas']}\n"
            f"<b>Bacterias muertas:</b> {row['bacterias_muertas']}\n"
            f"<b>Bacterias resistentes:</b> {row['bacterias_resistentes']}"
        )
        self.label_info.set_label(texto)

    def ir_anterior(self, button):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self.actualizar_imagen()
            self.actualizar_info_csv()

    def ir_siguiente(self, button):
        if self.paso_actual < self.pasos_max:
            self.paso_actual += 1
            self.actualizar_imagen()
            self.actualizar_info_csv()

    def lanzar_ventana():
        Ventana()
        loop = GLib.MainContext().default()
        while not QUIT:
            loop.iteration(True)