import numpy as np
from poligono import Poligono
import pymunk

class Ancora(Poligono):
    def __init__(self, pos: np.ndarray, escala = 1, velocidade = None, velocidadeAngular = 0, angulo = 0, massa = 1, space = None) -> None:
        pontos = np.array([[0.0,-5.0],[50.0,45.0],[40.0,55.0],[40.0,45.0],[0.0,15.0], [-40.0,45.0], [-40.0,55.0], [-50.0,45.0]])
        pontos *= escala
        super().__init__(pontos)
        pontos = pontos.tolist()
        moment = pymunk.moment_for_poly(self.massa, vertices=pontos)
        self.body = pymunk.Body(massa, moment)
        self.body.position = pos
        self.shapes = []
        for triangulo in self.pontosColisao:
            shape = pymunk.Poly(self.body,vertices=triangulo.tolist())
            shape.elasticity = 0.95
            shape.friction = 0.9
            self.shapes.append(shape)
        self.space = space
        if self.space:
            self.space.add(self.body, *self.shapes)