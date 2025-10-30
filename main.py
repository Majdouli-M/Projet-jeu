import pygame
import os
import random
import ctypes
import game_state
import items_data
import rooms_data

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
GRAY = (200, 200, 200)

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


inInventory = False
intended_direction = (0, 0)

IMAGE_FOLDER = 'rooms' 


# MODIFIÉ: Utilise les nouvelles dimensions totales de la FENÊTRE
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu + Interface")
clock = pygame.time.Clock()

# --- Section de chargement des images (Inchangée) ---
loaded_images = {} 
print(f"Taille cible des cellules : {CELL_SIZE}x{CELL_SIZE} pixels")
if os.path.exists(IMAGE_FOLDER):
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(IMAGE_FOLDER, filename)
            try:
                image_hires = pygame.image.load(path).convert_alpha()
                image_scaled = pygame.transform.smoothscale(image_hires, (CELL_SIZE, CELL_SIZE))
                loaded_images[filename] = image_scaled
                print(f"Image chargée et redimensionnée: {filename}")
            except pygame.error as e:
                print(f"Erreur de chargement de l'image {filename}: {e}")
else:
    print(f"AVERTISSEMENT: Le dossier '{IMAGE_FOLDER}' n'existe pas.")






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
                image_name_to_draw = room_id + ".png" # ex: "r2.png"
                
                # 4. Dessine l'image si elle a été chargée
                if image_name_to_draw in loaded_images_dict:
                    image_surface = loaded_images_dict[image_name_to_draw]
                    screen.blit(image_surface, (x * CELL_SIZE, y * CELL_SIZE))

def draw_player_and_indicator(px, py, direction):
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

def draw_inventory(surface, font, inventory_data):
    """
    Dessine l'inventaire (statistiques) du joueur sur la surface de l'interface.
    
    Args:
        surface: L'écran principal (screen)
        font: L'objet pygame.font.Font à utiliser (text_font)
        inventory_data: Le dictionnaire game_state.inventory
    """
    
    # Position de départ pour dessiner (coin haut-gauche de l'UI + marge)
    start_x = WINDOW_WIDTH - 200
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
        
def tirer_valeurs_aleatoires(liste, n):
    valeurs_tirees = [random.choice(liste) for _ in range(n)]
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
            if event.key == pygame.K_z: intended_direction = (0, -1)
            elif event.key == pygame.K_s: intended_direction = (0, 1)
            elif event.key == pygame.K_q: intended_direction = (-1, 0)
            elif event.key == pygame.K_d: intended_direction = (1, 0)
            elif event.key == pygame.K_SPACE:






                
                if intended_direction != (0, 0):
                    new_x = game_state.player_x + intended_direction[0]
                    new_y = game_state.player_y + intended_direction[1]
                    
                    if 0 <= new_x < game_state.GRID_WIDTH and 0 <= new_y < game_state.GRID_HEIGHT:
                        
                        # --- C'EST LA NOUVELLE LOGIQUE IMPORTANTE ---
                        
                        # 1. On regarde ce qu'il y a dans la case où on veut aller
                        target_room_id = game_state.map_grid[new_y][new_x]
                        
                        # 2. Si la case est vide ('0'), on doit "générer" une nouvelle pièce
                        if target_room_id == "0":



                            #on va dans l'inv 
                            #on choisit un room


                            new_room_id = "r10" 
                            
                            # (Plus tard, vous aurez une fonction: 
                            # new_room_id = generate_new_room(new_x, new_y) )
                            
                            # On MET A JOUR la carte du monde !
                            game_state.map_grid[new_y][new_x] = new_room_id
                            print(f"Vous avez découvert : {new_room_id}")

                        # 3. Déplace le joueur
                        game_state.player_x = new_x
                        game_state.player_y = new_y
                    
                    intended_direction = (0, 0)

    # --- Logique de dessin (MODIFIÉE) ---
    
    # 1. Remplit TOUT l'écran principal (1800x1620) de noir
    screen.fill(BLACK)
    
    # 2. Dessine la grille de jeu (images) sur la moitié GAUCHE
    draw_grid(loaded_images)
    
    # 3. Dessine le joueur (outlines) sur la moitié GAUCHE
    draw_player_and_indicator(game_state.player_x, game_state.player_y, intended_direction)
    
    # 4. NOUVEAU: Dessine le rectangle blanc de l'interface à DROITE
    #    (x, y, largeur, hauteur)
    ui_rect = pygame.Rect(GRID_PIXEL_WIDTH, 0, UI_PIXEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, WHITE, ui_rect)
    draw_inventory(screen, text_font, game_state.inventory)
    # 5. Met à jour l'écran
    pygame.display.flip()
    
    clock.tick(30)

# --- Fin ---
pygame.quit()