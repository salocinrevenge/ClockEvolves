import numpy as np
import pygame
from poligono import Poligono
import algebra

class Catraca(Poligono):
    def __init__(self, pos: np.ndarray, comprimento = 100, largura = 10, velocidade = None, velocidadeAngular = 0, angulo = 0, massa = 1) -> None:
        pontos = np.array([[-comprimento//2,-largura//2],[comprimento//2,-largura//2],[comprimento//2,largura//2],[-comprimento//2,largura//2]])
        super().__init__(pontos)
        self.posicao = pos
        self.velocidade = velocidade
        if velocidade is None:
            self.velocidade = np.zeros(2)
        self.velocidadeAngular = velocidadeAngular
        self.corPadrao = (255, 255, 255)
        self.angulo = angulo
        self.cor = self.corPadrao
        self.cor = (100+np.random.randint(155),100+np.random.randint(155),100+np.random.randint(155))
        self.massa = massa
        self.comprimento = comprimento
        self.largura = largura
        self.inercia = 0


    def tick(self):
        super().tick()

    def detectarColisao(self, objeto):
        colisao = False
        if colisao:
            algebra.colisaoCirculoPoligono(self, objeto)
        