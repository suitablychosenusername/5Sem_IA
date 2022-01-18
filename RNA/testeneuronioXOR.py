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
    def transf(soma): # funcao de transformacao se y <= 0.5, y = 0, senao, y = 1
        if soma <= 0.5:
            return 0
        else:
            return 1

    @staticmethod
    def erro(output, desejada): # funcao de calculo de erro E = Sd - So
        return desejada - output

    @staticmethod
    def correcao(c, input, erro): # funcao de correcao F = c * x * E
        return c * input * erro

    @staticmethod
    def ajuste(weight, fatorCorrecao): # funcao de ajuste wn = wa + F
        return weight + fatorCorrecao

    def compute(self, input, weight): # funcao para computar o neuronio (ja aplica as correcoes e imprime a resposta)
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
weightNAND = []
weightOR = []

input.append(0)
input.append(1)

weightNAND.append(-0.25)
weightNAND.append(-0.25)

weightOR.append(1)
weightOR.append(1)

nNAND = Neuron(1, int(not(input[0] == 1 and input[1] == 1))) # bias = 1
nOR = Neuron(0, int(input[0] == 1 or input[1] == 1))

outputLayer1 = []
weightAND =[]

outputLayer1.append(nNAND.compute(input, weightNAND))
outputLayer1.append(nOR.compute(input, weightOR))

weightAND.append(0.5)
weightAND.append(0.5)

nAND = Neuron(0, int(outputLayer1[0] == 1 and outputLayer1[1] == 1))
print(nAND.compute(outputLayer1, weightAND))

