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



# --- Bloc anti-flou (Inchangé) ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        print("Avertissement : Impossible de régler la sensibilisation PPP (DPI).")



try:
    # Police pour les titres de l'interface
    title_font = pygame.font.SysFont('Arial', 36, bold=True)
    # Police pour le texte normal
    text_font = pygame.font.SysFont('Arial', 30,bold=True)
except pygame.error:
    print("Police 'Arial' non trouvée, utilisation de la police par défaut.")
    title_font = pygame.font.Font(None, 40)
    text_font = pygame.font.Font(None, 34)


















##############################################################################################


# --- Fonctions de dessin ---
# (draw_grid et draw_player_and_indicator dessinent toujours
# par rapport au coin (0,0)




def draw_grid():
    """
    Dessine la grille en lisant game_state.map_grid.

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

def draw_player_and_indicator(px, py, direction):
    """
    Dessine le contour représentant le joueur sur la grille.
    Args:
        px (int): Position du joueur en X (colonne)
        py (int): Position du joueur en Y (ligne)
        direction (tuple): Direction choisie par le joueur, ex. (1, 0) pour droite.
    """

    if not(game_state.inInventory):


        """Dessine le joueur (outline) où l'arête sélectionnée est plus épaisse."""
            
        default_thickness = 2
        selected_thickness = 8
        player_rect = pygame.Rect(px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        p_topleft = (player_rect.left, player_rect.top)
        p_topright = (player_rect.right - 1, player_rect.top)
        p_bottomleft = (player_rect.left, player_rect.bottom - 1)
        p_bottomright = (player_rect.right - 1, player_rect.bottom - 1)
        dx, dy = direction
        thickness_top = default_thickness
        thickness_bottom = default_thickness
        thickness_left = default_thickness
        thickness_right = default_thickness
        new_x = px + dx
        new_y = py + dy
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


            room_id = game_state.rooms_on_offer[i + 1] # Convertit -1,0,1 en 0,1,2
                
            image_surface = pygame.transform.smoothscale(game_state.rooms_on_offer_images[i+1], (INV_CELL_SIZE, INV_CELL_SIZE))
            price_text_surface = text_font.render(str(rooms_data.rooms[room_id].price), True, BLACK)   
            
            # BUG 3 CORRIGÉ: Il ne faut pas multiplier les coordonnées
            screen.blit(image_surface, (start_x, current_y))
            screen.blit(price_text_surface, (x_room_price, current_y))
            
        elif i == -2:

            if game_state.inventory_indicator_pos != -2:

                    
                reroll_text = text_font.render("Reroll", True, BLACK) 
            else:
                reroll_text = text_font.render("Reroll", True, RED) 
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
    start_x = GRID_PIXEL_WIDTH + 0.5 * INV_CELL_SIZE



    title_y = WINDOW_HEIGHT - (4) * INV_CELL_SIZE

    text_surface = text_font.render("Items found:", True, BLACK)
    screen.blit(text_surface, (start_x, title_y))



    ecart = 0.5
    for i, item_id in enumerate(game_state.items_tirees):
        current_y = WINDOW_HEIGHT - (4 - ecart * (i+1)) * INV_CELL_SIZE

        # On suppose que item[0] contient l'ID ou le nom de l'objet
        if item_id < 100:

            item_name = items_data.resource_items[item_id].name
        else:
            item_name = items_data.special_items[item_id].name
        # Crée la surface texte

        if game_state.items_indicator_pos == i:

            text_surface = text_font.render(item_name, True, RED)

        else:
            text_surface = text_font.render(item_name, True, BLACK)




        
        # Affiche le texte sur l'écran
        screen.blit(text_surface, (start_x, current_y))

        


    



def tirage_items():

    roomid = game_state.map_grid[game_state.player_y][game_state.player_x]
    #(ID, rarity_score, min value, max value),
    pool_resource = rooms_data.rooms[roomid].resource_pool
    pool_special = rooms_data.rooms[roomid].special_pool
    
    min_items = rooms_data.rooms[roomid].min_items
    max_items = random.randint(min_items,rooms_data.rooms[roomid].max_items)
    min_special_items = rooms_data.rooms[roomid].min_special_items
    items_tirees = []

    
    tirage_1_item = ["Oui","Non"]





    


    if min_special_items == -1 : #on impose pas un ou des items speciaux a la room 



        for i in range(0,len(pool_special)):


            proba = [1,pool_special[i][1]]

            tirage = random.choices(tirage_1_item,weights=proba,k=pool_special[i][3])

            resultat = Counter(tirage)
            nb = resultat.get("Oui",0)

            for _ in range(0,nb):
                if (len(items_tirees) < max_items):

                    items_tirees.append(pool_special[i][0])

                else:
                    break
    else:
        
        while (len(items_tirees) < min_special_items):

            for i in range(0,len(pool_special)):


                proba = [1,pool_special[i][1]]

                tirage = random.choices(tirage_1_item,weights=proba,k=pool_special[i][3])

                resultat = Counter(tirage)
                nb = resultat.get("Oui",0)

                for _ in range(0,nb):
                    if (len(items_tirees) < max_items):

                        items_tirees.append(pool_special[i][0])

                    else:
                        break
    while (len(items_tirees) < min_items) or (len(items_tirees) < max_items ):
        for i in range(0,len(pool_resource)):


            proba = [1,pool_resource[i][1]]

            tirage = random.choices(tirage_1_item,weights=proba,k=pool_resource[i][3])

            resultat = Counter(tirage)
            nb = resultat.get("Oui",0)
            
            


            for _ in range(0,nb):
                if (len(items_tirees) < max_items):

                    items_tirees.append(pool_resource[i][0])

                else:
                    break




    return items_tirees    











def draw_inventory(surface, font, inventory_data):
    """
    Dessine l'inventaire (statistiques) du joueur sur la surface de l'interface.
    
    Args:
        surface: L'écran principal (screen)
        font: L'objet pygame.font.Font à utiliser (text_font)
        inventory_data: Le dictionnaire game_state.inventory
    """
    
    # Position de départ pour dessiner (coin haut-gauche de l'UI + marge)
    start_x = WINDOW_WIDTH - 300
    start_y = 20
    line_height = 40 # Espace entre chaque ligne
    special_items_x = GRID_PIXEL_WIDTH+20
    special_items_y = 20
    special_items_title = "Items Permanents:"
    # Boucle sur l'inventaire (ex: {"Pas": 70, "Pieces": 0})
    for index, (key, value) in enumerate(inventory_data.items()):
        if key != "Items permanents":
            
            # 1. Crée le texte (ex: "Pas: 70")
            text_to_draw = f"{key}: {value}"
            
            # 2. Crée la surface de texte
            text_surface = font.render(text_to_draw, True, BLACK) # Texte en noir
            
            # 3. Calcule la position Y
            y_pos = start_y + (index * line_height)
            
            # 4. Dessine le texte sur l'écran
            surface.blit(text_surface, (start_x, y_pos))
    
    text_surface = font.render(special_items_title,True,BLACK)
    surface.blit(text_surface, (special_items_x, special_items_y))
    for index, item in enumerate(game_state.inventory["Items permanents"]):

        
                    # 1. Crée le texte (ex: "Pas: 70")
            
            
            # 2. Crée la surface de texte
            text_surface = font.render(item, True, BLACK) # Texte en noir
            
            # 3. Calcule la position Y
            special_items_y = special_items_y + ((index+1) * line_height)
            
            # 4. Dessine le texte sur l'écran
            surface.blit(text_surface, (special_items_x, special_items_y))

        # --- Affiche un message temporaire si défini ---
    now = pygame.time.get_ticks()
    if game_state.temp_message != None  and now <= game_state.duree_temp_message:

        msg_surf = font.render(game_state.temp_message, True, (0, 0, 0))
        msg_rect = msg_surf.get_rect(center=(GRID_PIXEL_WIDTH + UI_PIXEL_WIDTH // 2, WINDOW_HEIGHT - 50))
        
        screen.blit(msg_surf, msg_rect)
    elif game_state.temp_message != None and now > game_state.duree_temp_message:
        game_state.temp_message = None

            
            


        
def normaliser_portes(portes1):

    lignes1,cols1 = np.where(portes1 != ' ')
    

    for y1,x1 in zip(lignes1,cols1): #on "normalise" la matrice avec les #
        portes1[y1,x1] = '#'
        
     

  



def can_move(portes_joueur, portes_cible, direction):

    p_joueur_tampon = np.array(portes_joueur)
    p_cible_tampon = np.array(portes_cible)
    
    normaliser_portes(p_joueur_tampon)
    normaliser_portes(p_cible_tampon)

    """
    Vérifie si les portes de deux matrices (NumPy) correspondent
    pour une direction donnée.
    """

    try:
        


        # On compare les tableaux, puis on vérifie si .all() (tous) sont True
        if direction == (0, -1) and np.array_equal(p_joueur_tampon[0, :] ,p_cible_tampon[2, :]) and np.array_equal(p_cible_tampon[2, :],[' ','#',' ']): # Haut
            return True
        
        elif direction == (0, 1) and np.array_equal(p_joueur_tampon[2, :],p_cible_tampon[0, :]) and np.array_equal(p_cible_tampon[0, :],[' ','#',' ']) : # Bas
            return True
        
        elif direction == (-1, 0) and np.array_equal(p_joueur_tampon[:, 0],p_cible_tampon[:, 2]) and np.array_equal(p_cible_tampon[:, 2],[' ','#',' ']): # Gauche
            return True
        
        elif direction == (1, 0) and np.array_equal(p_joueur_tampon[:, 2] , p_cible_tampon[:, 0]) and np.array_equal(p_cible_tampon[:, 0],[' ','#',' ']): # Droite
            return True
        
        else:
            return False
            
    except Exception as e:
        # Sécurité si les matrices n'ont pas la bonne forme
        print(f"Erreur dans can_move: {e}")
        return False
    

def bord_portes_joueur(matrice_portes,dir): 
     #retourne le cote de la matrice portes vers lequel le joueur regarde

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
    
def ouvrir_portes(matrice_portes,dir):

    if dir == (0,-1):  # haut

        matrice_portes[0, :] = [' ', '#',' ']
    elif dir == (0,1):  # bas
              # ligne du haut de B
        matrice_portes[-1, :] = [' ', '#',' ']
    elif dir == (-1,0):  # gauche

                # colonne droite de B
        matrice_portes[:, 0] = [' ', '#',' ']
    elif dir == (1,0):  # droite
            # colonne gauche de B
        matrice_portes[:, -1] = [' ', '#',' ']




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




            
            #dans le cas ou une room va etre ajoutée a coté d'un bord de la map, il ne faut pas que la room ait des portes qui menne vers l'exterieur de la map
            if (target_x == GRID_WIDTH-1 and np.array_equal(chosen_ids_portes[j][:,-1],np.array([' ', '#', ' '])  )) or (target_x == 0 and np.array_equal(chosen_ids_portes[j][:,0],np.array([' ', '#', ' '])  )): #on nentre jamais dans ce if
                #print("pas bon")
                valide = False

            elif (target_y == GRID_HEIGHT-1 and np.array_equal(chosen_ids_portes[j][-1,:],np.array([' ', '#', ' '])  )) or (target_y == 0 and np.array_equal(chosen_ids_portes[j][0,:],np.array([' ', '#', ' '])  )): #on nentre jamais dans ce if
                #print("pas bon")
                valide = False

            else:
                #print("bon")
                valide = True
                j +=1
                

            




    return chosen_ids,chosen_ids_portes,chosen_ids_images

"""  #: porte ouverte
     % porte verouillée
     X: porte verouillée à double tour   


    Y = 8 : ###
    Y = 7 à 4 : # %% X
    Y = 3  :  % XX
    Y = 2 à 0 : XXX


"""


def random_doors_generation(matrice_portes,score_ouv,score_verr,score_dbverr):


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


        choix = random.choices(["#","%","X"],weights=[score_ouv,score_verr,score_dbverr],k=1)
        print(choix[0])

        matrice_portes[y,x] = choix[0]


    matrice_portes[ligne,col] = '#' #on conserve l'etat ouvert de la porte par lequel le joueur va entrer





        




def difficulty_scaled_doors(matrice_portes,y):
    

    if y == 8:
        pass
    elif y <= 7  and y > 3:

        random_doors_generation(matrice_portes,0.5,1,0.5)

    elif y == 3:

        random_doors_generation(matrice_portes,0,0.5,2)  

    else:
        random_doors_generation(matrice_portes,0,0,1)  




   

# --- Boucle principale du jeu ---


"""
Boucle principale :
- Gère les événements clavier (déplacement, inventaire)
- Met à jour l'état du jeu
- Dessine la grille, le joueur et l'interface utilisateur
- Maintient un framerate constant.
"""


running = True
print("Utilisez ZQSD pour choisir une direction.")
print("Appuyez sur ESPACE pour vous déplacer dans cette direction.")



while running:
    # --- Gestion des événements (Inchangée) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            running = False

        

        if event.type == pygame.KEYDOWN :
                
                    
            # -----------------------------------------------------
            # CAS 1: Le joueur est dans l'inventaire (mode construction)
            # -----------------------------------------------------
            if game_state.inInventory:

                # (Ici, ZQSD devrait bouger ton curseur d'inventaire)
                if event.key == pygame.K_z:
                    print("Curseur inventaire HAUT") # (Logique à ajouter)
                    if game_state.inventory_indicator_pos < 1:

                        game_state.inventory_indicator_pos += 1
                elif event.key == pygame.K_s:
                    print("Curseur inventaire BAS") # (Logique à ajouter)
                    if game_state.inventory_indicator_pos > -2:

                        game_state.inventory_indicator_pos -= 1   
                        # Le joueur VALIDE son choix de pièce

                elif event.key == pygame.K_SPACE:
                    chosen_room_id = game_state.rooms_on_offer[game_state.inventory_indicator_pos+1] 


                    if game_state.inventory_indicator_pos == -2 and game_state.inventory["Des"] > 0:
                        game_state.rooms_on_offer,game_state.rooms_on_offer_mats,game_state.rooms_on_offer_images = tirage()
                        game_state.inventory["Des"] -= 1
                        break # on relance le tirage donc le code en dessous ne doit pas s'executer 
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
                    target_x, target_y = game_state.build_target_coords # Récupère les coords
                    chosen_room_id_portes = np.array(game_state.rooms_on_offer_mats[game_state.inventory_indicator_pos+1])


                    difficulty_scaled_doors(chosen_room_id_portes,target_y) # genere l'etat de chaque porte ( a l'exception de celle qu'on ouvre qui doit etre ouverte)
                    print(chosen_room_id_portes)
                    chosen_room_id_image = game_state.rooms_on_offer_images[game_state.inventory_indicator_pos+1] 
                            
                            # 2. Récupère les matrices de portes
                    current_room_id = game_state.map_grid[game_state.player_y][game_state.player_x]
                    current_room_id_portes = np.array(game_state.map_grid_portes[game_state.player_y][game_state.player_x])


  
                            # 3. Vérifie si le placement est valide
                            # (On utilise 'intended_direction' car il contient la direction 
                            # qui nous a amenés ici)
                            
                    if can_move(np.array(current_room_id_portes), np.array(chosen_room_id_portes), game_state.intended_direction):
                                
                                # 4. Placement RÉUSSI :
                        
                                
                                # Met à jour la carte
                        game_state.map_grid[target_y][target_x] = chosen_room_id
                        game_state.map_grid_portes[target_y][target_x] = chosen_room_id_portes


                        game_state.map_grid_images[target_y][target_x] = chosen_room_id_image
                        print(f"Vous avez construit : {chosen_room_id}")
                                

                                
                        # Quitte le mode inventaire
                        game_state.inInventory = False
                            
                    else:

                        print(f"Placement impossible: Les portes de {chosen_room_id} ne correspondent pas.") # ce message ne doit jamais s'afficher si pas de bug

                        print(current_room_id_portes)
                        print(chosen_room_id_portes)
                            # (On reste en mode inventaire pour choisir autre chose)



            elif game_state.items_selection:

                if len(game_state.items_tirees) == 0:

                    game_state.items_selection = False
                    
                    
                else:
                 
                    if event.key == pygame.K_z:
                        
                        if game_state.items_indicator_pos > 0:

                            game_state.items_indicator_pos -= 1

                        print("Curseur inventaire HAUT",game_state.items_indicator_pos,len(game_state.items_tirees))
                    elif event.key == pygame.K_s:
                        
                        if game_state.items_indicator_pos < (len(game_state.items_tirees)-1):

                            game_state.items_indicator_pos += 1   
                            # Le joueur VALIDE son choix de pièce

                        print("Curseur inventaire BAS",game_state.items_indicator_pos,len(game_state.items_tirees)) 

                    elif event.key == pygame.K_SPACE:

                        chosen_item = game_state.items_tirees[game_state.items_indicator_pos]

                        if chosen_item <= 4:
                            game_state.inventory[items_data.resource_items[chosen_item].name+'s'] += 1
                            
                        elif chosen_item >= 5 and  chosen_item<= 9:
                            game_state.inventory["Pas"] += items_data.resource_items[chosen_item].arg
                            
                        elif chosen_item >= 100:
                            if chosen_item not in game_state.inventory["Items permanents"]:
                                print("DACCORD")
                                game_state.inventory["Items permanents"].append(items_data.special_items[chosen_item].name)

                        game_state.items_tirees.remove(chosen_item)
                        if game_state.items_indicator_pos > len(game_state.items_tirees)-1:
                            game_state.items_indicator_pos -= 1
                        elif game_state.items_indicator_pos < 0:
                            game_state.items_indicator_pos == 0

                                
                        if len(game_state.items_tirees) == 0:

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
                    
                            
                    if game_state.intended_direction != (0, 0):
                        
                        new_x = game_state.player_x + game_state.intended_direction[0]
                        new_y = game_state.player_y + game_state.intended_direction[1]
                                
                        if 0 <= new_x < game_state.GRID_WIDTH and 0 <= new_y < game_state.GRID_HEIGHT:
                            
                                    
                            target_room_id = game_state.map_grid[new_y][new_x]
                            target_room_id_portes = np.array(game_state.map_grid_portes[new_y][new_x])
                            current_room_id = game_state.map_grid[game_state.player_y][game_state.player_x]
                            current_room_id_portes = np.array(game_state.map_grid_portes[game_state.player_y][game_state.player_x])
                            
                            # -----------------------------------------------
                            # C'EST TA CONDITION : if target_room_id == "0"
                            # -----------------------------------------------
                            if (target_room_id == "0" and can_move(current_room_id_portes,np.array(rooms_data.rooms["r2"].portes),game_state.intended_direction)) or (target_room_id != "0" and can_move(current_room_id_portes,target_room_id_portes,game_state.intended_direction) ):  #si la direction choisie n'est pas un mur
                                
                               


                                if target_room_id == "0"   :
                                    
                                    game_state.porte_ouverte = False

                                    
                                    
                                    if ("%" in bord_portes_joueur(current_room_id_portes,game_state.intended_direction)) or ("X" in bord_portes_joueur(current_room_id_portes,game_state.intended_direction)):
                                        print("OKK")
                                        if 102 in game_state.inventory["Items permanents"] and "%" in bord_portes_joueur(current_room_id_portes,game_state.intended_direction) :
                                            #on ouvre avec lockpick

                                            game_state.porte_ouverte = True
                                            ouvrir_portes(current_room_id_portes,game_state.intended_direction)
                                            print("a")


                                        elif game_state.inventory["Cles"] > 0:
                                            #on ouvre avec cles
                                            game_state.porte_ouverte = True
                                            print("b")

                                            ouvrir_portes(current_room_id_portes,game_state.intended_direction)
                                            game_state.inventory["Cles"] -=1

                                        else:
                                            game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                                            game_state.temp_message = "Pas assez de clés"     

                                    else:
                                        game_state.porte_ouverte = True
                                    
                                    if game_state.porte_ouverte:



                                        # 1. On PASSE EN MODE INVENTAIRE
                                        
                                        game_state.build_target_coords = (new_x, new_y)  # 2. On STOCKE la position ou la room va etre posée

                                        game_state.rooms_on_offer,game_state.rooms_on_offer_mats,game_state.rooms_on_offer_images = tirage()

                                        game_state.inInventory = True
                                                    
                                       
                                            
                                                    

                                            
                                        # Le joueur se déplace vers une pièce EXISTANTE
                                else:
                                    
                                    
                                    if game_state.inventory["Pas"] > 0:
                                            


                                        if can_move(np.array(current_room_id_portes), np.array(target_room_id_portes), game_state.intended_direction):
                                            # Déplace le joueur
                                            game_state.player_x = new_x
                                            game_state.player_y = new_y

          
                                    else:
                                        print("Pas assez de Pas")


                            else:   #sinon on affiche un msg dans linv

                                
                                game_state.duree_temp_message = pygame.time.get_ticks() + 1500
                                game_state.temp_message = "Il y a un mur ici, essayez une autre direction"                

                            
                        if game_state.player_x == new_x and game_state.player_y == new_y:
                            game_state.inventory["Pas"] -=1

                    # On réinitialise la direction après chaque action Espace
                    if not game_state.inInventory:
                        game_state.intended_direction = (0, 0)

    # --- Logique de dessin (MODIFIÉE) ---
    
    # 1. Remplit TOUT l'écran principal (1800x1620) de noir
    screen.fill(BLACK)
    
    # 2. Dessine la grille de jeu (images) sur la moitié GAUCHE
    draw_grid()

    # 3. Dessine le joueur (outlines) sur la moitié GAUCHE
    draw_player_and_indicator(game_state.player_x, game_state.player_y, game_state.intended_direction)


    # 4. NOUVEAU: Dessine le rectangle blanc de l'interface à DROITE
    #    (x, y, largeur, hauteur)
    ui_rect = pygame.Rect(GRID_PIXEL_WIDTH, 0, UI_PIXEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, WHITE, ui_rect)



    draw_inventory(screen, text_font, game_state.inventory)

    if game_state.inInventory:

        draw_inventory_selection()

    elif (game_state.player_y,game_state.player_x) not in game_state.visited_coords:
        print("nouvelle map,tirage d'items")
        game_state.items_tirees = tirage_items()
        game_state.items_indicator_pos = 0
        if len(game_state.items_tirees) > 0:

            game_state.items_selection = True
        game_state.visited_coords.append((game_state.player_y,game_state.player_x))
    

    if game_state.items_selection:
        
        draw_inventory_items()

    # 5. Met à jour l'écran
    pygame.display.flip()
    
    clock.tick(30)

# --- Fin ---
pygame.quit()