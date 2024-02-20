# Fichier principal du projet B
import numpy as np


def creer_grille(longueur, largeur, n_x, n_y):
    x = np.linspace(0, longueur, n_x)
    y = np.linspace(0, largeur, n_y)
    xx, yy = np.meshgrid(x,y)

    return xx,yy


creer_grille(1,1,100,100)
