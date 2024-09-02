from parede import Parede
from engrenagem import Engrenagem
from ancora import Ancora
from viga import Viga
import numpy as np
from botao import Botao
import pygame

class Terremoto():

    def __init__(self) -> None:
        self.debug = False

    def inicializaAleatorio(self):
        self.parede = Parede()
        # self.parede.objetos.append(Engrenagem(np.array([300.,300.]), 10, velocidade=np.array([1.,1.]), massa=1))
        # self.parede.objetos.append(Engrenagem(np.array([500.,300.]), 10, velocidade=np.array([-1.,1.]), massa=1))
        # self.parede.objetos.append(Engrenagem(np.array([550.,250.]), 10, velocidade=np.array([-4.,4.]), massa=1))
        # self.parede.objetos.append(Engrenagem(np.array([200.,300.]), 10, velocidade=np.array([1.,1.]), massa=1))
        # self.parede.objetos.append(Engrenagem(np.array([100.,300.]), 10, velocidade=np.array([-1.,1.]), massa=1))
        # self.parede.objetos.append(Engrenagem(np.array([650.,250.]), 10, velocidade=np.array([-4.,4.]), massa=1))
        # self.parede.objetos.append(Engrenagem(np.array([400.,400.]), 10))
        # self.parede.objetos.append(Engrenagem(np.array([450.,600.]), 10))

        # self.parede.objetos.append(Engrenagem(np.array([300.,410.]), 10))
        # self.parede.objetos.append(Engrenagem(np.array([350.,450.]), 10))
        # self.parede.objetos.append(Engrenagem(np.array([450.,50.]), 10, velocidade=np.array([1.,4.]), massa=1))
        # self.parede.objetos.append(Engrenagem(np.array([500.,200.]), 10, velocidade=np.array([1.,1.]), massa=1))

        # self.parede.objetos.append(Viga(np.array([100.,200.]), 100, 10, velocidade=np.array([1.,-3.]),velocidadeAngular=0.1, massa=1))
        self.parede.objetos.append(Ancora(np.array([392.0, 311.0]), escala=1))
        self.parede.objetos.append(Ancora(np.array([390.0, 279.0]), escala=1))
        
        return self.parede
    
    def criarSalaVazia(self):
        self.parede = Parede()
        return self.parede
    
    def editar(self):
        self.botoes = []
        self.botoes.append(Botao(10, 100, 140, 20, "M para ocultar", textSize = 24))
        self.botoes.append(Botao(20, 130, 120, 20, "Viga", textSize = 24))
        self.botoes.append(Botao(20, 160, 120, 20, "Engrenagem", textSize = 24))
        self.botoes.append(Botao(20, 190, 120, 20, "Ancora", textSize = 24))
        self.botoes.append(Botao(340, 700, 120, 40, "Iniciar", textSize = 36))
        self.estados = {"menu": True}
        self.pecaSelecionada = None
        return self.parede
    
    def input(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # ver se é o botão esquierdo
            if evento.button == 1:
                if self.pecaSelecionada is not None:
                    self.parede.objetos.append(self.pecaSelecionada)
                    self.pecaSelecionada = None
                    return
                if self.estados["menu"]:
                    for botao in self.botoes:
                        clique = botao.identificaClique(evento.pos)
                        if clique:
                            print(clique)
                            if clique == "M para ocultar":
                                self.estados["menu"] = not self.estados["menu"]
                            if clique == "Viga":
                                self.pecaSelecionada = Viga(np.array([evento.pos[0], evento.pos[1]]))
                            if clique == "Engrenagem":
                                self.pecaSelecionada = Engrenagem(np.array([evento.pos[0], evento.pos[1]]))
                            if clique == "Ancora":
                                self.pecaSelecionada = Ancora(np.array([evento.pos[0], evento.pos[1]]), escala=1)
                            if clique == "Iniciar":
                                return "Iniciar"
            if evento.button == 3:
                self.pecaSelecionada = None
                    
        # se apertar a tecla M, oculta o menu
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                self.estados["menu"] = not self.estados["menu"]

    def render(self, screen):
        self.parede.render(screen)
        if self.estados["menu"]:
            for botao in self.botoes:
                botao.render(screen)
        if self.pecaSelecionada is not None:
            self.pecaSelecionada.render(screen)

    def tick(self):
        if self.pecaSelecionada is not None:
            self.pecaSelecionada.posicao = np.array(pygame.mouse.get_pos()).astype(float)
            self.pecaSelecionada.tick()
            self.parede.teste_coolisao(self.pecaSelecionada)
