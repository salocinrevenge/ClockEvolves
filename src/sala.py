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
from utils import hash
import random
import time

class Sala():
    def __init__(self, editor = False, carregar = None, pais = None, percents = None, n_mut = None, taxa_mut = None, aleatorio = False, tipo_hash = "repeat") -> None:
        """
        
        
        tipo_hash = "local" / "global" / "repeat"
        """

        self.ID = 0

        self.space = pymunk.Space()
        self.space.gravity = 0.0, 1000.0
        self.dim = (800, 800)

        self.parametros_editaveis_padrao = {"x": 100, "y": 100,"escala": 100, "largura": 10, "parede": False, "angulo": 0, "orientation": 0}
        self.limites_parametros = {"x": (10,790), "y": (10,790), "escala": (50, 200), "largura": (10,500) ,"parede": (False, True), "angulo": (0, 360), "orientation": (-0.3, 0.3)}

        self.debug = False
        self.STATE = "edicao"
        self.objetos = []
        if carregar:
            self.carregar_sala(carregar)
            self.STATE = "simulacao"
        if editor:
            self.cria_editor()
        elif pais:
            self.cruzar(pais, percents, n_mut, taxa_mut)
            self.STATE = "simulacao"
        elif aleatorio:
            self.STATE = "simulacao"

            self.criar_aleatorio()

            # self.objetos.append(Engrenagem(pos = (301.0, 311.0), ID = self.get_ID(), space = self.space, raio = 20, massa=10, categoria=1))
            # a = Engrenagem(pos = (192.0, 511.0), ID = self.get_ID(), space = self.space,categoria=2)
            # self.objetos.append(a)

            # self.objetos.append(Ancora(pos = (92.0, 211.0), ID = self.get_ID(), space = self.space, massa=4, escala=0.75, categoria=2))
            # self.objetos.append(Ancora(pos = (92.0, 311.0), ID = self.get_ID(), space = self.space, massa=4, categoria=2))

            # b = Viga(pos = (192.0, 521.0), ID = self.get_ID(), space = self.space, massa=2, categoria=1)
            # self.objetos.append(b)

            # self.objetos.append(Pino(body1= a.body, ID = self.get_ID(), body2= b.body, pos = (192.0, 521.0), space = self.space))
            # self.objetos.append(Pino(body1= a.body, ID = self.get_ID(), body2= b.body, pos = (195.0, 524.0), space = self.space))
            
            # engre = Engrenagem(pos = (392.0, 521.0), ID = self.get_ID(), space = self.space, raio = 50, friction=0, elasticity=0, categoria=1)
            # self.objetos.append(engre)
            # self.objetos.append(Pino(body1= engre.body, ID = self.get_ID(), body2= (392.0, 521.0), pos = (392.0, 521.0), space = self.space))

            # roda = Engrenagem(pos = (535.0, 531.0), ID = self.get_ID(), space = self.space, raio = 50, friction=0, elasticity=0, categoria=1)
            # self.objetos.append(roda)
            # self.objetos.append(Pino(body1= roda.body, ID = self.get_ID(), body2= (535.0, 531.0), pos = (535.0, 531.0), space = self.space))

            

            # # # vigas conectadas
            # self.objetos.append(Viga(pos = (100.0, 171.0), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            # self.objetos.append(Viga(pos = (120.0, 181.0), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=1))
            # self.objetos.append(Viga(pos = (100.0, 201.0), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            # self.objetos.append(Viga(pos = (80.0, 191.0), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            # self.objetos.append(Pino(pos = (100.0, 181.0), ID = self.get_ID(), space = self.space, parede=True))

            
            # self.objetos.append(Viga(pos = (100.0, 171.0+200), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            # self.objetos.append(Viga(pos = (120.0, 181.0+200), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=1))
            # self.objetos.append(Viga(pos = (100.0, 201.0+200), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=1))
            # self.objetos.append(Viga(pos = (80.0, 191.0+200), ID = self.get_ID(), space = self.space, massa=2, largura=100, comprimento=100, categoria=2))
            # self.objetos.append(Pino(pos = (100.0, 181.0+200), ID = self.get_ID(), space = self.space, parede=False))

        self.build_border()

        # ordena os objetos com base nas categorias se ele possuir categoria, se não, ele vai por ultimo

        self.objetos.sort(key = lambda x: x.categoria if hasattr(x, "categoria") else 3)
        self.estados = dict()
        self.numero_estados_sem_repetir = 0
        self.repetiu = False
        self.contador_debug = 0
        self.times = dict()
        self.tipo_hash = tipo_hash
        self.pontos = 0

    def criar_aleatorio(self):

        need_create = {"engrenagem": 9, "ancora": 3, "viga": 6, "pino": 30}
        need_create = {"engrenagem": 0, "ancora": 0, "viga": 1, "pino": 0}
        for tipo, quantidade in need_create.items():
            for _ in range(quantidade):
                x = random.uniform(0+50, 800-50)
                y = random.uniform(0+50, 800-50)
                if tipo == "pino":
                    if random.random() < 0.3:
                        parede = True
                    else:
                        parede = False
                    self.objetos.append(Pino(pos=(x, y), ID=self.get_ID(), space=self.space, parede=parede))
                else:
                    rotacao = random.uniform(0, 360)
                    escala = random.triangular(0.50, 1.50, 0.50)
                    categoria = random.randint(1, 2)
                    if tipo == "engrenagem":
                        orientation = random.triangular(-0.6, 0.6, 0)/2
                        orientation = round(orientation, 1)
                        self.objetos.append(Engrenagem(pos=(x, y), ID=self.get_ID(), space=self.space, angulo=rotacao, orientation=orientation, escala=escala, categoria=categoria))
                    elif tipo == "ancora":
                        self.objetos.append(Ancora(pos=(x, y), ID=self.get_ID(), space=self.space, angulo=rotacao, escala=escala, categoria=categoria))
                    elif tipo == "viga":
                        self.objetos.append(Viga(pos=(x, y), ID=self.get_ID(), space=self.space, angulo=rotacao, escala=escala, categoria=categoria))

    def cruzar(self, pais, percents = None, n_mut = None, taxa_mut = None):
        print("Cruzando salas")
        if percents is None:
            percents = [1]
        if n_mut is None:
            n_mut = 1
        if taxa_mut is None:
            taxa_mut = 0.1
        novos_parametros_objetos = []
        for i in range(len(pais[0].objetos)):
            valor_prob = random.random() # gera um numero entre 0 e 1
            j = 0
            for p in percents:
                valor_prob -= p
                if valor_prob <= 0:
                    break
                j += 1
            if hasattr(pais[j].objetos[i], "all_param"):
                novos_parametros_objetos.append(pais[j].objetos[i].all_param.copy())
                # define tipo como nome da classe
                novos_parametros_objetos[-1]["tipo"] = pais[j].objetos[i].__class__.__name__

        # gera um vetor de 0 a len(novo_objetos)
        indices = list(range(len(novos_parametros_objetos)))
        random.shuffle(indices)
        for i in range(n_mut):
            # print("mutando objeto: ", novos_parametros_objetos[indices[i]]["tipo"])
            self.mutar(novos_parametros_objetos[indices[i]], taxa_mut)
        
        novos_objetos = []
        # recriar todos os objetos com base nos novos parametros e adicionar eles ao space atual
        for objeto in novos_parametros_objetos:
            objeto["space"] = self.space
            # cria o objeto com esses parametros e o adiciona ao space
            if objeto["tipo"] == "Pino":
                del objeto["tipo"]
                novos_objetos.append(Pino(**objeto))
            elif objeto["tipo"] == "Engrenagem":
                # remove "tipo" de objeto
                del objeto["tipo"]
                novos_objetos.append(Engrenagem(**objeto))
            elif objeto["tipo"] == "Ancora":
                del objeto["tipo"]
                novos_objetos.append(Ancora(**objeto))
            elif objeto["tipo"] == "Viga":
                del objeto["tipo"]
                novos_objetos.append(Viga(**objeto))

        self.objetos = novos_objetos

    def mutar(self, objeto, taxa):
        # escolhe um parametro pra alterar
        parametros_a_alterar = ("pos", "angulo", "escala", "orientation", "parede", "categoria")
        while True:
            param = random.choice(list(objeto.keys()))
            if param in parametros_a_alterar:
                break
        # print("param: ", param)
        match param:
            case "escala":
                objeto[param] *= random.uniform(1-taxa, 1+taxa)
                mini, maxi = self.limites_parametros["escala"]
                objeto[param] = clamp(objeto[param], mini/100, maxi/100)
            case "pos":
                a = [0, 0]
                for i in range(2):
                    a[i] = objeto[param][i] * random.uniform(1-taxa*100, 1+taxa*100)
                    a[i] = clamp(a[i], 0+50, 800-50)
                objeto[param] = tuple(a)
            case "orientation":
                objeto[param] *= random.uniform(1-taxa, 1+taxa)
                objeto[param] = clamp(objeto[param], -0.6, 0.6)
            case "parede":
                objeto[param] = not objeto[param]
            case "categoria":
                objeto[param] = 3-objeto[param]
            case "angulo":
                objeto[param] *= random.uniform(1-taxa, 1+taxa)
                objeto[param] = clamp(objeto[param], 0, 360)

    def get_ID(self):
        self.ID+=1
        return self.ID-1

    def build_border(self):
        positions = [((0,800), (800,800)), ((0,0), (0,800)), ((800,0), (800,800)), ((0,0), (800,0))]
        elasticity = [0.3, 0.95, 0.95, 0.95]
        elasticity = [0, 0.95, 0.95, 0.95]
        friction = [1.8, 0.95, 0.95, 0.95]
        friction = [100,100,100,100]
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
        if self.debug:
            if self.contador_debug == 0:
                self.times = dict()
            self.contador_debug += 1
            if self.contador_debug == 1000:
                self.contador_debug = 0

        if self.STATE == "simulacao" and not self.repetiu:
            self.numero_estados_sem_repetir += 1
            continuar = False
            if self.debug:  # marcar tempo
                if "simulacao" not in self.times:
                    self.times["simulacao"] = 0
                tempo = time.perf_counter()
                continuar = True
            self.space.step(dt)
            if self.debug and continuar: # marcar tempo
                self.times["simulacao"] += (time.perf_counter() - tempo)
                if "atualizar_estados" not in self.times:
                    self.times["atualizar_estados"] = 0
                tempo = time.perf_counter()

            self.atualiza_estados()

            if self.debug and continuar:
                self.times["atualizar_estados"] += (time.perf_counter() - tempo)

        elif self.STATE == "edicao":
            pass
 
    def pontuar(self, a, b, c): #  atual, anterior, preanterior
        return max(b-c-abs(a-b-(b-c)), 0)

    def atualiza_estados(self):

        if self.tipo_hash == "global":
            objetos, hash_value = hash(self.get_current_objects())

            if hash_value not in self.estados:
                self.estados[hash_value] = []
            
            if objetos in self.estados[hash_value]:
                print("Estado ja existe: ", hash_value, "score da simulacao: ", self.numero_estados_sem_repetir)
                self.repetiu = True
                self.pontos = self.numero_estados_sem_repetir
                return
            self.estados[hash_value].append(objetos)
        elif self.tipo_hash == "local":
            # se ainda n tem pecas_repetiram criar atributo disso
            if not hasattr(self, "pecas_repetiram"):
                self.pecas_repetiram = []
                for i in range(len(self.get_current_objects())):
                    self.pecas_repetiram.append(False)
            todos_repetiram = True
            for i, obj in enumerate(self.get_current_objects()):
                if self.pecas_repetiram[i]:
                    continue
                objetos, hash_value = hash([obj])
                if i not in self.estados:
                    self.estados[i] = dict()
                if hash_value not in self.estados[i]:
                    self.estados[i][hash_value] = []

                if objetos in self.estados[i][hash_value]:
                    # print("Estado ja existe: ", hash_value, "score da peca: ", self.numero_estados_sem_repetir, "tipo da peca: ", obj)
                    self.pecas_repetiram[i] = True
                    continue
                todos_repetiram = False
                self.estados[i][hash_value].append(objetos)
            if todos_repetiram:
                self.repetiu = True
                self.pontos = self.numero_estados_sem_repetir
                
        elif self.tipo_hash == "repeat":
            # se ainda n tem pecas_repetiram criar atributo disso
            objetos_atualmente = self.get_current_objects()
            objetos, hash_value_geral = hash(objetos_atualmente)

            if hash_value_geral not in self.estados:
                self.estados[hash_value_geral] = []
            
            if objetos in self.estados[hash_value_geral]:
                print("Estado ja existe: ", hash_value_geral, "numero de estados da simulacao: ", self.numero_estados_sem_repetir)
                self.repetiu = True
                for i in range(len(objetos_atualmente)):
                    self.pontos = max(self.pontos, self.tempos_pecas[i][0])
                self.pontos+= self.numero_estados_sem_repetir
                print("Pontos: ", self.pontos)
                return
            self.estados[hash_value_geral].append(objetos.copy())
            # print(len(self.estados[hash_value_geral]))
            # if len(self.estados[hash_value_geral]) > 3:
                # print(self.estados[hash_value_geral][-4], self.estados[hash_value_geral][-3], self.estados[hash_value_geral][-2], self.estados[hash_value_geral][-1], objetos)


            if not hasattr(self, "tempos_pecas"):   # cria um dicionario para cada peça
                self.tempos_pecas = []
                for i in range(len(objetos_atualmente)):
                    self.tempos_pecas.append([0,dict()])    # pontos, dicionario
            for i, obj in enumerate(objetos_atualmente):    # atualiza o estado atual de cada peça
                objetos, hash_value = hash([obj])
                if hash_value not in self.tempos_pecas[i][1]:
                    self.tempos_pecas[i][1][hash_value] = [[],[]] # objetos 
                try: # procurar os objetos na lista, se não existir, adicionar
                    index = self.tempos_pecas[i][1][hash_value][0].index(objetos)
                except: 
                    self.tempos_pecas[i][1][hash_value][0].append(objetos)
                    self.tempos_pecas[i][1][hash_value][1].append([0,0])
                    index = -1
                self.tempos_pecas[i][1][hash_value][1][index].append(self.numero_estados_sem_repetir)
                self.tempos_pecas[i][0] += self.pontuar(self.tempos_pecas[i][1][hash_value][1][index][-1], self.tempos_pecas[i][1][hash_value][1][index][-2], self.tempos_pecas[i][1][hash_value][1][index][-3])

                

                
        else:
            raise ValueError("Tipo de hash invalido")


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
                if evento.key == pygame.K_BACKSPACE:
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
                
                # se o
                if evento.key == pygame.K_o:
                    print("o: ", self.parametros_editaveis["orientation"])
                    self.parametros_editaveis["orientation"] = clamp(self.parametros_editaveis["orientation"] + 0.05, *self.limites_parametros["orientation"])
                    print("o depois: ", self.parametros_editaveis["orientation"])
                    self.update_selected(rebuild = True)
                    return
                # se i
                if evento.key == pygame.K_i:
                    print("o: ", self.parametros_editaveis["orientation"])
                    self.parametros_editaveis["orientation"] = clamp(self.parametros_editaveis["orientation"] - 0.05, *self.limites_parametros["orientation"])
                    print("o depois: ", self.parametros_editaveis["orientation"])
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

                if evento.key == pygame.K_c:
                    print(hash(self.get_current_objects()))
                    return

                if evento.key == pygame.K_v:
                    print("Estados: ", self.estados)
                    return
                
                if evento.key == pygame.K_o:
                    for objeto in self.objetos:
                        if hasattr(objeto, "all_param"):
                            print(type(objeto), objeto.all_param)
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
                    if isinstance(self.peca_selecionada, Engrenagem):
                        self.peca_selecionada = classe(pos = (self.parametros_editaveis["x"], self.parametros_editaveis["y"]), ID = self.get_ID(), space = self.space, escala= self.parametros_editaveis["escala"]/100, orientation = self.parametros_editaveis["orientation"])
                    else:
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


        if self.debug:
            if "render" not in self.times:
                self.times["render"] = 0
            tempo = time.perf_counter()
        for objeto in self.objetos:
            if isinstance(objeto, pymunk.Segment):
                pygame.draw.lines(screen, objeto.color, False, [objeto.a, objeto.b], 10)
            else:
                objeto.render(screen)
        # nova adicao
        if self.debug:
            try:
                self.times["render"] += (time.perf_counter() - tempo)
            except:
                pass

            # desenha um grafico de pizza no canto inferior direito, mostrando cada tempo gasto
            total_time = sum(self.times.values())
            if total_time > 0:
                for i, (key, value) in enumerate(self.times.items()):
                    pygame.draw.rect(screen, (255, 0, 0), (800 - 100, 600 - 100 + i * 20, 80, 10))
                    pygame.draw.rect(screen, (0, 255, 0), (800 - 100, 600 - 100 + i * 20, 80 * (value / total_time), 10))
                    font = pygame.font.Font(None, 12)
                    text = font.render(f"{key}: {(value / total_time):.2f}%", True, (255, 255, 255))
                    screen.blit(text, (800 - 100, 600 - 100 + i * 20))

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
        self.parametros_editaveis = self.parametros_editaveis_padrao.copy()

        self.interface_editor.append(Botao(800-10-self.largura_botoes, 800-self.altura_botoes-10, self.largura_botoes, self.altura_botoes, "Executar", textSize = 32))

        self.posMouse = (0,0)
        self.grade = [1,10,50,100]
        self.grade_selecionada = 0

    def get_current_objects(self):
        objects_info = []
        for obj in self.objetos:
            if obj.__class__.__name__ == "Segment":
                continue
            if hasattr(obj, 'body'):
                info = {
                    'name': obj.__class__.__name__,
                    'position': obj.body.position,
                    'rotation': obj.shapes[0].body.angle,
                    'linear_velocity': obj.body.velocity,
                    'angular_velocity': obj.body.angular_velocity
                }

                objects_info.append(info)
        return objects_info

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