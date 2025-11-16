import pygame
from images_initialisation import screen,loaded_images
from constantes import *
import random
import ctypes
import game_state
import items_data
import rooms_data
import numpy as np
from collections import Counter
clock = pygame.time.Clock()




"""
Jeu de construction en grille utilisant Pygame.

Ce script gère :
- L'affichage du plateau de jeu (grille, joueur, interface)
- Les déplacements du joueur
- Le tirage aléatoire et la sélection de pièces à construire
- L'inventaire et les statistiques du joueur
"""



# --- Bloc anti-flou ajouté car les images des rooms étaient pixelisées ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        print("Avertissement : Impossible de régler la sensibilisation PPP (DPI).")



try:

    # Police pour le texte normal
    text_font = pygame.font.SysFont('Arial', 30,bold=True)
except pygame.error:
    print("Police 'Arial' non trouvée, utilisation de la police par défaut.")

    text_font = pygame.font.Font(None, 34)


















##############################################################################################


# --- Fonctions de dessin ---
# (draw_grid et draw_player_and_indicator dessinent toujours
# par rapport au coin (0,0)




def draw_grid():
    """
    Dessine la grille en lisant game_state.map_grid et  game_state.map_grid_images

    """
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            
            # 1. Trouve l'ID de la pièce à cette coordonnée
            room_id = game_state.map_grid[y][x] # ex: "r2" ou "0"
            
            # 2. Si ce n'est pas une case vide ("0")
            if room_id != "0":
                
                # 3. CONSTRUIT le nom du fichier image à partir de l'ID
                image_name_to_draw = game_state.map_grid[y][x]+".png"  
                
                # 4. Dessine l'image si elle a été chargée
                if image_name_to_draw in loaded_images:
                    image_surface = game_state.map_grid_images[y][x]
                    screen.blit(image_surface, (x * CELL_SIZE, y * CELL_SIZE))

def draw_player_and_indicator():
    """
    Dessine le contour représentant le joueur sur la grille.
    Rend plus epais la face du contour correspondant à la direction selectionnée par le joueur avec les touches zqsd
    
    """

    if not(game_state.inInventory):


        
            
        default_thickness = 2
        selected_thickness = 8 #le coté vers lequel le joueur regarde est plus epais que les autres
        player_rect = pygame.Rect(game_state.player_x * CELL_SIZE, game_state.player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        p_topleft = (player_rect.left, player_rect.top)
        p_topright = (player_rect.right - 1, player_rect.top)
        p_bottomleft = (player_rect.left, player_rect.bottom - 1)
        p_bottomright = (player_rect.right - 1, player_rect.bottom - 1)
        dx, dy = game_state.intended_direction
        thickness_top = default_thickness
        thickness_bottom = default_thickness
        thickness_left = default_thickness
        thickness_right = default_thickness
        new_x = game_state.player_x + dx
        new_y = game_state.player_y + dy
        is_move_valid = (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT)
        if (dx, dy) != (0, 0) and is_move_valid:
            if (dx, dy) == (0, -1): thickness_top = selected_thickness
            elif (dx, dy) == (0, 1): thickness_bottom = selected_thickness
            elif (dx, dy) == (-1, 0): thickness_left = selected_thickness
            elif (dx, dy) == (1, 0): thickness_right = selected_thickness
        pygame.draw.line(screen, WHITE, p_topleft, p_topright, thickness_top)
        pygame.draw.line(screen, WHITE, p_bottomleft, p_bottomright, thickness_bottom)
        pygame.draw.line(screen, WHITE, p_topleft, p_bottomleft, thickness_left)
        pygame.draw.line(screen, WHITE, p_topright, p_bottomright, thickness_right)


def draw_inventory_selection():
    """
    Dessine les 3 images de pièces proposées ET l'indicateur. à l'aide de la position de selection (game_state.room_on_offer)

    """
    
    
    # 1. Définir la géométrie
    
 
    start_x = GRID_PIXEL_WIDTH + 0.5*INV_CELL_SIZE 
    ecart = 1.1
    x_room_price = start_x-40
    
    # --- 2. Dessiner les 3 images de pièces ---
    
    # BUG 1 CORRIGÉ: La boucle était imbriquée. Elle doit être unique.
    for i in [-2,-1, 0, 1 ]: # Boucle sur les 3 slots: -1 (haut), 0 (milieu), 1 (bas)
        
       
                
        # Calcule la position Y de cette boîte (en utilisant ta logique)
        current_y = WINDOW_HEIGHT - (3 + ecart*i) *INV_CELL_SIZE
        

     
        # Récupère le bon room_id (index 0, 1, ou 2)

        
        if i != -2:


            room_id = game_state.rooms_on_offer[i + 1] # Convertit -1,0,1 en 0,1,2 car l'indicateur est initialement positionné sur la room du milieu 
                
            image_surface = pygame.transform.smoothscale(game_state.rooms_on_offer_images[i+1], (INV_CELL_SIZE, INV_CELL_SIZE))
            price_text_surface = text_font.render(str(rooms_data.rooms[room_id].price), True, BLACK)   
            
            # BUG 3 CORRIGÉ: Il ne faut pas multiplier les coordonnées
            screen.blit(image_surface, (start_x, current_y))
            screen.blit(price_text_surface, (x_room_price, current_y))
            
        elif i == -2:

            if game_state.inventory_indicator_pos != -2: # si l'indicateur n'est pas sur l'option Reroll

                    
                reroll_text = text_font.render("Reroll", True, BLACK) 
            else:
                reroll_text = text_font.render("Reroll", True, RED)  # si l'indicateur ests sur l'option Reroll on l'affiche en rouge
            screen.blit(reroll_text, (start_x, current_y))

            


        
    

    # --- 3. Dessiner l'indicateur (la boîte grise) ---
    
    # Calcule la position Y de la boîte sélectionnée (selon ta logique)
    cursor_y_pixel = WINDOW_HEIGHT - (3 + ecart*game_state.inventory_indicator_pos) * INV_CELL_SIZE

    thickness_selection = 7 # Augmenté pour la visibilité
    
    # Simplification: Utiliser draw.rect au lieu de 4 lignes
    if (game_state.inventory_indicator_pos != -2):

        selection_rect = pygame.Rect(start_x, cursor_y_pixel, INV_CELL_SIZE, INV_CELL_SIZE)
        pygame.draw.rect(screen, RED, selection_rect, thickness_selection, border_radius=5)

def draw_inventory_items():


    """
    Dessine les noms des items tirés au hasard lors dans l'inventaire
    
    """
    start_x = GRID_PIXEL_WIDTH + 0.5 * INV_CELL_SIZE



    title_y = WINDOW_HEIGHT - (4) * INV_CELL_SIZE

    text_surface = text_font.render("Items found:", True, BLACK)
    screen.blit(text_surface, (start_x, title_y))



    ecart = 0.5
    for i, item_id in enumerate(game_state.items_tirees+[""]): # on ajoute "" a la liste pour ajouter un indice pour l'option 'Leave'
        current_y = WINDOW_HEIGHT - (4 - ecart * (i+1)) * INV_CELL_SIZE

        # la condition type(item_id) == int pour verifier si l'index se trouve avant le caractere vide "" a la fin de la liste game_state.items_tirees
        if type(item_id) == int and i < (len(game_state.items_tirees)+1):

            if item_id < 100 :

                item_name = items_data.resource_items[item_id].name
            else:
                item_name = items_data.special_items[item_id].name
            # Crée la surface texte

        else:
            item_name = "Leave"



        if game_state.items_indicator_pos == i:

            text_surface = text_font.render(item_name, True, RED)

        else:
            text_surface = text_font.render(item_name, True, BLACK)


        

        
        # Affiche le texte sur l'écran
        screen.blit(text_surface, (start_x, current_y))

        


    



def tirage_items():


    """
    Tirage des items en fonction des pools de la room dans laquelle le joueur se trouve
    
    Returns
    ----------
        
    items_tirees : list[int]
                   La liste contenant les ids des items tirés aléatoirement
        
    """
    roomid = game_state.map_grid[game_state.player_y][game_state.player_x]
    #(ID, rarity_score, min value, max value),
    pool_resource = rooms_data.rooms[roomid].resource_pool
    pool_special = rooms_data.rooms[roomid].special_pool
    
    #calcul de min items
    min_items = 0
    for i in range(0,len(pool_special)): 

        min_items += pool_special[i][2]


    for i in range(0,len(pool_resource)):
        min_items += pool_resource[i][2]


    if min_items > rooms_data.rooms[roomid].max_items:  #si depassement a cause d'erreurs dans rooms_data.py
        min_items = rooms_data.rooms[roomid].max_items


    
    max_items = random.randint(min_items,rooms_data.rooms[roomid].max_items)



    min_special_items = rooms_data.rooms[roomid].min_special_items
    items_tirees = []

    
    tirage_1_item = ["Oui","Non"] #soit on obtient l'item soit on l'obtient pas



    

    


    if min_special_items == -1 : #on impose pas un ou des items speciaux a la room 



        for i in range(0,len(pool_special)):


            poids  = [1,pool_special[i][1]] #poids dans le cas ou on drop : 1/(1+pool_special[i][1])
                                            # poids dans le cas ou on drop pas : 1 - 1/(1+pool_special[i][1]) = pool_special[i][1]/(1+pool_special[i][1])
                                            # meme denominateur donc on a 1 le poids associé au cas ou on obtient l'objet et pool_special[i][1] le poids associé au cas ou on obtient pas l'objet

            tirage = random.choices(tirage_1_item,weights=poids ,k=pool_special[i][3])

            resultat = Counter(tirage)
            nb = resultat.get("Oui",0) #nombres de "Oui" obtenus <=> nb de fois que l'objet a été tiré

            if nb < pool_special[i][2]: #si on a tiré moins que le nb minimum droppable de cet item ()
                nb = pool_special[i][2]


            for _ in range(0,nb):
                if (len(items_tirees) < max_items and items_tirees.count(pool_special[i][0]) < pool_special[i][3]):

                    items_tirees.append(pool_special[i][0])

                else:
                    break
    else:   #si on impose un item special
        
        while (len(items_tirees) < min_special_items): 

            for i in range(0,len(pool_special)):


                proba = [1,pool_special[i][1]]

                tirage = random.choices(tirage_1_item,weights=proba,k=pool_special[i][3])

                resultat = Counter(tirage)
                nb = resultat.get("Oui",0)

                if nb < pool_special[i][2]: #si on a tiré moins que le nb minimum droppable de cet item ()
                    nb = pool_special[i][2]

                for _ in range(0,nb):
                    if (len(items_tirees) < max_items and items_tirees.count(pool_special[i][0]) < pool_special[i][3] ):

                        items_tirees.append(pool_special[i][0])

                    else:
                        break
    while ((len(items_tirees) < max_items )): #tirage des resource_items
        
        for i in range(0,len(pool_resource)):


            proba = [1,pool_resource[i][1]]

            tirage = random.choices(tirage_1_item,weights=proba,k=pool_resource[i][3])

            resultat = Counter(tirage)
            nb = resultat.get("Oui",0)
            
            if nb < pool_resource[i][2]: #si on a tiré moins que le nb minimum droppable de cet item 
                nb = pool_resource[i][2]

            print(f"{nb} pour {pool_resource[i][2]}")
            for _ in range(0,nb):
                if (len(items_tirees) < max_items and items_tirees.count(pool_resource[i][0]) < pool_resource[i][3] ):

                    items_tirees.append(pool_resource[i][0])

                else:
                    break




    return items_tirees    











def draw_inventory(font):
    """
    Dessine l'inventaire (statistiques) du joueur sur la surface de l'interface.
    
    Parameters
    ----------
        
    font: pygame.font.Font 
          police d'écriture à utiliser
        
    """
    
    # Position de départ pour dessiner (coin haut-gauche de l'UI + marge)
    start_x = WINDOW_WIDTH - 300
    start_y = 20
    line_height = 40 # Espace entre chaque ligne
    special_items_x = GRID_PIXEL_WIDTH+20
    special_items_y = 20
    special_items_title = "Items Permanents:"
    # Boucle sur l'inventaire (ex: {"Pas": 70, "Pieces": 0})
    for index, (key, value) in enumerate(game_state.inventory.items()):
        if key != "Items permanents":
            
            # 1. Crée le texte (ex: "Pas: 70")
            text_to_draw = f"{key}: {value}"
            
            # 2. Crée la surface de texte
            text_surface = font.render(text_to_draw, True, BLACK) # Texte en noir
            
            # 3. Calcule la position Y
            y_pos = start_y + (index * line_height)
            
            # 4. Dessine le texte sur l'écran
            screen.blit(text_surface, (start_x, y_pos))
    
    text_surface = font.render(special_items_title,True,BLACK)
    screen.blit(text_surface, (special_items_x, special_items_y))
    for index, item in enumerate(game_state.inventory["Items permanents"]):

        
                    # 1. Crée le texte (ex: "Pas: 70")
            
            
            # 2. Crée la surface de texte
            text_surface = font.render(items_data.special_items[item].name, True, BLACK) # Texte en noir
            
            # 3. Calcule la position Y
            special_items_y = special_items_y + ((index+1) * line_height)
            
            # 4. Dessine le texte sur l'écran
            screen.blit(text_surface, (special_items_x, special_items_y))

        # --- Affiche un message temporaire si défini ---
    now = pygame.time.get_ticks()
    if game_state.temp_message != None  and now <= game_state.duree_temp_message:

        msg_surf = font.render(game_state.temp_message, True, (0, 0, 0))
        msg_rect = msg_surf.get_rect(center=(GRID_PIXEL_WIDTH + UI_PIXEL_WIDTH // 2, WINDOW_HEIGHT - 50))
        
        screen.blit(msg_surf, msg_rect)
    elif game_state.temp_message != None and now > game_state.duree_temp_message:
        game_state.temp_message = None

            
            


        
def normaliser_portes(portes1):

    """
    Uniformise tous les états des portes par l'état de base ('#' -> porte ouverte)  

    Parameters
    ----------
        
    portes1 : numpy.array[str]
              La matrice des portes
        
    """
    lignes1,cols1 = np.where(portes1 != ' ')
    

    for y1,x1 in zip(lignes1,cols1): #on "normalise" la matrice avec les #
        portes1[y1,x1] = '#'
        
     

  



def can_move(portes_joueur, portes_cible):

    """
    Verifie si le joueur peut se deplacer vers la direction qu'il a choisi
    Parameters
    ----------
    portes_joueur : numpy.array | array
                    La matrice des portes du joueur

    portes_cible : numpy.array | array
                    La matrice des portes de la room vers laquelle le joueur se dirige
    
    Returns
    ----------
        
    Un booléen qui indique le resultat de la comparaison
        
    """
    p_joueur_tampon = np.array(portes_joueur)
    p_cible_tampon = np.array(portes_cible)
    
    normaliser_portes(p_joueur_tampon)
    normaliser_portes(p_cible_tampon)



    try:
        


        # On compare les tableaux
        if game_state.intended_direction == (0, -1) and np.array_equal(p_joueur_tampon[0, :] ,p_cible_tampon[2, :]) and np.array_equal(p_cible_tampon[2, :],[' ','#',' ']): # Haut
            return True
        
        elif game_state.intended_direction == (0, 1) and np.array_equal(p_joueur_tampon[2, :],p_cible_tampon[0, :]) and np.array_equal(p_cible_tampon[0, :],[' ','#',' ']) : # Bas
            return True
        
        elif game_state.intended_direction == (-1, 0) and np.array_equal(p_joueur_tampon[:, 0],p_cible_tampon[:, 2]) and np.array_equal(p_cible_tampon[:, 2],[' ','#',' ']): # Gauche
            return True
        
        elif game_state.intended_direction == (1, 0) and np.array_equal(p_joueur_tampon[:, 2] , p_cible_tampon[:, 0]) and np.array_equal(p_cible_tampon[:, 0],[' ','#',' ']): # Droite
            return True
        
        else:
            return False
            
    except Exception as e:
        # Sécurité si les matrices n'ont pas la bonne forme
        print(f"Erreur dans can_move: {e}")
        return False
    

def bord_portes_joueur(matrice_portes,dir): 
     
    """
    Retourne le cote de la matrice portes vers la direction choisie
    Parameters
    ----------
    matrice_portes : numpy.array | array
                    La matrice des portes du joueur
    dir : tuple[int,int]
          La direction du joueur
    
    Returns
    ----------
    La colonne ou la ligne de la matrice correspondant au coté de la matrice que le joueur regarde

                
    """
    if dir == (0,-1):  # haut

        return matrice_portes[0, :]
    elif dir == (0,1):  # bas
              # ligne du haut de B
        return matrice_portes[-1, :]
    elif dir == (-1,0):  # gauche
                # colonne droite de B
        return matrice_portes[:, 0]
    elif dir == (1,0):  # droite
            # colonne gauche de B
        return matrice_portes[:, -1]
    
def ouvrir_portes(matrice_portes):

    """

    Ouvre la porte (change '%' ou 'X' en '#') que le joueur souhaite traverser
    Parameters
    ----------
    matrice_portes : numpy.array 
                    La matrice des portes du joueur

    
    Returns
    ----------
    
    La colonne ou la ligne de la matrice correspondant au coté de la matrice que le joueur regarde
    """
    if game_state.intended_direction == (0,-1):  # haut

        matrice_portes[0, :] = [' ', '#',' ']
    elif game_state.intended_direction == (0,1):  # bas
              # ligne du haut de B
        matrice_portes[-1, :] = [' ', '#',' ']
    elif game_state.intended_direction == (-1,0):  # gauche

                # colonne droite de B
        matrice_portes[:, 0] = [' ', '#',' ']
    elif game_state.intended_direction == (1,0):  # droite
            # colonne gauche de B
        matrice_portes[:, -1] = [' ', '#',' ']




def tirage():

    """ Tire aléatoirement 3 éléments d'une liste donnée (avec répétition possible).



    Returns:
    --------
    chosen_ids : list[str]
                 Liste des ids des rooms tirées
    chosen_ids_portes : list[numpy.array]
                        Liste des matrice des portes des rooms tirées

    chosen_ids_images : list[pygame.image]
                        Liste des images des rooms tirées


    """
   
    liste_ids = list(rooms_data.rooms.keys())
    
    liste_ids_0 = [i for i in rooms_data.rooms.keys() if rooms_data.rooms[i].rarity == 0]
    
    rarity = list(rooms_data.rooms[i].rarity for i in liste_ids)
    # On inverse la rareté pour obtenir un poids (1 = très commun)
    poids = [1/(r+1) for r in rarity]  
    target_x, target_y = game_state.build_target_coords
    dir = game_state.intended_direction
    current_room_portes = np.array(game_state.map_grid_portes[game_state.player_y][game_state.player_x])
    normaliser_portes(current_room_portes)
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
                # Extraire la ligne ou colonne de chosen_ids_portes[j] selon la direction
                if dir == (0,-1):  # haut
                    bord = chosen_ids_portes[j][-1, :]        # ligne du bas de chosen_ids_portes[j]
                    target = current_room_portes[0, :]
                elif dir == (0,1):  # bas
                    bord = chosen_ids_portes[j][0, :]         # ligne du haut de chosen_ids_portes[j]
                    target = current_room_portes[-1, :]
                elif dir == (-1,0):  # gauche
                    bord = chosen_ids_portes[j][:, -1]        # colonne droite de chosen_ids_portes[j]
                    target = current_room_portes[:, 0]
                elif dir == (1,0):  # droite
                    bord = chosen_ids_portes[j][:, 0]         # colonne gauche de chosen_ids_portes[j]
                    target = current_room_portes[:, -1]

                if np.array_equal(bord, target): 

                    #conditions qui verifient que on est sur le bord de la map et qu'il n'y a pas de portes qui menent vers l'exterieur de la grille
                    if not(target_x == GRID_WIDTH-1 and np.array_equal(chosen_ids_portes[j][:,-1],np.array([' ', '#', ' '])  )) and not(target_x == 0 and np.array_equal(chosen_ids_portes[j][:,0],np.array([' ', '#', ' '])  )): 
                        if not(target_y == GRID_HEIGHT-1 and np.array_equal(chosen_ids_portes[j][-1,:],np.array([' ', '#', ' '])  )) and not(target_y == 0 and np.array_equal(chosen_ids_portes[j][0,:],np.array([' ', '#', ' '])  )):
                            valide = True
                            break   #si tout correspond on a une bonne pioche pas besoin de faire plus de rotations on garde celle ci

                
                    
                    
                # Rotation horaire 90° si les conditions pas respectees
                chosen_ids_portes[j] = np.rot90(chosen_ids_portes[j], k=-1)
                   
                chosen_ids_images[j] = pygame.transform.rotozoom(chosen_ids_images[j], -90, 1)      

        j+=1  #on passe a la room suivant (3 au total)






    return chosen_ids,chosen_ids_portes,chosen_ids_images




def random_doors_generation(matrice_portes,score_ouv,score_verr,score_dbverr):

    
    """
    Genere aléatoirement l'état de chaque porte d'une room 

    Parameters
    ----------
        
    matrice_portes : numpy.array[str]
                    La matrice des portes

    score_ouv : float | int
                score de rarité pour les portes ouvertes '#'

    score_verr : float | int
                 score de rarité pour les portes verrouillées '%'

    score_dbverr : float | int
                   score de rarité pour les portes verrouillées à double tour 'X'
        
    """







    ligne = 0
    col = 0
    if game_state.intended_direction == (0,-1):  # haut
        ligne,col = 2,1
        
        
    elif game_state.intended_direction == (0,1):  # bas
        ligne,col = 0,1
        
        
    elif game_state.intended_direction == (-1,0):  # gauche
        ligne,col = 1,2
        
        
    elif game_state.intended_direction == (1,0):  # droite
       ligne,col = 1,0
       

    lignes,cols = np.where(matrice_portes== '#' )                

    

    for y,x in zip(lignes,cols):
        """ 
            #: porte ouverte
            % porte verouillée
            X: porte verouillée à double tour   
        """

        choix = random.choices(["#","%","X"],weights=[score_ouv,score_verr,score_dbverr],k=1)
        print(choix[0])

        matrice_portes[y,x] = choix[0]


    matrice_portes[ligne,col] = '#' #on conserve l'etat ouvert de la porte par lequel le joueur va entrer





        




def difficulty_scaled_doors(matrice_portes,y):
    """
    Utilise random_doors_generation et fixe des score de rarités en fonction de la distance entre le joueur et la room d'arrivée AnteChamber

    Parameters
    ----------
        
    matrice_portes : numpy.array[str]
                    La matrice des portes

    y : int
        position du joueur en y sur la grille/map
        
    """    

    if y == 8:
        pass
    elif y <= 7  and y > 3:

        random_doors_generation(matrice_portes,0.5,1,0.5)

    elif y == 3:

        random_doors_generation(matrice_portes,0,0.5,2)  

    else:
        random_doors_generation(matrice_portes,0,0,1)  



    """  #: porte ouverte
        % porte verouillée
        X: porte verouillée à double tour   


        Y = 8 : ###
        Y = 7 à 4 : # %% X
        Y = 3  :  % XX
        Y = 2 à 0 : XXX


    """
   

# --- Boucle principale du jeu ---


"""
Boucle principale :
- Gère les événements clavier (déplacement, inventaire)
- Met à jour l'état du jeu
- Dessine la grille, le joueur et l'interface utilisateur
"""


running = True
print("Utilisez ZQSD pour choisir une direction.")
print("Appuyez sur ESPACE pour vous déplacer dans cette direction.")



while running:
    # --- Gestion des événements (Inchangée) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            running = False

        

        if event.type == pygame.KEYDOWN and not(game_state.game_lost) and not(game_state.game_won) :
                
                    
            # ------------------------------------------------------------------
            # CAS 1: Le joueur est dans l'inventaire pour selectionner des rooms
            # ------------------------------------------------------------------
            if game_state.inInventory:

                # selection avec les touches zqsd (indicateur initialement sur la map du milieu)
                if event.key == pygame.K_z:
                     
                    if game_state.inventory_indicator_pos < 1:

                        game_state.inventory_indicator_pos += 1
                elif event.key == pygame.K_s:
                    
                    if game_state.inventory_indicator_pos > -2: # indicateur à -2 -> option pour reroll

                        game_state.inventory_indicator_pos -= 1   
                        

                elif event.key == pygame.K_SPACE: # Le joueur VALIDE son choix de pièce
                    chosen_room_id = game_state.rooms_on_offer[game_state.inventory_indicator_pos+1] 


                    if game_state.inventory_indicator_pos == -2 and game_state.inventory["Des"] > 0:
                        game_state.rooms_on_offer,game_state.rooms_on_offer_mats,game_state.rooms_on_offer_images = tirage()
                        game_state.inventory["Des"] -= 1
                        break # on relance le tirage donc le code en dessous ne doit pas s'executer (interruption boucle for)
                    elif (game_state.inventory_indicator_pos == -2 and game_state.inventory["Des"] ==0) :

                        game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                        game_state.temp_message = "Pas assez de des"     
                        break

                    elif (game_state.inventory_indicator_pos >-2 and game_state.inventory["Gemmes"] < rooms_data.rooms[chosen_room_id].price):
                        game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                        game_state.temp_message = "Pas assez de gemmes"     
                        break
                    elif (game_state.inventory_indicator_pos >-2 and game_state.inventory["Gemmes"] >= rooms_data.rooms[chosen_room_id].price):

                        game_state.inventory["Gemmes"] -= rooms_data.rooms[chosen_room_id].price
                    

                        

                            
                    # 1. Récupère la pièce choisie dans l'inventaire
                    target_x, target_y = game_state.build_target_coords # Récupère les coords ou le joueur souhaite ajouter une room
                    chosen_room_id_portes = np.array(game_state.rooms_on_offer_mats[game_state.inventory_indicator_pos+1]) #id de la room que la joueur a choisi
                    chosen_room_id_image = game_state.rooms_on_offer_images[game_state.inventory_indicator_pos+1] # image de la room que le joueur a choisi         

                    # 2. generation aleatoire de l'etat des portes en fonction du niveau en y du joueur sur la map/grille


                    if chosen_room_id != "h4": #les portes du corridor sont toujours ouvertes

                        difficulty_scaled_doors(chosen_room_id_portes,target_y) # genere l'etat de chaque porte ( a l'exception de celle qu'on ouvre qui doit etre ouverte)
                    


                    # 3. Récupère l'id, la matrice de portes et l'image images associées
                    current_room_id = game_state.map_grid[game_state.player_y][game_state.player_x]
                    current_room_id_portes = np.array(game_state.map_grid_portes[game_state.player_y][game_state.player_x])


  
                    # 4. Vérifie si le placement est valide avec can_move()

                            
                    if can_move(np.array(current_room_id_portes), np.array(chosen_room_id_portes)):
                                
                         # 5. Placement RÉUSSI :
                        
                                
                        # Met à jour la carte
                        game_state.map_grid[target_y][target_x] = chosen_room_id
                        game_state.map_grid_portes[target_y][target_x] = chosen_room_id_portes


                        game_state.map_grid_images[target_y][target_x] = chosen_room_id_image
                        print(f"Vous avez construit : {chosen_room_id}")
                                

                                
                        # Quitte le mode inventaire
                        game_state.inInventory = False
                            
                    else: #on ne doit jamais tomber dans ce else sinon truc qui bug (c'est pas le cas normalement)

                        print(f"Placement impossible: Les portes de {chosen_room_id} ne correspondent pas.") # ce message ne doit jamais s'afficher si pas de bug

                        print(current_room_id_portes)  #pour voir ce qui va pas 
                        print(chosen_room_id_portes)  #
                        
                            
            # ------------------------------------------------------------------
            # CAS 2: Le joueur est dans l'inventaire pour selectionner des items
            # ------------------------------------------------------------------z

            elif game_state.items_selection:  

                if len(game_state.items_tirees) == 1: #si il y a eu une selection et que le joueur n'a pas eu de chance (rien eu) -> on quitte le menu de selection
                    
                    game_state.items_selection = False
                    if game_state.inventory["Pas"] <= 0: #activation flag game_lost si on a plus de pas apres avoir selectionné tous les objets
                        game_state.game_lost = True
                        
                    
                    

                        
                    
                    
                else:
                    #selection des items
                    #position initiale de l'indicateur : 0
                    if event.key == pygame.K_z:
                        
                        if game_state.items_indicator_pos > 0:

                            game_state.items_indicator_pos -= 1

                        
                    elif event.key == pygame.K_s:
                        
                        if game_state.items_indicator_pos < (len(game_state.items_tirees)):

                            game_state.items_indicator_pos += 1   
                        print(game_state.items_indicator_pos)
                            

                        

                    elif event.key == pygame.K_SPACE:
                        
                        if game_state.items_indicator_pos == len(game_state.items_tirees): # si on selectionne "Leave"
                            game_state.items_selection = False
                            
                            if game_state.inventory["Pas"] <= 0: #activation flag game_lost si on a plus de pas apres avoir quitté le menu de selection items
                                game_state.game_lost = True

                            break


                        chosen_item = game_state.items_tirees[game_state.items_indicator_pos]

                        if chosen_item <= 4:
                            game_state.inventory[items_data.resource_items[chosen_item].name+'s'] += 1  #on ajoute un s car noms items au pluriel dans l'inventaire
                            
                        elif chosen_item >= 5 and  chosen_item<= 9:  #items qui donne plusieurs Pas (sandwich,pomme etc..)
                            game_state.inventory["Pas"] += items_data.resource_items[chosen_item].arg



                        elif chosen_item >=10 and chosen_item <=11: #endroit a creuser ou casiers
                            if chosen_item == 10 and 100 not in game_state.inventory["Items permanents"]:  #si on choisit endroit a creuser et pas de pelle
                                game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                                game_state.temp_message = "Vous n'avez pas de pelle pour creuser" 
                                break

                            found_item_index = random.randint(0,len(items_data.resource_items[chosen_item].arg)-1) #on choisit au hasard dans le pool de l'endroit a creuser (probas pour chaque items uniformes)
                            found_item = items_data.resource_items[chosen_item].arg[found_item_index]
                            #conditions en fct de l'item deterré
                            if found_item <= 4:

                                game_state.inventory[items_data.resource_items[found_item].name+'s'] += 1

                            elif found_item >= 5 and  found_item<= 9:
                                game_state.inventory["Pas"] += items_data.resource_items[found_item].arg

                            game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                            game_state.temp_message = f"Vous avez trouvé {items_data.resource_items[found_item].name} ! "    


                        elif chosen_item >= 12 and chosen_item <=13: #item 3 pieces et item 40 pieces
                            game_state.inventory["Pieces"] += items_data.resource_items[chosen_item].arg
                            

                        elif chosen_item >= 100:

                            #pas de doublons d'items permanents (inutile)
                            if chosen_item not in game_state.inventory["Items permanents"]:
                                
                                game_state.inventory["Items permanents"].append(chosen_item)

                                if chosen_item == 104: #proba bonus patte de lapin
                                    items_data.rabbit_bonus = 30
                                elif chosen_item == 103 : #proba bonus detecteur de metaux
                                    items_data.metal_bonus = 30




                        game_state.items_tirees.remove(chosen_item)  #on le retire de la liste d'items selectionnables
                        if game_state.items_indicator_pos > len(game_state.items_tirees)-1:   #conditions pour changer la position du l'indicateur quand l'item à été selectionné
                            game_state.items_indicator_pos -= 1
                        elif game_state.items_indicator_pos < 0:
                            game_state.items_indicator_pos == 0

                                
                        if len(game_state.items_tirees) == 0:  #si plus d'items -> on quite le menu de selection d'items (faisaible aussi en selectionnant 'Leave')

                            game_state.items_selection = False
                    









            # -----------------------------------------------------
            # CAS 3: Le joueur est sur la grille (mode déplacement)
            # -----------------------------------------------------


            elif not(game_state.inInventory) and not(game_state.items_selection):

                    # ZQSD contrôle la direction du joueur
                if event.key == pygame.K_z: game_state.intended_direction = (0, -1)
                elif event.key == pygame.K_s: game_state.intended_direction = (0, 1)
                elif event.key == pygame.K_q: game_state.intended_direction = (-1, 0)
                elif event.key == pygame.K_d: game_state.intended_direction = (1, 0)
                        
                        # Le joueur VALIDE son déplacement
                elif event.key == pygame.K_SPACE:
                    
                            
                    if game_state.intended_direction != (0, 0): #si le joueur n'a pas choisi de directeur => on fait rien
                        
                        new_x = game_state.player_x + game_state.intended_direction[0]
                        new_y = game_state.player_y + game_state.intended_direction[1]
                                
                        if 0 <= new_x < game_state.GRID_WIDTH and 0 <= new_y < game_state.GRID_HEIGHT: #on doit construire a l'interieur de la grille
                            
                                    
                            target_room_id = game_state.map_grid[new_y][new_x]
                            target_room_id_portes = np.array(game_state.map_grid_portes[new_y][new_x])
                            current_room_id = game_state.map_grid[game_state.player_y][game_state.player_x]
                            current_room_id_portes = np.array(game_state.map_grid_portes[game_state.player_y][game_state.player_x])
                            
                            # --------------------------------------------------------------------------------
                            # Si le joueur se deplace dans une position sans room et qu'un mur ne le bloque pas
                            # --------------------------------------------------------------------------------
                            if (target_room_id == "0" and can_move(current_room_id_portes,np.array(rooms_data.rooms["r2"].portes))) or (target_room_id != "0" and can_move(current_room_id_portes,target_room_id_portes) ):  #si la direction choisie n'est pas un mur
                                
                               


                                if target_room_id == "0"   :
                                    
                                    game_state.porte_ouverte = False

                                    
                                    #on verifie si la porte est verrouillée
                                    if ("%" in bord_portes_joueur(current_room_id_portes,game_state.intended_direction)) or ("X" in bord_portes_joueur(current_room_id_portes,game_state.intended_direction)):
                                        
                                        if 102 in game_state.inventory["Items permanents"] and "%" in bord_portes_joueur(current_room_id_portes,game_state.intended_direction) :
                                            #on ouvre avec lockpick

                                            game_state.porte_ouverte = True
                                            ouvrir_portes(current_room_id_portes)
                                            


                                        elif game_state.inventory["Cles"] > 0:
                                            #on ouvre avec cles
                                            game_state.porte_ouverte = True
                                            

                                            ouvrir_portes(current_room_id_portes)
                                            game_state.inventory["Cles"] -=1

                                        else:
                                            game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                                            game_state.temp_message = "Pas assez de clés"     

                                    else:
                                        #sinon la porte est deja ouverte
                                        game_state.porte_ouverte = True
                                    
                                    if game_state.porte_ouverte:



                                        # 1. On PASSE EN MODE INVENTAIRE
                                        
                                        game_state.build_target_coords = (new_x, new_y)  # 2. On STOCKE la position ou la room va etre posée
                                        game_state.inventory_indicator_pos_indicator_pos = 0
                                        game_state.rooms_on_offer,game_state.rooms_on_offer_mats,game_state.rooms_on_offer_images = tirage()

                                        game_state.inInventory = True
                                                    
                                       
                                            
                                                    

                                            
                                        # Le joueur se déplace vers une pièce EXISTANTE
                                else:
                                    
                                    
                                    if game_state.inventory["Pas"] > 0:
                                            


                                        if can_move(np.array(current_room_id_portes), np.array(target_room_id_portes)):
                                            # Déplace le joueur
                                            game_state.prev_player_x = game_state.player_x
                                            game_state.prev_player_y = game_state.player_y
                                            game_state.player_x = new_x
                                            game_state.player_y = new_y

                                    else:

                                        game_state.game_lost = True





                            else:   #sinon on affiche un msg dans linv

                                
                                game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                                game_state.temp_message = "Il y a un mur ici, essayez une autre direction"                

                            
                        if game_state.player_x == new_x and game_state.player_y == new_y: #si le joueur a reussi a se deplacer , càd que ses coordonnées on changées
                            game_state.inventory["Pas"] -=1


                            #En dessous on peut mettre les effets speciaux specifiques a chaque room

                            if game_state.map_grid[new_y][new_x] == "b1" and game_state.map_grid[game_state.prev_player_y][game_state.prev_player_x] != "b1" : #deuxieme condition ajouté pour eviter generation de pas infinis
                                game_state.inventory["Pas"] += 2 
                            elif game_state.map_grid[new_y][new_x] == "b1" and game_state.map_grid[game_state.prev_player_y][game_state.prev_player_x] == "b1":
                                game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                                game_state.temp_message = "Le bonus de BedRoom n'a pas été appliqué"       


                            elif game_state.map_grid[new_y][new_x] == "red5":
                                game_state.inventory["Pas"] -= 2


                            elif game_state.map_grid[new_y][new_x] == "b5" and ((new_y,new_x) not in game_state.visited_coords):

                                for ligne_grille in game_state.map_grid:
                                    for roomid in ligne_grille:
                                        if  roomid == "b1":
                                            game_state.inventory["Cles"]+= 1


                            #       --Fin bloc effets speciaux--


                            if (game_state.player_y,game_state.player_x) not in game_state.visited_coords: 
                                
                                game_state.items_tirees = tirage_items() # si la map n'a jamais été tirée on fait un tirage d'objets
                                game_state.items_tirees 
                                game_state.items_indicator_pos = 0
                                if len(game_state.items_tirees) > 0: # si qqch a été tiré

                                    game_state.items_selection = True
                                
                                game_state.visited_coords.append((game_state.player_y,game_state.player_x))

                                







                            

                        if game_state.inventory["Pas"] <= 0 and game_state.items_selection == False :
                            game_state.game_lost = True 
                            
                            break
                        elif game_state.player_x == 2 and game_state.player_y == 0:
                            game_state.game_won = True
                            break
                        


                    # On réinitialise la direction après chaque action Espace
                    if not game_state.inInventory:
                        game_state.intended_direction = (0, 0)

    # --- Logique de dessin (MODIFIÉE) ---
    
    # Remplit TOUT l'écran principal de noit
    screen.fill(BLACK)
    
    # 2. Dessine la grille de jeu (images)
    draw_grid()

   


    # Dessine le rectangle blanc de l'interface à DROITE
    
    ui_rect = pygame.Rect(GRID_PIXEL_WIDTH, 0, UI_PIXEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, WHITE, ui_rect)

    if game_state.game_lost == False and game_state.game_won == False:
        # Dessine le joueur (indicateur)

        draw_player_and_indicator()

        #dessine l'inventaire du joueur
        draw_inventory(text_font)

        if game_state.inInventory:#selection de maps

            draw_inventory_selection()



        

        if game_state.items_selection: #affichage des items tirés
            
            draw_inventory_items()

    elif game_state.game_lost == True: #si perdu on affiche l'inventaire en rouge
        
        ui_rect = pygame.Rect(GRID_PIXEL_WIDTH, 0, UI_PIXEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(screen, RED, ui_rect)

        game_lost_text = text_font.render("GAME OVER", True, BLACK)     
        screen.blit(game_lost_text, (1030, 500))


    elif game_state.game_won == True: #si gagné on affiche l'inventaire en vert

        ui_rect = pygame.Rect(GRID_PIXEL_WIDTH, 0, UI_PIXEL_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(screen, GREEN, ui_rect)

        game_won_text = text_font.render("YOU WIN", True, BLACK)     
        screen.blit(game_won_text, (1030, 500))



    # 5. Met à jour l'écran
    pygame.display.flip()
    
    clock.tick(30)

# --- Fin ---
pygame.quit()