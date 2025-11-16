GRID_WIDTH = 5
GRID_HEIGHT = 9
# --- Constantes ---

GRID_PIXEL_WIDTH = 700  


# CELL_SIZE est calculé à partir de la grille
CELL_SIZE = GRID_PIXEL_WIDTH // GRID_WIDTH 
INV_CELL_SIZE = CELL_SIZE*1.5

GRID_PIXEL_HEIGHT = CELL_SIZE * GRID_HEIGHT 

# NOUVEAU: Largeur de la zone d'interface (identique à la grille)
UI_PIXEL_WIDTH = GRID_PIXEL_WIDTH*1.2

# NOUVEAU: Dimensions totales de la FENÊTRE
WINDOW_WIDTH = GRID_PIXEL_WIDTH + UI_PIXEL_WIDTH 
WINDOW_HEIGHT = GRID_PIXEL_HEIGHT 



# Couleurs (Inchangé)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
GRAY = (100, 100, 100)