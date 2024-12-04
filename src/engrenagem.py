import numpy as np
from poligono import Poligono
from algebra import rotaciona

class Engrenagem(Poligono):
    def __init__(self, pos: tuple, raio = 64, dentes = None, massa = 1, space = None, elasticity = 0.6, friction = 0.0, color = None, angulo = 0, categoria = 1, escala = 1, tamanho_dente = 10) -> None:
        raio = int(raio*escala)

        circunferencia = 2*np.pi*raio
        ndentes = int(circunferencia//(tamanho_dente*2)) # *2 para considerar o espaço entre os dentes
        
        if ndentes < 4:
            raise ValueError("engrenagem deve ter no mínimo 4 dentes, tamanho muito pequeno")

        novo_raio = ndentes*tamanho_dente/np.pi

        if dentes is None:
            print(f"Dentes não especificados, criando engrenagem com {ndentes} dentes e raio {novo_raio}")
            dentes = ndentes
            raio = novo_raio
        pontos = self.get_points(raio, dentes, angulo, tamanho_dente*1.5)
        super().__init__(pontos, pos = pos, massa = massa, elasticity = elasticity, friction = friction, color = color, space = space, categoria = categoria, meta_info = {"tipo":"engrenagem"}, escala=1)

    def get_points(self, raio, dentes, angulo, altura_dente):
        # um poligono com 20 pontos é equivalente a uma circunferencia
        pontos = []
        lados = dentes*5
        # lados = dentes*3

        for i in range(lados):
            angulo = 2*np.pi*i/lados
            acrecimo = 0
            if i % 5 == 0 or i % 5 == 1:
            # if i % 3 == 0:
                acrecimo = altura_dente
            x = float((raio+acrecimo)*np.cos(angulo))
            y = float((raio+acrecimo)*np.sin(angulo))
            pontos.append((x,y))
        pontos = np.array(pontos)
        pontos = pontos @ rotaciona(angulo)
        pontos = pontos.tolist()
        return pontos