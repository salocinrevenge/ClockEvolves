import numpy as np
from poligono import Poligono

class Ancora(Poligono):
    def __init__(self, pos: np.ndarray, escala = 1, angulo = 0, massa = 1, space = None, elasticity = 0.3, friction = 1.0, color = None, categoria = 1) -> None:
        pontos = np.array([[0.0,-5.0],[50.0,45.0],[40.0,55.0],[40.0,45.0],[0.0,15.0], [-40.0,45.0], [-40.0,55.0], [-50.0,45.0]])
        pontos *= escala
        super().__init__(pontos.tolist(), pos = pos, massa = massa, elasticity = elasticity, friction = friction, color = color, space = space, categoria = categoria, meta_info = {"tipo":"ancora"})
        
