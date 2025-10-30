class Room:
    #("name",item_pool,rarity,price)

    def __init__(self, name, resource_pool, special_pool, rarity, price, directions, portes):
        self.name = name
        self.resource_pool = resource_pool
        self.special_pool = special_pool
        self.rarity = rarity
        self.price = price
        self.directions = directions
        self.portes = portes


rooms = {
    "r2": Room(
        name="Entrance Hall",
        resource_pool=[],
        special_pool=[],
        rarity=999,
        price=0,
        directions=["up", "left", "right"],
        portes=[
            [' ', '#', ' '],
            ['#', ' ', '#'],
            [' ', ' ', ' ']
        ]
    ),

    "r9": Room(
        name="Closet",
        resource_pool=[2, 3, 4],
        special_pool=[104, 101, 103, 100],
        rarity=1,
        price=1,
        directions=["down"],
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "r10": Room(
        name="Walk-in Closet",
        resource_pool=[7, 4, 4, 3, 3, 3, 2, 2, 11],
        special_pool=[104, 102],
        rarity=1,
        price=1,
        directions=["down"],
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "r11": Room(
        name="Attic",
        resource_pool=[3, 3, 3, 3, 2, 2, 2, 2, 3],
        special_pool=[101, 102],
        rarity=3,
        price=3,
        directions=["down"],
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "r12": Room(
        name="Storeroom",
        resource_pool=[1, 2, 3],
        special_pool=[101, 100],
        rarity=0,
        price=0,
        directions=["down"],
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "b1": Room(
        name="BedRoom",
        resource_pool=[3, 2, 4, 5, 12],
        special_pool=[],
        rarity=0,
        price=0,
        directions=["down", "left"],
        portes=[
            [' ', ' ', ' '],
            ['#', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "b2": Room(
        name="Boudoir",
        resource_pool=[9, 12],
        special_pool=[],
        rarity=1,
        price=0,
        directions=["down", "left"],
        portes=[
            [' ', ' ', ' '],
            ['#', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "b5": Room(
        name="Servant's Quarter",
        resource_pool=[2, 4, 4],
        special_pool=[100],
        rarity=3,
        price=2,
        directions=["down"],
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "g4": Room(
        name="Cloister",
        resource_pool=[10, 10, 10, 10],
        special_pool=[],
        rarity=2,
        price=3,
        directions=["down", "up", "left", "right"],
        portes=[
            [' ', '#', ' '],
            ['#', ' ', '#'],
            [' ', '#', ' ']
        ]
    ),

    "g5": Room(
        name="Veranda",
        resource_pool=[10, 10, 10, 10, 2, 100, 101],
        special_pool=[],
        rarity=2,
        price=2,
        directions=["down", "up"],
        portes=[
            [' ', '#', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "h1": Room(
        name="Hallway",
        resource_pool=[1, 2, 5],
        special_pool=[],
        rarity=0,
        price=0,
        directions=["down"],
        portes=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "h4": Room(
        name="Corridor",
        resource_pool=[1, 1, 2, 3, 5],
        special_pool=[],
        rarity=0,
        price=0,
        directions=["down", "up"],
        portes=[
            [' ', '#', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),

    "r45": Room(
        name="Antechamber",
        resource_pool=[1, 2, 5],
        special_pool=[],
        rarity=999,
        price=0,
        directions=["down", "up"],
        portes=[
            [' ', '#', ' '],
            [' ', ' ', ' '],
            [' ', '#', ' ']
        ]
    ),
}
