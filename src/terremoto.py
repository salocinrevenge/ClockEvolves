from parede import Parede
from engrenagem import Engrenagem
from viga import Viga
import numpy as np

class Terremoto():

    def __init__(self) -> None:
        pass

    def inicializaAleatorio(self):
        self.parede = Parede()
        self.parede.objetos.append(Engrenagem(np.array([300.,300.,0.]), 10, velocidade=np.array([1.,1.,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([500.,300.,0.]), 10, velocidade=np.array([-1.,1.,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([550.,250.,0.]), 10, velocidade=np.array([-4.,4.,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([200.,300.,0.]), 10, velocidade=np.array([1.,1.,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([100.,300.,0.]), 10, velocidade=np.array([-1.,1.,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([650.,250.,0.]), 10, velocidade=np.array([-4.,4.,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([400.,400.,0.]), 10))
        self.parede.objetos.append(Engrenagem(np.array([450.,600.,0.]), 10))

        self.parede.objetos.append(Engrenagem(np.array([300.,410.,0.]), 10))
        self.parede.objetos.append(Engrenagem(np.array([350.,450.,0.]), 10))
        self.parede.objetos.append(Engrenagem(np.array([450.,50.,0.]), 10, velocidade=np.array([1.,4.,0.]), massa=1))
        self.parede.objetos.append(Engrenagem(np.array([500.,200.,0.]), 10, velocidade=np.array([1.,1.,0.]), massa=1))

        self.parede.objetos.append(Viga(np.array([100.,200.,0.]), 100, 10, velocidade=np.array([1.,-3.,0.1]), massa=1))
        
        return self.parede