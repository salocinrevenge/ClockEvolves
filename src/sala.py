import pygame
from parede import Parede

class Sala():
    def __init__(self) -> None:
        self.paredes = []
        self.estado = "Criar"

    def organizar(self):
        if self.estado == "Criar":
            self.paredes.append(Parede())
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