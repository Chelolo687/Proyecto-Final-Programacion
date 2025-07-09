import numpy as np
import random

class Ambiente:
    def __init__(self, tamaño_grilla, nutrientes_por_celda, factor_ambiental=None):
        self.tamaño_grilla = tamaño_grilla
        self.nutrientes = np.full((tamaño_grilla, tamaño_grilla), nutrientes_por_celda)
        self.grilla = np.full((tamaño_grilla, tamaño_grilla), None, dtype=object)
        self.biofilm = np.zeros((tamaño_grilla, tamaño_grilla))

        if factor_ambiental is not None:
            self.factor_ambiental = factor_ambiental
        else:
            # Crear algunas zonas con antibiótico de forma aleatoria
            self.factor_ambiental = np.zeros((tamaño_grilla, tamaño_grilla))
            self.generar_zonas_antibiotico()
            
        # Generar zonas de biofilm después de los antibióticos
        self.generar_zonas_biofilm()
        
    def generar_zonas_antibiotico(self):
        """Genera algunas zonas con concentración de antibiótico"""
        # Crear 2-3 zonas pequeñas con antibiótico
        num_zonas = random.randint(2, 4)
        for _ in range(num_zonas):
            centro_x = random.randint(1, self.tamaño_grilla - 2)
            centro_y = random.randint(1, self.tamaño_grilla - 2)
            
            # Crear una zona pequeña de 1-2 celdas de radio
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    x, y = centro_x + dx, centro_y + dy
                    if 0 <= x < self.tamaño_grilla and 0 <= y < self.tamaño_grilla:
                        if random.random() < 0.6:  # No todas las celdas vecinas tienen antibiótico
                            self.factor_ambiental[x, y] = random.uniform(0.3, 0.8)

    def generar_zonas_biofilm(self):
        """Genera zonas de biofilm de forma similar a las de antibiótico"""
        # Crear 1-2 zonas de biofilm
        num_zonas = random.randint(1, 3)
        for _ in range(num_zonas):
            centro_x = random.randint(2, self.tamaño_grilla - 3)
            centro_y = random.randint(2, self.tamaño_grilla - 3)
            
            # Crear una zona más grande que las de antibiótico (2-3 celdas de radio)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    x, y = centro_x + dx, centro_y + dy
                    if 0 <= x < self.tamaño_grilla and 0 <= y < self.tamaño_grilla:
                        # Distancia al centro para formar zonas más compactas
                        distancia = abs(dx) + abs(dy)
                        if distancia <= 2 and random.random() < 0.7:
                            self.biofilm[x, y] = 1

    def obtener_concentracion_antibiotico(self, x, y):
        """Obtiene la concentración de antibiótico en una posición"""
        return self.factor_ambiental[x, y]

    def es_zona_biofilm(self, x, y):
        """Verifica si una posición está en zona de biofilm"""
        return self.biofilm[x, y] == 1

    def obtener_nutrientes(self, x, y):
        """Obtiene los nutrientes disponibles en una posición"""
        return self.nutrientes[x, y]

    def reducir_nutrientes(self, x, y, cantidad):
        """Reduce los nutrientes en una posición"""
        self.nutrientes[x, y] = max(0, self.nutrientes[x, y] - cantidad)

    def colocar_bacteria(self, x, y, bacteria):
        """Coloca una bacteria en la posición especificada"""
        self.grilla[x, y] = bacteria

    def obtener_vecinos_libres(self, x, y):
        """Obtiene posiciones vecinas libres"""
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
        """Difusión simple de nutrientes a celdas vecinas"""
        pass

    def aplicar_ambiente(self):
        """Aplica efectos ambientales (antibióticos, estrés, etc.)"""
        pass