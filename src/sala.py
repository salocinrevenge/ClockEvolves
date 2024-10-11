import pygame
import pymunk
from engrenagem import Engrenagem
from ancora import Ancora
from viga import Viga
from pino import Pino

class Sala():
    def __init__(self) -> None:
        self.draw_options = None

        self.space = pymunk.Space()
        self.space.gravity = 0.0, 1000.0

        Engrenagem(pos = (301.0, 311.0), space = self.space)
        Engrenagem(pos = (492.0, 311.0), space = self.space)
        Engrenagem(pos = (300.0, 200.0), space = self.space, color = (0,255,0,1), raio = 50)
        a = Engrenagem(pos = (192.0, 511.0), space = self.space)
        a.set_group(1)

        Ancora(pos = (392.0, 211.0), space = self.space, massa=4, escala=0.75, color = (255,255,0,1))
        Ancora(pos = (392.0, 311.0), space = self.space, massa=4, color = (255,100,0,1))

        b = Viga(pos = (192.0, 521.0), space = self.space, massa=2, escala=2)
        b.set_group(1)
        Pino(a.body, b.body, pos = (192.0, 521.0), space = self.space)
        Pino(a.body, b.body, pos = (195.0, 524.0), space = self.space)
        Viga(pos = (192.0, 621.0), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
        

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
