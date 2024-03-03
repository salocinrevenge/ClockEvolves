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

def intersecaoPoligonosCompostos(a, b):
    # poligonos compostos sao poligonos que sao formados por uma lista de poligonos
    # print("a: ", a, "b: ", b)
    for poligonoA in a:
        for poligonoB in b:
            # input()
            # print("Poligono A: ", poligonoA, "Poligono B: ", poligonoB)
            if intersecaoPoligonos(poligonoA, poligonoB):
                # print("interceptou!")
                return True
    # print("Não interceptou!")
    return False

def intersecaoPoligonos(a, b):
    for i in range(len(a)):
        va = a[i]
        vb = a[(i+1)%len(a)]

        edge = vb - va
        normal = np.array([-edge[1], edge[0]])
        minA, maxA = projectVertices(a, normal)
        minB, maxB = projectVertices(b, normal)
        if maxA < minB or maxB < minA:
            return False
        
    for i in range(len(b)):
        va = b[i]
        vb = b[(i+1)%len(b)]

        edge = vb - va
        normal = np.array([-edge[1], edge[0]])
        minA, maxA = projectVertices(a, normal)
        minB, maxB = projectVertices(b, normal)
        if maxA < minB or maxB < minA:
            return False
    return True

def intersecaoPoligonoPonto(a, b):
    for i in range(len(a)):
        va = a[i]
        vb = a[(i+1)%len(a)]

        edge = vb - va
        normal = np.array([-edge[1], edge[0]])
        minA, maxA = projectVertices(a, normal)
        minB, maxB = projectVertices(b, normal)
        if maxA < minB or maxB < minA:
            return False
    return True
        

def projectVertices(vertices, axis):
    min = np.dot(axis, vertices[0])
    max = min
    for i in range(1, len(vertices)):
        p = np.dot(axis, vertices[i])
        if p < min:
            min = p
        elif p > max:
            max = p
    return (min, max)

def triangulariza(pontos):
    pontos = pontos.tolist()
    
    # recebe um vetor numpy de n x 2 e devolve um vetor numpy de (n-2) x 3 x 2
    triangulos = []

    verticeAlvo = -1
    while len(pontos) > 3:
        # pega o proximo vertice
        verticeAlvo = (verticeAlvo + 1) % len(pontos)
        # input()
        # print("Vertice Alvo: ", verticeAlvo, "Pontos: ", pontos, "Triangulos: ", triangulos)
        # verifica se o triangulo formado pelo verticeAlvo e os dois vizinhos contem algum outro vertice
        possivelTriangulo = np.asarray([pontos[verticeAlvo], pontos[(verticeAlvo+1)%len(pontos)], pontos[(verticeAlvo+2)%len(pontos)]])
        # verifica se o angulo formado pelos 3 pontos é maior que 180 graus
        if np.cross(possivelTriangulo[1]-possivelTriangulo[0], possivelTriangulo[2]-possivelTriangulo[0]) < 0:
            continue
        contem = False
        for i in range(len(pontos)):
            if i == verticeAlvo or i == (verticeAlvo+1)%len(pontos) or i == (verticeAlvo+2)%len(pontos):
                continue
            if intersecaoPoligonoPonto(possivelTriangulo, np.asarray([pontos[i]])):
                contem = True
                break
        if not contem:
            triangulos.append(possivelTriangulo)
            pontos.pop((verticeAlvo+1)%len(pontos))
    triangulos.append(np.asarray(pontos))
    return np.array(triangulos)

