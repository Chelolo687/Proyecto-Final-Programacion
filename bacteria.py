import random

class Bacteria:
    def __init__(self, id, raza, energia, resistente=False, estado="activa"):
        self.id = id
        self.raza = raza
        self.energia = energia
        self.resistente = resistente
        self.estado = estado

    def alimentar(self, nutrientes_disponibles):
        """Consume nutrientes y aumenta la energía"""
        if nutrientes_disponibles > 0:
            consumido = min(nutrientes_disponibles, random.randint(15, 25))
            self.energia += consumido
            return consumido
        else:
            self.energia -= 10
            return 0
