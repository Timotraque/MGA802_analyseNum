# Module de l'exercice 1

import numpy as np
import matplotlib.pyplot as plt
import timeit

def solve_integration_numpy(p1=0, p2=0, p3=0, p4=0, debut=0, fin=10**10, n=100):
    start = timeit.default_timer()
    x = np.linspace(debut, fin, n)
    y = p1 + p2 * x + p3 * x**2 + p4 * x**3
    integration = np.trapz(y,x)
    return integration, timeit.default_timer() - start

resultat = solve_integration_numpy(1,1,0,6,0,100,1000)
print(f"Résultat de l'intégrale : {resultat[0]}\ntemps = {resultat[1]}")
