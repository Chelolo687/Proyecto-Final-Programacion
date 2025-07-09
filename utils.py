import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
import os


def graficar_grilla_bacteriana(
    ambiente, nombre_imagen=None, titulo="Grilla bacteriana"
):
    # Mapear valores a estados: 0=vacio, 1=activa, 2=muerta, 3=resistente, 4=biofilm
    grilla = np.zeros((ambiente.tamaño_grilla, ambiente.tamaño_grilla))
    
    # Primero marcar las zonas de biofilm (prioridad más baja)
    for i in range(ambiente.tamaño_grilla):
        for j in range(ambiente.tamaño_grilla):
            if ambiente.es_zona_biofilm(i, j):
                grilla[i, j] = 4  # Biofilm
    
    # Luego marcar las bacterias (prioridad más alta)
    for i in range(ambiente.tamaño_grilla):
        for j in range(ambiente.tamaño_grilla):
            b = ambiente.grilla[i, j]
            if b is not None:
                if b.estado == "activa" and not b.resistente:
                    grilla[i, j] = 1  # Activa (verde)
                elif b.estado == "muerta":
                    grilla[i, j] = 2  # Muerta (rojo)
                elif b.estado == "activa" and b.resistente:
                    grilla[i, j] = 3  # Resistente (gris)

    # Definir colores personalizados: vacío, activa, muerta, resistente, biofilm
    colores = ["white", "limegreen", "red", "yellow", "darkgray"]
    cmap = ListedColormap(colores)

    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(grilla, cmap=cmap, vmin=0, vmax=4)

    # Leyenda personalizada
    legend_elements = [
        Patch(facecolor="limegreen", label="Bacteria activa"),
        Patch(facecolor="red", label="Bacteria muerta"),
        Patch(facecolor="yellow", label="Bacteria resistente"),
        Patch(facecolor="darkgray", label="Biofilm"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", bbox_to_anchor=(1.45, 1))

    # Configuración de la grilla
    ax.set_xticks(np.arange(0, ambiente.tamaño_grilla, 1))
    ax.set_yticks(np.arange(0, ambiente.tamaño_grilla, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color="gray", linestyle="-", linewidth=0.5)

    # Mostrar valores en cada celda (opcional)
    for i in range(ambiente.tamaño_grilla):
        for j in range(ambiente.tamaño_grilla):
            val = grilla[i, j]
            if val > 0:
                ax.text(j, i, int(val), va="center", ha="center", color="white")

    plt.title(titulo)
    plt.tight_layout()

    # Crear la carpeta si no existe
    if not os.path.exists("imagenes_generadas"):
        os.makedirs("imagenes_generadas")

    if nombre_imagen:
        # Corrección: quita la barra inicial para usar ruta relativa
        plt.savefig(f"imagenes_generadas/{nombre_imagen}")
        plt.close()
    else:
        plt.show()