import pymunk
from pymunk import PivotJoint

class Pino:
    def __init__(self, body1, body2, pos, space):
        joint = PivotJoint(body1, body2, pos)
        space.add(joint)