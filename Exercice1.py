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


def calcul_erreur(p1=0, p2=0, p3=0, p4=0, debut=0, fin=1, n=100):
    val_sqr, temps_sqr = solve_integration_square(p1, p2, p3, p4, debut, fin, n)
    val_numpy, temps_numpy = solve_integration_numpy(p1, p2, p3, p4, debut, fin, n)
    if val_sqr > val_numpy:
        erreur = val_sqr-val_numpy
    elif val_sqr <= val_numpy:
        erreur = val_sqr - val_numpy
    return erreur, temps_sqr - temps_numpy


def afficher_erreur(p1=0, p2=0, p3=0, p4=0, debut=0, fin=1):
    n = np.linspace(10,1000,100, dtype=int)
    erreur=[]
    temps=[]
    for j in range(100):
        resultat = calcul_erreur(p1, p2, p3, p4, debut, fin, n[j])
        erreur.append(resultat[0])
        temps.append(resultat[1])
    plt.plot(n, erreur)
    plt.xlabel("n")
    plt.ylabel("erreur")
    plt.title("Evolution de l'erreur en fonction de n")
    plt.show()
    print(erreur)


afficher_erreur(1,1,6,5,0,10)
