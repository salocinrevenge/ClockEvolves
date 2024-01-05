import numpy as np

class Objeto():
    massa: int = 1
    posicao = np.zeros(3) # x, y, angulo
    velocidade = np.zeros(3) # vx, vy, vang
    gravidade = 0.1
    aceleracao = np.array([0,gravidade,0]) # ax, ay, aang
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
        if self.posicao[0] - self.raio + self.velocidade[0] < limites[0] or self.posicao[0] + self.raio + self.velocidade[0] > limites[1]:
            self.velocidadeAcressimo += self.velocidade * np.array([-2,0,0])
        if self.posicao[1] - self.raio + self.velocidade[1] < limites[2] or self.posicao[1] + self.raio + self.velocidade[1] > limites[3]:
            self.velocidadeAcressimo += self.velocidade * np.array([0,-2,0])

    def projetar(self, a, b):
        # projeta o vetor a no vetor b
        return np.dot(a, b) / np.dot(b, b) * b


    def colidir(self, objeto: 'Objeto'):
        if self.detectarColisao(objeto):
            vetorObjeto = objeto.posicao - self.posicao
            vetorSelf = self.posicao - objeto.posicao
            velocidadeColisao = self.projetar(self.velocidade, vetorObjeto)
            velocidadeColisaoObjeto = self.projetar(objeto.velocidade, vetorSelf)

            self.velocidadeAcressimo += ((self.massa-objeto.massa)*velocidadeColisao/(self.massa+objeto.massa) + 2*objeto.massa*velocidadeColisaoObjeto/(self.massa+objeto.massa)) - self.velocidade
            # print(self.velocidadeAcressimo)
    

    def detectarColisao(self, objeto):
        if self.distancia(objeto) < self.raio + objeto.raio:
            return True
        return False
    
    def energiaCinetica(self):
        return self.massa * np.dot(self.velocidade, self.velocidade) / 2
    
    def energiaPotencial(self, altura = 800):
        return self.massa * self.gravidade * (800-self.posicao[1])
