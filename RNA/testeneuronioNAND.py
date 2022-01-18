import numpy as np

class Neuron:
    def __init__(self, bias, result):
        self.bias = bias
        self.result = result
        
    def somatoria(self, input, weight):
        montante = 0
        for i, w in zip(input, weight):
            montante += i * w
        return montante + self.bias

    @staticmethod
    def transf(soma):
        if soma <= 0.5:
            return 0
        else:
            return 1

    @staticmethod
    def erro(output, desejada):
        # desejada = 1
        return desejada - output

    @staticmethod
    def correcao(c, input, erro):
        return c * input * erro

    @staticmethod
    def ajuste(weight, fatorCorrecao):
        return weight + fatorCorrecao

    def compute(self, input, weight):
        output = self.transf(self.somatoria(input, weight))
        print(output)
        while True:
            if output == self.result:
                print('sucesso')
                break
            else:
                wnew = []
                print('corrigindo')
                for i, w in zip(input, weight):
                    wnew.append(self.ajuste(w, self.correcao(0.5, i, self.erro(output, self.result))))
                weight = wnew.copy()
                wnew.clear()
                print("pesos corrigidos:", weight)
                output = self.transf(self.somatoria(input, weight))
                print(output)
        return output

input = []
weight = []

input.append(0)
input.append(0)

weight.append(-0.25)
weight.append(-0.25)

nNAND = Neuron(1, not(input[0] == 1 and input[1] == 1)) # bias = 1
x = nNAND.compute(input, weight)

print(x)



