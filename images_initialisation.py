import os
import pygame
from constantes import *






screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu + Interface")

IMAGE_FOLDER = 'rooms' 
loaded_images = {}   #images de dimension cellule

print(f"Taille cible des cellules : {CELL_SIZE}x{CELL_SIZE} pixels")
if os.path.exists(IMAGE_FOLDER):
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(IMAGE_FOLDER, filename)
            try:
                image_hires = pygame.image.load(path).convert_alpha()
                image_scaled = pygame.transform.smoothscale(image_hires, (CELL_SIZE, CELL_SIZE))
                
                loaded_images[filename] = image_scaled



                #print(f"Image chargée et redimensionnée: {filename}")
            except pygame.error as e:
                print(f"Erreur de chargement de l'image {filename}: {e}")
else:
    print(f"AVERTISSEMENT: Le dossier '{IMAGE_FOLDER}' n'existe pas.")

