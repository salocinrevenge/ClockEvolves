import pygame
from parede import Parede
from terremoto import Terremoto

class Sala():
    def __init__(self, config = "Aleatorizar") -> None:
        self.paredes = []
        self.estado = config
        self.terremoto = Terremoto()

    def organizar(self):
        if self.estado == "Aleatorizar":
            self.paredes.append(self.terremoto.inicializaAleatorio())
            self.estado = "Simular"
        if self.estado == "Criar":
            self.paredes.append(self.terremoto.criarSalaVazia())
            self.terremoto.editar()
            self.estado = "Criando"

    def tick(self):
        self.organizar()
        if self.estado == "Simular":
            for parede in self.paredes:
                parede.tick()
        if self.estado == "Criando":
            self.terremoto.tick()


    def input(self, evento):
        if self.estado == "Criando":
            resposta = self.terremoto.input(evento)
            if resposta == "Iniciar":
                print("Iniciar simulacao")
                self.estado = "Simular"
        # testa se evento eh pressioanr tecla D
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_d:
                for parede in self.paredes:
                    for objeto in parede.objetos:
                        objeto.debug = not objeto.debug

    def render(self, screen):
        # desenha a borda da sala
        pygame.draw.rect(screen, (255, 60, 60), pygame.Rect(0, 0, 800, 800), 2)
        if self.estado == "Criando":
            self.terremoto.render(screen)
        if self.estado == "Simular":
            for parede in self.paredes:
                parede.render(screen)