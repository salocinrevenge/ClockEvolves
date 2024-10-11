import pygame
import pymunk
from engrenagem import Engrenagem
from ancora import Ancora
from viga import Viga

class Sala():
    def __init__(self) -> None:
        self.draw_options = None

        self.space = pymunk.Space()
        self.space.gravity = 0.0, 1000.0

        Engrenagem(pos = (301.0, 311.0), space = self.space)
        Engrenagem(pos = (492.0, 311.0), space = self.space)
        Engrenagem(pos = (392.0, 211.0), space = self.space)

        Ancora(pos = (392.0, 211.0), space = self.space, massa=4, escala=0.75, color = (255,255,0,1))
        Ancora(pos = (392.0, 311.0), space = self.space, massa=4, color = (255,100,0,1))

        Viga(pos = (192.0, 511.0), space = self.space, massa=2, escala=2)

        self.build_border()

    def build_border(self):
        positions = [((0,800), (800,800)), ((0,0), (0,800)), ((800,0), (800,800)), ((0,0), (800,0))]
        elasticity = [0.3, 0.95, 0.95, 0.95]
        friction = [1.8, 0.95, 0.95, 0.95]
        cor = (100, 100, 100, 1)
        for i in range(4):
            segment_shape = pymunk.Segment(self.space.static_body, positions[i][0], positions[i][1], 10)
            segment_shape.color = cor
            segment_shape.elasticity = elasticity[i]
            segment_shape.friction = friction[i]
            self.space.add(segment_shape)

    def tick(self, dt):
        self.space.step(dt)

    def input(self, evento):
        pass

    def render(self, screen):
        if self.draw_options is None:
            self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.space.debug_draw(self.draw_options)
