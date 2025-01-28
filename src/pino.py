import pymunk
from pymunk import PivotJoint
import pygame

class Pino:
    def __init__(self, pos, space, ID, body1 = None, body2 = None, parede = False):
        self.all_param = {k: v for k, v in locals().items() if k != 'self'}
        self.ID = ID
        self.parede = parede
        self.joint = None
        if body1:
            if type(body2) == tuple:
                body2 = space.static_body
                self.parede = True
            else:
                # garante que o plano do corpo 1 é diferente do corpo 2
                # shapes não é subscritivel
                for shape in body1.shapes:
                    for shape2 in body2.shapes:
                        if shape.filter.categories == shape2.filter.categories:
                            return
            joint = PivotJoint(body1, body2, pos)
            space.add(joint)
            self.joint = joint
        else:
            # busca todos os corpos no espaco para conectar nesse ponto
            conectados = []
            for body in space.bodies:
                # procura se as shapes do corpo contem o ponto
                for shape in body.shapes:
                    if shape.point_query(pos).distance <= 0:
                        if body not in conectados:
                            # procura um corpo com grupo igual no conectados
                            igual = False
                            for body2 in conectados:
                                for shape2 in body2.shapes:
                                    if shape2.filter.categories == shape.filter.categories:
                                        igual = True
                                    break
                            if igual:
                                continue
                            conectados.append(body)
                        # nao colide
                        if parede:
                            joint = PivotJoint(body, space.static_body, pos)
                            space.add(joint)
                            self.joint = joint
            for i in range(len(conectados)-1):
                joint = PivotJoint(conectados[i], conectados[i+1], pos)
                space.add(joint)
                self.joint = joint
                


    def render(self, screen):
        pygame.draw.circle(screen, (255,0,0,1) if self.parede else (0,255,255,1), self.joint.a.position + self.joint.anchor_a.rotated(self.joint.a.angle), 5)

class Pseudo_Pino:
    def __init__(self, pos, space, ID, parede = False):
        self.all_param = {k: v for k, v in locals().items() if k != 'self'}
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.ID = ID
        self.shapes = [pymunk.Circle(self.body, 5)]
        if parede:
            self.shapes[0].color = (255,0,0,1)
        else:
            self.shapes[0].color = (0,255,255,1)
        self.parede = parede
        space.add(self.body, *self.shapes)
        self.space = space

    def remove(self):
        self.space.remove(self.body, *self.body.shapes)
        del self

    def render(self, screen):
        pygame.draw.circle(screen, self.shapes[0].color, self.body.position, 5)

    def update_parametros(self, param: dict):
        self.body.position = param["x"], param["y"]
        self.parede = param["parede"]
        if self.parede:
            self.shapes[0].color = (255,0,0,1)
        else:
            self.shapes[0].color = (0,255,255,1)