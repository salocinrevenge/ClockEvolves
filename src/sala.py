import pymunk
from engrenagem import Engrenagem
from ancora import Ancora
from viga import Viga
from pino import Pino, Pseudo_Pino
import pygame
from botao import Botao
from random import randint

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
                if evento.button == 1:  # botao esquerdo
                    if self.peca_selecionada:
                        if isinstance(self.peca_selecionada, Pseudo_Pino):
                            # cria um pino na mesma posicao do pseudo pino
                            position = self.peca_selecionada.body.position
                            parede = self.peca_selecionada.parede
                            self.peca_selecionada.remove()
                            Pino(pos = position, space = self.space, parede=parede)
                        self.peca_selecionada = None
                        self.parametros_editaveis = self.parametros_editaveis_padrao.copy()
                        return
                    for interface in self.interface_editor:
                        clique = interface.identificaClique(evento.pos)
                        if clique:
                            cor = (randint(50,255), randint(50,255), randint(50,255), 1)
                            match clique:
                                case "Engrenagem":
                                    self.peca_selecionada = Engrenagem(pos = evento.pos, space = self.space, color=cor)
                                case "Ancora":
                                    self.peca_selecionada = Ancora(pos = evento.pos, space = self.space, color=cor)
                                case "Viga":
                                    self.peca_selecionada = Viga(pos = evento.pos, space = self.space, color=cor)
                                case "Pino":            
                                    self.peca_selecionada = Pseudo_Pino(pos = evento.pos, space = self.space)
                                case "Executar":
                                    self.STATE = "simulacao"
                                case _:
                                    print("clique não identificado")
                            break
                if evento.button == 4:
                    self.parametros_editaveis["angulo"] -= 0.1
                    self.parametros_editaveis["parede"] = not self.parametros_editaveis["parede"]
                    self.update_selected()
                    return
                if evento.button == 5:
                    self.parametros_editaveis["angulo"] += 0.1
                    self.parametros_editaveis["parede"] = not self.parametros_editaveis["parede"]
                    self.update_selected()
                    return

            if evento.type == pygame.MOUSEMOTION:
                self.parametros_editaveis["x"], self.parametros_editaveis["y"] = evento.pos
                self.update_selected()
                return

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # remove do espaco
                    if self.peca_selecionada:
                        self.space.remove(self.peca_selecionada.body, *self.peca_selecionada.shapes)
                    del self.peca_selecionada
                    self.peca_selecionada = None
                    return

                # se +
                if evento.key == pygame.K_KP_PLUS:
                    self.parametros_editaveis["comprimento"] += 10
                    self.update_selected(rebuild = True)
                    return
                # se -
                if evento.key == pygame.K_KP_MINUS:
                    self.parametros_editaveis["comprimento"] -= 10
                    self.update_selected(rebuild = True)
                    return
                

    def update_selected(self, rebuild = False):
        if self.peca_selecionada:
            # remove a peca selecionada do espaco
            self.space.remove(self.peca_selecionada.body, *self.peca_selecionada.shapes)
            print(self.space._bodies)
            if rebuild:
                # obtem a classe da peca selecionada para criar uma nova
                classe = self.peca_selecionada.__class__
                self.peca_selecionada = classe(pos = (self.parametros_editaveis["x"], self.parametros_editaveis["y"]), space = self.space)
            else:
                self.peca_selecionada.update_parametros(self.parametros_editaveis)

            # recoloca na nova posicao
            self.space.add(self.peca_selecionada.body, *self.peca_selecionada.shapes)


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
        self.parametros_editaveis_padrao = {"x": 100, "y": 100,"comprimento": 100, "largura": 10, "parede": False, "angulo": 0}
        self.parametros_editaveis = self.parametros_editaveis_padrao.copy()
        self.limites_parametros = {"x": (10,790), "y": (10,790), "comprimento": (10, 500), "largura": (10,500) ,"parede": (False, True), "angulo": (0, 360)}

        self.interface_editor.append(Botao(800-10-self.largura_botoes, 800-self.altura_botoes-10, self.largura_botoes, self.altura_botoes, "Executar", textSize = 32))

    def desenha_editor(self, screen):
        # desenha retangulo cinza e largura 2
        pygame.draw.rect(screen, (100,100,100), (0,0,self.largura_botoes+20,(self.altura_botoes+10)*(len(self.interface_editor)-1)+10), 2)
        for interface in self.interface_editor:
            interface.render(screen)