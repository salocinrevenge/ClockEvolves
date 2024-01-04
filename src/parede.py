class Parede():
    def __init__(self, preset = None) -> None:
        self.objetos = [] # lista de Objeto

    def tick(self):
        for i in range(len(self.objetos)):
            for j in range(len(self.objetos)):
                if i != j:
                    self.objetos[i].colidir(self.objetos[j])
                
        for objeto in self.objetos:
            objeto.tick()
        

    def render(self, screen):
        for objeto in self.objetos:
            objeto.render(screen)