from engrenagem import Engrenagem
import numpy as np

class Parede():
    def __init__(self, preset = None) -> None:
        if preset == None:
            self.inicializaAleatorio()

    def inicializaAleatorio(self):
        self.objetos = [] # lista de Objeto
        self.objetos.append(Engrenagem(np.array([300.,300.,0.]), 10, velocidade=np.array([0.,1,0.]), massa=2))
        self.objetos.append(Engrenagem(np.array([300.,400.,0.]), 10))

    def tick(self):
        for i in range(len(self.objetos)):
            for j in range(i+1, len(self.objetos)):
                if self.objetos[i].detectarColisao(self.objetos[j]):
                    self.objetos[i].colidir(self.objetos[j])
                
        for objeto in self.objetos:
            objeto.tick()
        

    def render(self, screen):
        for objeto in self.objetos:
            objeto.render(screen)