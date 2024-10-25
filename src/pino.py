import pymunk
from pymunk import PivotJoint
import random

class Pino:
    def __init__(self, pos, space, body1 = None, body2 = None, parede = False, grupo = None):
        # mostra todos os parametros
        if grupo is None:
            grupo = random.randint(1, 100000000)
        if body1:
            if type(body2) == tuple:
                body2 = space.static_body
            else:
                # 
                for shape in body2.shapes:
                            shape.filter = pymunk.ShapeFilter(group=grupo)
            joint = PivotJoint(body1, body2, pos)
            space.add(joint)
            # seta o grupo para as shapes do corpo
            for shape in body1.shapes:
                            shape.filter = pymunk.ShapeFilter(group=grupo)
        else:
            # busca todos os corpos no espaco para conectar nesse ponto
            conectados = []
            for body in space.bodies:
                # procura se as shapes do corpo contem o ponto
                for shape in body.shapes:
                    if shape.point_query(pos).distance <= 0:
                        if body not in conectados:
                            conectados.append(body)
                        # nao colide
                        if parede:
                            joint = PivotJoint(body, space.static_body, pos)
                            space.add(joint)
            # procura grupo nao nulo
            for body in conectados:
                for shape in body.shapes:
                    if shape.filter.group != 0:
                        grupo = shape.filter.group
                        break
            for body in conectados:
                for shape in body.shapes:
                    shape.filter = pymunk.ShapeFilter(group=grupo)
                    random.seed(grupo)
                    cor = (random.randint(50,255), random.randint(50,255), random.randint(50,255), 1)
                    shape.color = cor
            for i in range(len(conectados)-1):
                joint = PivotJoint(conectados[i], conectados[i+1], pos)
                space.add(joint)

class Pseudo_Pino:
    def __init__(self, pos, space, parede = False):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = pos
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

    def update_parametros(self, param: dict):
        self.body.position = param["x"], param["y"]
        self.parede = param["parede"]
        if self.parede:
            self.shapes[0].color = (255,0,0,1)
        else:
            self.shapes[0].color = (0,255,255,1)