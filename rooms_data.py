

class Room:
    #("name",item_pool,rarity,price)

    def __init__(self,name,resource_pool,special_pool,rarity,price,directions):

        self.name = name
        self.resource_pool = resource_pool
        self.special_pool = special_pool
        self.rarity = rarity
        self.price = price
        self.directions= directions
    
    

rooms = {"r2":Room(name="Entrance Hall",resource_pool=[],special_pool=[],rarity=999,price=0,directions=["up","left","right"]),
        "r9":Room(name="Closet",resource_pool=[2,3,4],special_pool=[104,101,103,100],rarity=1,price=1,directions=["down"]),

        "r10":Room(name="Walk-in Closet",resource_pool=[7,4,4,3,3,3,2,2,11],special_pool=[104,102],rarity=1,price=1,directions=["down"]),
        "r11":Room(name="Attic",resource_pool=[3,3,3,3,2,2,2,2,3,],special_pool=[101,102],rarity=3,price=3,directions=["down"]),
        "r12":Room(name="Attic",resource_pool=[3,3,3,3,2,2,2,2,3,],special_pool=[101,102],rarity=3,price=3,directions=["down"]),



             
             
             
                     
             
             
             
             
} 