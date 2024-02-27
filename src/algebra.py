import numpy as np

def projecao(a, b):
    # projeta o vetor a no vetor b
    return np.dot(a, b) / np.dot(b, b) * b

def perpendicular(v):
    # encontra um vetor perpendicular ao vetor v
    return np.array([-v[1],v[0]])

def somaVetores(a, b):
    return a + b

def colisaoCirculos(a, b):
    velA = a.velocidade
    velB = b.velocidade
    posA = a.posicao
    posB = b.posicao
    vetorAB = posB - posA
    vetorBA = posA - posB
    superficie = perpendicular(vetorAB)
    velAProj = projecao(velA, vetorAB)
    velBProj = projecao(velB, vetorBA)
    velASuperficie = projecao(velA, superficie)
    velocidadeAFinal = ((a.massa-b.massa)*velAProj/(a.massa+b.massa) + 2*b.massa*velBProj/(a.massa+b.massa))  # formula da conservacao de momento
    velocidadeAFinal = velocidadeAFinal + velASuperficie
    return velocidadeAFinal

def colisaoCirculoPoligono(circulo, poligono):
    # TODO
    normal
    v1 = 0 # TODO velocidadePerpendicularColisao
    c = 0 # TODO distancia horizontal até o centro de massa (ou vertical se a colisao ocorrer na lateral)
    w = 2*v1*c*self.massa*objeto.massa/(self.massa*objeto.massa*c*c+objeto.massa-self.inercia*self.massa) # velocidade angular final
    v2 = (m*v1*c-I*w)/(m*c)
    velocidadeFinal = V+np.array([0,0,w]) # TODO vetor velocidade final
    return velocidadeFinal

def colisaoRetanguloCirculo(a, b):
    # TODO
    v1 = 0 # TODO velocidadePerpendicularColisao
    c = 0 # TODO distancia horizontal até o centro de massa (ou vertical se a colisao ocorrer na lateral)
    w = 2*v1*c*self.massa*objeto.massa/(self.massa*objeto.massa*c*c+objeto.massa-self.inercia*self.massa) # velocidade angular final
    V = self.inercia*w/(self.massa*c) # velocidade linear final na direcao da colisao
    velocidadeFinal = V+np.array([0,0,w]) # TODO vetor velocidade final
    self.velocidadeAcressimo += velocidadeFinal
