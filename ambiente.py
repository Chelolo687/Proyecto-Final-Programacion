import numpy as np

class Ambiente:
    def __init__(self, tamaño_grilla, nutrientes_por_celda, factor_ambiental=None):
        self.tamaño_grilla = tamaño_grilla
        self.nutrientes = np.full((tamaño_grilla, tamaño_grilla), nutrientes_por_celda)
        self.grilla = np.full((tamaño_grilla, tamaño_grilla), None, dtype=object)

        if factor_ambiental is not None:
            self.factor_ambiental = factor_ambiental
        else:
            self.factor_ambiental = np.zeros((tamaño_grilla, tamaño_grilla))
