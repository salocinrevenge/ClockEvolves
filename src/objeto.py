import numpy as np
import algebra

class Objeto():

    def __init__(self) -> None:
        self.massa: int = 1
        self.posicao = np.zeros(2,dtype=float) # x, y
        self.angulo = 0
        self.velocidade = np.zeros(2,dtype=float) # vx, vy
        self.velocidadeAngular = 0
        self.gravidade = 0.1
        self.aceleracao = np.array([0,self.gravidade]) # ax, ay
        self.velocidadeAcressimo = np.zeros(2) # lista de Forca
        self.velocidadeAngularAcressimo = 0
        self.conexoes = [] # lista de Conexao
        self.debug = True
        self.atrito = 0.0001
        self.corPadrao = (100+np.random.randint(155),100+np.random.randint(155),100+np.random.randint(155))
        self.cor = self.corPadrao
        self.colidindo = False


    def distancia(self, objeto):
        # calcula a distancia euclidiana entre os dois pontos dados pelos primeiros 2 valores de cada vetor posicao
        return np.linalg.norm(self.posicao - objeto.posicao)

    def tick(self):
        self.velocidade += self.velocidadeAcressimo
        self.posicao += self.velocidade
        self.angulo += self.velocidadeAngularAcressimo
        self.velocidade += self.aceleracao
        self.velocidade *= 1-self.atrito
        self.velocidadeAcressimo = np.zeros(2)
        self.velocidadeAngularAcressimo = 0
        self.semitick()

    def semitick(self):
        if self.colidindo:
            self.colidindo = False
            self.cor = self.corPadrao

    def render(self, screen):
        pass

    def colidirLimites(self, limites):
        pass


    def colidir(self, objeto: 'Objeto'):
        if self.detectarColisao(objeto):
            self.velocidadeAcressimo += algebra.colisaoCirculos(self, objeto)
            self.velocidadeAcressimo -= self.velocidade # para simular aceleracao

    

    def detectarColisao(self, objeto):
        return False
    
    def energiaCinetica(self):
        return self.massa * np.dot(self.velocidade, self.velocidade) / 2
    
    def energiaPotencial(self, altura = 800):
        return self.massa * self.gravidade * (altura-self.posicao[1])
