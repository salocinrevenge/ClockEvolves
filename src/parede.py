class Parede():
    def __init__(self, preset = None) -> None:
        self.objetos = [] # lista de Objeto

    def teste_coolisao(self, objeto):
        colisoes = []
        for alvo in self.objetos:
                if objeto is not alvo:
                    if objeto.colidir(alvo):
                        colisoes.append(alvo)
        return colisoes # util para ver colisoes quando criando sala (terremoto.tick)

    def tick(self):
        for objeto in self.objetos:
            objeto.tick()
            
        for objeto in self.objetos:
            objeto.colidirLimites((0, 800, 0, 800))

        for objeto in self.objetos:
            self.teste_coolisao(objeto)
                

        energia = 0
        for objeto in self.objetos:
            energia += objeto.energiaCinetica()+objeto.energiaPotencial()
        # print(energia)
        

    def render(self, screen):
        for objeto in self.objetos:
            objeto.render(screen)