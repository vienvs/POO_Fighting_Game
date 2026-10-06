import pygame
from personagens import Personagem


ARTES = {
    'Personagem': ['   O', '  /|\\', '  / \\'],
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
        self.classe = Personagem
        self.reiniciar()

    def reiniciar(self):
        self.jogador = Personagem("Jogador", 140)
        self.inimigo = Personagem("Alvo", 100)
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
        self.texto('R: reiniciar | ESC: sair', 35, 57)
        self.personagem(jogador, "Personagem", 50, (87, 207, 170))
        arte = "Personagem"
        self.personagem(inimigo, arte, 450, (236, 116, 112))
        for i, mensagem in enumerate(mensagens[-4:]):
            self.texto(mensagem, 35, 595 + i * 27)
        pygame.display.flip()

    def executar(self):
        while self.rodando:
            self.eventos()
            self.desenhar()
            self.relogio.tick(60)
        pygame.quit()
