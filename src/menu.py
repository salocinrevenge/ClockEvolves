import pygame
from botao import Botao
from sala import Sala
from evoluidor import Evoluidor
import os

class Menu():
    def __init__(self) -> None:
        self.criaBotoesMenuPrincipal()
        self.criaBotoesMenuCriar()
        self.STATE = "Menu"
        self.sala = None

        self.arquivosMenu = []     # botoes da seleção de arquivos
        self.caminho_atual = None  # diretório atual na navegação
        self.scroll_offset = 0     # controle da rolagem


    def tick(self, dt):
        if self.STATE == "Sala":
            self.sala.tick(dt)
        if self.STATE == "Evoluir":
            self.evoluidor.tick(dt)

    def render(self, screen):
        if self.STATE == "Menu":
            for botao in self.botoesMenuPrincipal:
                botao.render(screen)
        elif self.STATE == "Criar Sala":
            for botao in self.botoesMenuCriar:
                botao.render(screen)
        elif self.STATE == "Selecionar Arquivo":
            self.botao_voltar.render(screen)
            for botao in self.arquivosMenu:
                botao.render(screen)
        elif self.STATE == "Sala":
            self.sala.render(screen)
        elif self.STATE == "Evoluir":
            self.evoluidor.render(screen)
        
    def criarSala(self, config = "Aleatorizar"):
        self.STATE = "Sala"
        if config == "Aleatorizar":
            self.sala = Sala()
        elif config == "Criar":
            self.sala = Sala(editor=True)
        elif config == "Carregar":
            self.abrirSelecaoArquivos("save")

    def criarEvoluir(self):
        self.evoluidor = Evoluidor()


    def criaBotoesMenuPrincipal(self):
        self.botoesMenuPrincipal = []
        self.botoesMenuPrincipal.append(Botao(100, 100, 600, 150, "Criar Sala", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(100, 300, 600, 150, "Evoluir", textSize = 72))
        self.botoesMenuPrincipal.append(Botao(100, 500, 600, 150, "Configurações", textSize = 72))

    def criaBotoesMenuCriar(self):
        self.botoesMenuCriar = []
        self.botoesMenuCriar.append(Botao(250, 350, 300, 100, "Carregar", textSize = 72))
        self.botoesMenuCriar.append(Botao(250, 500, 300, 100, "Aleatorizar", textSize = 72))
        self.botoesMenuCriar.append(Botao(250, 650, 300, 100, "Criar", textSize = 72))


    def abrirSelecaoArquivos(self, caminho):
        """Cria os botoes listando arquivos/pastas em 'caminho'"""
        self.STATE = "Selecionar Arquivo"
        self.caminho_atual = caminho
        self.scroll_offset = 0
        self.arquivosMenu = []

        try:
            conteudo = sorted(os.listdir(caminho))
        except FileNotFoundError:
            conteudo = []

        y = 120  # começa abaixo do botão voltar
        for item in conteudo:
            caminho_item = os.path.join(caminho, item)
            label = f"[DIR] {item}" if os.path.isdir(caminho_item) else item
            self.arquivosMenu.append(Botao(100, y, 600, 50, label, textSize=36))
            y += 60

        # botão de voltar (fixo no topo)
        self.botao_voltar = Botao(20, 40, 50, 50, "<", textSize=36)


    def scroll(self, dy):
        """Desloca todos os botoes da lista em dy pixels"""
        self.scroll_offset += dy
        for botao in self.arquivosMenu:
            botao.update_y(botao.y + dy)


    def input(self, evento):
        # se ESC
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.STATE = "Menu"
            return
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.STATE == "Menu":
                for botao in self.botoesMenuPrincipal:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        print(clique)
                        if clique == "Criar Sala":
                            self.STATE = clique
                            return
                        if clique == "Evoluir":
                            self.STATE = clique
                            self.criarEvoluir()
                            return

            elif self.STATE == "Criar Sala":
                for botao in self.botoesMenuCriar:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        print(clique)
                        self.criarSala(config = clique)
                        return

            elif self.STATE == "Selecionar Arquivo":
                if self.botao_voltar.identificaClique(evento.pos):
                    pai = os.path.dirname(self.caminho_atual)
                    if pai == "":
                        pai = "save"
                    self.abrirSelecaoArquivos(pai)
                    return

                for botao in self.arquivosMenu:
                    clique = botao.identificaClique(evento.pos)
                    if clique:
                        print("Selecionado:", clique)
                        if clique.startswith("[DIR]"):
                            pasta = clique.replace("[DIR] ", "")
                            self.abrirSelecaoArquivos(os.path.join(self.caminho_atual, pasta))
                            return
                        else:
                            arquivo = os.path.join(self.caminho_atual, clique)
                            if arquivo.endswith(".txt"):
                                self.STATE = "Sala"
                                self.sala = Sala(carregar=arquivo)
                            return

        elif evento.type == pygame.MOUSEWHEEL:
            if self.STATE == "Selecionar Arquivo":
                self.scroll(evento.y * 30)
        elif evento.type == pygame.KEYDOWN:
            if self.STATE == "Selecionar Arquivo":
                if evento.key == pygame.K_DOWN:
                    self.scroll(-30)
                elif evento.key == pygame.K_UP:
                    self.scroll(30)
        

        if self.STATE == "Sala":
            self.sala.input(evento)
