import numpy as np

def projecao(a, b):
    # projeta o vetor a no vetor b
    return np.dot(a, b) / np.dot(b, b) * b

def perpendicular(v):
    # encontra um vetor perpendicular ao vetor v
    if v[0] == 0:
        return np.array([1,0,0])
    return np.array([-v[1],v[0],0])

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
