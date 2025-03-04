import numpy as np
from poligono import Poligono
import algebra

class Ancora(Poligono):
    def __init__(self, pos: np.ndarray, ID, escala = 1, angulo = 0, massa = 1, space = None, elasticity = 0.3, friction = 1.0, color = None, categoria = 1) -> None:
        self.all_param = {k: v for k, v in locals().items() if k not in ('self', '__class__')}
        pontos = np.array([[0.0,-5.0],[50.0,45.0],[40.0,55.0],[40.0,45.0],[0.0,15.0], [-40.0,45.0], [-40.0,55.0], [-50.0,45.0]])
        pontos *= escala
        pontos = pontos @ algebra.rotaciona(-angulo)
        super().__init__(pontos.tolist(), pos = pos, ID = ID, massa = massa, elasticity = elasticity, friction = friction, color = color, space = space, categoria = categoria, meta_info = {"tipo":"ancora"}, escala=escala)
        
