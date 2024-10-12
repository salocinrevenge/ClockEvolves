import pymunk
from pymunk import PivotJoint

class Pino:
    def __init__(self, body1, body2, pos, space):
        if type(body2) == tuple:
            body2 = space.static_body
        joint = PivotJoint(body1, body2, pos)
        space.add(joint)