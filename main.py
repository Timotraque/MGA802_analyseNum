# Fichier principal du projet B
import numpy as np
import matplotlib.pyplot as plt
import time

def creer_grille(longueur, largeur, delta_x, delta_y):
    x = np.arange(0, longueur, delta_x)
    y = np.arange(0, largeur, delta_y)
    xx, yy = np.meshgrid(x, y)

    return xx,yy


def surchauffe_initiale(x0, y0, A, sigma, n_x, n_y):
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




print("Visualisation de la répartition de chaleur\nLe matériau utilisé est l'aluminium !")

print("Définissez la géométrie de la plaque de métal : ")
longueur = float(input("Longueur [m] : "))
largeur = float(input("Largeur [m] : "))

print("\nDéfinissez le point chaud : ")
amplitude = float(input("Temperature [K] : "))
sigma = float(input("Ecartement sigma : "))
x0 = float(input("Position longitudinale du point chaud [m] : "))
y0 = float(input("Position laterale du point chaud [m] : "))
T_zero = float(input("Température initiale [k] : "))

print("\nDéfinissez les paramètres de simulation :")
n_x = int(input("Nombre de points en x : "))
n_y = int(input("Nombre de points en y : "))
temps_simulation = float(input("Temps de simulation [s] : "))
temps_affiche = float(input("Temps de l'affichage [s] : "))
temps_affiche = temps_affiche - 10

delta_x = longueur / (n_x+1)
delta_y = largeur / (n_y+1)

x = np.arange(0, longueur,delta_x)
y = np.arange(0, longueur,delta_y)

#facteur de relaxation de fourrier
f0 = 0.25

# [m²/s] Diffusivité thermique pour l'Aluminium
k = 98.8 * 10**(-6)

# Lancement du chrono de simulation
tsimu_start=time.perf_counter()

dt = min((f0 * np.power(delta_x,2) / k ), (f0 * np.power(delta_y,2) / k))
xx, yy = creer_grille(longueur, largeur,delta_x,delta_y)

# Calcul de la temperature initiale à la surchauffe
surchauffe = surchauffe_initiale(x0, y0, amplitude, sigma, n_x, n_y)

# Calcul du RHS
RHS = np.zeros(shape=(n_x+1, n_y+1,int(temps_simulation/dt)), dtype=float)

# Création de la grille de la plaque et addition de la surchauffe
temperature = np.ndarray(shape=(n_x+1, n_y+1, int(temps_simulation/dt)), dtype=float)
temperature[:,:,0] = surchauffe + T_zero

# Affichage de la plaque
afficher_grille(x, y, temperature[:,:,0],"Temperature initiale")


pas = 0
while pas*dt < temps_affiche:

    RHS = calcul_RHS(RHS, temperature, n_x, n_y, delta_x, delta_y, k, pas)
    temperature[:, :, pas+1] = temperature[:, :, pas] + dt*RHS[:, :, 0]

    #import pdb; pdb.set_trace()
    pas +=1

temp_min = temperature[:, :, pas-1].min()
temp_max = temperature[:, :, pas-1].max()
temp_mean = temperature[:, :, pas-1].mean()

afficher_grille(x, y,temperature[:,:,pas-1],"Temperature finale")

print(f"En fin de simulation :\nLa température minimale vaut {temp_min} K\nLa température maximale vaut {temp_max} K\nLa température moyenne est {temp_mean} K")
print("Le temps de simulation est de {:.2} s".format(time.perf_counter()-tsimu_start))
