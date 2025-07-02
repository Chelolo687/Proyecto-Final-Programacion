from bacteria import Bacteria

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
