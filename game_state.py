# Fichier: game_state.py
import rooms_data

from constantes import GRID_WIDTH,GRID_HEIGHT
# --- Donn�es du Joueur ---

# L'inventaire du joueur
# On peut utiliser un dictionnaire pour stocker l'ID de l'objet et sa quantit�
# Exemple: {"pot_S": 3, "cle_rouillee": 1}
inventory = {
			"Pas":70,
			"Pieces":0,
			"Gemmes":200,
			"Cles":200,
			"Des":200,
            "Items permanents":[]


}

# La position actuelle du joueur (sera mise � jour par main.py)
player_x = 2
player_y = 8
middle_map_pos = (950, 200)
inventory_indicator_pos = 0
items_indicator_pos = 0 #curseur de selection des items
intended_direction = (0, 0)
build_target_coords = (0,0)
rooms_on_offer = [] # NOUVEAU: Stocke les 3 ID de pièces proposées
rooms_on_offer_mats = []
rooms_on_offer_images = []

items_tirees = []



visited_coords = [(8,2)] #liste de tuples des coordonnées visitees
porte_ouverte = False
inInventory = False



items_selection = False #si on est dans le menu de selection des items tires aleatoirement


temp_message = None #message affiché temporairement qd choix deplacement joueur impossible
duree_temp_message = 0 # duree affichage


map_grid = [["0" for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]



map_grid_portes =  [[ [[' ', ' ', ' ]'],[' ', ' ', ' '],[' ', ' ', ' ']] for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]  

map_grid_images = [["" for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]



# --- Initialisation de la carte ---
# Maintenant, on place manuellement les pi�ces de d�part.
# C'est ici que vous construisez votre "monde".

map_grid[8][2] = "r2"
map_grid_portes[8][2] = rooms_data.rooms["r2"].portes
map_grid_images[8][2] = rooms_data.rooms["r2"].image

map_grid[0][2] = "r45"
map_grid_portes[0][2] = rooms_data.rooms["r45"].portes
map_grid_images[0][2] = rooms_data.rooms["r45"].image



