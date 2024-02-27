from objeto import Objeto
import numpy as np
import pygame
from poligono import Poligono

class Engrenagem(Objeto):
    def __init__(self, pos: np.ndarray, raio = 10, dentes = 1000, velocidade = None, massa = 1) -> None:
        super().__init__()
        self.posicao = pos
        self.raio = raio
        self.dentes = dentes
        self.velocidade = velocidade
        if velocidade is None:
            self.velocidade = np.zeros(2)
        self.corPadrao = (255, 255, 255)
        self.cor = self.corPadrao
        self.cor = (100+np.random.randint(155),100+np.random.randint(155),100+np.random.randint(155))
        self.massa = massa


    def tick(self):
        super().tick()

    def render(self, screen):
        pygame.draw.circle(screen, self.cor, (self.posicao[0],self.posicao[1]), self.raio)
        if self.debug:
            pygame.draw.line(screen, self.cor, (self.posicao[0],self.posicao[1]), (self.posicao[0]+self.velocidade[0]*10,self.posicao[1]+self.velocidade[1]*10), 2)

    def colidirLimites(self, limites):
        # limites é uma tupla no formato (minX, maxX, minY, maxY)
        if self.posicao[0] - self.raio + self.velocidade[0] < limites[0] or self.posicao[0] + self.raio + self.velocidade[0] > limites[1]: # limite de x
            self.velocidadeAcressimo += self.velocidade * np.array([-2,0,0])
        if self.posicao[1] - self.raio + self.velocidade[1] < limites[2] or self.posicao[1] + self.raio + self.velocidade[1] > limites[3]: # limite de y
            self.velocidadeAcressimo += self.velocidade * np.array([0,-2,0])

    def detectarColisao(self, objeto):
        if isinstance(objeto, Poligono):
            return False
        if self.distancia(objeto) < self.raio + objeto.raio:
            return True
        return False


        