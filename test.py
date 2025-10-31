import numpy as np
import random
def can_move(portes_joueur, portes_cible, direction):

    """
    Vérifie si les portes de deux matrices (NumPy) correspondent
    pour une direction donnée.
    """
    try:

        # On compare les tableaux, puis on vérifie si .all() (tous) sont True
        if direction == (0, -1) and (portes_joueur[0, :] == portes_cible[2, :]).all(): # Haut
            return True
        
        elif direction == (0, 1) and (portes_joueur[2, :] == portes_cible[0, :]).all(): # Bas
            return True
        
        elif direction == (-1, 0) and (portes_joueur[:, 0] == portes_cible[:, 2]).all(): # Gauche
            return True
        
        elif direction == (1, 0) and (portes_joueur[:, 2] == portes_cible[:, 0]).all(): # Droite
            return True
        
        else:
            return False
            
    except Exception as e:
        # Sécurité si les matrices n'ont pas la bonne forme
        print(f"Erreur dans can_move: {e}")
        return False
####

def tirer_valeurs_aleatoires(liste, n):
    valeurs_tirees = [random.choice(liste) for _ in range(n)]
    return valeurs_tirees



print(tirer_valeurs_aleatoires(["r1","r1","r3","r4","r5"],3))


