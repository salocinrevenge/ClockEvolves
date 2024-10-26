import numpy as np
from poligono import Poligono

class Viga(Poligono):
    def __init__(self, pos: np.ndarray, comprimento = 100, largura = 10, massa = 1, elasticity = 0.3, friction = 1.0, space = None, color = (255,255,255,1), categoria = 1) -> None: # largura padrao é 10
        self.pontos = np.array([[-comprimento//2,-largura//2],[comprimento//2,-largura//2],[comprimento//2,largura//2],[-comprimento//2,largura//2]])
        self.comprimento = comprimento
        self.largura = largura
        self.massa = massa
        self.elasticity = elasticity
        self.friction = friction
        self.color = color
        super().__init__(self.pontos.tolist(), pos = pos, massa = massa, elasticity = elasticity, friction = friction, color = color, space = space,categoria=categoria)