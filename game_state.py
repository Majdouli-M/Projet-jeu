# Fichier: game_state.py

# --- Donn�es du Joueur ---

# L'inventaire du joueur
# On peut utiliser un dictionnaire pour stocker l'ID de l'objet et sa quantit�
# Exemple: {"pot_S": 3, "cle_rouillee": 1}
inventory = {
			"Pas":70,
			"Pieces":0,
			"Gemmes":0,
			"Cles":0,
			"Des":0,
            "Items permanents":[]


}

# La position actuelle du joueur (sera mise � jour par main.py)
player_x = 2
player_y = 8
middle_map_pos = (950, 200)
inventory_indicator_pos = 0
intended_direction = (0, 0)
rooms_on_offer = [] # NOUVEAU: Stocke les 3 ID de pièces proposées
inInventory = False


GRID_WIDTH = 5
GRID_HEIGHT = 9




map_grid = [["0" for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]



# --- Initialisation de la carte ---
# Maintenant, on place manuellement les pi�ces de d�part.
# C'est ici que vous construisez votre "monde".

map_grid[8][2] = "r2"
map_grid[0][2] = "r45"


