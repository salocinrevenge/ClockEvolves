import numpy as np
from poligono import Poligono
from algebra import rotaciona

class Engrenagem(Poligono):
    def __init__(self, ID, pos: tuple, raio = 64, dentes = None, massa = 1, space = None, elasticity = 0.6, friction = 0.0, color = None, angulo = 0, categoria = 1, escala = 1, tamanho_dente = 10, orientation = 0) -> None:
        # salva todos os parametros em um dicionario
        self.all_param = {k: v for k, v in locals().items() if k not in ('self', '__class__')}
        epsilon = 1e-6
        if abs(orientation) < epsilon:
            orientation = 0
            self.all_param["orientation"] = 0
        print(self.all_param)
        raio = int(raio*escala)

        circunferencia = 2*np.pi*raio
        ndentes = int(circunferencia//(tamanho_dente*2)) # *2 para considerar o espaço entre os dentes
        
        if ndentes < 4:
            raise ValueError("engrenagem deve ter no mínimo 4 dentes, tamanho muito pequeno")

        novo_raio = ndentes*tamanho_dente/np.pi

        if dentes is None:
            dentes = ndentes
            raio = novo_raio
        pontos = self.get_points(raio, dentes, tamanho_dente*1.5, orientation)
        pontos = (pontos @ rotaciona(-angulo)).tolist()
        super().__init__(pontos, pos = pos, ID = ID, massa = massa, elasticity = elasticity, friction = friction, color = color, space = space, categoria = categoria, meta_info = {"tipo":"engrenagem"}, escala=1)
        # self.update_parametros({"angulo": angulo, "x": pos[0], "y": pos[1]})

    def get_points(self, raio, dentes, altura_dente, orientation):
        # um poligono com 20 pontos é equivalente a uma circunferencia
        pontos = []

        if orientation == 0:
            lados = dentes*5
        else:
            lados = dentes*7
        # lados = dentes*3

        for i in range(lados):
            angulo_tmp = 2*np.pi*i/lados
            acrecimo = 0
            if orientation == 0:
                if i % 5 == 0 or i % 5 == 1:
                # if i % 3 == 0:
                    acrecimo = altura_dente
            else:
                if i % 7 == 1:
                # if i % 3 == 0:
                    acrecimo = altura_dente*1.1
                    angulo_tmp += orientation

            x = float((raio+acrecimo)*np.cos(angulo_tmp))
            y = float((raio+acrecimo)*np.sin(angulo_tmp))
            pontos.append((x,y))
        pontos = np.array(pontos)
        pontos = pontos.tolist()
        return pontos