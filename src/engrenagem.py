from objeto import Objeto
import numpy as np
import pygame

class Engrenagem(Objeto):
    def __init__(self, pos: np.ndarray, raio = 10, dentes = 1000, velocidade = np.zeros(3), massa = 1) -> None:
        super().__init__()
        self.posicao = pos
        self.raio = raio
        self.dentes = dentes
        self.velocidade = velocidade
        self.aceleracao = np.zeros(3)
        self.corPadrao = (255, 255, 255)
        self.cor = self.corPadrao
        self.massa = massa


    def tick(self):
        self.posicao += self.velocidade
        self.velocidade += self.aceleracao


    def render(self, screen):
        pygame.draw.circle(screen, self.cor, (self.posicao[0],self.posicao[1]), self.raio, 20)

    def colidir(self, objeto):
        velocidade = self.velocidade.copy()
        self.velocidade = (self.massa-objeto.massa)*self.velocidade/(self.massa+objeto.massa) + 2*objeto.massa*objeto.velocidade/(self.massa+objeto.massa)
        objeto.velocidade = (objeto.massa-self.massa)*objeto.velocidade/(self.massa+objeto.massa) + 2*self.massa*velocidade/(self.massa+objeto.massa)
        