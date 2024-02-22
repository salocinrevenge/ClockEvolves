import numpy as np

class Objeto():
    massa: int = 0.01
    posicao = np.zeros(3) # x, y, angulo (centro do objeto)
    velocidade = np.zeros(3) # vx, vy, vang
    gravidade = 0.15
    aceleracao = np.array([0,gravidade,0]) # ax, ay, aang
    colisoes = [] # lista de aceleracoes
    k = 0.2 # constante de elasticidade
    conexoes = [] # lista de Conexao
    debug = True


    def distancia(self, objeto):
        # calcula a distancia euclidiana entre os dois pontos dados pelos primeiros 2 valores de cada vetor posicao
        return np.linalg.norm(self.posicao[:2] - objeto.posicao[:2])

    def tick(self):
        self.posicao += self.velocidade
        self.velocidade += self.aceleracao

    def render(self, screen):
        pass

    def colidirLimites(self, limites):
        # limites é uma tupla no formato (minX, maxX, minY, maxY)
        if self.posicao[0] - self.raio + self.velocidade[0] < limites[0] or self.posicao[0] + self.raio + self.velocidade[0] > limites[1]:
            self.aceleracao += self.velocidade * np.array([-2,0,0])
        if self.posicao[1] - self.raio + self.velocidade[1] < limites[2] or self.posicao[1] + self.raio + self.velocidade[1] > limites[3]:
            self.aceleracao += self.velocidade * np.array([0,-2,0])

    def projetar(self, a, b):
        # projeta o vetor a no vetor b
        print("projetando")
        print(np.dot(a, b))
        print(np.dot(b, b))
        print(np.dot(a, b) / np.dot(b, b))
        print(b)
        return np.dot(a, b) / np.dot(b, b) * b

    def resetTick(self):
        self.colisoes = []
        self.aceleracao = np.array([0,self.gravidade,0]) # ax, ay, aang


    def colidir(self, objeto: 'Objeto'):
        colisao = self.detectarColisao(objeto)
        if colisao is not None:
            moduloForcaMinha = self.k*colisao
            moduloForcaDele = objeto.k*colisao
            moduloTotal = moduloForcaMinha + moduloForcaDele
            direcao = self.posicao - objeto.posicao
            print("direcao:")
            print(direcao)
            print("moduloTotal:")
            print(moduloTotal)
            forcaMinha = moduloTotal* direcao/np.linalg.norm(direcao)
            acc = forcaMinha/self.massa
            self.aceleracao += acc
            self.colisoes.append(acc)
            print(acc)
            print("colidi")
    

    def detectarColisao(self, objeto):
        dist = self.distancia(objeto)
        if dist < self.raio + objeto.raio:
            compressao = (self.raio + objeto.raio - dist)/2 # aqui a compressao eh simplificada, uma vez que devido a cada k, a compressao de cada um sera diferente
            return compressao   # retorna a compressão
        return None
    
    def energiaCinetica(self):
        return self.massa * np.dot(self.velocidade, self.velocidade) / 2
    
    def energiaPotencial(self, altura = 800):
        return self.massa * self.gravidade * (800-self.posicao[1])
