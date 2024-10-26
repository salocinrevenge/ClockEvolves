import pygame
from botao import Botao
from sala import Sala

class Menu():
    def __init__(self) -> None:
        self.criaBotoesMenuPrincipal()
        self.criaBotoesMenuCriar()
        self.STATE = "Menu"
        self.sala = None

        # remova para voltar menu
        self.criarSala()


    def tick(self, dt):
        if self.STATE == "Sala":
            self.sala.tick(dt)

    def render(self, screen):
        if self.STATE == "Menu":
            for botao in self.botoesMenuPrincipal:
                botao.render(screen)
        if self.STATE == "Criar Sala":
            for botao in self.botoesMenuCriar:
                botao.render(screen)
        if self.STATE == "Sala":
            self.sala.render(screen)
        
    def criarSala(self, config = "Aleatorizar"):
        self.STATE = "Sala"
        if config == "Aleatorizar":
            self.sala = Sala()
        else:
            self.sala = Sala(editor=True)

    def criaBotoesMenuPrincipal(self):
        self.botoesMenuPrincipal = []
        self.botoesMenuPrincipal.append(Botao(100, 100, 600, 150, "Criar Sala", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(100, 300, 600, 150, "Carregar Sala", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(100, 500, 600, 150, "Configurações", textSize = 72))

    def criaBotoesMenuCriar(self):
        self.botoesMenuCriar = []
        self.botoesMenuCriar.append(Botao(250, 500, 300, 100, "Aleatorizar", textSize = 72))
        self.botoesMenuCriar.append(Botao(250, 650, 300, 100, "Criar", textSize = 72))

    def input(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.STATE == "Menu":
                for botao in self.botoesMenuPrincipal:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        print(clique)
                        if clique == "Criar Sala":
                            self.STATE = clique
                            return
            if self.STATE == "Criar Sala":
                for botao in self.botoesMenuCriar:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        print(clique)
                        self.criarSala(config = clique)
                        return
        if self.STATE == "Sala":
            self.sala.input(evento)