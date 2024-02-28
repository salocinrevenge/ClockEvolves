class Parede():
    def __init__(self, preset = None) -> None:
        self.objetos = [] # lista de Objeto

    def tick(self):
        for objeto in self.objetos:
            objeto.tick()
            
        for objeto in self.objetos:
            objeto.colidirLimites((0, 800, 0, 800))

        for i in range(len(self.objetos)):
            for j in range(len(self.objetos)):
                if i != j:
                    self.objetos[i].colidir(self.objetos[j])
                

        energia = 0
        for objeto in self.objetos:
            energia += objeto.energiaCinetica()+objeto.energiaPotencial()
        print(energia)
        

    def render(self, screen):
        for objeto in self.objetos:
            objeto.render(screen)