import numpy as np
from poligono import Poligono

class Viga(Poligono):
    def __init__(self, pos: np.ndarray, comprimento = 100, largura = 100, escala = 1, velocidade = None, velocidadeAngular = 0, angulo = 0, massa = 1) -> None: # largura padrao é 10
        pontos = np.array([[-comprimento//2,-largura//2],[comprimento//2,-largura//2],[comprimento//2,largura//2],[-comprimento//2,largura//2]])
        pontos *= escala
        super().__init__(pontos)
        self.posicao = pos
        self.velocidade = velocidade
        if velocidade is None:
            self.velocidade = np.zeros(2)
        self.velocidadeAngular = velocidadeAngular
        self.angulo = angulo
        self.massa = massa
        self.comprimento = comprimento
        self.largura = largura
        self.inercia = self.massa*(self.comprimento**2 + self.largura**2)/12


    def tick(self):
        super().tick()

        