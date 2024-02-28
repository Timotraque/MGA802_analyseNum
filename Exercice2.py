# Fichier principal du projet B
import numpy as np
import matplotlib.pyplot as plt
import time

def creer_grille(longueur, largeur, delta_x, delta_y):
    x = np.arange(0, longueur, delta_x)
    y = np.arange(0, largeur, delta_y)
    xx, yy = np.meshgrid(x, y)

    return xx,yy


def surchauffe_initiale(x0, y0, A, sigma, n_x, n_y, xx, yy):
    delta_temp = np.ndarray(shape=(n_x+1,n_y+1), dtype=float)
    delta_temp = A * np.exp(-(np.power(xx - x0, 2)/(2 * np.power(sigma,2)) +
                              np.power(yy - y0, 2)/(2 * np.power(sigma, 2))))
    return delta_temp


def afficher_grille(longueur, largeur, temperature,titre):
    plt.title(titre)
    h = plt.contourf(longueur, largeur, temperature, cmap='hot')
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.axis('scaled')
    plt.colorbar()
    plt.show()
    plt.pause(3)
    plt.close()
    plt.clf()


def enregistrer_grille_jpeg(longueur, largeur, temperature, numero):
    h = plt.contourf(longueur, largeur, temperature,cmap='hot')
    plt.axis('scaled')
    plt.colorbar()
    nom_fichier = f"Temperature_{numero}.jpeg"
    plt.savefig(nom_fichier,)


def calcul_RHS(RHS, temperature, n_x, n_y, delta_x, delta_y, k, pas):
    # Aux limites du domaine le RHS vaut 0
    RHS[0, :, pas] = 0
    RHS[:, n_y, pas] = 0
    RHS[:, 0, pas] = 0
    RHS[n_x, :, pas] = 0

    # Calcul le nouvel RHS
    # import pdb; pdb.set_trace()
    RHS[1:n_x - 1, 1:n_y - 1, pas] = k * (((temperature[2:n_x, 1:n_y - 1, pas] -
                                            2 * temperature[1:n_x - 1, 1:n_y - 1, pas] + temperature[0:n_x - 2,
                                                                                         1:n_y - 1, pas]) / (
                                               np.power(delta_x, 2))) +
                                          ((temperature[1:n_x - 1, 2:n_y, pas] - 2 * temperature[1:n_x - 1, 1:n_y - 1,
                                                                                     pas] +
                                            temperature[1:n_x - 1, 0:n_y - 2, pas]) / (np.power(delta_y, 2))))

    # Remplacer les valeur RHS <1 par des zeros
    RHS[RHS < 1] = 0

    return RHS


def calcul_T(grille_RHS, ancien_T, dt, longueur, largeur, delta_x, delta_y):
    t_n1 = np.ndarray(shape=(int(longueur / delta_x), int(largeur / delta_y)), dtype=float)
    for x in range(longueur):
        for y in range(largeur):
            t_n1[x, y] = ancien_T[x, y] + dt * grille_RHS[x, y]
            if t_n1[x, y] < 1:
                t_n1[x, y] = 0
    return t_n1


"""____________________________________________
MAIN

_______________________________________________"""

