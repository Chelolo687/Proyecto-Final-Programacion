import random

class Bacteria:
    def __init__(self, id, raza, energia, resistente=False, estado="activa"):
        self.id = id
        self.raza = raza
        self.energia = energia
        self.resistente = resistente
        self.estado = estado
