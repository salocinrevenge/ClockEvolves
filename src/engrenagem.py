from objeto import Objeto
import numpy as np
import pygame
import pymunk
from poligono import Poligono

class Engrenagem(Objeto):
    def __init__(self, pos: tuple, raio = 10, dentes = 1000, velocidade = None, massa = 1) -> None:
        super().__init__()
        moment = pymunk.moment_for_circle(massa, 0, raio)
        self.ball_body = pymunk.Body(massa, moment)
        self.ball_body.position = pos
        self.ball_shape = pymunk.Circle(self.ball_body, raio)
        self.ball_shape.elasticity = 0.95
        self.ball_shape.friction = 0.9