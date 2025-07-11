import pandas as pd
from utils import (graficar_grilla_bacteriana,)


class Simulador:
    def __init__(self, colonia):
        self.colonia = colonia
        self.historia = []  # Guarda el estado de cada paso

    def run(self, pasos, guardar_csv=True, guardar_imagenes=True, guardar_eventos_txt=True):
        # PASO 0: Solo visualización del estado inicial (sin eventos)
        estado_inicial = self.colonia.reporte_estado()
        estado_inicial["paso"] = 0
        estado_inicial["eventos"] = []  # No hay eventos en el paso inicial
        self.historia.append(estado_inicial)
        print(f"Paso 0 (Estado inicial): {estado_inicial}")

        if guardar_imagenes:
            nombre_img = f"grilla_paso_0.png"
            graficar_grilla_bacteriana(
                self.colonia.ambiente,
                nombre_imagen=nombre_img,
                titulo="Paso 0 - Estado inicial",
            )

        # PASOS 1 en adelante: Procesamiento de eventos
        for paso in range(1, pasos + 1):
            eventos = self.colonia.paso()
            estado = self.colonia.reporte_estado()
            estado["paso"] = paso
            estado["eventos"] = eventos
            self.historia.append(estado)
            print(f"Paso {paso}: {estado}")

            if guardar_imagenes:
                nombre_img = f"grilla_paso_{paso}.png"
                graficar_grilla_bacteriana(
                    self.colonia.ambiente,
                    nombre_imagen=nombre_img,
                    titulo=f"Paso {paso}",
                )

        if guardar_csv:
            self.exportar_historia_csv()
            
        if guardar_eventos_txt:
            self.exportar_eventos_txt()

    def exportar_historia_csv(self, nombre_archivo="historial_colonia.csv"):
        df = pd.DataFrame(self.historia)
        df.to_csv(nombre_archivo, index=False)
        print(f"Historial exportado a {nombre_archivo}")

    def exportar_eventos_txt(self, nombre_archivo="eventos_simulacion.txt"):
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            for entrada in self.historia:
                paso = entrada["paso"]
                eventos = entrada["eventos"]
                f.write(f"Paso {paso}:\n")
                if eventos:
                    for evento in eventos:
                        f.write(f"  - {evento}\n")
                else:
                    if paso == 0:
                        f.write("  - Estado inicial (sin eventos)\n")
                    else:
                        f.write("  - No ocurrieron eventos\n")
                f.write("\n")
        print(f"Eventos exportados a {nombre_archivo}")