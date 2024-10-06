import pygame
import pymunk
from engrenagem import Engrenagem
from ancora import Ancora

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

        engrenagem = Engrenagem(pos = (391.0, 311.0))
        self.space.add(engrenagem.body, engrenagem.shape)
        engrenagem = Engrenagem(pos = (492.0, 311.0))
        self.space.add(engrenagem.body, engrenagem.shape)
        engrenagem = Engrenagem(pos = (392.0, 211.0))
        self.space.add(engrenagem.body, engrenagem.shape)

        engrenagem = Ancora(pos = (392.0, 211.0))
        self.space.add(engrenagem.body, engrenagem.shape)

        segment_shape = pymunk.Segment(self.space.static_body, (0, 800), (800, 800), 2)
        # muda a cor do segmento
        segment_shape.color = (255, 255, 0, 1)
        segment_shape.elasticity = 0.95
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
