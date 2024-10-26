import algebra
import pymunk
import random

class Poligono():
    def __init__(self, pontos, pos, massa = 1, elasticity = 0, friction = 0, color = None, space = None, categoria = 1, meta_info = None) -> None:
        self.pontosColisao, self.pontos_externos = algebra.triangulariza(pontos)
        moment = pymunk.moment_for_poly(mass = massa, vertices=pontos)
        self.body = pymunk.Body(massa, moment)
        self.body.position = pos
        self.shapes = []
        self.color = (255,255,255,1)
        self.categoria = categoria
        if meta_info:
            self.color = self.get_color(meta_info)
        if color:
            print("color: ", color)
            self.color = color
        for triangulo in self.pontosColisao:
            shape = pymunk.Poly(self.body,vertices=triangulo.tolist())
            shape.elasticity = elasticity
            shape.friction = friction
            shape.color = self.color
            # shape.color = (random.randint(50,255), random.randint(50,255), random.randint(50,255), 1)
            shape.filter = pymunk.ShapeFilter(categories=categoria, mask= categoria)
            self.shapes.append(shape)
        self.space = space
        if self.space:
            self.space.add(self.body, *self.shapes)

    def update_parametros(self, param: dict):
        self.body.position = param["x"], param["y"]
        self.body.angle = param["angulo"]

    def get_color(self, meta_info):
        if meta_info["tipo"] == "viga":
            h= (360 + random.randint(0, 60))%360
            s = 30 + random.randint(0, 70)
            l = 33+ random.randint(-5, 5) if self.categoria == 1 else 66 + random.randint(-5, 5)
            return (255,0,0,1)
        elif meta_info["tipo"] == "engrenagem":
            h= 120 + random.randint(0, 60)
            s = 30 + random.randint(0, 70)
            l = 33+ random.randint(-5, 5) if self.categoria == 1 else 66 + random.randint(-5, 5)
        elif meta_info["tipo"] == "ancora":
            h= 240 + random.randint(0, 60)
            s = 30 + random.randint(0, 70)
            l = 33+ random.randint(-5, 5) if self.categoria == 1 else 66 + random.randint(-5, 5)
        # converte pra RGB
        return algebra.hsl_to_rgb(h,s,l)