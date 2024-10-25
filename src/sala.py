import pymunk
from engrenagem import Engrenagem
from ancora import Ancora
from viga import Viga
from pino import Pino
import pygame
from botao import Botao

class Sala():
    def __init__(self, editor = False) -> None:
        self.draw_options = None

        self.space = pymunk.Space()
        self.space.gravity = 0.0, 1000.0

        self.STATE = "edicao"
        if not editor:
            self.STATE = "simulacao"
            Engrenagem(pos = (301.0, 311.0), space = self.space, raio = 20, massa=10)
            a = Engrenagem(pos = (192.0, 511.0), space = self.space)
            a.set_group(1)

            # Ancora(pos = (392.0, 211.0), space = self.space, massa=4, escala=0.75, color = (255,255,0,1))
            # Ancora(pos = (392.0, 311.0), space = self.space, massa=4, color = (255,100,0,1))

            b = Viga(pos = (192.0, 521.0), space = self.space, massa=2, escala=2)
            b.set_group(1)
            Pino(body1= a.body, body2= b.body, pos = (192.0, 521.0), space = self.space)
            Pino(body1= a.body, body2= b.body, pos = (195.0, 524.0), space = self.space)
            Viga(pos = (192.0, 621.0), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            
            engre = Engrenagem(pos = (392.0, 521.0), space = self.space, color = (0,255,0,1), raio = 50, friction=0, elasticity=0)
            Pino(body1= engre.body, body2= (392.0, 521.0), pos = (392.0, 521.0), space = self.space)

            roda = Engrenagem(pos = (535.0, 531.0), space = self.space, raio = 50, friction=0, elasticity=0)
            Pino(body1= roda.body, body2= (535.0, 531.0), pos = (535.0, 531.0), space = self.space)

            # vigas conectadas
            Viga(pos = (100.0, 171.0), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            Viga(pos = (120.0, 181.0), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            Viga(pos = (100.0, 201.0), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            Viga(pos = (80.0, 191.0), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            Pino(pos = (100.0, 181.0), space = self.space, parede=True)

            Viga(pos = (100.0, 171.0+200), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            Viga(pos = (120.0, 181.0+200), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            Viga(pos = (100.0, 201.0+200), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            Viga(pos = (80.0, 191.0+200), space = self.space, massa=2, largura=100, comprimento=100, color = (255,100,0,1))
            Pino(pos = (100.0, 181.0+200), space = self.space, parede=False)
        else:
            self.cria_editor()

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
        if self.STATE == "simulacao":
            self.space.step(dt)
        elif self.STATE == "edicao":
            pass

    def input(self, evento):
        if self.STATE == "edicao":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for interface in self.interface_editor:
                    clique = interface.identificaClique(evento.pos)
                    if clique:
                        match clique:
                            case "Engrenagem":
                                self.peca_selecionada = Engrenagem(pos = (100,100), space = self.space)
                            case "Ancora":
                                self.peca_selecionada = Ancora(pos = (100,100), space = self.space)
                            case "Viga":
                                self.peca_selecionada = Viga(pos = (100,100), space = self.space)
                            case "Pino":            
                                self.peca_selecionada = Pino(pos = (100,100), space = self.space)
                            case _:
                                print("clique não identificado")
                        break

    def render(self, screen):
        if self.draw_options is None:
            self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.space.debug_draw(self.draw_options)
        if self.STATE == "edicao":
            self.desenha_editor(screen)

    def cria_editor(self):
        self.interface_editor = []
        self.altura_botoes = 100
        self.largura_botoes = 100
        self.interface_editor.append(Botao(10, 10, self.largura_botoes, self.altura_botoes, "Engrenagem", textSize = 22))
        self.interface_editor.append(Botao(10, 10 + (self.altura_botoes+10), self.largura_botoes, self.altura_botoes, "Ancora", textSize = 32))
        self.interface_editor.append(Botao(10, 10 + (self.altura_botoes+10)*2, self.largura_botoes, self.altura_botoes, "Viga", textSize = 32))
        self.interface_editor.append(Botao(10, 10 + (self.altura_botoes+10)*3, self.largura_botoes, self.altura_botoes, "Pino", textSize = 32))
        self.peca_selecionada = None

    def desenha_editor(self, screen):
        # desenha retangulo cinza e largura 2
        pygame.draw.rect(screen, (100,100,100), (0,0,self.largura_botoes+20,(self.altura_botoes+10)*(len(self.interface_editor))+10), 2)
        for interface in self.interface_editor:
            interface.render(screen)