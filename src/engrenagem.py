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
        self.corPadrao = (255, 255, 255)
        self.cor = self.corPadrao
        self.massa = massa


    def tick(self):
        super().tick()



    def render(self, screen):
        pygame.draw.circle(screen, self.cor, (self.posicao[0],self.posicao[1]), self.raio)


        