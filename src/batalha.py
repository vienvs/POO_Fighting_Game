from random import randint
from personagens import Guerreiro, Inimigo, PocaoVida, Orc, Chefe


class Batalha:
    def __init__(self, jogador, inimigo, sortear=randint):
        if not jogador.esta_vivo() or not inimigo.esta_vivo():
            raise ValueError("Os dois participantes precisam estar vivos.")
        self.jogador = jogador
        self.inimigo = inimigo
        self.sortear = sortear

    @property
    def finalizada(self):
        return not self.jogador.esta_vivo() or not self.inimigo.esta_vivo()

    def agir(self, indice=0, pocao=False):
        if self.finalizada:
            raise ValueError("Esta batalha terminou.")
        if pocao:
            mensagem = self.jogador.usar_pocao()
        else:
            mensagem = self.jogador.atacar(self.inimigo, indice, self.sortear)
        mensagens = [mensagem]
        if not self.finalizada:
            mensagens.append(self.inimigo.atacar(self.jogador, sortear=self.sortear))
        return mensagens


class Torre:
    def __init__(self, classe=Guerreiro, sortear=randint):
        self.jogador = classe()
        self.jogador.inventario = [PocaoVida() for _ in range(3)]
        self.inimigos = [
            Inimigo("Goblin", 65, 10, 80),
            Orc(),
            Inimigo("Duelista", 80, 15, 90),
            Inimigo("Berserker", 100, 18, 75),
            Inimigo("Assassino", 95, 16, 95),
            Inimigo("Gladiador", 115, 19, 85),
            Inimigo("Sentinela", 125, 20, 85),
            Inimigo("Campeao", 140, 22, 80),
            Inimigo("Executor", 155, 23, 85),
            Chefe(),
        ]
        self.indice = 0
        self.sortear = sortear
        self.estado = "batalha"
        self.mensagens = ["Escolha 1, 2, 3 ou P. Vença cada luta para subir."]
        self.batalha = Batalha(self.jogador, self.inimigos[0], sortear)

    @property
    def andar(self):
        return self.indice + 1

    def registrar(self, mensagem):
        self.mensagens.append(mensagem)
        self.mensagens = self.mensagens[-4:]

    def agir(self, indice=0, pocao=False):
        try:
            if self.estado == "intervalo" and pocao:
                self.registrar(self.jogador.usar_pocao())
            elif self.estado == "batalha":
                for mensagem in self.batalha.agir(indice, pocao):
                    self.registrar(mensagem)
                self.verificar_resultado()
        except ValueError as erro:
            self.registrar(str(erro))

    def verificar_resultado(self):
        if self.estado != "batalha" or not self.batalha.finalizada:
            return
        if not self.jogador.esta_vivo():
            self.estado = "derrota"
            self.registrar("Você foi derrotado. R começa uma nova torre.")
        elif self.andar == len(self.inimigos):
            self.estado = "vitoria"
            self.registrar("Você conquistou a torre! R começa outra partida.")
        else:
            self.estado = "intervalo"
            self.jogador.descansar()
            self.registrar("Vitória! Descanso: até +40 vida e +40 mana.")
            if self.andar in (3, 6, 9):
                self.jogador.inventario.append(PocaoVida())
                self.registrar("Recompensa: uma poção de vida.")
            self.registrar("P: preparar-se com uma poção. ENTER: próxima luta.")

    def avancar(self):
        if self.estado != "intervalo":
            return
        self.indice += 1
        self.batalha = Batalha(self.jogador, self.inimigos[self.indice], self.sortear)
        self.estado = "batalha"
        self.registrar(f"Luta {self.andar}/{len(self.inimigos)}: {self.batalha.inimigo.nome}.")
