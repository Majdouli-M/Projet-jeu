import numpy as np
import random
import rooms_data
import pygame
from constantes import *
pygame.init()

#A: matrice des portes de la room actuelle du joueur
#chosen_id: id des rooms tirées
"""
def tirer_avec_rarity_1ere():


    liste_ids = list(rooms_data.rooms.keys())
    rarity = list(rooms_data.rooms[i].rarity for i in liste_ids)
    # On inverse la rareté pour obtenir un poids (1 = très commun)
    poids = [1/(r+1) for r in rarity]  
    valeurs_tirees = []
    # On tire n valeurs pondérées
    while (np.sum([rooms_data.rooms[i].rarity == 0 for i in valeurs_tirees]) == False):

        valeurs_tirees = random.choices(liste_ids, weights=poids, k=3)
    return valeurs_tirees
"""




"""

if ims and isinstance(ims[0], pygame.Surface):

    # L'image que nous voulons afficher
    image_a_afficher = ims[0]
    
    # Récupérer la taille de l'image pour créer une fenêtre adaptée
    largeur, hauteur = image_a_afficher.get_size()
    
    # Définir la taille de la fenêtre (un peu plus grande que l'image)
    TAILLE_FENETRE = (largeur + 100, hauteur + 100)
    POSITION_IMAGE = (50, 50) # Où dessiner l'image (avec une marge de 50px)
    COULEUR_FOND = (0, 0, 0) # Fond noir

    # Créer la fenêtre
    screen = pygame.display.set_mode(TAILLE_FENETRE)
    pygame.display.set_caption(f"Affichage de ims[0] ({largeur}x{hauteur})")

    # Boucle principale pour garder la fenêtre ouverte
    running = True
    while running:
        # Gérer les événements (pour fermer la fenêtre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Appuyer sur Echap pour quitter
                    running = False

        # --- Logique de dessin ---
        
        # 1. Remplir l'écran avec une couleur de fond
        screen.fill(COULEUR_FOND)
        
        # 2. "Blitter" (dessiner) votre image sur l'écran
        # ) being drawn onto the 'screen' surface at 'POSITION_IMAGE']
        screen.blit(image_a_afficher, POSITION_IMAGE)
        
        # 3. Mettre à jour l'affichage pour montrer ce qui a été dessiné
        pygame.display.flip()

else:
    print("Erreur : 'ims' est vide ou ims[0] n'est pas une Surface Pygame.")
    print("Veuillez vérifier votre fichier 'rooms_data.py' et que les images sont chargées.")

# Quitter proprement Pygame
pygame.quit()
"""


 



def tirage():

    """ Tire aléatoirement 3 éléments d'une liste donnée (avec répétition possible).

    Args:
        liste (list): liste source
        n (int): nombre d'éléments à tirer

    Returns:
        list: liste de n éléments choisis au hasard."""
   
    liste_ids = list(rooms_data.rooms.keys())
    
    liste_ids_0 = [i for i in rooms_data.rooms.keys() if rooms_data.rooms[i].rarity == 0]
    
    rarity = list(rooms_data.rooms[i].rarity for i in liste_ids)
    # On inverse la rareté pour obtenir un poids (1 = très commun)
    poids = [1/(r+1) for r in rarity]  
    target_x, target_y = 0,8
    dir = (-1,0)
    current_room_portes = np.array(rooms_data.rooms["g4"].portes)
    valide = False
    chosen_ids = [0,0,0]
    chosen_ids_portes = [0,0,0]
    chosen_ids_images = [0,0,0]



    j = 0
    while j < 3:
        
        valide = False
        while not(valide):

            

            if j == 0:
                chosen_id = random.choices(liste_ids_0)
                

            else:

                chosen_id = random.choices(liste_ids, weights=poids)
            
            chosen_ids[j] = chosen_id[0]
            

            
            chosen_ids_portes[j] = np.array(rooms_data.rooms[chosen_ids[j]].portes)
            chosen_ids_images[j] = rooms_data.rooms[chosen_ids[j]].image
            
            
                

            for _ in range(4):
                # Extraire la ligne ou colonne de B selon la direction
                if dir == (0,-1):  # haut
                    bord = chosen_ids_portes[j][-1, :]        # ligne du bas de B
                    target = current_room_portes[0, :]
                elif dir == (0,1):  # bas
                    bord = chosen_ids_portes[j][0, :]         # ligne du haut de B
                    target = current_room_portes[-1, :]
                elif dir == (-1,0):  # gauche
                    bord = chosen_ids_portes[j][:, -1]        # colonne droite de B
                    target = current_room_portes[:, 0]
                elif dir == (1,0):  # droite
                    bord = chosen_ids_portes[j][:, 0]         # colonne gauche de B
                    target = current_room_portes[:, -1]

                if np.array_equal(bord, target):
                    break
                    
                # Rotation horaire 90°
                chosen_ids_portes[j] = np.rot90(chosen_ids_portes[j], k=-1)
                    
                chosen_ids_images[j] = pygame.transform.rotozoom(chosen_ids_images[j], -90, 1)        




            
            #print(chosen_ids_portes[j][:,0])
            #print(np.array([' ', '#', ' ']))
            if (target_x == GRID_WIDTH-1 and np.array_equal(chosen_ids_portes[j][:,-1],np.array([' ', '#', ' '])  )) or (target_x == 0 and np.array_equal(chosen_ids_portes[j][:,0],np.array([' ', '#', ' '])  )): #on nentre jamais dans ce if
                #print("pas bon")
                valide = False

            else:
                #print("bon")
                valide = True
                j +=1
                

            




    return chosen_ids,chosen_ids_portes,chosen_ids_images



a,b,c = tirage()

#print(b[0])
#print(b[1])
#print(b[2])


# ---------------------------------
