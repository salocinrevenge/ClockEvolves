import algebra
import pymunk

class Poligono():
    def __init__(self, pontos, pos, massa = 1, elasticity = 0, friction = 0, color = (255,255,255,1), space = None) -> None:
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
            self.shapes.append(shape)
        self.space = space
        if self.space:
            self.space.add(self.body, *self.shapes)

    def set_group(self, group):
        for shape in self.shapes:
            shape.filter = pymunk.ShapeFilter(group=group)

    def render(self, screen):
        pass

    def update_parametros(self, param: dict):
        self.body.position = param["x"], param["y"]
        self.body.angle = param["angulo"]