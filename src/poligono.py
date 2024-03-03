from objeto import Objeto
import numpy as np
import pygame
import algebra

class Poligono(Objeto):
    def __init__(self, pontos) -> None:
        super().__init__()
        self.pontosOriginais = pontos
        self.pontos = self.pontosOriginais.copy()
        self.pontosColisaoOriginal = algebra.triangulariza(self.pontos)
        self.pontosColisao = self.pontosColisaoOriginal.copy()
        #obtem a maior distancia até o centro
        print(self.pontos)
        self.raio = np.max(np.linalg.norm(self.pontos, axis=1))
        self.debugColors = []

    def posicionaPontos(self, pontos, posicao, angulo):
        # pontos é um vetor numpy de n x 2
        # x e y são as coordenadas que devem ser adicionadas a cada ponto
        # angulo é o angulo de rotacao em radianos
        # retorna um vetor numpy de n x 2
        matrizRotacao = np.array([[np.cos(angulo), -np.sin(angulo)], [np.sin(angulo), np.cos(angulo)]])
        return np.dot(pontos, matrizRotacao) + np.array(posicao)

    def tick(self):
        super().tick()
    
    def semitick(self):
        super().semitick()
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
                self.velocidadeAcressimo += self.velocidade * np.array([-2,0])
                return
            if ponto[1] < limites[2] or ponto[1] > limites[3]: # limite de y
                self.velocidadeAcressimo += self.velocidade * np.array([0,-2])
                return
    

    def detectarColisao(self, objeto):
        if isinstance(objeto, Poligono):
            if algebra.intersecaoPoligonosCompostos(self.pontosColisao, objeto.pontosColisao):
                self.colidindo = True
                self.cor = (255,0,0)
                print("alterando cor")
                return True


    def render(self, screen):
        pygame.draw.polygon(screen, self.cor, self.pontos)
        if self.debug:
            #desenha circulo de colisao
            pygame.draw.circle(screen, self.cor, (self.posicao[0],self.posicao[1]), self.raio, 1)
            pygame.draw.line(screen, self.cor, (self.posicao[0],self.posicao[1]), (self.posicao[0]+self.velocidade[0]*10,self.posicao[1]+self.velocidade[1]*10), 2)
            
            for i in range(len(self.pontosColisao)):
                if len(self.debugColors) <= i:
                    self.debugColors.append((100+np.random.randint(155),100+np.random.randint(155),100+np.random.randint(155)))
                pygame.draw.polygon(screen, self.debugColors[i], self.pontosColisao[i])


        