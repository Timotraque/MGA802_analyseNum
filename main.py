# Fichier principal du projet B
import numpy as np
import matplotlib.pyplot as plt


def creer_grille(x, y, n_x, n_y):
    x = np.linspace(0, longueur, n_x)
    y = np.linspace(0, largeur, n_y)
    xx, yy = np.meshgrid(x, y)

    return xx,yy

def calcul_intial(x0, y0, xx, yy, A, sigma):
    delta_t = A * np.exp(-(np.power(xx - x0, 2)/(2 * np.power(sigma,2)) + np.power(yy - y0, 2)/(2 * np.power(sigma, 2)) ))
    import pdb; pdb.set_trace()
    return delta_t

def afficher_grid(longueur, largeur, delta_t):
    h = plt.contourf(longueur, largeur, delta_t)
    plt.axis('scaled')
    plt.colorbar()
    plt.show()

longueur = 1
largeur = 1
n_x = 100
n_y = 100
x = np.linspace(0, longueur, n_x)
y = np.linspace(0, largeur, n_y)

xx, yy = creer_grille(longueur, largeur, n_x, n_y)
temp = calcul_intial(50, 50, xx, yy, 200, 0.1)
#afficher_grid(x, y, temp)
