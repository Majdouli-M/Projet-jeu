

class Item:
    def __init__(self, name, rarity_score, arg):
        self.name = name
        self.rarity_score = rarity_score
        self.arg = arg

rabbit_bonus = 0 #bonus de rarité pour la patte de lapin
metal_bonus = 0  #bonus de rarité pour le detecteur de metaux
resource_items = {


    1: Item(
        name="Piece", 
        rarity_score=20 + metal_bonus,
        arg = 0
    ),
    2: Item(
        name="Gemme", 
        rarity_score=10 + rabbit_bonus,
        arg = 0
    ),
    3: Item(
        name="Cle", 
        rarity_score=1 + metal_bonus,
        arg = 0
    ),


    4: Item(
        name="De", 
        rarity_score=20 + rabbit_bonus,
        arg = 0
    ),
    5: Item(
        name="Pomme", 
        rarity_score=55 + rabbit_bonus,
        arg = 2
    ),
    6: Item(
        name="Banane", 
        rarity_score=50 + rabbit_bonus,
        arg = 3
    ),
    7: Item(
        name="Gateau", 
        rarity_score=45 + rabbit_bonus,
        arg = 10
    ),
    8: Item(
        name="Sandwich", 
        rarity_score=35 + rabbit_bonus,
        arg = 15
    ),


    9: Item(
        name="Repas", 
        rarity_score=20 + rabbit_bonus,
        arg = 25
    ),

    10: Item(
        name="endroit a creuser", 
        rarity_score=20 + rabbit_bonus,
        arg = [1,2,3,4,5]
    ),

    11: Item(
        name="casier", 
        rarity_score=20 + rabbit_bonus,
        arg = [1,2,3,4,5,6,7,8,9]
    ),

    12: Item(
        name="3 Pieces", 
        rarity_score=50 + rabbit_bonus,
        arg = 3
    ),

    13: Item(
        name="40 Pieces", 
        rarity_score=50 + rabbit_bonus,
        arg = 40
    )


}

special_items = {
    100: Item(
        name="Pelle", 
        rarity_score=20 + rabbit_bonus,
        arg = 0
    ),
    101: Item(
        name="Marteau", 
        rarity_score=50 + rabbit_bonus,
        arg = 0
    ),
    102: Item(
        name="Kit de crochetage", 
        rarity_score=10 + rabbit_bonus,
        arg = 0
    ),
    103: Item(
        name="Detecteur de metaux", 
        rarity_score=1 + rabbit_bonus,
        arg = 0
    ),


    104: Item(
        name="Patte de lapin", 
        rarity_score=1 + rabbit_bonus,
        arg = 0
    )


}