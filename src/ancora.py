import numpy as np
import pygame
from poligono import Poligono
import algebra

class Ancora(Poligono):
    def __init__(self, pos: np.ndarray, escala = 1, velocidade = None, velocidadeAngular = 0, angulo = 0, massa = 1) -> None:
        pontos = [[0.0,-5.0],[50.0,45.0],[40.0,55.0],[40.0,45.0],[0.0,15.0], [-40.0,45.0], [-40.0,55.0], [-50.0,45.0], [0.0,-5.0]]
        pontos = np.array(pontos)
        pontos *= escala
        super().__init__(pontos)
        self.posicao = pos
        self.velocidade = velocidade
        if velocidade is None:
            self.velocidade = np.zeros(2)
        self.velocidadeAngular = velocidadeAngular
        self.angulo = angulo
        self.massa = massa
        self.inercia = 0


    def tick(self):
        super().tick()

        