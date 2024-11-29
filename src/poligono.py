import algebra
import pymunk
import random
import pygame
import numpy as np

class Poligono():
    def __init__(self, pontos, pos, massa = 1, elasticity = 0, friction = 0, color = None, space = None, categoria = 1, meta_info = None, escala = 1) -> None:
        self.escala = escala
        if escala < 0.01:
            escala = 0.01
        if escala != 1:
            pontos = np.array(pontos, dtype = np.float64)
            pontos *= escala
            pontos = pontos.tolist()
        self.pontos_originais = pontos
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

    def set_categoria(self, categoria, toggle = False):
        self.categoria = categoria
        for shape in self.shapes:
            shape.filter = pymunk.ShapeFilter(categories=categoria, mask= categoria)
        self.update_color_categoria(toggle=toggle)

    def toggle_categoria(self):
        self.set_categoria(3 - self.categoria, toggle = True)

    def render(self, screen):
        # usa os pontos originais e a rotacao do corpo para desenhar ele na posicao correta
        pontos = [algebra.rotaciona_ponto(ponto, self.body.angle) for ponto in self.pontos_originais] # rotaciona os pontos
        pontos = [(int(ponto[0] + self.body.position.x), int(ponto[1] + self.body.position.y)) for ponto in pontos] # translada os pontos
        pygame.draw.polygon(screen, self.color, pontos)


    def update_parametros(self, param: dict):
        self.body.position = param["x"], param["y"]
        self.body.angle = param["angulo"]

    def get_color(self, meta_info):
        if meta_info["tipo"] == "viga":
            h= (360 + random.randint(-15, 15))%360
            s = 30 + random.randint(0, 70)
            l = 33+ random.randint(-5, 5) if self.categoria == 1 else 66 + random.randint(-5, 5)
        elif meta_info["tipo"] == "engrenagem":
            h= 120 + random.randint(-30, 30)
            s = 30 + random.randint(0, 70)
            l = 33+ random.randint(-5, 5) if self.categoria == 1 else 66 + random.randint(-5, 5)
        elif meta_info["tipo"] == "ancora":
            h= 240 + random.randint(-60, 60)
            s = 30 + random.randint(0, 70)
            l = 33+ random.randint(-5, 5) if self.categoria == 1 else 50 + random.randint(-5, 5)
        return algebra.hsl_to_rgb(h,s,l)
    
    def identificaClique(self, pos):
        for shape in self.shapes:
            if shape.point_query(pos).distance <= 0:
                return True
        return False

    def update_color_categoria(self, toggle = False):
        h, s, l = algebra.rgb_to_hsl(*self.color)
        if toggle:
            if self.categoria == 2:
                l  = l/2
            elif self.categoria == 1:
                l = l*2
            else:
                raise ValueError("Categoria invalida")
        else:
            if self.categoria == 1:
                l = 33+ random.randint(-5, 5)
            else:
                l = 66 + random.randint(-5, 5)

        self.color = algebra.hsl_to_rgb(h,s,l)
        for shape in self.shapes:
            shape.color = self.color