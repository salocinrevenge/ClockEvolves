import numpy as np

import matplotlib.pyplot as plt

def plotar(filename):
    with open(filename, 'r') as f:
        n_individuals = int(f.readline().split()[0])
        generations = []
        data = []
        
        for line in f:
            if line.startswith("Geracao"):
                values = list(map(int, line.split(":")[1].strip().split()))
                generations.append(int(line.split()[1][:-1]))
                data.append(values)
        
        data = np.array(data)
        
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(generations, data[:, 0], label='First Individual')
        plt.plot(generations, data[:, -1], label='Last Individual')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend()
        plt.title('First and Last Individual per Generation')
        
        plt.subplot(1, 2, 2)
        plt.imshow(data.T, aspect='auto', interpolation='nearest')
        plt.colorbar(label='Fitness')
        plt.xlabel('Generation')
        plt.ylabel('Individual')
        plt.title('All Individuals across Generations')
        
        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    plotar("save/evolucao/n_estados.txt")