from bacteria import Bacteria
from ambiente import Ambiente
from colonia import Colonia
from simulador import Simulador
from ventana import lanzar_ventana
import random


def crear_bacterias_iniciales(num_bacterias, energia_inicial, tamaño_grilla):
    bacterias = []
    posiciones_ocupadas = set()
    for i in range(num_bacterias):
        while True:
            x = random.randint(0, tamaño_grilla - 1)
            y = random.randint(0, tamaño_grilla - 1)
            if (x, y) not in posiciones_ocupadas:
                posiciones_ocupadas.add((x, y))
                break
        bacterias.append(
            Bacteria(
                id=i,
                raza="A",
                energia=energia_inicial,
                resistente=False,
                estado="activa",
            )
        )
    return bacterias, posiciones_ocupadas


def main():
    tamaño_grilla = 10
    nutrientes_por_celda = 100
    num_bacterias = 20
    energia_inicial = 40
    pasos_simulacion = 30

    ambiente = Ambiente(tamaño_grilla, nutrientes_por_celda)
    bacterias, posiciones = crear_bacterias_iniciales(
        num_bacterias, energia_inicial, tamaño_grilla
    )

    # Ubica las bacterias iniciales en la grilla
    for bact, (x, y) in zip(bacterias, posiciones):
        ambiente.grilla[x, y] = bact

    colonia = Colonia(bacterias, ambiente)
    simulador = Simulador(colonia)
    simulador.run(pasos_simulacion)

    lanzar_ventana()


if __name__ == "__main__":
    main()