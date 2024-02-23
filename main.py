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


def calcul_RHS(temperature, longueur, largeur, x0, y0, xx, yy, k, dt):
    f0 = 0.25
    delta_x = int(k * dt / f0)
    delta_y = delta_x
    # On suppose que delta_x = delta_y

    RHS = temperature   #Pour avoir la même forme et le même type de variables

    # Aux limites du domaine le RHS vaut 0
    RHS[0,:] = 0
    RHS[:, largeur - 1] = 0
    RHS[:,0] = 0
    RHS[:, longueur - 1] = 0

    # Parcours toute la grille
    for x in range(1, longueur-1):
        for y in range(1, largeur-1):

            # Calcul le nouvel RHS
            RHS[x,y] = k * ((temperature[x + delta_x, y] - 2 * temperature[x, y] + temperature[x - delta_x, y])/(np.power(delta_x, 2)) +
                    (temperature[x, y + delta_y] - 2 * temperature[x, y] + temperature[x, y - delta_y])/(np.power(delta_y, 2)))

    # Renvoie une grille contenant tous les RHS
    return RHS


def calcul_T(grille_RHS, ancien_T, dt, longueur, largeur):
    t_n1 = ancien_T
    for x in range(longueur):
        for y in range(largeur):
            t_n1[x, y] = ancien_T[x, y] + dt * grille_RHS[x, y]
    return t_n1

longueur = 10
largeur = 10
n_x = 100
n_y = 100
x = np.linspace(-longueur/2, longueur/2, n_x)
y = np.linspace(-largeur/2, largeur/2, n_y)
x0 = 0
y0 = 0
k = 98.8 # Valeur de diffusivité thermique pour l'Aluminium
dt = 0.01 #s


xx, yy = creer_grille(longueur, largeur, n_x, n_y)
temp = calcul_intial(x0,y0, xx, yy, 200, 0.1)
RHS = calcul_RHS(temp, longueur, largeur, x0, y0, xx, yy, k, dt)
nouveau_temp = calcul_T(RHS,temp,dt,longueur,largeur)
import pdb; pdb.set_trace()

#afficher_grid(x, y, temp)

