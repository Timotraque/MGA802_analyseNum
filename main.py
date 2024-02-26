# Fichier principal du projet B
import numpy as np
import matplotlib.pyplot as plt


def creer_grille(longueur, largeur, delta_x, delta_y):
    x = np.arange(0, longueur, delta_x)
    y = np.arange(0, largeur, delta_y)
    xx, yy = np.meshgrid(x, y)

    return xx,yy


def calcul_intial(x0, y0, xx, yy, A, sigma, longueur, largeur, delta_x, delta_y):
    delta_temp = np.ndarray(shape=(int(longueur / delta_x), int(largeur / delta_y)), dtype=float)
    for x in range(1, int(longueur/delta_x)-1):
        for y in range(1, int(largeur/delta_y)-1):
            # Calcul ledelta de temperature
            delta_temp[x, y] = A * np.exp(-((np.power(x * delta_x - x0, 2) / (2 * np.power(sigma, 2))) + (np.power(y * delta_y - y0, 2) / (2 * np.power(sigma, 2)))))


    #delta_temp = A * np.exp(-(np.power(xx - x0, 2)/(2 * np.power(sigma,2)) + np.power(yy - y0, 2)/(2 * np.power(sigma, 2))))


    return delta_temp

def afficher_grid(longueur, largeur, delta_t):
    h = plt.contourf(longueur, largeur, delta_t)
    plt.axis('scaled')
    plt.colorbar()
    plt.show()


def calcul_RHS(RHS, temperature, longueur, largeur, k, delta_x, delta_y, x0,y0):

    # Aux limites du domaine le RHS vaut 0
    RHS[0, :] = 0
    RHS[largeur - 1, :] = 0
    RHS[:, 0] = 0
    RHS[:, longueur - 1] = 0

    # Parcours toute la grille
    """ for x in range(1, int(longueur/delta_x)-1):
         for y in range(1, int(largeur/delta_y)-1):
             # Calcul le nouvel RHS
             RHS[x, y] = k * (((temperature[x + 1, y] - 2 * temperature[x, y] + temperature[x - 1, y])/(np.power(delta_x, 2))) + ((temperature[x, y + 1] - 2 * temperature[x, y] + temperature[x, y - 1])/(np.power(delta_y, 2))))
             import pdb; pdb.set_trace()"""

    for x in range(int(x0/delta_x),int(longueur/delta_x)-1):
        for y in range(int(y0/delta_y), int(largeur / delta_y) - 1):
            RHS[x, y] = k * (((temperature[x + 1, y] - 2 * temperature[x, y] + temperature[x - 1, y])/(np.power(delta_x, 2))) + ((temperature[x, y + 1] - 2 * temperature[x, y] + temperature[x, y - 1])/(np.power(delta_y, 2))))

        for y in range(int(y0/delta_y),1):
            RHS[x, y] = k * (((temperature[x + 1, y] - 2 * temperature[x, y] + temperature[x - 1, y]) / (np.power(delta_x, 2))) + ((temperature[x, y + 1] - 2 * temperature[x, y] + temperature[x, y - 1]) / (np.power(delta_y, 2))))

    for x in range(int(x0 / delta_x), 1):
        for y in range(int(y0 / delta_y), int(largeur / delta_y) - 1):
            RHS[x, y] = k * (((temperature[x + 1, y] - 2 * temperature[x, y] + temperature[x - 1, y]) / (
                np.power(delta_x, 2))) + ((temperature[x, y + 1] - 2 * temperature[x, y] + temperature[x, y - 1]) / (
                np.power(delta_y, 2))))

        for y in range(int(y0 / delta_y), 1):
            RHS[x, y] = k * (((temperature[x + 1, y] - 2 * temperature[x, y] + temperature[x - 1, y]) / (
                np.power(delta_x, 2))) + ((temperature[x, y + 1] - 2 * temperature[x, y] + temperature[x, y - 1]) / (
                np.power(delta_y, 2))))

    # Force les limites a nouveau
    RHS[0, :] = 0
    RHS[largeur - 1, :] = 0
    RHS[:, 0] = 0
    RHS[:, longueur - 1] = 0

    # Renvoie une grille contenant tous les RHS

    return RHS


def calcul_T(grille_RHS, ancien_T, dt, longueur, largeur, delta_x, delta_y):
    t_n1 = np.ndarray(shape=(int(longueur / delta_x), int(largeur / delta_y)), dtype=float)
    for x in range(longueur):
        for y in range(largeur):
            t_n1[x, y] = ancien_T[x, y] + dt * grille_RHS[x, y]
            if t_n1[x,y] < 1:
                t_n1[x,y] = 0

    return t_n1


longueur = 1    #[m]
largeur = 1     #[m]
x0 = 0.5
y0 = 0.5
k = 98.8 * 10**(-6)     # [m²/s] Diffusivité thermique pour l'Aluminium
f0 = 0.25
n_x = 100
n_y = 100
amplitude = 200     # [k] Température au centre

delta_x = longueur / n_x
delta_y = largeur / n_y
dt = f0 * np.power(delta_x,2) / k

x = np.arange(-longueur/2, longueur/2,delta_x)
y = np.arange(-longueur/2, longueur/2,delta_y)
xx, yy = creer_grille(longueur, largeur, delta_x, delta_y)

temp_simu = 1# s
boucle_tempo = np.arange(0, temp_simu, dt)

list_of_events = []

# temp est le meshgrid sur lequel toutes les températures sont reportée à un instant t
"""temp = calcul_intial(x0, y0, xx, yy, amplitude, 0.1)
list_of_events.append(temp)
import pdb; pdb.set_trace()
for counter in range(len(boucle_tempo)):
    RHS = calcul_RHS(temp, n_x, n_y, k, delta_x, delta_y)
    nouveau_temp = calcul_T(RHS, temp, dt, n_x, n_y)
    temp = nouveau_temp
    list_of_events.append(nouveau_temp)"""

RHS = np.ndarray(shape=(int(longueur/delta_x), int(largeur/delta_y)), dtype=float)
temp = np.ndarray(shape=(int(longueur/delta_x), int(largeur/delta_y)), dtype=float)

liste_x = np.array(int(longueur/delta_x))
liste_y = np.array(int(largeur/delta_y))

delta_temp = calcul_intial(x0, y0, xx, yy, amplitude, 0.3,longueur, largeur, delta_x, delta_y)
temp = temp + delta_temp
import pdb; pdb.set_trace()

for i in range(1000):
    RHS = calcul_RHS(RHS, temp, longueur, largeur, k, delta_x, delta_y,x0,y0)
    nouveau_temp = calcul_T(RHS, temp, dt,longueur, largeur, delta_x, delta_y)
    temp = nouveau_temp
   # import pdb; pdb.set_trace()

afficher_grid(x, y, temp)
