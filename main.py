# Fichier principal du projet B
import numpy as np
import matplotlib.pyplot as plt

def creer_grille(longueur, largeur, delta_x, delta_y):
    x = np.arange(0, longueur, delta_x)
    y = np.arange(0, largeur, delta_y)
    xx, yy = np.meshgrid(x, y)

    return xx,yy


def surchauffe_initiale(x0, y0, xx, yy, A, sigma, n_x, n_y):
    delta_temp = np.ndarray(shape=(n_x+1,n_y+1), dtype=float)
    delta_temp = A * np.exp(-(np.power(xx - x0, 2)/(2 * np.power(sigma,2)) +
                              np.power(yy - y0, 2)/(2 * np.power(sigma, 2))))

    return delta_temp

def afficher_grille(longueur, largeur, temperature):
    h = plt.contourf(longueur, largeur, temperature, cmap='hot')
    plt.axis('scaled')
    plt.colorbar()
    plt.show()

def enregistrer_grille_jpeg(longueur, largeur, temperature, numero):
    h = plt.contourf(longueur, largeur, temperature,cmap='hot')
    plt.axis('scaled')
    plt.colorbar()
    nom_fichier = f"Temperature_{numero}.jpeg"
    plt.savefig(nom_fichier,)

def calcul_RHS(RHS, temperature, longueur, largeur, k, delta_x, delta_y):
    # On suppose que delta_x = delta_y
    # Pour avoir la même forme et le même type de variables

    # Aux limites du domaine le RHS vaut 0
    RHS[0, :] = 0
    RHS[:, largeur - 1] = 0
    RHS[:, 0] = 0
    RHS[:, longueur - 1] = 0

    # Parcours toute la grille
    for x in range(1, int(longueur / delta_x) - 1):
        for y in range(1, int(largeur / delta_y) - 1):
            # Calcul le nouvel RHS
            RHS[x, y] = k * (((temperature[x + 1, y] - 2 * temperature[x, y] + temperature[x - 1, y]) / (
                np.power(delta_x, 2))) + ((temperature[x, y + 1] - 2 * temperature[x, y] + temperature[x, y - 1]) / (
                np.power(delta_y, 2))))

            if RHS[x, y] < 1:
                RHS[x, y] = 0

    # Force les limites a nouveau
    RHS[0, :] = 0
    RHS[:, largeur - 1] = 0
    RHS[:, 0] = 0
    RHS[:, longueur - 1] = 0

    # Renvoie une grille contenant tous les RHS

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

# [m²/s] Diffusivité thermique pour l'Aluminium
k = 98.8 * 10**(-6)

# Temperature iniriale hor zone point chaud
T_zero = 300

# temps total de simulation [s]
temps_simulation = 40

longueur = 1    #[m]
largeur = 1     #[m]
sigma = 0.05
n_x=8
n_y=8
x0=0.5
y0=0.5
# [k] Amplitude de la surchauffe au centre"""
amplitude = 200

#facteur de relaxation de fourrier
f0 = 0.25
numero = 0
delta_x = longueur / (n_x+1)
delta_y = largeur / (n_y+1)
dt = min((f0 * np.power(delta_x,2) / k ), (f0 * np.power(delta_y,2) / k))



x = np.arange(0, longueur,delta_x)
y = np.arange(0, longueur,delta_y)

xx,yy = creer_grille(longueur, largeur,delta_x,delta_y)

#import pdb; pdb.set_trace()
surchauffe = surchauffe_initiale(x0, y0, xx, yy, amplitude, sigma, n_x, n_y)

RHS = np.ndarray(shape=(n_x+1, n_y+1,int(temps_simulation/dt)), dtype=float)
temperature = np.ndarray(shape=(n_x+1, n_y+1,int(temps_simulation/dt)), dtype=float)
temperature[:,:,0] =surchauffe+T_zero

"""
for i in range(1000):
    RHS = calcul_RHS(RHS, temp, longueur, largeur, k, delta_x, delta_y)
    nouveau_temp = calcul_T(RHS, temp, dt, longueur, largeur, delta_x, delta_y)
    temp = nouveau_temp
    import pdb;

    pdb.set_trace()"""

