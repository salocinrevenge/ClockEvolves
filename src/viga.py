import numpy as np
from poligono import Poligono
import pymunk

class Viga(Poligono):
    def __init__(self, pos: np.ndarray, comprimento = 100, largura = 10, escala = 1, velocidade = None, velocidadeAngular = 0, angulo = 0, massa = 1, elasticity = 0.3, friction = 1.0, space = None) -> None: # largura padrao é 10
        pontos = np.array([[-comprimento//2,-largura//2],[comprimento//2,-largura//2],[comprimento//2,largura//2],[-comprimento//2,largura//2]])
        pontos *= escala
        super().__init__(pontos)
        pontos = pontos.tolist()
        moment = pymunk.moment_for_poly(self.massa, vertices=pontos)
        self.body = pymunk.Body(massa, moment)
        self.body.position = pos
        self.shapes = []
        for triangulo in self.pontosColisao:
            shape = pymunk.Poly(self.body,vertices=triangulo.tolist())
            shape.elasticity = elasticity
            shape.friction = friction
            self.shapes.append(shape)
        self.space = space
        if self.space:
            self.space.add(self.body, *self.shapes)
        