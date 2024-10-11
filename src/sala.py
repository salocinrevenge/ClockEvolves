import pygame
import pymunk
from engrenagem import Engrenagem
from ancora import Ancora
from viga import Viga

class Sala():
    def __init__(self) -> None:
        # cria objetos
        # self.parede.objetos.append(Engrenagem(np.array([392.0, 311.0])))
        # self.parede.objetos.append(Engrenagem(np.array([390.0, 279.0])))

        # self.parede.player = Player(np.array([500., 300.]))
        # self.parede.objetos.append(self.parede.player)
        self.draw_options = None


        self.space = pymunk.Space()
        self.space.gravity = 0.0, 1000.0

        Engrenagem(pos = (391.0, 311.0), space = self.space)
        Engrenagem(pos = (492.0, 311.0), space = self.space)
        Engrenagem(pos = (392.0, 211.0), space = self.space)

        Ancora(pos = (392.0, 211.0), space = self.space, massa=4, escala=0.75, color = (255,255,0,1))
        Ancora(pos = (392.0, 311.0), space = self.space, massa=4, color = (255,100,0,1))

        Viga(pos = (192.0, 511.0), space = self.space, massa=2, escala=2)

        segment_shape = pymunk.Segment(self.space.static_body, (0, 800), (800, 800), 2)
        # muda a cor do segmento
        segment_shape.color = (255, 255, 0, 1)
        segment_shape.elasticity = 0.3
        segment_shape.friction = 1.8
        self.space.add(segment_shape)

        segment_shape = pymunk.Segment(self.space.static_body, (0, 0), (0, 800), 2)
        # muda a cor do segmento
        segment_shape.color = (255, 255, 0, 1)
        segment_shape.elasticity = 0.95
        self.space.add(segment_shape)

        segment_shape = pymunk.Segment(self.space.static_body, (800, 0), (800, 800), 2)
        # muda a cor do segmento
        segment_shape.color = (255, 255, 0, 1)
        segment_shape.elasticity = 0.95
        self.space.add(segment_shape)

        segment_shape = pymunk.Segment(self.space.static_body, (0, 0), (800, 0), 2)
        # muda a cor do segmento
        segment_shape.color = (255, 255, 0, 1)
        segment_shape.elasticity = 0.95
        self.space.add(segment_shape)


    def tick(self, dt):
        self.space.step(dt)

    def input(self, evento):
        pass

    def render(self, screen):
        # desenha a borda da sala
        if self.draw_options is None:
            self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.space.debug_draw(self.draw_options)
