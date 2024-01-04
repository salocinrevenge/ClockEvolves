import numpy as np

class Objeto():
    massa: int = 1
    posicao = np.zeros(3) # x, y, angulo
    velocidade = np.zeros(3) # vx, vy, vang
    aceleracao = np.zeros(3) # ax, ay, aang
    forcas = np.zeros(3) # lista de Forca
    conexoes = [] # lista de Conexao


    def distancia(self, objeto):
        # calcula a distancia euclidiana entre os dois pontos dados pelos primeiros 2 valores de cada vetor posicao
        return np.linalg.norm(self.posicao[:2] - objeto.posicao[:2])

    def tick(self):
        pass

    def render(self, screen):
        pass

    def colidir(self, objeto):
        pass
        

    def detectarColisao(self, objeto):
        if self.distancia(objeto) < self.raio + objeto.raio:
            return True
        return False
