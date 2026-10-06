class Personagem:
    def __init__(self, nome, vida):
        if type(vida) is not int or vida <= 0:
            raise ValueError("Vida deve ser um inteiro positivo.")
        self.nome = nome
        self.vida_maxima = vida
        self._vida = vida
        self.ataques = []

    @property
    def vida(self):
        return self._vida

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano):
        if type(dano) is not int or dano < 0:
            raise ValueError("Dano deve ser um inteiro não negativo.")
        recebido = min(self.vida, dano)
        self._vida -= recebido
        return recebido
