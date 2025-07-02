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
        with open(archivo, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                datos.append(row)
        return datos
    def actualizar_imagen(self):
        img_path = f"imagenes_generadas/grilla_paso_{self.paso_actual}.png"
        if not os.path.exists(img_path):
            img_path = "imagenes_generadas/grilla_paso_0.png"
        self.picture.set_file(Gio.File.new_for_path(img_path))
