import pygame
import os
import random
import ctypes  # NOUVEAU: Importé pour corriger le flou sur Windows

# NOUVEAU: Début du bloc anti-flou pour Windows
# Cela force Windows à ne pas "zoomer" l'application,
# ce qui est la cause principale du flou.
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except AttributeError:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        print("Avertissement : Impossible de régler la sensibilisation PPP (DPI).")
# NOUVEAU: Fin du bloc


# --- Constantes ---
# Définissez la largeur que vous souhaitez pour votre fenêtre
DISPLAY_WIDTH = 900  # (Doit être un multiple de 5, ex: 400, 500...)

GRID_WIDTH = 5
GRID_HEIGHT = 9

# CELL_SIZE est maintenant CALCULÉ en fonction de la largeur
CELL_SIZE = DISPLAY_WIDTH // GRID_WIDTH # (ex: 450 / 5 = 90)

# La hauteur de l'écran est aussi CALCULÉE
DISPLAY_HEIGHT = CELL_SIZE * GRID_HEIGHT # (ex: 90 * 9 = 810)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

IMAGE_FOLDER = 'rooms' 

# --- Initialisation de Pygame ---
# Doit être APRES le bloc ctypes
pygame.init()

# Crée l'écran principal
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Déplacement sur Grille 5x9 (Rendu Net)")
clock = pygame.time.Clock()

# --- Section de chargement des images ---
loaded_images = {} 
print(f"Taille cible des cellules : {CELL_SIZE}x{CELL_SIZE} pixels")

if os.path.exists(IMAGE_FOLDER):
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(IMAGE_FOLDER, filename)
            try:
                # 1. Charge l'image haute résolution (ex: 185x185)
                image_hires = pygame.image.load(path).convert_alpha()
                
                # 2. Rétrécit l'image avec smoothscale (rendu doux)
                image_scaled = pygame.transform.smoothscale(image_hires, (CELL_SIZE, CELL_SIZE))
                
                # 3. Stocke l'image pré-rétrécie
                loaded_images[filename] = image_scaled
                print(f"Image chargée et redimensionnée: {filename}")
                
            except pygame.error as e:
                print(f"Erreur de chargement de l'image {filename}: {e}")
else:
    print(f"AVERTISSEMENT: Le dossier '{IMAGE_FOLDER}' n'existe pas.")

# --- Variables du jeu ---
player_y = 8  # Ligne (0 à 8)
player_x = 2  # Colonne (0 à 4)
intended_direction = (0, 0)
cell_content = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# --- Bloc de placement des images spécifiques ---
try:
    # Syntaxe: cell_content[Y][X] = loaded_images["nom_du_fichier.png"]
    if "2.png" in loaded_images:
         cell_content[8][2] = loaded_images["2.png"]
    if "rocher.jpg" in loaded_images:
         cell_content[7][3] = loaded_images["rocher.jpg"]
    # (Ajoutez vos autres images ici)
         
except KeyError as e:
    print(f"Erreur: Impossible de placer l'image {e}. Fichier non chargé.")

# --- Fonction pour dessiner la grille (sans lignes) ---
def draw_grid():
    """Dessine UNIQUEMENT les images des cellules."""
    
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            image_to_draw = cell_content[y][x]
            if image_to_draw is not None:
                # Dessine l'image pré-rétrécie directement sur l'écran
                screen.blit(image_to_draw, (x * CELL_SIZE, y * CELL_SIZE))

# --- Fonction pour dessiner le joueur et l'indicateur ---
def draw_player_and_indicator(px, py, direction):
    """Dessine le joueur (outline) où l'arête sélectionnée est plus épaisse."""
    
    default_thickness = 2   # Épaisseur standard
    selected_thickness = 8  # Épaisseur de l'arête sélectionnée
    
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
    
    # Dessine l'outline en BLANC
    pygame.draw.line(screen, WHITE, p_topleft, p_topright, thickness_top)
    pygame.draw.line(screen, WHITE, p_bottomleft, p_bottomright, thickness_bottom)
    pygame.draw.line(screen, WHITE, p_topleft, p_bottomleft, thickness_left)
    pygame.draw.line(screen, WHITE, p_topright, p_bottomright, thickness_right)

# --- Boucle principale du jeu ---
running = True
print("Utilisez ZQSD pour choisir une direction.")
print("Appuyez sur ESPACE pour vous déplacer dans cette direction.")

while running:
    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z: intended_direction = (0, -1)
            elif event.key == pygame.K_s: intended_direction = (0, 1)
            elif event.key == pygame.K_q: intended_direction = (-1, 0)
            elif event.key == pygame.K_d: intended_direction = (1, 0)
                
            elif event.key == pygame.K_SPACE:
                if intended_direction != (0, 0):
                    new_x = player_x + intended_direction[0]
                    new_y = player_y + intended_direction[1]
                    
                    if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                        player_x = new_x
                        player_y = new_y
                    
                    intended_direction = (0, 0) 

    # --- Logique de dessin ---
    
    # 1. Remplit l'écran principal de noir
    screen.fill(BLACK)
    
    # 2. Dessine la grille (images pré-rétrécies)
    draw_grid()
    
    # 3. Dessine le joueur (outlines)
    draw_player_and_indicator(player_x, player_y, intended_direction)
    
    # 4. Met à jour l'écran
    pygame.display.flip()
    
    clock.tick(30)

# --- Fin ---
pygame.quit()