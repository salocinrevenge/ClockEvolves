from sala import Sala
import os
import time
from concurrent.futures import ProcessPoolExecutor
import random

class Evoluidor():
    def __init__(self, n_salas = 3, save = None, n_mut = 1):
        os.makedirs("save/evolucao", exist_ok=True)
        self.ultimo_id = 0
        while True:
            if not os.path.exists(f"save/evolucao/{self.ultimo_id}"):
                break
            self.ultimo_id += 1
        os.makedirs(f"save/evolucao/{self.ultimo_id}", exist_ok=True)

        self.iniciar_salas(n_salas = n_salas, save = save)
        self.geracao = 0
        self.state = "criando"
        self.mostrando = 0
        self.debug = False
        self.n_geracoes = 0
        self.vou_recriar = 3
        self.n_mut = n_mut
        # self.n_mut = 1
        self.executor = ProcessPoolExecutor()

    def toggle_debug(self):
        for sala in self.salas:
            sala.debug = not sala.debug

    def iniciar_salas(self, n_salas, save):
        with open(f"save/evolucao/{self.ultimo_id}/n_estados.txt", "w") as f:
            f.write(f"{n_salas} individuos \n")
        self.salas = []
        for _ in range(n_salas):
            if save:
                self.salas.append(Sala(carregar=save))
            else:
                self.salas.append(Sala(aleatorio=True))

    def colocar_outras_em_processos(self):
        # Agora usamos ProcessPoolExecutor para rodar e receber salas atualizadas
        futures = [self.executor.submit(submotor, sala, self.dt) for sala in self.salas]
        self.process_results = futures
        self.state = "rodando"

    def reproduzir(self):
        novas_salas = [Sala(pais = [self.salas[0]], percents = [1], n_mut = 0, taxa_mut = 0)]
        for i in range(1, len(self.salas)):
            novas_salas.append(Sala(pais = [self.salas[0], self.salas[1], self.salas[2]], percents = [0.7, 0.2, 0.1], n_mut = self.n_mut, taxa_mut = 1))
        random.shuffle(novas_salas)
        self.salas = novas_salas
        self.geracao += 1

    def avaliar_resultados(self):
        self.salas.sort(key=lambda sala: sala.pontos, reverse=True)
        for i in range(len(self.salas)):
            print(f"sala {i}: ", self.salas[i].pontos)
        self.salas[0].salvar_sala(f"save/evolucao/{self.ultimo_id}/{self.geracao}.txt")
        n_estados = []
        for sala in self.salas:
            n_estados.append(sala.pontos)
        with open(f"save/evolucao/{self.ultimo_id}/n_estados.txt", "a") as f:
            f.write(f"\nGeracao {self.geracao}: " + " ".join(map(str, n_estados)))

    def tick(self, dt):
        self.dt = dt

        if self.state == "criando":
            self.colocar_outras_em_processos()

        elif self.state == "rodando":
            if all(f.done() for f in self.process_results):
                # Coletar resultados das salas atualizadas
                self.salas = [f.result() for f in self.process_results]
                self.vou_recriar -= 1
                if self.vou_recriar == 0:
                    self.state = "criando"
                    self.avaliar_resultados()
                    self.reproduzir()
                    self.mostrando = 0
                    self.vou_recriar = 3

    def render(self, screen):
        if self.salas[self.mostrando].repetiu:
            while self.salas[self.mostrando].repetiu:
                self.mostrando += 1
                if self.mostrando >= len(self.salas):
                    self.mostrando = 0
                    break

        self.salas[self.mostrando].render(screen)

def submotor(sala, dt):
    while not sala.repetiu:
        sala.tick(dt)
        time.sleep(0.01)
    return sala  # <- devolve a sala modificada

if __name__ == "__main__":
    evoluidor = Evoluidor(n_salas=50, save=None)

    tick_time = 1.0/120.0
    while evoluidor.geracao < 1000000:
        evoluidor.tick(tick_time)
