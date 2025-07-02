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
        
    def obtener_concentracion_antibiotico(self, x, y):
        #Obtiene la concentración de antibiótico en una posición
        return self.factor_ambiental[x, y]

    def obtener_nutrientes(self, x, y):
        #Obtiene los nutrientes disponibles en una posición
        return self.nutrientes[x, y]

    def reducir_nutrientes(self, x, y, cantidad):
        #Reduce los nutrientes en una posición
        self.nutrientes[x, y] -= cantidad

    def colocar_bacteria(self, x, y, bacteria):
        #Coloca una bacteria en la posición especificada
        self.grilla[x, y] = bacteria
