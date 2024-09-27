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

def intersecaoPoligonosCompostos(a, b, externos_a = None, externos_b = None):
    # poligonos compostos sao poligonos que sao formados por uma lista de poligonos
    # print("a: ", a, "b: ", b)
    colisoes = []
    for i in range(len(a)):
        for j in range(len(b)):
            # input()
            # print("Poligono A: ", poligonoA, "Poligono B: ", poligonoB)
            colisao = intersecaoPoligonos(a[i], b[j],externos_a[i],externos_b[j])
            if colisao[0]:
                print(colisao)
                print(f"colidiu poligono {i} com poligono {j}")
                # print("interceptou!")
                colisoes.append(colisao)
    # print(colisoes)
    if len(colisoes) > 0:
        colisaoescolida = colisoes[np.argmax([colisao[2] for colisao in colisoes])]
        print("a colisao que eu detectei foi: ", colisaoescolida)
        return colisaoescolida
    # print("Não interceptou!")
    return (False,)

def intersecaoPoligonos(a, b, a_externos = None, b_externos = None):  # a e b são vetores numpy de n x 2, a está colidindo com b, o que a deve fazer? retorna a normal de b
    if a_externos is None:
        a_externos = np.array([False]*len(a))
    if b_externos is None:
        b_externos = np.array([False]*len(b))

    penetracoes = np.full(len(a)+len(b), np.inf)
    sentidos = np.full(len(a)+len(b), 1)
    
    for i in range(len(a)):
        va = a[i]
        vb = a[(i+1)%len(a)]

        edge = vb - va
        normal = np.array([edge[1], -edge[0]]) # coordenadas com y invertido
        normal = normal / np.linalg.norm(normal) # normaliza o vetor
        minA, maxA = projectVertices(a, normal)
        minB, maxB = projectVertices(b, normal)
        if maxA < minB or maxB < minA:
            return (False,)
        if a_externos[i]:
            # print(f"EU: minA: {minA} maxA: {maxA} minB: {minB} maxB: {maxB}")
            # print(f"{maxB - minA=}, {maxA - minB=}")
            if maxB - minA < maxA - minB:
                # print("marquei para inverter")
                sentidos[i] = -1
            penetracoes[i]=min(maxB - minA, maxA - minB) # não eh necessario abs pois o if acima garante que a subtracao seja positiva
        
    for i in range(len(b)): # necessario pois ha casos em que o lado que garante nao intercecao esta de frente para um vertice do outro poligono, exemplo: equilatero sobre equilatero pertinho.
        va = b[i]
        vb = b[(i+1)%len(b)]

        edge = vb - va
        normal = np.array([edge[1], -edge[0]])
        normal = normal / np.linalg.norm(normal) # normaliza o vetor
        minA, maxA = projectVertices(a, normal)
        minB, maxB = projectVertices(b, normal)
        if maxA < minB or maxB < minA:
            return (False,)
        if b_externos[i]:
            # print(f"ELE: minA: {minA} maxA: {maxA} minB: {minB} maxB: {maxB}")
            # print(f"{maxB - minA=}, {maxA - minB=}")

            # if maxB - minA > maxA - minB:
            #     print("marquei para inverter")
            #     sentidos[i] = -1
            penetracoes[i+len(a)]=min(maxB - minA, maxA - minB)

    i = np.argmin(penetracoes)
    sentido = sentidos[i]
    if i < len(a):
        edge = a[(i+1)%len(b)] - a[i]
        direcao = np.array([-edge[1], edge[0]]) # rotacioona 90 graus, pois A esta penetrando B
    else:
        i = i - len(a)
        edge = b[(i+1)%len(b)] - b[i]
        direcao = np.array([edge[1], -edge[0]]) # rotacioona -90 graus, pois A esta sendo penetrado em sua aresta
    direcao = direcao / np.linalg.norm(direcao) # normaliza o vetor de penetracao
    # if sentido<1:
    #     print("inverteu")
    direcao = direcao * sentido # inverte a direcao se necessario
    distPenetrada = np.min(penetracoes)
    # print(penetracoes)

    return (True, direcao, distPenetrada+0.01)

def resolveCollision(bodyA, bodyB, vetorColision):
    print("resolveCollision, vetorColision: ", vetorColision)
    print(f"{bodyA.velocidade=}, {bodyB.velocidade=}")
    velRel = bodyB.velocidade - bodyA.velocidade
    e = min(bodyA.restituicao, bodyB.restituicao)
    normal = vetorColision/np.linalg.norm(vetorColision)
    j = (1+e)* np.dot(velRel, normal) / (1/bodyA.massa + 1/bodyB.massa)
    print(f"{j=}")
    bodyA.velocidade += j/bodyA.massa * normal
    print(f"{bodyA.velocidade=}, {bodyB.velocidade=}")
    # raise Exception("colisao")
    

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
    # pontos passa a ser uma lista de tuplas com o primeiro valor sendo o index
    for i in range(len(pontos)):
        pontos[i] = (i, pontos[i])
    
    # recebe um vetor numpy de n x 2 e devolve um vetor numpy de (n-2) x 3 x 2, e um vetor numpy de n x 2 representando os vertices iniciais das arestas internas
    triangulos = []
    externos = []

    verticeAlvo = -1
    max_len = len(pontos)
    while len(pontos) > 3:
        # pega o proximo vertice
        verticeAlvo = (verticeAlvo + 1) % len(pontos)

        # verifica se o triangulo formado pelo verticeAlvo e os dois vizinhos contem algum outro vertice

        possivelTriangulo = np.asarray([pontos[verticeAlvo][1], pontos[(verticeAlvo+1)%len(pontos)][1], pontos[(verticeAlvo+2)%len(pontos)][1]])
        # verifica se o angulo formado pelos 3 pontos é maior que 180 graus
        if np.cross(possivelTriangulo[1]-possivelTriangulo[0], possivelTriangulo[2]-possivelTriangulo[0]) < 0:
            continue
        contem = False
        for i in range(len(pontos)):
            if i == verticeAlvo or i == (verticeAlvo+1)%len(pontos) or i == (verticeAlvo+2)%len(pontos):
                continue
            if intersecaoPoligonoPonto(possivelTriangulo, np.asarray([pontos[i][1]])):
                contem = True
                break
        if not contem:
            triangulos.append(possivelTriangulo)
            externos.append(np.asarray([pontos[verticeAlvo+1][0]-pontos[verticeAlvo][0]==1, pontos[verticeAlvo+2][0]-pontos[verticeAlvo+1][0]==1, pontos[verticeAlvo][0]-pontos[verticeAlvo+2][0]==1]))
            pontos.pop((verticeAlvo+1)%len(pontos))
    triangulos.append(np.asarray([pontos[0][1], pontos[(1)%len(pontos)][1], pontos[(2)%len(pontos)][1]]))
    externos.append(np.asarray([(pontos[1][0]-pontos[0][0])%max_len==1, (pontos[2][0]-pontos[1][0])%max_len==1, (pontos[0][0]-pontos[2][0])%max_len==1]))
    # print(f"ultima conta: {pontos[0][0]=} {pontos[2][0]=} {max_len} {(pontos[0][0]-pontos[2][0])%len(pontos)=} {(pontos[0][0]-pontos[2][0])%len(pontos)==1} {internos[-1]=}")
    return np.array(triangulos), np.array(externos)

