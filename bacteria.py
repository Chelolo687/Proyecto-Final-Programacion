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
    
    def puede_dividirse(self):
        """Determina si puede dividirse"""
        return self.estado == "activa" and self.energia >= 80
    
    def dividir(self, nuevo_id, posicion=None):
        """Realiza el proceso de división celular"""
        energia_hija = self.energia // 2
        self.energia -= energia_hija

        # Determinar resistencia de la hija
        resistente_hija = self.resistente
        
        # Herencia de resistencia con pequeña probabilidad de pérdida
        if self.resistente and random.random() < 0.05:
            resistente_hija = False  # Pérdida de resistencia muy rara
        elif self.resistente and random.random() < 0.95:
            resistente_hija = True  # Herencia normal
        
        # Mutación espontánea a resistencia
        if not resistente_hija and random.random() < 0.12:
            resistente_hija = True

        return Bacteria(
            id=nuevo_id,
            raza=self.raza,
            energia=energia_hija,
            resistente=resistente_hija,
            estado="activa"
        )
    
    def morir(self):
     self.estado = "muerta"