import pygame
from personagens import Personagem, Guerreiro, Inimigo, Mago


ARTES = {
    'Personagem': ['   O', '  /|\\', '  / \\'],
    'Guerreiro': ['   O   /', '  /|--/', ' [ |', '  / \\'],
    'Inimigo': [' /\\ /\\', '( o o )', ' / V \\', '  / \\'],
    'Mago': ['   /\\', '  /__\\', '   O  *', '  /|\\ |', '  / \\ |'],
}



class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((1100, 720))
        pygame.display.set_caption("POO Fighting Game")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("consolas", 18)
        self.fonte_arte = pygame.font.SysFont("consolas", 32)
        self.rodando = True
        self.classe = Guerreiro
        self.reiniciar()

    def reiniciar(self):
        self.jogador = self.classe()
        self.inimigo = Inimigo("Goblin", 65, 10, 80)
        self.mensagens = ["R: reiniciar. ESC: sair."]

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                self.tecla(evento.key)

    def tecla(self, tecla):
        if tecla == pygame.K_ESCAPE:
            self.rodando = False
        elif tecla == pygame.K_r:
            self.reiniciar()
        elif tecla == pygame.K_F1:
            self.classe = Guerreiro
            self.reiniciar()
        elif tecla == pygame.K_F2:
            self.classe = Mago
            self.reiniciar()
        else:
            try:
                if tecla in (pygame.K_1, pygame.K_2, pygame.K_3):
                    self.mensagens.append(self.jogador.atacar(self.inimigo, tecla - pygame.K_1))
                elif tecla == pygame.K_e:
                    self.mensagens.append(self.inimigo.atacar(self.jogador))
            except ValueError as erro:
                self.mensagens.append(str(erro))
            self.mensagens = self.mensagens[-4:]

    def texto(self, texto, x, y, cor=(224, 228, 236), fonte=None):
        if fonte is None:
            fonte = self.fonte
        imagem = fonte.render(texto, True, cor)
        self.tela.blit(imagem, (x, y))

    def personagem(self, personagem, arte, x, cor):
        self.texto(personagem.nome, x, 100, cor)
        for i, linha in enumerate(ARTES[arte]):
            self.texto(linha, x, 145 + i * 35, cor, self.fonte_arte)
        pygame.draw.rect(self.tela, (52, 56, 66), (x, 342, 260, 18))
        largura = 260 * personagem.vida // personagem.vida_maxima
        pygame.draw.rect(self.tela, cor, (x, 342, largura, 18))
        self.texto(f"Vida: {personagem.vida}/{personagem.vida_maxima}", x, 370)

    def desenhar(self):
        self.tela.fill((18, 21, 29))
        jogador = self.jogador
        inimigo = self.inimigo
        mensagens = self.mensagens
        self.texto("POO FIGHTING GAME", 35, 25)
        self.texto('F1: Guerreiro | F2: Mago | R: reiniciar | ESC: sair', 35, 57)
        self.personagem(jogador, jogador.nome, 50, (87, 207, 170))
        arte = "Inimigo"
        self.personagem(inimigo, arte, 450, (236, 116, 112))
        for i, ataque in enumerate(jogador.ataques, 1):
            self.texto(f"{i}: {ataque}", 50, 460 + (i - 1) * 28)
        self.texto("E: testar ataque do inimigo", 450, 400)
        for i, mensagem in enumerate(mensagens[-4:]):
            self.texto(mensagem, 35, 595 + i * 27)
        pygame.display.flip()

    def executar(self):
        while self.rodando:
            self.eventos()
            self.desenhar()
            self.relogio.tick(60)
        pygame.quit()
