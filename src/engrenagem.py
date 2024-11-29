import numpy as np
from poligono import Poligono
from algebra import rotaciona

class Engrenagem(Poligono):
    def __init__(self, pos: tuple, raio = 32, dentes = None, massa = 1, space = None, elasticity = 0.3, friction = 0.0, color = None, angulo = 0, categoria = 1, escala = 1) -> None:
        raio = int(raio*escala)
        if raio < 16:
            raise ValueError("raio de engrenagem deve ser no mínimo 16")
        if dentes is None:
            dentes = int(raio/4)
        pontos = self.get_points(raio, dentes, angulo)
        super().__init__(pontos, pos = pos, massa = massa, elasticity = elasticity, friction = friction, color = color, space = space, categoria = categoria, meta_info = {"tipo":"engrenagem"}, escala=escala)

    def get_points(self, raio, dentes, angulo):
        # um poligono com 20 pontos é equivalente a uma circunferencia
        pontos = []
        lados = dentes*5
        # lados = dentes*3

        for i in range(lados):
            angulo = 2*np.pi*i/lados
            mutiplier = 1
            if i % 5 == 0 or i % 5 == 1:
            # if i % 3 == 0:
                mutiplier = 1.5
            x = float(raio*mutiplier*np.cos(angulo))
            y = float(raio*mutiplier*np.sin(angulo))
            pontos.append((x,y))
        pontos = np.array(pontos)
        pontos = pontos @ rotaciona(angulo)
        pontos = pontos.tolist()
        return pontos