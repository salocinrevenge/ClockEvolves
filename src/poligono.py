import algebra
import pymunk
import random

class Poligono():
    def __init__(self, pontos, pos, massa = 1, elasticity = 0, friction = 0, color = (255,255,255,1), space = None, categoria = 1) -> None:
        self.pontosColisao, self.pontos_externos = algebra.triangulariza(pontos)
        moment = pymunk.moment_for_poly(mass = massa, vertices=pontos)
        self.body = pymunk.Body(massa, moment)
        self.body.position = pos
        self.shapes = []
        for triangulo in self.pontosColisao:
            shape = pymunk.Poly(self.body,vertices=triangulo.tolist())
            shape.elasticity = elasticity
            shape.friction = friction
            if color:
                shape.color = color
                # shape.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255), 1)
            shape.filter = pymunk.ShapeFilter(categories=categoria, mask= categoria)
            self.shapes.append(shape)
        self.space = space
        if self.space:
            self.space.add(self.body, *self.shapes)

    def update_parametros(self, param: dict):
        self.body.position = param["x"], param["y"]
        self.body.angle = param["angulo"]