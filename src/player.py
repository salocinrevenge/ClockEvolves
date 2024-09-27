# This class must only be used for debugging process.
import numpy as np
from poligono import Poligono
import pygame

class Player(Poligono):
    def __init__(self, pos: np.ndarray, escala = 1, velocidade = None, velocidadeAngular = 0, angulo = 0, massa = 1) -> None:
        pontos = np.array([[0,-10], [10,-3], [3,10], [-3,10], [-10,-3]])
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

    def input(self, event):
        # verifica se o evento é de teclado
        if event.type == pygame.KEYDOWN:
            # verifica se a tecla pressionada é a seta para cima
            if event.key == pygame.K_UP:
                self.velocidade[1] += 1
            # verifica se a tecla pressionada é a seta para baixo
            elif event.key == pygame.K_DOWN:
                self.velocidade[1] -= 1
            # verifica se a tecla pressionada é a seta para esquerda
            elif event.key == pygame.K_LEFT:
                self.velocidade[0] -= 1
            # verifica se a tecla pressionada é a seta para direita
            elif event.key == pygame.K_RIGHT:
                self.velocidade[0] += 1
        # verifica se o evento é de soltar tecla
        elif event.type == pygame.KEYUP:
            # verifica se a tecla solta é a seta para cima
            if event.key == pygame.K_UP:
                self.velocidade[1] -= 1
            # verifica se a tecla solta é a seta para baixo
            elif event.key == pygame.K_DOWN:
                self.velocidade[1] += 1
            # verifica se a tecla solta é a seta para esquerda
            elif event.key == pygame.K_LEFT:
                self.velocidade[0] += 1
            # verifica se a tecla solta é a seta para direita
            elif event.key == pygame.K_RIGHT:
                self.velocidade[0] -= 1