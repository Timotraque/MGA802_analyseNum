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


def solve_integration_square(p1=0, p2=0, p3=0, p4=0, debut=0, fin=1, n=100):
    start = timeit.default_timer()
    pas = (fin - debut)/n
    integration = 0

    x = []
    x.append(debut)
    for i in range(1, n+1):
        x.append(x[i-1] + pas)

    y = []
    for i in range(0, n+1):
        y.append(p1 + p2 * x[i] + p3 * x[i]**2 + p4 * x[i]**3)
        integration += pas * y[i]

    return integration, timeit.default_timer() - start

resultat_np = solve_integration_numpy(0,1,0,0,0,100,1000)
print(f"Résultat de l'intégrale : {resultat_np[0]}\ntemps = {resultat_np[1]}")

resultat_sqr = solve_integration_square(0,1,0,0,0,100,10)
print(f"Résultat de l'intégrale : {resultat_sqr[0]}\ntemps = {resultat_sqr[1]}")
