from sala import Sala
import os
import threading
import time

class Evoluidor():
    def __init__(self, n_salas = 4, save = None):
        # save = "save/salvo.txt"
        os.makedirs("save/evolucao", exist_ok=True)
        self.ultimo_id = 0
        while True:
            if not os.path.exists(f"save/evolucao/{self.ultimo_id}"):
                break
            self.ultimo_id += 1
        self.ultimo_id = self.ultimo_id
        os.makedirs(f"save/evolucao/{self.ultimo_id}", exist_ok=True)

        self.iniciar_salas(n_salas = n_salas, save = save) # 4
        self.geracao = 0
        self.contador = [0]
        self.state = "criando"
        self.mostrando = 0
        self.debug = False
        self.n_geracoes = 0

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

    def colocar_outras_em_threads(self):
        for sala in self.salas:
            threading.Thread(target=submotor, args=(sala,self.contador, self.dt)).start()
        self.state = "rodando"

    def reproduzir(self):
        novas_salas = [Sala(pais = [self.salas[0]], percents = [1], n_mut = 0, taxa_mut = 0)]

        for i in range(1, len(self.salas)):
            novas_salas.append(Sala(pais = [self.salas[0], self.salas[1], self.salas[2]], percents = [0.7, 0.2, 0.1], n_mut = 10, taxa_mut = 1))
        self.salas = novas_salas
        self.geracao += 1

    def avaliar_resultados(self):
        # ordena as salas com base no valor numero_estados_sem_repetir
        self.salas.sort(key=lambda sala: sala.numero_estados_sem_repetir, reverse=True)
        # salva o resultado da melhor sala
        self.salas[0].salvar_sala(f"save/evolucao/{self.ultimo_id}/{self.geracao}.txt")
        n_estados = []
        for sala in self.salas:
            n_estados.append(sala.numero_estados_sem_repetir)
        with open(f"save/evolucao/{self.ultimo_id}/n_estados.txt", "a") as f:
            f.write(f"\nGeracao {self.geracao}: " + " ".join(map(str, n_estados)))


    def tick(self, dt):
        self.dt = dt

        if self.state == "criando":
            self.colocar_outras_em_threads()

        elif self.state == "rodando":
            if self.contador[0] == len(self.salas):
                self.state = "criando"
                self.avaliar_resultados()
                self.reproduzir()
                self.contador[0] = 0
                self.mostrando = 0



    def render(self, screen):
        if self.salas[self.mostrando].repetiu:
            while self.salas[self.mostrando].repetiu:
                self.mostrando += 1
                if self.mostrando >= len(self.salas):
                    self.mostrando = 0
                    break

        self.salas[self.mostrando].render(screen)


def submotor(sala, finalizado, dt):
    # sala é a sala a executar e "finalizado é uma lista com 1 unico numero representando quantos individuos terminaram"
    while not sala.repetiu:
        sala.tick(dt)
        time.sleep(0.01)
    finalizado[0] += 1
    

# if main
if __name__ == "__main__":
    evoluidor = Evoluidor(n_salas=10, save=None)

    tick_time = 1.0/120.0
    while evoluidor.geracao < 100:
        evoluidor.tick(tick_time)