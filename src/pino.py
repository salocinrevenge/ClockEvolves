import pymunk
from pymunk import PivotJoint
import random

class Pino:
    def __init__(self, pos, space, body1 = None, body2 = None, parede = False, grupo = None):
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
                        conectados.append(body)
                        # nao colide
                        for shape in body.shapes:
                            shape.filter = pymunk.ShapeFilter(group=1)
                        if parede:
                            joint = PivotJoint(body, space.static_body, pos)
                            space.add(joint)
            for i in range(len(conectados)-1):
                joint = PivotJoint(conectados[i], conectados[i+1], pos)
                space.add(joint)