from objeto import Objeto
import numpy as np
import pygame

class Viga(Objeto):
    def __init__(self, pos: np.ndarray, comprimento = 100, largura = 10, velocidade = None, massa = 1) -> None:
        super().__init__()
        self.posicao = pos
        self.comprimento = comprimento
        self.largura = largura
        self.velocidade = velocidade
        if velocidade is None:
            self.velocidade = np.zeros(3)
        self.corPadrao = (255, 255, 255)
        self.cor = self.corPadrao
        self.cor = (100+np.random.randint(155),100+np.random.randint(155),100+np.random.randint(155))
        self.massa = massa


    def tick(self):
        super().tick()

    def colidirLimites(self, limites):
        pass

    def detectarColisao(self, objeto):
        return False


    def render(self, screen):
        # desenha um retangulo com centro em posicao e com comprimento e largura
        pygame.draw.rect(screen, self.cor, (self.posicao[0]-self.comprimento//2,self.posicao[1]-self.largura//2,self.comprimento,self.largura))
        if self.debug:
            pygame.draw.line(screen, self.cor, (self.posicao[0],self.posicao[1]), (self.posicao[0]+self.velocidade[0]*10,self.posicao[1]+self.velocidade[1]*10), 2)


        