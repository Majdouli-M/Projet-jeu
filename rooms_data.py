
import items_data
from images_initialisation import loaded_images,loaded_ui_images



class Room:
    #("name",item_pool,rarity,price)

    def __init__(self, name, resource_pool, special_pool, rarity, price, portes,image):
        self.name = name
        self.resource_pool = resource_pool
        self.special_pool = special_pool
        self.rarity = rarity
        self.price = price
        self.portes = portes
        self.image = image










rooms = {
    "r2": Room(
        name="Entrance Hall",
        resource_pool=[],
        special_pool=[],
        rarity=999,
        price=0,
        portes=[
            [' ', '#', ' '],
            ['#', ' ', '#'],
            [' ', '#', ' ']
        ],
        image=loaded_images["r2.png"]
    ),

    "r9": Room(
        name="Closet",
        resource_pool=[
            (2, items_data.resource_items[2].rarity_score, 1, 1),
            (3, items_data.resource_items[3].rarity_score, 1, 1),
            (4, items_data.resource_items[4].rarity_score, 1, 1)
        ],
        special_pool=[
            (104, items_data.special_items[104].rarity_score, 0, 1),
            (101, items_data.special_items[101].rarity_score, 0, 1),
            (103, items_data.special_items[103].rarity_score, 0, 1),
            (100, items_data.special_items[100].rarity_score, 0, 1)
        ],
        rarity=1,
        price=1,
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ],
        image=loaded_images["r9.png"]

    ),

    "r10": Room(
        name="Walk-in Closet",
        resource_pool=[
            (7, items_data.resource_items[7].rarity_score, 1, 1),
            (4, items_data.resource_items[4].rarity_score, 1, 2),
            (3, items_data.resource_items[3].rarity_score, 1, 3),
            (2, items_data.resource_items[2].rarity_score, 1, 2),
            (11, items_data.resource_items[11].rarity_score, 1, 1)
        ],
        special_pool=[
            (104, items_data.special_items[104].rarity_score, 0, 1),
            (102, items_data.special_items[102].rarity_score, 0, 1)
        ],
        rarity=1,
        price=1,
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ],
        image=loaded_images["r10.png"]

    ),

    "r11": Room(
        name="Attic",
        resource_pool=[
            (3, items_data.resource_items[3].rarity_score, 1, 5),
            (2, items_data.resource_items[2].rarity_score, 1, 4)
        ],
        special_pool=[
            (101, items_data.special_items[101].rarity_score, 0, 1),
            (102, items_data.special_items[102].rarity_score, 0, 1)
        ],
        rarity=3,
        price=3,
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ],
        image=loaded_images["r11.png"]

    ),

    "r12": Room(
        name="Storeroom",
        resource_pool=[
            (1, items_data.resource_items[1].rarity_score, 1, 1),
            (2, items_data.resource_items[2].rarity_score, 1, 1),
            (3, items_data.resource_items[3].rarity_score, 1, 1)
        ],
        special_pool=[
            (101, items_data.special_items[101].rarity_score, 0, 1),
            (100, items_data.special_items[100].rarity_score, 0, 1)
        ],
        rarity=0,
        price=0,
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ],
        image=loaded_images["r12.png"]

    ),

    "b1": Room(
        name="BedRoom",
        resource_pool=[
            (3, items_data.resource_items[3].rarity_score, 1, 1),
            (2, items_data.resource_items[2].rarity_score, 1, 1),
            (4, items_data.resource_items[4].rarity_score, 1, 1),
            (5, items_data.resource_items[5].rarity_score, 1, 1),
            (12, items_data.resource_items[12].rarity_score, 1, 1)
        ],
        special_pool=[],
        rarity=0,
        price=0,
        portes=[
            [' ', ' ', ' '],
            ['#', ' ', ' '],
            [' ', '#', ' ']
        ],
        image=loaded_images["b1.png"]

    ),

    "b2": Room(
        name="Boudoir",
        resource_pool=[
            (9, items_data.resource_items[9].rarity_score, 1, 1),
            (12, items_data.resource_items[12].rarity_score, 1, 1)
        ],
        special_pool=[],
        rarity=1,
        price=0,
        portes=[
            [' ', ' ', ' '],
            ['#', ' ', ' '],
            [' ', '#', ' ']
        ],
        image=loaded_images["b2.png"]

    ),

    "b5": Room(
        name="Servant's Quarter",
        resource_pool=[
            (2, items_data.resource_items[2].rarity_score, 1, 1),
            (4, items_data.resource_items[4].rarity_score, 1, 2)
        ],
        special_pool=[
            (100, items_data.special_items[100].rarity_score, 0, 1)
        ],
        rarity=3,
        price=2,
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ],
        image=loaded_images["b5.png"]

    ),

    "g4": Room(
        name="Cloister",
        resource_pool=[
            (10, items_data.resource_items[10].rarity_score, 1, 4)
        ],
        special_pool=[],
        rarity=2,
        price=3,
        portes=[
            [' ', '#', ' '],
            ['#', ' ', '#'],
            [' ', '#', ' ']
        ],
        image=loaded_images["g4.png"]

    ),

    "g5": Room(
        name="Veranda",
        resource_pool=[
            (10, items_data.resource_items[10].rarity_score, 1, 4),
            (2, items_data.resource_items[2].rarity_score, 1, 1),
            (100, items_data.special_items[100].rarity_score, 1, 1),
            (101, items_data.special_items[101].rarity_score, 1, 1)
        ],
        special_pool=[],
        rarity=2,
        price=2,
        portes=[
            [' ', '#', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ],
        image=loaded_images["g5.png"]

    ),

    "h1": Room(
        name="Hallway",
        resource_pool=[
            (1, items_data.resource_items[1].rarity_score, 1, 1),
            (2, items_data.resource_items[2].rarity_score, 1, 1),
            (5, items_data.resource_items[5].rarity_score, 1, 1)
        ],
        special_pool=[],
        rarity=0,
        price=0,
        portes=[
            [' ', ' ', ' '],
            ['#', ' ', '#'],
            [' ', '#', ' ']
        ],

        image=loaded_images["h1.png"]

    ),

    "h4": Room(
        name="Corridor",
        resource_pool=[
            (1, items_data.resource_items[1].rarity_score, 1, 2),
            (2, items_data.resource_items[2].rarity_score, 1, 1),
            (3, items_data.resource_items[3].rarity_score, 1, 1),
            (5, items_data.resource_items[5].rarity_score, 1, 1)
        ],
        special_pool=[],
        rarity=0,
        price=0,
        portes=[
            [' ', '#', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ],

        image=loaded_images["h4.png"]

    ),

    "r45": Room(
        name="Antechamber",
        resource_pool=[
            (1, items_data.resource_items[1].rarity_score, 1, 1),
            (2, items_data.resource_items[2].rarity_score, 1, 1),
            (5, items_data.resource_items[5].rarity_score, 1, 1)
        ],
        special_pool=[],
        rarity=999,
        price=0,
        portes=[
            [' ', '#', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ],

        image=loaded_images["r45.png"]

    ),
}

    



