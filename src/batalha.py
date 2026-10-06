from random import randint


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
