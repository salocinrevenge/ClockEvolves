from sala import Sala
import os

class Evoluidor():
    def __init__(self):
        os.makedirs("save/evolucao", exist_ok=True)
        self.ultimo_id = 0
        while True:
            if not os.path.exists(f"save/evolucao/{self.ultimo_id}"):
                break
            self.ultimo_id += 1
        self.ultimo_id = self.ultimo_id
        os.makedirs(f"save/evolucao/{self.ultimo_id}", exist_ok=True)

        self.iniciar_salas(n_salas = 1)
        self.geracao = 0

    def iniciar_salas(self, n_salas):
        with open(f"save/evolucao/{self.ultimo_id}/estados.txt", "w") as f:
            f.write(f"{n_salas} individuos \n")
        self.salas = []
        for _ in range(n_salas):
            self.salas.append(Sala())

    def reproduzir(self):
        novas_salas = [Sala(pais = [self.salas[0]], percents = [1], n_mut = 10, taxa_mut = 0.1)]
        self.salas = novas_salas

    def avaliar_resultados(self):
        # ordena as salas com base no valor numero_estados_sem_repetir
        self.salas.sort(key=lambda sala: sala.numero_estados_sem_repetir, reverse=True)
        # salva o resultado da melhor sala
        self.salas[0].salvar_sala(f"save/evolucao/{self.ultimo_id}/{self.geracao}.txt")
        n_estados = []
        for sala in self.salas:
            n_estados.append(sala.numero_estados_sem_repetir)
        with open(f"save/evolucao/{self.ultimo_id}/n_estados.txt", "w") as f:
            f.write(f"\n Geracao {self.geracao}: ".join(map(str, n_estados)))

    def tick(self, dt):
        alguem_rodando = False
        for sala in self.salas:
            sala.tick(dt)
            if not sala.repetiu:
                alguem_rodando = True
        if not alguem_rodando:
            print("ta na hora de reproduzir")
            self.avaliar_resultados()
            self.reproduzir()


    def render(self, screen):
        self.salas[0].render(screen)