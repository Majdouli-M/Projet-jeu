import pygame
import os
import random
import ctypes
import game_state
import items_data
import rooms_data
import numpy as np
# --- Initialisation de Pygame ---
pygame.init()
pygame.font.init()


# --- Bloc anti-flou (Inchangé) ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        print("Avertissement : Impossible de régler la sensibilisation PPP (DPI).")

# --- Constantes ---
# MODIFIÉ: Renommage pour plus de clarté
GRID_PIXEL_WIDTH = 900  # Largeur de la zone de jeu (votre ancien DISPLAY_WIDTH)

GRID_WIDTH = 5
GRID_HEIGHT = 9

# CELL_SIZE est calculé à partir de la grille
CELL_SIZE = GRID_PIXEL_WIDTH // GRID_WIDTH # (900 / 5 = 180)
INV_CELL_SIZE = CELL_SIZE*1.5
# MODIFIÉ: Renommage pour plus de clarté
GRID_PIXEL_HEIGHT = CELL_SIZE * GRID_HEIGHT # (180 * 9 = 1620)

# NOUVEAU: Largeur de la zone d'interface (identique à la grille)
UI_PIXEL_WIDTH = GRID_PIXEL_WIDTH

# NOUVEAU: Dimensions totales de la FENÊTRE
WINDOW_WIDTH = GRID_PIXEL_WIDTH + UI_PIXEL_WIDTH # (900 + 900 = 1800)
WINDOW_HEIGHT = GRID_PIXEL_HEIGHT # (Hauteur inchangée: 1620)

# Couleurs (Inchangé)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

try:
    # Police pour les titres de l'interface
    title_font = pygame.font.SysFont('Arial', 36, bold=True)
    # Police pour le texte normal
    text_font = pygame.font.SysFont('Arial', 30,bold=True)
except pygame.error:
    print("Police 'Arial' non trouvée, utilisation de la police par défaut.")
    title_font = pygame.font.Font(None, 40)
    text_font = pygame.font.Font(None, 34)


# --- Fin Constantes ---



IMAGE_FOLDER = 'rooms' 


# MODIFIÉ: Utilise les nouvelles dimensions totales de la FENÊTRE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu + Interface")
clock = pygame.time.Clock()

# --- Section de chargement des images (Inchangée) ---
loaded_images = {} 
loaded_ui_images = {}
print(f"Taille cible des cellules : {CELL_SIZE}x{CELL_SIZE} pixels")
if os.path.exists(IMAGE_FOLDER):
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(IMAGE_FOLDER, filename)
            try:
                image_hires = pygame.image.load(path).convert_alpha()
                image_scaled = pygame.transform.smoothscale(image_hires, (CELL_SIZE, CELL_SIZE))
                image_ui_scaled = pygame.transform.smoothscale(image_hires, (INV_CELL_SIZE, INV_CELL_SIZE))
                loaded_images[filename] = image_scaled
                loaded_ui_images[filename] = image_ui_scaled



                print(f"Image chargée et redimensionnée: {filename}")
            except pygame.error as e:
                print(f"Erreur de chargement de l'image {filename}: {e}")
else:
    print(f"AVERTISSEMENT: Le dossier '{IMAGE_FOLDER}' n'existe pas.")



##############################################################################################


# --- Fonctions de dessin (Inchangées) ---
# (draw_grid et draw_player_and_indicator dessinent toujours
# par rapport au coin (0,0), ce qui est maintenant la moitié gauche)




def draw_grid(loaded_images_dict):
    """
    Dessine la grille en lisant game_state.map_grid.
    (Plus besoin de 'visited_coords'!)
    """
    for y in range(game_state.GRID_HEIGHT):
        for x in range(game_state.GRID_WIDTH):
            
            # 1. Trouve l'ID de la pièce à cette coordonnée
            room_id = game_state.map_grid[y][x] # ex: "r2" ou "0"
            
            # 2. Si ce n'est pas une case vide ("0")
            if room_id != "0":
                
                # 3. CONSTRUIT le nom du fichier image à partir de l'ID
                image_name_to_draw = room_id + ".png" # ex: 
                
                # 4. Dessine l'image si elle a été chargée
                if image_name_to_draw in loaded_images_dict:
                    image_surface = loaded_images_dict[image_name_to_draw]
                    screen.blit(image_surface, (x * CELL_SIZE, y * CELL_SIZE))

def draw_player_and_indicator(px, py, direction):


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


def draw_inventory_selection(cursor_pos, map_selection, loaded_images_dict):
    """
    Dessine les 3 images de pièces proposées ET l'indicateur.
    cursor_pos est l'index (-1, 0, ou 1).
    map_selection est la liste des 3 ID (ex: ["r10", "r45", "r2"])
    """
    
    # 1. Définir la géométrie
    
 
    start_x = GRID_PIXEL_WIDTH + 0.5*INV_CELL_SIZE 
    ecart = 1.1
    
    # --- 2. Dessiner les 3 images de pièces ---
    
    # BUG 1 CORRIGÉ: La boucle était imbriquée. Elle doit être unique.
    for i in [-1, 0, 1]: # Boucle sur les 3 slots: -1 (haut), 0 (milieu), 1 (bas)
        
        # Calcule la position Y de cette boîte (en utilisant ta logique)
        current_y = WINDOW_HEIGHT - (3 + ecart*i) *INV_CELL_SIZE
        
        try:
            # Récupère le bon room_id (index 0, 1, ou 2)
            room_id = map_selection[i + 1] # Convertit -1,0,1 en 0,1,2
            
            # BUG 2 CORRIGÉ: Il faut ajouter ".png" au nom du fichier
            image_name = room_id + ".png" 
            
            # Dessine l'image si elle existe
            if image_name in loaded_images_dict:
                image_surface = loaded_images_dict[image_name]
                
                # BUG 3 CORRIGÉ: Il ne faut pas multiplier les coordonnées
                screen.blit(image_surface, (start_x, current_y))
            else:
                # (Optionnel) Dessine une boîte noire si l'image manque
                pygame.draw.rect(screen, BLACK, (start_x, current_y, INV_CELL_SIZE, INV_CELL_SIZE), 2)
        
        except IndexError:
            # S'il n'y a pas (encore) 3 pièces dans map_selection, ne rien faire
            pass 

    # --- 3. Dessiner l'indicateur (la boîte grise) ---
    
    # Calcule la position Y de la boîte sélectionnée (selon ta logique)
    cursor_y_pixel = WINDOW_HEIGHT - (3 + ecart*cursor_pos) * INV_CELL_SIZE

    thickness_selection = 7 # Augmenté pour la visibilité
    
    # Simplification: Utiliser draw.rect au lieu de 4 lignes
    selection_rect = pygame.Rect(start_x, cursor_y_pixel, INV_CELL_SIZE, INV_CELL_SIZE)
    pygame.draw.rect(screen, RED, selection_rect, thickness_selection, border_radius=5)


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
    
    # Boucle sur l'inventaire (ex: {"Pas": 70, "Pieces": 0})
    for index, (key, value) in enumerate(inventory_data.items()):
        
        # 1. Crée le texte (ex: "Pas: 70")
        text_to_draw = f"{key}: {value}"
        
        # 2. Crée la surface de texte
        text_surface = font.render(text_to_draw, True, BLACK) # Texte en noir
        
        # 3. Calcule la position Y
        y_pos = start_y + (index * line_height)
        
        # 4. Dessine le texte sur l'écran
        surface.blit(text_surface, (start_x, y_pos))
    surface.blit(font.render(str(game_state.player_x),True,BLACK),((WINDOW_WIDTH - 300),WINDOW_HEIGHT-50)) #AFFICHAGE POSITION X
    surface.blit(font.render(str(game_state.player_y),True,BLACK),((WINDOW_WIDTH - 300),WINDOW_HEIGHT-80)) #AFFICHAGE POSITION Y
    surface.blit(font.render(str(game_state.intended_direction),True,BLACK),((WINDOW_WIDTH - 300),WINDOW_HEIGHT-110)) #AFFICHAGE intented_direction
    surface.blit(font.render(str(game_state.inInventory),True,BLACK),((WINDOW_WIDTH - 300),WINDOW_HEIGHT-130)) #AFFICHAGE inInventory
    surface.blit(font.render(str(game_state.inventory_indicator_pos),True,BLACK),((WINDOW_WIDTH - 300),WINDOW_HEIGHT-150)) #AFFICHAGE inventory_indicator_pos

    


        


  



def can_move(portes_joueur, portes_cible, direction):

    """
    Vérifie si les portes de deux matrices (NumPy) correspondent
    pour une direction donnée.
    """
    try:
        


        # On compare les tableaux, puis on vérifie si .all() (tous) sont True
        if direction == (0, -1) and np.array_equal(portes_joueur[0, :] ,portes_cible[2, :]) and np.array_equal(portes_cible[2, :],[' ','#',' ']): # Haut
            return True
        
        elif direction == (0, 1) and np.array_equal(portes_joueur[2, :],portes_cible[0, :]) and np.array_equal(portes_cible[0, :],[' ','#',' ']) : # Bas
            return True
        
        elif direction == (-1, 0) and np.array_equal(portes_joueur[:, 0],portes_cible[:, 2]) and np.array_equal(portes_cible[:, 2],[' ','#',' ']): # Gauche
            return True
        
        elif direction == (1, 0) and np.array_equal(portes_joueur[:, 2] , portes_cible[:, 0]) and np.array_equal(portes_cible[:, 0],[' ','#',' ']): # Droite
            return True
        
        else:
            return False
            
    except Exception as e:
        # Sécurité si les matrices n'ont pas la bonne forme
        print(f"Erreur dans can_move: {e}")
        return False
    

def tirer_valeurs_aleatoires(liste, n):
    valeurs_tirees = [random.choice(liste) for _ in range(n)]
    return valeurs_tirees


def tirer_avec_rarity(liste, rarity, n):

    """ Tire aléatoirement n éléments d'une liste donnée (avec répétition possible).

    Args:
        liste (list): liste source
        n (int): nombre d'éléments à tirer

    Returns:
        list: liste de n éléments choisis au hasard."""
   
    # On inverse la rareté pour obtenir un poids (1 = très commun)
    poids = [1/(r+1) for r in rarity]  
    
    # On tire n valeurs pondérées
    valeurs_tirees = random.choices(liste, weights=poids, k=n)
    return valeurs_tirees





# --- Boucle principale du jeu ---
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
                    if game_state.inventory_indicator_pos > -1:

                        game_state.inventory_indicator_pos -= 1   
                        # Le joueur VALIDE son choix de pièce
                elif event.key == pygame.K_SPACE:
                            
                    # 1. Récupère la pièce choisie dans l'inventaire
                    # (Pour l'instant, on met "r10" en dur, comme avant)
                    chosen_room_id = rooms_on_offer[game_state.inventory_indicator_pos+1] 
                            
                            # 2. Récupère les matrices de portes
                    current_room_id = game_state.map_grid[game_state.player_y][game_state.player_x]
                    mat_A = rooms_data.rooms[current_room_id].portes
                    mat_B = rooms_data.rooms[chosen_room_id].portes
                            
                            # 3. Vérifie si le placement est valide
                            # (On utilise 'intended_direction' car il contient la direction 
                            # qui nous a amenés ici)
                    if can_move(np.array(mat_A), np.array(mat_B), game_state.intended_direction):
                                
                                # 4. Placement RÉUSSI :
                        target_x, target_y = game_state.build_target_coords # Récupère les coords
                                
                                # Met à jour la carte
                        game_state.map_grid[target_y][target_x] = chosen_room_id
                        print(f"Vous avez construit : {chosen_room_id}")
                                

                                
                        # Quitte le mode inventaire
                        game_state.inInventory = False
                            
                    else:

                        print(f"Placement impossible: Les portes de {chosen_room_id} ne correspondent pas.")
                            # (On reste en mode inventaire pour choisir autre chose)

                    # -----------------------------------------------------
                    # CAS 2: Le joueur est sur la grille (mode déplacement)
                    # -----------------------------------------------------
            else:

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
                            current_room_id = game_state.map_grid[game_state.player_y][game_state.player_x]
                            mat_A = rooms_data.rooms[current_room_id].portes

                            # -----------------------------------------------
                            # C'EST TA CONDITION : if target_room_id == "0"
                            # -----------------------------------------------
                            if target_room_id == "0"   :

                                if can_move(np.array(mat_A),np.array(rooms_data.rooms["r2"].portes),game_state.intended_direction):


                                    # 1. On PASSE EN MODE INVENTAIRE
                                    print("Ouverture de l'inventaire de construction...")
                                    rooms_on_offer = tirer_avec_rarity(list(rooms_data.rooms.keys()),[room.rarity for room in rooms_data.rooms.values()],3)
                                    game_state.inInventory = True
                                            
                                    # 2. On STOCKE la cible
                                    game_state.build_target_coords = (new_x, new_y)
                                            
                                    # (On NE BOUGE PAS le joueur)
                                    
                                # Le joueur se déplace vers une pièce EXISTANTE
                            else:
                                mat_B = rooms_data.rooms[target_room_id].portes
                                        
                                if can_move(np.array(mat_A), np.array(mat_B), game_state.intended_direction):
                                    # Déplace le joueur
                                    game_state.player_x = new_x
                                    game_state.player_y = new_y
                                else:
                                    print("Mouvement bloqué par un mur !")

                            
                    if game_state.player_x == new_x and game_state.player_y == new_y:
                        game_state.inventory["Pas"] -=1

                    # On réinitialise la direction après chaque action Espace
                    if not game_state.inInventory:
                        game_state.intended_direction = (0, 0)

    # --- Logique de dessin (MODIFIÉE) ---
    
    # 1. Remplit TOUT l'écran principal (1800x1620) de noir
    screen.fill(BLACK)
    
    # 2. Dessine la grille de jeu (images) sur la moitié GAUCHE
    draw_grid(loaded_images)

    # 3. Dessine le joueur (outlines) sur la moitié GAUCHE
    draw_player_and_indicator(game_state.player_x, game_state.player_y, game_state.intended_direction)


    # 4. NOUVEAU: Dessine le rectangle blanc de l'interface à DROITE
    #    (x, y, largeur, hauteur)
    ui_rect = pygame.Rect(GRID_PIXEL_WIDTH, 0, UI_PIXEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, WHITE, ui_rect)



    draw_inventory(screen, text_font, game_state.inventory)

    if game_state.inInventory:

        draw_inventory_selection(game_state.inventory_indicator_pos,rooms_on_offer,loaded_ui_images)
    # 5. Met à jour l'écran
    pygame.display.flip()
    
    clock.tick(30)

# --- Fin ---
pygame.quit()