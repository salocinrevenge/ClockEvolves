import pygame
from parede import Parede
from terremoto import Terremoto

class Sala():
    def __init__(self) -> None:
        self.paredes = []
        self.estado = "Criar"
        self.terremoto = Terremoto()

    def organizar(self):
        if self.estado == "Criar":
            self.paredes.append(self.terremoto.inicializaAleatorio())
            self.estado = "Simular"

    def tick(self):
        self.organizar()
        for parede in self.paredes:
            parede.tick()

    def input(self, evento):
        pass

    def render(self, screen):
        # desenha a borda da sala
        pygame.draw.rect(screen, (255, 60, 60), pygame.Rect(0, 0, 800, 800), 2)
        for parede in self.paredes:
            parede.render(screen)