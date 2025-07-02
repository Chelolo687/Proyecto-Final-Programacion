from bacteria import Bacteria
import random

class Colonia:
    def __init__(self, bacterias, ambiente):
        self.bacterias = bacterias
        self.ambiente = ambiente
        self.proximo_id = self.calcular_proximo_id()

    def calcular_proximo_id(self, nuevas_bacterias=None):
        """Calcula el próximo ID disponible verificando bacterias existentes y nuevas"""
        max_id = 0

        # Buscar en bacterias existentes
        for bacteria in self.bacterias:
            if bacteria.id > max_id:
                max_id = bacteria.id

        # Buscar en nuevas bacterias pendientes de agregar (si se proporcionan)
        if nuevas_bacterias is not None:
            for (bacteria, _, _) in nuevas_bacterias:
                if bacteria.id > max_id:
                    max_id = bacteria.id

        # Si no hay bacterias, empezamos con ID 1
        if max_id == 0 and not self.bacterias and (nuevas_bacterias is None or not nuevas_bacterias):
            return 1

        return max_id + 1
    
    def paso(self):
        #Ejecuta un paso de simulación
        nuevas_bacterias = []
        tamaño = self.ambiente.tamaño_grilla

        for i in range(tamaño):
            for j in range(tamaño):
                bacteria = self.ambiente.grilla[i, j]
                if bacteria and bacteria.estado == "activa":
                    self.procesar_bacteria(bacteria, i, j, nuevas_bacterias)

        # Agregar nuevas bacterias al final del ciclo
        self.agregar_nuevas_bacterias(nuevas_bacterias)

    def procesar_bacteria(self, bacteria, i, j, nuevas_bacterias):
        #Procesa todas las acciones de una bacteria
        # 1. Alimentación
        nutrientes = self.ambiente.obtener_nutrientes(i, j)
        consumido = bacteria.alimentar(nutrientes)
        if consumido > 0:
            self.ambiente.reducir_nutrientes(i, j, consumido)

        # 2. Verificar muerte
        if bacteria.morir_por_inanicion():
            return

        concentracion = self.ambiente.obtener_concentracion_antibiotico(i, j)
        if bacteria.morir_por_antibiotico(concentracion):
            return

        # 3. División
        if bacteria.puede_dividirse():
            self.intentar_division(bacteria, i, j, nuevas_bacterias)
    
    def intentar_division(self, bacteria, i, j, nuevas_bacterias):
        """Intenta dividir la bacteria si hay espacio"""
        vecinos = self.ambiente.obtener_vecinos_libres(i, j)
        if not vecinos:
            return

        # Seleccionar posición para la hija
        nx, ny = random.choice(vecinos)

        # Crear nueva bacteria
        nuevo_id = self.calcular_proximo_id(nuevas_bacterias)
        hija = bacteria.dividir(nuevo_id)

        # Registrar nueva bacteria
        nuevas_bacterias.append((hija, nx, ny))

    def agregar_nuevas_bacterias(self, nuevas_bacterias):
        """Agrega nuevas bacterias al ambiente"""
        for hija, nx, ny in nuevas_bacterias:
            self.bacterias.append(hija)
            self.ambiente.colocar_bacteria(nx, ny, hija)

    def reporte_estado(self):
        activas = 0
        muertas = 0
        resistentes = 0
        for b in self.bacterias:
            if b.estado == "activa":
                activas += 1
                if b.resistente:
                    resistentes += 1
            elif b.estado == "muerta":
                muertas += 1
        return {
            "bacterias_activas": activas,
            "bacterias_muertas": muertas,
            "bacterias_resistentes": resistentes,
        }