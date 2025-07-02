import gi
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

       