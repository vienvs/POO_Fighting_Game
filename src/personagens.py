from random import randint


class Ataque:
    def __init__(self, nome, dano, precisao):
        if type(dano) is not int or dano < 0:
            raise ValueError("Dano deve ser um inteiro não negativo.")
        if type(precisao) is not int or not 0 <= precisao <= 100:
            raise ValueError("Precisão deve ser um inteiro entre 0 e 100.")
        self.nome = nome
        self.dano = dano
        self.precisao = precisao

    def __str__(self):
        texto = f"{self.nome}: {self.dano} dano, {self.precisao}%"
        return texto


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

    def atacar(self, alvo, indice=0, sortear=randint):
        if not self.esta_vivo() or not alvo.esta_vivo():
            raise ValueError("Atacante e alvo precisam estar vivos.")
        if type(indice) is not int or not 0 <= indice < len(self.ataques):
            raise ValueError("Escolha um dos ataques disponíveis.")
        ataque = self.ataques[indice]
        if sortear(1, 100) > ataque.precisao:
            return f"{self.nome} errou {ataque.nome}."
        dano = alvo.receber_dano(ataque.dano)
        return f"{self.nome}: {ataque.nome} causou {dano} de dano."


class Guerreiro(Personagem):
    def __init__(self):
        super().__init__("Guerreiro", 140)
        self.ataques = [Ataque("Corte rapido", 18, 95),
                        Ataque("Espadada", 30, 80),
                        Ataque("Golpe pesado", 46, 60)]


class Inimigo(Personagem):
    def __init__(self, nome, vida, dano, precisao):
        super().__init__(nome, vida)
        self.ataques = [Ataque("Golpe", dano, precisao)]


class Mago(Personagem):
    def __init__(self):
        super().__init__("Mago", 110)
        self.ataques = [Ataque("Cajado", 16, 95)]
