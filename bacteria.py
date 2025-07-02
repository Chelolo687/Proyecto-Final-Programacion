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
    
   def morir_por_inanicion(self):
        """Verifica si debe morir por inanición"""
        if self.energia < 10:
            self.morir()
            return True
        return False

    def morir_por_antibiotico(self, concentracion_antibiotico):
        """Verifica si debe morir por antibiótico"""
        if concentracion_antibiotico > 0 and not self.resistente:
            if random.random() > 0.15:  # 85% de probabilidad de morir
                self.morir()
                return True
        return False
    
    def morir(self):
    self.estado = "muerta"