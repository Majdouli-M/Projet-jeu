import numpy as np
import random
import rooms_data
import pygame

pygame.init()

#A: matrice des portes de la room actuelle du joueur
#chosen_id: id des rooms tirées

def aligner_matB_avec_matA(current_room_portes, rooms_id, dir):
    """
    Aligne la matrice B par rapport à la matrice A sur le bord choisi (bords uniquement).
    

    Paramètres :
        A : np.array, matrice principale
        B : np.array, matrice à orienter
        dir : direction du bord de A à comparer
              0 = haut, 1 = bas, 2 = gauche, 3 = droite
    
    Retour :
        B_rot : matrice B orientée pour que le bord corresponde à A
    """

    
    B = [np.array(rooms_data.rooms[i].portes) for i in rooms_id]
    room_images = [rooms_data.rooms[i].image for i in rooms_id]
    for i in range(0,len(B)):
        

        for _ in range(4):
            # Extraire la ligne ou colonne de B selon la direction
            if dir == (0,-1):  # haut
                bord_B = B[i][-1, :]        # ligne du bas de B
                target = current_room_portes[0, :]
            elif dir == (0,1):  # bas
                bord_B = B[i][0, :]         # ligne du haut de B
                target = current_room_portes[-1, :]
            elif dir == (-1,0):  # gauche
                bord_B = B[i][:, -1]        # colonne droite de B
                target = current_room_portes[:, 0]
            elif dir == (1,0):  # droite
                bord_B = B[i][:, 0]         # colonne gauche de B
                target = current_room_portes[:, -1]

            if np.array_equal(bord_B, target):
                break
            
            # Rotation horaire 90°
            B[i] = np.rot90(B[i], k=-1)
            
            room_images[i] = pygame.transform.rotozoom(room_images[i], -90, 1)
        
    return B,room_images



A = np.array([  [' ',' ',' '],['#',' ',' '], [' ','#',' ']      ])
B = ["r12","r9","r9" ]


B1,ims = aligner_matB_avec_matA(A,B,(-1,0))



print(B1[0])




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
sys.exit()
# ---------------------------------
