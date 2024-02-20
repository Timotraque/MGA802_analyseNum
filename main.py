# Fichier principal du projet B
import numpy as np
import matplotlib.pyplot as plt


def creer_grille(x, y, n_x, n_y):
    x = np.linspace(0, longueur, n_x)
    y = np.linspace(0, largeur, n_y)
    xx, yy = np.meshgrid(x, y)

    return xx,yy


def calcul_intial(x0, y0, xx, yy, A, sigma):
    delta_t = np.ndarray
    delta_t = A * np.exp(-(np.power(xx - x0, 2)/(2 * np.power(sigma,2)) + np.power(yy - y0, 2)/(2 * np.power(sigma, 2))))
    #import pdb; pdb.set_trace()
    return delta_t


def afficher_grid(longueur, largeur, delta_t):
    h = plt.contourf(longueur, largeur, delta_t)
    plt.axis('scaled')
    plt.colorbar()
    plt.show()


def calcul_RHS(delta_t, longueur, largeur, x0, y0, xx, yy, k, dt):
    f0 = 0.25
    delta_x = k * dt / f0
    delta_y = delta_x                                                                                                   # On suppose que delta_x = delta_y
    RHS = k * ((delta_t[x0 + delta_x, y0] - 2 * delta_t[x0, y0] + delta_t[x0 - delta_x, y0])/(np.power(delta_x, 2)) +
               (delta_t[x0, y0 + delta_y] - 2 * delta_t[x0, y0] + delta_t[x0, y0 - delta_y])/(np.power(delta_y, 2)))

    # Aux limites du domaine le RHS vaut 0
    RHS[0, :] = 0
    RHS[:, 0] = 0
    RHS[longueur - 1, :] = 0
    RHS[:, largeur - 1] = 0
    return RHS


longueur = 10
largeur = 10
n_x = 100
n_y = 100
x = np.linspace(-longueur/2, longueur/2, n_x)
y = np.linspace(-largeur/2, largeur/2, n_y)
x0 = 0
y0 = 0
k = 98.8 # Valeur de diffusivité thermique pour l'Aluminium

xx, yy = creer_grille(longueur, largeur, n_x, n_y)
temp = calcul_intial(x0,y0, xx, yy, 200, 0.1)
#afficher_grid(x, y, temp)
afficher_grid(x, y , calcul_RHS(temp, longueur, largeur, x0, y0, xx, yy, k, 1))
