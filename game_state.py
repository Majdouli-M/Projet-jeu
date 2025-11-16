# Fichier: game_state.py
import rooms_data

from constantes import GRID_WIDTH,GRID_HEIGHT


#inventaire du joueur
inventory = {
			"Pas":3,
			"Pieces":0,
			"Gemmes":2,
			"Cles":0,
			"Des":0,
            "Items permanents":[]


}

player_x = 2 #coordonnées du joueur ( colonnes)
player_y = 8 #coordonée du joueur (lignes)
middle_map_pos = (950, 200) #coordonnées de la map du milieu lors de la selection dans l'inventaire
inventory_indicator_pos = 0 # indicateur de selection des maps
items_indicator_pos = 0 # indicateur de selection des items
intended_direction = (0, 0) #direction du joueur choisie avec les touches zqsd
build_target_coords = (0,0) #utilisé pour sauvegarder la position où le joueur va ajouter une room
rooms_on_offer = [] #stockage des ids des rooms tirées
rooms_on_offer_mats = [] #stockage des matrices des rooms tirées
rooms_on_offer_images = [] #stockage de l'image des rooms tirées
items_tirees = [] #stockage des items tirés 
visited_coords = [(8,2)] #liste de tuples des coordonnées visitees
porte_ouverte = False # si la porte est ouverte
inInventory = False #si le joueur est dans l'inventaire
items_selection = False #si on est dans le menu de selection des items tires aleatoirement
game_won = False #flag si le joueur a gagné (= atteint la room r45)
game_lost = False #flag si le joueur a perdu (plus de pas)
temp_message = None #message affiché temporairement qd choix deplacement joueur impossible
duree_temp_message = 0 # duree affichage



#matrice qui contient les ids de chaque rooms presente sur la map
map_grid = [["0" for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]


#matrice qui contient les portes (matrice associée à une room) de chaque rooms presente sur la map

map_grid_portes =  [[ [[' ', ' ', ' ]'],[' ', ' ', ' '],[' ', ' ', ' ']] for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]  


#matrice qui contient les images (dans le fichier rooms) de chaque rooms présente sur la map
map_grid_images = [["" for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]



# --- Initialisation de la carte ---



#room de départ
map_grid[8][2] = "r2"
map_grid_portes[8][2] = rooms_data.rooms["r2"].portes
map_grid_images[8][2] = rooms_data.rooms["r2"].image



#room d'arrivée 
map_grid[0][2] = "r45"
map_grid_portes[0][2] = rooms_data.rooms["r45"].portes
map_grid_images[0][2] = rooms_data.rooms["r45"].image



