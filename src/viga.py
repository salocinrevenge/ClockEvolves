import numpy as np
from poligono import Poligono
import algebra

class Viga(Poligono):
    def __init__(self, pos: np.ndarray, ID, comprimento = 200, largura = 10, massa = 1, elasticity = 0.3, friction = 1.0, space = None, color = None, angulo = 0, categoria = 1, escala=1) -> None: # largura padrao é 10
        self.all_param = {k: v for k, v in locals().items() if k not in ('self', '__class__')}
        self.pontos = np.array([[-comprimento//2,-largura//2],[comprimento//2,-largura//2],[comprimento//2,largura//2],[-comprimento//2,largura//2]])
        self.pontos = self.pontos @ algebra.rotaciona(-angulo)
        self.comprimento = comprimento
        self.largura = largura
        self.massa = massa
        self.elasticity = elasticity
        self.friction = friction
        super().__init__(self.pontos.tolist(), pos = pos, ID = ID, massa = massa, elasticity = elasticity, friction = friction, color = color, space = space,categoria=categoria, meta_info = {"tipo":"viga"}, escala=escala)