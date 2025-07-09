import numpy as np
import random   

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

    def obtener_vecinos_libres(self, x, y):
        #Obtiene posiciones vecinas libres
        vecinos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.tamaño_grilla and 0 <= ny < self.tamaño_grilla:
                if self.grilla[nx, ny] is None:
                    vecinos.append((nx, ny))
        return vecinos
    
    def actualizar_nutrientes(self):
        """Recarga lentamente los nutrientes en algunas celdas"""
        for i in range(self.tamaño_grilla):
            for j in range(self.tamaño_grilla):
                if self.nutrientes[i, j] < 50 and random.random() < 0.1:
                    self.nutrientes[i, j] += random.randint(5, 15)

    def difundir_nutrientes(self):
        # Ejemplo: difusión simple de nutrientes a celdas vecinas
        pass

    def aplicar_ambiente(self):
        # Aplica efectos ambientales (antibióticos, estrés, etc.)
        pass