from objeto import Objeto
import numpy as np
import pygame
import algebra

class Poligono(Objeto):
    def __init__(self, pontos) -> None:
        super().__init__()
        self.pontosOriginais = pontos
        self.pontos = self.pontosOriginais.copy()
        self.pontosColisaoOriginal, self.pontos_externos = algebra.triangulariza(self.pontos)
        self.pontosColisao = self.pontosColisaoOriginal.copy()
        #obtem a maior distancia até o centro
        self.raio = np.max(np.linalg.norm(self.pontos, axis=1))
        self.debugColors = []
        self.vetor_colisao = np.zeros(2)

    def posicionaPontos(self, pontos, posicao, angulo):
        # pontos é um vetor numpy de n x 2
        # x e y são as coordenadas que devem ser adicionadas a cada ponto
        # angulo é o angulo de rotacao em radianos
        # retorna um vetor numpy de n x 2
        matrizRotacao = np.array([[np.cos(angulo), -np.sin(angulo)], [np.sin(angulo), np.cos(angulo)]])
        return np.dot(pontos, matrizRotacao) + np.array(posicao)

    def tick(self):
        super().tick()
        self.atualizaPontos()
    
    def atualizaPontos(self):
        self.pontos = self.posicionaPontos(self.pontosOriginais, self.posicao, self.angulo)
        self.pontosColisao = self.posicionaPontos(self.pontosColisaoOriginal, self.posicao, self.angulo)


    def colidirLimites(self, limites):
        # limites é uma tupla no formato (minX, maxX, minY, maxY)

        # verifica primeiro se o circulo de colisao está fora dos limites
        colidindo = False
        if self.posicao[0] - self.raio < limites[0] or self.posicao[0] + self.raio > limites[1]: # limite de x
            colidindo = True
        if self.posicao[1] - self.raio < limites[2] or self.posicao[1] + self.raio > limites[3]: # limite de y
            colidindo = True
        if not colidindo:
            return
        
        # verifica qual ponto está fora dos limites
        for ponto in self.pontos:
            if ponto[0] < limites[0] or ponto[0] > limites[1]: # limite de x
                # acelera o objeto para dentro dos limites
                # self.velocidadeAcressimo += self.velocidade * np.array([-2,0])
                return
            if ponto[1] < limites[2] or ponto[1] > limites[3]: # limite de y
                # acelera o objeto para dentro dos limites
                # self.velocidadeAcressimo += self.velocidade * np.array([0,-2])
                return
            
    def colidir(self, objeto: Objeto):
        if isinstance(objeto, Poligono):
            if self.detectarColisao(objeto):
                # separa a briga
                self.posicao+=self.vetor_colisao
                self.atualizaPontos()

                # resolve a colisao como descrito por chrishecker: https://www.chrishecker.com/Rigid_Body_Dynamics
                algebra.resolveCollision(self, objeto, self.vetor_colisao)
                self.vetor_colisao = np.zeros(2)


                # self.velocidade = np.zeros(2)
                # self.velocidadeAcressimo = np.zeros(2)
                # self.velocidadeAcressimo += self.vetor_colisao
                # self.velocidadeAcressimo -= self.velocidade # para simular aceleracao

    

    def detectarColisao(self, objeto):
        if isinstance(objeto, Poligono):
            colisao = algebra.intersecaoPoligonosCompostos(self.pontosColisao, objeto.pontosColisao, self.pontos_externos, objeto.pontos_externos)
            if colisao[0]:
                self.colidindo = True
                self.cor = (255,0,0)
                print("detectei colisao, alterando cor")
                self.vetor_colisao = colisao[1]*colisao[2]
                return True


    def render(self, screen):
        pygame.draw.polygon(screen, self.cor, self.pontos)
        if self.debug:
            for i in range(len(self.pontosColisao)):
                if len(self.debugColors) <= i:
                    self.debugColors.append((100+np.random.randint(155),100+np.random.randint(155),100+np.random.randint(155)))
                pygame.draw.polygon(screen, self.debugColors[i], self.pontosColisao[i])

            #desenha circulo de colisao
            pygame.draw.circle(screen, self.cor, (self.posicao[0],self.posicao[1]), self.raio, 1)
            pygame.draw.line(screen, self.cor, (self.posicao[0],self.posicao[1]), (self.posicao[0]+self.velocidade[0]*10,self.posicao[1]+self.velocidade[1]*10), 2)

        