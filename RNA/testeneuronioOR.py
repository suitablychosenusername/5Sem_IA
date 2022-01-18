
def somatoria(input, weight):
    montante = 0
    for i, w in zip(input, weight):
        montante += i * w
    return montante

def transf(soma):
    if soma <= 0.5:
        return 0
    else:
        return 1

def erro(output, desejada):
    return desejada - output

def correcao(c, input, erro):
    return c * input * erro

def ajuste(weight, fatorCorrecao):
    return weight + fatorCorrecao

input = []
weight = []

input.append(1)
input.append(1)

weight.append(1)
weight.append(1)

soma = somatoria(input, weight)
output = transf(soma)
print(output)

# resultado desejado
if input[0] == 1 or input[1] == 1:
    result = 1
else:
    result = 0

while True:
    if output == result:
        print('sucesso')
        break
    else:
        wnew = []
        print('corrigindo')
        for i, w in zip(input, weight):
            wnew.append(ajuste(w, correcao(0.5, i, erro(output, result))))
        weight = wnew.copy()
        wnew.clear()
        print("pesos corrigidos:", weight)
        output = transf(somatoria(input, weight))
        print(output)


