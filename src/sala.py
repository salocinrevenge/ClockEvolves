import pygame

class Sala():
    def __init__(self) -> None:
        self.paredes = []

    def organizar(self):
        pass

    def tick(self):
        pass

    def input(self, evento):
        pass

    def render(self, screen):
        # desenha a borda da sala
        pygame.draw.rect(screen, (255, 60, 60), pygame.Rect(0, 0, 800, 800), 2)