GRID_WIDTH = 5
GRID_HEIGHT = 9
# --- Constantes ---
# MODIFIÉ: Renommage pour plus de clarté
GRID_PIXEL_WIDTH = 700  # Largeur de la zone de jeu (votre ancien DISPLAY_WIDTH)


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