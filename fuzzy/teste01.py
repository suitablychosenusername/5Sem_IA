import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control

# inputs
temp = control.Antecedent(np.arange(0,501,1), 'temp') # dominio, label
temp['cold'] = fuzz.trapmf(temp.universe, [0, 0, 110, 165]) # funcao de fuzzificacao
temp['cool'] = fuzz.trimf(temp.universe, [110, 165, 220])
temp['normal'] = fuzz.trimf(temp.universe, [165, 220, 275])
temp['warm'] = fuzz.trimf(temp.universe, [220, 275, 330])
temp['hot'] = fuzz.trapmf(temp.universe, [275, 330, 500, 500])
# temp.view()
# plt.show()

pres = control.Antecedent(np.arange(0,301,1), 'pres')
pres['weak'] = fuzz.trapmf(pres.universe, [0, 0, 10, 70])
pres['low'] = fuzz.trimf(pres.universe, [10, 70, 130])
pres['ok'] = fuzz.trimf(pres.universe, [70, 130, 190])
pres['strong'] = fuzz.trimf(pres.universe, [130, 190, 250])
pres['high'] = fuzz.trapmf(pres.universe, [190, 250, 300, 300])
# pres.view()
# plt.show()

# output
throttle = control.Consequent(np.arange(-60, 60, 1), 'throttle')
throttle['negative_large'] = fuzz.trapmf(throttle.universe, [-60, -60, -45, -30])
throttle['negative_med'] = fuzz.trimf(throttle.universe, [-45, -30, -15])
throttle['negative_small'] = fuzz.trimf(throttle.universe, [-30, -15, 0])
throttle['zero'] = fuzz.trimf(throttle.universe, [-15, 0, 15])
throttle['positive_small'] = fuzz.trimf(throttle.universe, [0, 15, 30])
throttle['positive_med'] = fuzz.trimf(throttle.universe, [15, 30, 45])
throttle['positive_large'] = fuzz.trapmf(throttle.universe, [30, 45, 60, 60])
# throttle.view()
# plt.show()

# regras
rules = []
rules.append(control.Rule(temp['cold'] & pres['weak'], throttle['positive_large']))
rules.append(control.Rule(temp['cold'] & pres['low'], throttle['positive_med']))
rules.append(control.Rule(temp['cold'] & pres['ok'], throttle['positive_small']))
rules.append(control.Rule(temp['cold'] & pres['strong'], throttle['negative_small']))
rules.append(control.Rule(temp['cold'] & pres['high'], throttle['negative_med']))

rules.append(control.Rule(temp['cool'] & pres['weak'], throttle['positive_large']))
rules.append(control.Rule(temp['cool'] & pres['low'], throttle['positive_med']))
rules.append(control.Rule(temp['cool'] & pres['ok'], throttle['zero']))
rules.append(control.Rule(temp['cool'] & pres['strong'], throttle['negative_med']))
rules.append(control.Rule(temp['cool'] & pres['high'], throttle['negative_med']))

rules.append(control.Rule(temp['normal'] & pres['weak'], throttle['positive_med']))
rules.append(control.Rule(temp['normal'] & pres['low'], throttle['positive_small']))
rules.append(control.Rule(temp['normal'] & pres['ok'], throttle['zero']))
rules.append(control.Rule(temp['normal'] & pres['strong'], throttle['negative_small']))
rules.append(control.Rule(temp['normal'] & pres['high'], throttle['negative_med']))

rules.append(control.Rule(temp['warm'] & pres['weak'], throttle['positive_med']))
rules.append(control.Rule(temp['warm'] & pres['low'], throttle['positive_small']))
rules.append(control.Rule(temp['warm'] & pres['ok'], throttle['negative_small']))
rules.append(control.Rule(temp['warm'] & pres['strong'], throttle['negative_med']))
rules.append(control.Rule(temp['warm'] & pres['high'], throttle['negative_large']))

rules.append(control.Rule(temp['hot'] & pres['weak'], throttle['positive_small']))
rules.append(control.Rule(temp['hot'] & pres['low'], throttle['positive_small']))
rules.append(control.Rule(temp['hot'] & pres['ok'], throttle['negative_med']))
rules.append(control.Rule(temp['hot'] & pres['strong'], throttle['negative_large']))
rules.append(control.Rule(temp['hot'] & pres['high'], throttle['negative_large']))

# Sistema controlador
valvula_controle = control.ControlSystem(rules)

# objeto de sistema
v1 = control.ControlSystemSimulation(valvula_controle)

# teste
v1.input['temp'] = 210
v1.input['pres'] = 50
v1.compute()
print(v1.output['throttle'])

temp.view(sim=v1)
pres.view(sim=v1)
throttle.view(sim=v1)
plt.show()