from parede import Parede
from engrenagem import Engrenagem
import numpy as np

class Terremoto():

    def __init__(self) -> None:
        pass

    def inicializaAleatorio(self):
        self.parede = Parede()
        self.parede.objetos.append(Engrenagem(np.array([300.,300.,0.]), 10, velocidade=np.array([1,1,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([500.,300.,0.]), 10, velocidade=np.array([-1,1,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([550.,250.,0.]), 10, velocidade=np.array([-4,4,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([400.,400.,0.]), 10))

        # self.parede.objetos.append(Engrenagem(np.array([300.,410.,0.]), 10))
        # self.parede.objetos.append(Engrenagem(np.array([350.,450.,0.]), 10))
        # self.parede.objetos.append(Engrenagem(np.array([400.,400.,0.]), 10))
        # self.parede.objetos.append(Engrenagem(np.array([450.,300.,0.]), 10))
        # self.parede.objetos.append(Engrenagem(np.array([500.,200.,0.]), 10))
        
        return self.parede