import pygame

def limitador(valor, min, max, subdivisoes = None):
    if subdivisoes < 2:
        raise ValueError("O valor de subdivisoes deve ser maior que 2")
    if valor < min:
        return min
    if valor > max:
        return max
    if subdivisoes == None:
        return valor
    subdivisoes -= 1
    # subdivisoes faz com que só seja possível retornar um valor múltiplo de 1/subdivisoes
    valor = valor - min
    valor /= max-min
    return (round(valor * subdivisoes) / subdivisoes) * (max-min) + min

# Define as cores
preto = (0, 0, 0)
branco = (255, 255, 255)
azul = (0, 122, 255)

# Inicialize Pygame
pygame.init()

# Variavel para se ta pressionado
pressionado = False

# Crie uma tela
tela = pygame.display.set_mode((600, 400))

# Crie um retângulo para o controle deslizante
controle_deslizante = pygame.Rect(200, 200, 200, 20)

# Crie um círculo para o controle deslizante
controle_deslizante_circulo = pygame.Rect(200-(20/2), 200, 20, 20)

# Defina o valor inicial do controle deslizante
valor_controle_deslizante = 1

# Loop principal
while True:
    # Atualize o estado do controle deslizante
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Verifique se o botão do mouse está dentro do controle deslizante
                if controle_deslizante.collidepoint(event.pos):
                    pressionado = True
                    # Mova o controle deslizante para a posição do mouse
                    controle_deslizante_circulo.centerx = event.pos[0]

        if event.type == pygame.MOUSEBUTTONUP:
            # Verifique se o botão do mouse está dentro do controle deslizante
            if event.button == 1:
                pressionado = False

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Desenhe a tela
    tela.fill(branco)

    if pressionado:
        # Mova o controle deslizante para a posição do mouse
        controle_deslizante_circulo.centerx = limitador(pygame.mouse.get_pos()[0], controle_deslizante.x, controle_deslizante.x + controle_deslizante.width, 6)

    # Desenhe o controle deslizante
    pygame.draw.rect(tela, (80,80,80), (controle_deslizante.x, controle_deslizante.y+7.5, 200, 5))

    pygame.draw.ellipse(tela, azul, controle_deslizante_circulo)

    # Desenhe o valor do controle deslizante
    tela.blit(
        pygame.font.SysFont("Arial", 20).render(str(valor_controle_deslizante), True, preto),
        (200, 250),
    )

    # Atualize a tela
    pygame.display.update()

    # Atualize o valor do controle deslizante
    valor_controle_deslizante = controle_deslizante_circulo.centerx - controle_deslizante.x
    valor_controle_deslizante = valor_controle_deslizante / controle_deslizante.width
    valor_controle_deslizante = round(valor_controle_deslizante, 2)

