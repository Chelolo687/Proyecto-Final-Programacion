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
        """Ejecuta un paso de simulación y retorna los eventos ocurridos"""
        nuevas_bacterias = []
        eventos = []
        tamaño = self.ambiente.tamaño_grilla
        
        # Contador para eventos de baja frecuencia
        total_bacterias_procesadas = 0

        for i in range(tamaño):
            for j in range(tamaño):
                bacteria = self.ambiente.grilla[i, j]
                if bacteria and bacteria.estado == "activa":
                    total_bacterias_procesadas += 1
                    eventos_bacteria = self.procesar_bacteria(bacteria, i, j, nuevas_bacterias)
                    eventos.extend(eventos_bacteria)

        # Agregar nuevas bacterias al final del ciclo
        self.agregar_nuevas_bacterias(nuevas_bacterias)
        
        # Eventos adicionales poco frecuentes
        if total_bacterias_procesadas > 0:
            eventos.extend(self.eventos_ambientales(total_bacterias_procesadas))
        
        return eventos

    def procesar_bacteria(self, bacteria, i, j, nuevas_bacterias):
        """Procesa todas las acciones de una bacteria y retorna los eventos"""
        eventos = []
        
        # 1. Alimentación
        nutrientes = self.ambiente.obtener_nutrientes(i, j)
        consumido = bacteria.alimentar(nutrientes)
        if consumido > 0:
            self.ambiente.reducir_nutrientes(i, j, consumido)
            # Reportar consumo alto ocasionalmente
            if consumido > 22 and random.random() < 0.08:
                eventos.append(f"Bacteria {bacteria.id} consumió {consumido} unidades de nutrientes")
        else:
            # Reportar escasez de nutrientes ocasionalmente
            if random.random() < 0.12:
                eventos.append(f"Bacteria {bacteria.id} no encontró nutrientes disponibles")

        # 2. Verificar muerte por inanición
        if bacteria.morir_por_inanicion():
            eventos.append(f"Bacteria {bacteria.id} murió por inanición")
            return eventos

        # 3. Verificar muerte por antibiótico
        concentracion = self.ambiente.obtener_concentracion_antibiotico(i, j)
        if concentracion > 0:
            if bacteria.morir_por_antibiotico(concentracion):
                if bacteria.resistente:
                    eventos.append(f"Bacteria {bacteria.id} (resistente) murió por antibiótico")
                else:
                    eventos.append(f"Bacteria {bacteria.id} murió por antibiótico")
                return eventos
            else:
                # Bacteria sobrevivió al antibiótico
                if not bacteria.resistente and random.random() < 0.15:
                    eventos.append(f"Bacteria {bacteria.id} sobrevivió al antibiótico")

        # 4. División
        if bacteria.puede_dividirse():
            evento_division = self.intentar_division(bacteria, i, j, nuevas_bacterias)
            if evento_division:
                eventos.append(evento_division)
        else:
            # Reportar bacterias con alta energía que no pueden dividirse
            if bacteria.energia > 70 and random.random() < 0.06:
                vecinos = self.ambiente.obtener_vecinos_libres(i, j)
                if not vecinos:
                    eventos.append(f"Bacteria {bacteria.id} no puede dividirse por falta de espacio")
                
        return eventos
    
    def intentar_division(self, bacteria, i, j, nuevas_bacterias):
        """Intenta dividir la bacteria si hay espacio y retorna el evento"""
        vecinos = self.ambiente.obtener_vecinos_libres(i, j)
        if not vecinos:
            return None

        # Seleccionar posición para la hija
        nx, ny = random.choice(vecinos)

        # Crear nueva bacteria
        nuevo_id = self.calcular_proximo_id(nuevas_bacterias)
        hija = bacteria.dividir(nuevo_id)

        # Registrar nueva bacteria
        nuevas_bacterias.append((hija, nx, ny))
        
        # Generar mensaje del evento
        if hija.resistente and not bacteria.resistente:
            return f"Bacteria {bacteria.id} se dividió → hija {hija.id} mutó y adquirió resistencia"
        elif hija.resistente and bacteria.resistente:
            return f"Bacteria {bacteria.id} (resistente) se dividió → hija {hija.id} heredó resistencia"
        else:
            return f"Bacteria {bacteria.id} se dividió → hija {hija.id}"

    def agregar_nuevas_bacterias(self, nuevas_bacterias):
        """Agrega nuevas bacterias al ambiente"""
        for hija, nx, ny in nuevas_bacterias:
            self.bacterias.append(hija)
            self.ambiente.colocar_bacteria(nx, ny, hija)

    def eventos_ambientales(self, total_bacterias):
        """Genera eventos ambientales poco frecuentes"""
        eventos = []
        # Eventos de nutrientes
        if random.random() < 0.18:
            eventos.append("Los nutrientes se están agotando en algunas zonas")
        
        # Eventos de competencia
        if total_bacterias > 15 and random.random() < 0.14:
            eventos.append("Aumenta la competencia por recursos")
            
        # Eventos de resistencia
        resistentes = sum(1 for b in self.bacterias if b.resistente and b.estado == "activa")
        if resistentes > 3 and random.random() < 0.16:
            eventos.append(f"Se detectaron {resistentes} bacterias resistentes en la colonia")
            
        return eventos        

    def reporte_estado(self):
        """Cuenta solo las bacterias que están actualmente en la grilla (visibles)"""
        activas = 0
        muertas = 0
        resistentes = 0
        ya_contadas = set()  # Para evitar contar la misma bacteria dos veces
        tamaño = self.ambiente.tamaño_grilla
        
        for i in range(tamaño):
            for j in range(tamaño):
                bacteria = self.ambiente.grilla[i, j]
                if bacteria is None or bacteria in ya_contadas:
                    continue
                ya_contadas.add(bacteria)
                
                if bacteria.estado == "activa":
                    activas += 1
                    if bacteria.resistente:
                        resistentes += 1
                elif bacteria.estado == "muerta":
                    muertas += 1
                    
        return {
            "bacterias_activas": activas,
            "bacterias_muertas": muertas,
            "bacterias_resistentes": resistentes,
        }

    def reporte_estado_historico(self):
        """Cuenta todas las bacterias que han existido (incluyendo las ya removidas de la grilla)"""
        activas = 0
        muertas = 0
        resistentes = 0
        for bacteria in self.bacterias:
            if bacteria.estado == "activa":
                activas += 1
                if bacteria.resistente:
                    resistentes += 1
            elif bacteria.estado == "muerta":
                muertas += 1
        return {
            "bacterias_activas_historico": activas,
            "bacterias_muertas_historico": muertas,
            "bacterias_resistentes_historico": resistentes,
        }