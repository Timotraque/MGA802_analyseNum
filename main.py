# Fichier principal du projet B
from Exercice2 import *

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
surchauffe = surchauffe_initiale(x0, y0, amplitude, sigma, n_x, n_y, xx, yy)

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
