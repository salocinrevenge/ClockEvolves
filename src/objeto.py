import numpy as np
import algebra

class Objeto():

    def __init__(self) -> None:
        self.massa: int = 1
        self.posicao = np.zeros(3,dtype=float) # x, y, angulo
        self.velocidade = np.zeros(3,dtype=float) # vx, vy, vang
        self.gravidade = 0.1
        self.aceleracao = np.array([0,self.gravidade,0]) # ax, ay, aang
        self.velocidadeAcressimo = np.zeros(3) # lista de Forca
        self.conexoes = [] # lista de Conexao
        self.debug = True
        self.atrito = 0.0001


    def distancia(self, objeto):
        # calcula a distancia euclidiana entre os dois pontos dados pelos primeiros 2 valores de cada vetor posicao
        return np.linalg.norm(self.posicao[:2] - objeto.posicao[:2])

    def tick(self):
        print(self.posicao, "posicao")
        self.velocidade += self.velocidadeAcressimo
        self.posicao += self.velocidade
        self.velocidade += self.aceleracao
        self.velocidade *= 1-self.atrito
        self.velocidadeAcressimo = np.zeros(3)

    def render(self, screen):
        pass

    def colidirLimites(self, limites):
        # limites é uma tupla no formato (minX, maxX, minY, maxY)
        if self.posicao[0] - self.raio + self.velocidade[0] < limites[0] or self.posicao[0] + self.raio + self.velocidade[0] > limites[1]: # limite de x
            self.velocidadeAcressimo += self.velocidade * np.array([-2,0,0])
        if self.posicao[1] - self.raio + self.velocidade[1] < limites[2] or self.posicao[1] + self.raio + self.velocidade[1] > limites[3]: # limite de y
            self.velocidadeAcressimo += self.velocidade * np.array([0,-2,0])


    def colidir(self, objeto: 'Objeto'):
        if self.detectarColisao(objeto):
            print("colidindo")
            self.velocidadeAcressimo += algebra.colisaoCirculos(self, objeto)
            self.velocidadeAcressimo -= self.velocidade # para simular aceleracao

    

    def detectarColisao(self, objeto):
        if self.distancia(objeto) < self.raio + objeto.raio:
            return True
        return False
    
    def energiaCinetica(self):
        return self.massa * np.dot(self.velocidade, self.velocidade) / 2
    
    def energiaPotencial(self, altura = 800):
        return self.massa * self.gravidade * (altura-self.posicao[1])
