from sala import Sala
import os
import multiprocessing
import time

class Evoluidor():
    def __init__(self, n_salas = 3, save = None):
        os.makedirs("save/evolucao", exist_ok=True)
        self.ultimo_id = 0
        while True:
            if not os.path.exists(f"save/evolucao/{self.ultimo_id}"):
                break
            self.ultimo_id += 1
        os.makedirs(f"save/evolucao/{self.ultimo_id}", exist_ok=True)

        self.iniciar_salas(n_salas = n_salas, save = save)
        self.geracao = 0
        self.contador = multiprocessing.Value('i', 0)
        self.state = "criando"
        self.mostrando = 0
        self.debug = False
        self.n_geracoes = 0
        self.vou_recriar = 3
        self.n_mut = 10
        self.n_mut = 1

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
        self.processos = []
        for sala in self.salas:
            p = multiprocessing.Process(target=submotor, args=(sala, self.contador, self.dt))
            p.start()
            self.processos.append(p)
        self.state = "rodando"

    def reproduzir(self):
        novas_salas = [Sala(pais = [self.salas[0]], percents = [1], n_mut = 0, taxa_mut = 0)]
        for i in range(1, len(self.salas)):
            novas_salas.append(Sala(pais = [self.salas[0], self.salas[1], self.salas[2]], percents = [0.7, 0.2, 0.1], n_mut = self.n_mut, taxa_mut = 1))
        self.salas = novas_salas
        self.geracao += 1

    def avaliar_resultados(self):
        self.salas.sort(key=lambda sala: sala.pontos, reverse=True)
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
            if self.contador.value >= len(self.salas)-1:
                self.vou_recriar -= 1
                if self.vou_recriar == 0:
                    self.state = "criando"
                    self.avaliar_resultados()
                    self.reproduzir()
                    self.contador.value = 0
                    self.mostrando = 0
                    self.vou_recriar = 3
                    # Finaliza processos antigos
                    for p in self.processos:
                        if p.is_alive():
                            p.terminate()
                    self.processos = []

    def render(self, screen):
        if self.salas[self.mostrando].repetiu:
            while self.salas[self.mostrando].repetiu:
                self.mostrando += 1
                if self.mostrando >= len(self.salas):
                    self.mostrando = 0
                    break

        self.salas[self.mostrando].render(screen)

def submotor(sala, finalizado, dt):
    while not sala.repetiu:
        sala.tick(dt)
        time.sleep(0.01)
    with finalizado.get_lock():
        finalizado.value += 1

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')  # Importante para compatibilidade cross-platform
    evoluidor = Evoluidor(n_salas=10, save=None)

    tick_time = 1.0/120.0
    while evoluidor.geracao < 100:
        evoluidor.tick(tick_time)
