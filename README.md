                      **Bleu Prince**

## **Description**

Notre projet consiste à développer en Python une version simplifiée du jeu Blue Prince. 
C'un jeu en 2D dans lequel le joueur progresse à travers différentes salles tout en gagnant des items qui l’aident à avancer.  
L’objectif principal était de créer un jeu structuré de manière modulaire, en appliquant les principes de la programmation orientée objet.


## **Fonctionnalités principales**

- Generation et affichage du manoir et de la grille
- Gestion des déplacements du joueur et des portes
- Tirage aléatoire des pièces et objets
- Inventaire et gestion des ressources du joueur
- Chargement et affichage des images
- Définition des caractéristiques des salles et des items


## **Structure du projet**

```bash
├── README.md                 # Ce fichier, explique le projet et ses fonctionnalités
├── requirements.txt          # Dépendances Python nécessaires pour exécuter le jeu
├── main.py                   # Fichier principal du jeu, gère la logique et l’affichage, lance le programme
│
├── constantes/               # Contient les paramètres et constantes du jeu (dimensions, couleurs, tailles de cellules)
│   └── ...                  
│
├── game_state/               # Gère les données globales du jeu : inventaire, position du joueur, état des pièces
│   └── ...                   
│
├── images_initialisation/    # Charge et initialise les images pour l’affichage des salles et items
│   └── ...                  
│
├── items_data/               # Définit les objets collectables et leurs propriétés (nom, rareté)
│   └── ...                   
│
├── rooms_data/               # Définit les rooms du manoir avec leurs caractéristiques, objets et emplacement des portes
│   └── ...                   
│
└── rooms/                    # Contient les images des rooms utilisées dans le jeu
    └── ...
```

## **Installation des dépendances**

Assure-toi d’avoir Python installé puis exécute :
pip install -r requirements.txt



## **Lancement du jeu**

Utilisez la commande suivante dans le terminal :
python main.py


## **Modification de la taille de la fenêtre du jeu** :

# Ligne 5 du fichier constantes.py vous pouvez adapter la taille de la fenêtre en pixels en augmentant ou diminuant 700:
GRID_PIXEL_WIDTH = 700  

## **Auteurs**

**BOUREMANI Yones*
**El MAJDOULI Mohamed*
**NIANG Serigne Moustapha*



