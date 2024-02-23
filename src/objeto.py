import numpy as np

class Objeto():
    massa: int = 1
    posicao = np.zeros(3) # x, y, angulo
    velocidade = np.zeros(3) # vx, vy, vang
    gravidade = 0.1
    aceleracao = np.array([0,gravidade,0]) # ax, ay, aang
    velocidadeAcressimo = np.zeros(3) # lista de Forca
    conexoes = [] # lista de Conexao
    debug = True
    atrito = 0.0001


    def distancia(self, objeto):
        # calcula a distancia euclidiana entre os dois pontos dados pelos primeiros 2 valores de cada vetor posicao
        return np.linalg.norm(self.posicao[:2] - objeto.posicao[:2])

    def tick(self):
        self.velocidade += self.velocidadeAcressimo
        self.posicao += self.velocidade
        self.velocidade += self.aceleracao
        # self.velocidade *= 1-self.atrito
        self.velocidadeAcressimo = np.zeros(3)

    def render(self, screen):
        pass

    def colidirLimites(self, limites):
        # limites é uma tupla no formato (minX, maxX, minY, maxY)
        if self.posicao[0] - self.raio + self.velocidade[0] < limites[0] or self.posicao[0] + self.raio + self.velocidade[0] > limites[1]: # limite de x
            self.velocidadeAcressimo += self.velocidade * np.array([-2,0,0])
        if self.posicao[1] - self.raio + self.velocidade[1] < limites[2] or self.posicao[1] + self.raio + self.velocidade[1] > limites[3]: # limite de y
            self.velocidadeAcressimo += self.velocidade * np.array([0,-2,0])

    def projetar(self, a, b):
        # projeta o vetor a no vetor b
        return np.dot(a, b) / np.dot(b, b) * b


    def colidir(self, objeto: 'Objeto'):
        if self.detectarColisao(objeto):
            print("colidindo")
            self.velocidadeAcressimo += ((self.massa-objeto.massa)*self.velocidade/(self.massa+objeto.massa) + 2*objeto.massa*objeto.velocidade/(self.massa+objeto.massa))  # formula da conservacao de momento
            self.velocidadeAcressimo -= self.velocidade # para simular aceleracao

    

    def detectarColisao(self, objeto):
        if self.distancia(objeto) < self.raio + objeto.raio:
            return True
        return False
    
    def energiaCinetica(self):
        return self.massa * np.dot(self.velocidade, self.velocidade) / 2
    
    def energiaPotencial(self, altura = 800):
        return self.massa * self.gravidade * (altura-self.posicao[1])
