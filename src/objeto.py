import numpy as np

class Objeto():
    massa: int = 1
    posicao = np.zeros(3) # x, y, angulo
    velocidade = np.zeros(3) # vx, vy, vang
    aceleracao = np.array([0,0.01,0]) # ax, ay, aang
    velocidadeAcressimo = np.zeros(3) # lista de Forca
    conexoes = [] # lista de Conexao


    def distancia(self, objeto):
        # calcula a distancia euclidiana entre os dois pontos dados pelos primeiros 2 valores de cada vetor posicao
        return np.linalg.norm(self.posicao[:2] - objeto.posicao[:2])

    def tick(self):
        self.velocidade += self.velocidadeAcressimo
        self.posicao += self.velocidade
        self.velocidade += self.aceleracao
        self.velocidadeAcressimo = np.zeros(3)

    def render(self, screen):
        pass

    def colidirLimites(self, limites):
        # limites é uma tupla no formato (minX, maxX, minY, maxY)
        if self.posicao[0] - self.raio + self.velocidade[0] < limites[0]:
            self.velocidadeAcressimo += self.velocidade * np.array([-2,0,0])


    def colidir(self, objeto):
        if self.detectarColisao(objeto):
            self.velocidadeAcressimo += ((self.massa-objeto.massa)*self.velocidade/(self.massa+objeto.massa) + 2*objeto.massa*objeto.velocidade/(self.massa+objeto.massa)) - self.velocidade
            print(self.velocidadeAcressimo)
        

    def detectarColisao(self, objeto):
        if self.distancia(objeto) < self.raio + objeto.raio:
            return True
        return False
