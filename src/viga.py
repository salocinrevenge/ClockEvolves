import numpy as np
from poligono import Poligono
import pymunk

class Viga(Poligono):
    def __init__(self, pos: np.ndarray, comprimento = 100, largura = 10, escala = 1, velocidade = None, velocidadeAngular = 0, angulo = 0, massa = 1, elasticity = 0.3, friction = 1.0, space = None, color = (255,255,255,1)) -> None: # largura padrao é 10
        pontos = np.array([[-comprimento//2,-largura//2],[comprimento//2,-largura//2],[comprimento//2,largura//2],[-comprimento//2,largura//2]])
        pontos *= escala
        super().__init__(pontos.tolist(), pos = pos, massa = massa, elasticity = elasticity, friction = friction, color = color, space = space)
        