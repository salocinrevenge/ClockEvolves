import pymunk
from engrenagem import Engrenagem
from ancora import Ancora
from viga import Viga
from pino import Pino, Pseudo_Pino
import pygame
from botao import Botao
from random import randint
from poligono import Poligono
from algebra import clamp
import re

class Sala():
    def __init__(self, editor = False, carregar = None) -> None:

        self.ID = 0

        self.space = pymunk.Space()
        self.space.gravity = 0.0, 1000.0

        self.STATE = "edicao"
        self.objetos = []
        if carregar:
            self.carregar_sala(carregar)
        elif not editor:
            self.STATE = "simulacao"
            

            self.objetos.append(Engrenagem(pos = (301.0, 311.0), ID = self.get_ID(), space = self.space, raio = 20, massa=10, categoria=1))
            a = Engrenagem(pos = (192.0, 511.0), ID = self.get_ID(), space = self.space,categoria=2)
            self.objetos.append(a)

            self.objetos.append(Ancora(pos = (92.0, 211.0), ID = self.get_ID(), space = self.space, massa=4, escala=0.75, categoria=2))
            self.objetos.append(Ancora(pos = (92.0, 311.0), ID = self.get_ID(), space = self.space, massa=4, categoria=2))

            b = Viga(pos = (192.0, 521.0), ID = self.get_ID(), space = self.space, massa=2, categoria=1)
            self.objetos.append(b)

            self.objetos.append(Pino(body1= a.body, ID = self.get_ID(), body2= b.body, pos = (192.0, 521.0), space = self.space))
            self.objetos.append(Pino(body1= a.body, ID = self.get_ID(), body2= b.body, pos = (195.0, 524.0), space = self.space))
            
            engre = Engrenagem(pos = (392.0, 521.0), ID = self.get_ID(), space = self.space, raio = 50, friction=0, elasticity=0, categoria=1)
            self.objetos.append(engre)
            self.objetos.append(Pino(body1= engre.body, ID = self.get_ID(), body2= (392.0, 521.0), pos = (392.0, 521.0), space = self.space))

            roda = Engrenagem(pos = (535.0, 531.0), ID = self.get_ID(), space = self.space, raio = 50, friction=0, elasticity=0, categoria=1)
            self.objetos.append(roda)
            self.objetos.append(Pino(body1= roda.body, ID = self.get_ID(), body2= (535.0, 531.0), pos = (535.0, 531.0), space = self.space))

            

            # # vigas conectadas
            self.objetos.append(Viga(pos = (100.0, 171.0), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            self.objetos.append(Viga(pos = (120.0, 181.0), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=1))
            self.objetos.append(Viga(pos = (100.0, 201.0), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            self.objetos.append(Viga(pos = (80.0, 191.0), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            self.objetos.append(Pino(pos = (100.0, 181.0), ID = self.get_ID(), space = self.space, parede=True))

            
            self.objetos.append(Viga(pos = (100.0, 171.0+200), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            self.objetos.append(Viga(pos = (120.0, 181.0+200), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=1))
            self.objetos.append(Viga(pos = (100.0, 201.0+200), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=1))
            self.objetos.append(Viga(pos = (80.0, 191.0+200), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            self.objetos.append(Pino(pos = (100.0, 181.0+200), ID = self.get_ID(), space = self.space, parede=False))
            
        else:
            self.cria_editor()

        self.build_border()

        # ordena os objetos com base nas categorias se ele possuir categoria, se não, ele vai por ultimo

        self.objetos.sort(key = lambda x: x.categoria if hasattr(x, "categoria") else 3)

    def get_ID(self):
        self.ID+=1
        return self.ID-1

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
            # todas categorias
            segment_shape.filter = pymunk.ShapeFilter(categories = pymunk.ShapeFilter.ALL_CATEGORIES(), mask = pymunk.ShapeFilter.ALL_MASKS())
            self.objetos.append(segment_shape)
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
                            self.peca_selecionada = Pino(pos = position, ID = self.get_ID(), space = self.space, parede=parede)
                            if self.peca_selecionada.joint is None:
                                self.peca_selecionada = None
                        if self.peca_selecionada:
                            self.objetos.append(self.peca_selecionada)
                        self.peca_selecionada = None
                        self.parametros_editaveis = self.parametros_editaveis_padrao.copy()
                        return
                    # detecta se ele clicou sobre o corpo de uma peca ja existente
                    for objeto in self.objetos:
                        if isinstance(objeto, Poligono):
                            if objeto.identificaClique(evento.pos):
                                self.objetos.remove(objeto)
                                self.peca_selecionada = objeto
                                self.parametros_editaveis = {"x": objeto.body.position.x, "y": objeto.body.position.y, "escala": objeto.escala*100, "angulo": objeto.body.angle, "parede": False}
                                self.update_selected()
                                return


                    for interface in self.interface_editor:
                        clique = interface.identificaClique(evento.pos)
                        if clique:
                            cor = (randint(50,255), randint(50,255), randint(50,255), 1)
                            match clique:
                                case "Engrenagem":
                                    self.peca_selecionada = Engrenagem(pos = evento.pos, ID = self.get_ID(), space = self.space, color=cor)
                                case "Ancora":
                                    self.peca_selecionada = Ancora(pos = evento.pos, ID = self.get_ID(), space = self.space, color=cor)
                                case "Viga":
                                    self.peca_selecionada = Viga(pos = evento.pos, ID = self.get_ID(), space = self.space, color=cor)
                                case "Pino":            
                                    self.peca_selecionada = Pseudo_Pino(pos = evento.pos, ID = self.get_ID(), space = self.space)
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
                pos = evento.pos
                pos = (((pos[0]+self.grade[self.grade_selecionada]//2)//self.grade[self.grade_selecionada])*self.grade[self.grade_selecionada], ((pos[1]+ self.grade[self.grade_selecionada]//2)//self.grade[self.grade_selecionada])*self.grade[self.grade_selecionada])
                self.posMouse = pos
                self.parametros_editaveis["x"], self.parametros_editaveis["y"] = pos
                self.update_selected()
                return

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # remove do espaco
                    if self.peca_selecionada:
                        self.space.remove(self.peca_selecionada.body, *self.peca_selecionada.shapes)
                    if self.peca_selecionada in self.objetos:
                        self.objetos.remove(self.peca_selecionada)
                    del self.peca_selecionada
                    self.peca_selecionada = None
                    return
                
                if evento.key == pygame.K_SPACE:
                    if self.peca_selecionada:
                        if isinstance(self.peca_selecionada, Pseudo_Pino):
                            return
                        self.peca_selecionada.toggle_categoria()

                # se +
                if evento.key == pygame.K_KP_PLUS:
                    self.parametros_editaveis["escala"] = clamp(self.parametros_editaveis["escala"] + 10, *self.limites_parametros["escala"])
                    self.update_selected(rebuild = True)
                    return
                # se -
                if evento.key == pygame.K_KP_MINUS:
                    self.parametros_editaveis["escala"] = clamp(self.parametros_editaveis["escala"] - 10, *self.limites_parametros["escala"])
                    self.update_selected(rebuild = True)
                    return
                
                # g
                if evento.key == pygame.K_g:
                    self.grade_selecionada = (self.grade_selecionada + 1) % len(self.grade)
                    return
 
        else:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_s:
                    self.salvar_sala()
                    return

                

    def update_selected(self, rebuild = False):
        if self.peca_selecionada:
            # remove a peca selecionada do espaco
            self.space.remove(self.peca_selecionada.body, *self.peca_selecionada.shapes)
            if rebuild:
                peca_antiga = self.peca_selecionada
                # obtem a classe da peca selecionada para criar uma nova
                classe = self.peca_selecionada.__class__
                # se ele for instancia de Poligono:
                if isinstance(self.peca_selecionada, Poligono):
                    self.peca_selecionada = classe(pos = (self.parametros_editaveis["x"], self.parametros_editaveis["y"]), ID = self.get_ID(), space = self.space, escala= self.parametros_editaveis["escala"]/100)
                else:
                    self.peca_selecionada = classe(pos = (self.parametros_editaveis["x"], self.parametros_editaveis["y"]), ID = self.get_ID(), space = self.space)
                self.peca_selecionada.update_parametros(self.parametros_editaveis)
                if peca_antiga in self.objetos:
                    self.objetos.remove(peca_antiga)
            else:
                self.peca_selecionada.update_parametros(self.parametros_editaveis)
                self.space.add(self.peca_selecionada.body, *self.peca_selecionada.shapes)


    def salvar_sala(self, caminho = "save/salvo.txt"):
        print("salvando sala")
        with open(caminho, "w") as f:
            for objeto in self.objetos:
                if isinstance(objeto, pymunk.Segment):
                    continue
                
                for key, value in objeto.all_param.items():
                    if isinstance(value, pymunk.Vec2d):
                        objeto.all_param[key] = (value.x, value.y)
                f.write(f"{objeto.__class__.__module__}.{objeto.__class__.__name__} dict:" + str(objeto.all_param) + "\n")

    def carregar_sala(self, caminho):
        with open(caminho, "r") as f:
                for line in f:
                    line = line.strip()
                    if line == "":
                        continue

                    """
                    <ancora.Ancora object at 0x796d7a358470> dict:{'pos': (61, 157), 'ID': 0, 'escala': 1, 'angulo': 0, 'massa': 1, 'space': <pymunk.space.Space object at 0x796d7a3584d0>, 'elasticity': 0.3, 'friction': 1.0, 'color': (215, 111, 126, 1), 'categoria': 1, '__class__': <class 'ancora.Ancora'>}
                    <ancora.Ancora object at 0x796d7a3594f0> dict:{'pos': (47, 173), 'ID': 1, 'escala': 1, 'angulo': 0, 'massa': 1, 'space': <pymunk.space.Space object at 0x796d7a3584d0>, 'elasticity': 0.3, 'friction': 1.0, 'color': (226, 76, 153, 1), 'categoria': 1, '__class__': <class 'ancora.Ancora'>}
                    <pino.Pino object at 0x796d7acfdac0> dict:{'pos': Vec2d(289.0, 281.0), 'space': <pymunk.space.Space object at 0x796d7a3584d0>, 'ID': 3, 'body1': None, 'body2': None, 'parede': False}
                    
                    """
                    params_str = line.split("dict:")[1]
                    params_str = re.sub(r'<pymunk[^>]*>', '\'criar\'', params_str)
                    params = eval(params_str)
                    class_name = line.split(" ")[0]
                    module_name, class_name = class_name.split('.')
                    module = __import__(module_name)
                    class_ = getattr(module, class_name)
                    params["space"] = self.space
                    obj = class_(**params)
                    self.objetos.append(obj)
                

        self.cria_editor()
        # self.STATE = "simulacao"

    def render(self, screen):
        # if self.draw_options is None:
        #     self.draw_options = pymunk.pygame_util.DrawOptions(screen)
        # self.space.debug_draw(self.draw_options)
        
        # desenha grade
        if self.STATE == "edicao":
            if self.grade_selecionada > 0:
                for i in range(0, 800, self.grade[self.grade_selecionada]):
                    pygame.draw.line(screen, (50,50,50), (i,0), (i,800), 1)
                    pygame.draw.line(screen, (50,50,50), (0,i), (800,i), 1)



        for objeto in self.objetos:
            if isinstance(objeto, pymunk.Segment):
                pygame.draw.lines(screen, objeto.color, False, [objeto.a, objeto.b], 10)
            else:
                objeto.render(screen)
        # nova adicao
        
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
        self.parametros_editaveis_padrao = {"x": 100, "y": 100,"escala": 100, "largura": 10, "parede": False, "angulo": 0}
        self.parametros_editaveis = self.parametros_editaveis_padrao.copy()
        self.limites_parametros = {"x": (10,790), "y": (10,790), "escala": (50, 200), "largura": (10,500) ,"parede": (False, True), "angulo": (0, 360)}

        self.interface_editor.append(Botao(800-10-self.largura_botoes, 800-self.altura_botoes-10, self.largura_botoes, self.altura_botoes, "Executar", textSize = 32))

        self.posMouse = (0,0)
        self.grade = [1,10,50,100]
        self.grade_selecionada = 0

    def desenha_editor(self, screen):
        # desenha retangulo cinza e largura 2
        pygame.draw.rect(screen, (100,100,100), (0,0,self.largura_botoes+20,(self.altura_botoes+10)*(len(self.interface_editor)-1)+10), 2)
        for interface in self.interface_editor:
            interface.render(screen)

        if self.peca_selecionada:
            self.peca_selecionada.render(screen)

        # escreve a posicao do mouse no canto inferior direito na cor branca
        font = pygame.font.Font(None, 24)
        text = font.render(f"({self.posMouse[0]}, {self.posMouse[1]})", True, (255,255,255))
        screen.blit(text, (800-10-text.get_width(), 10))