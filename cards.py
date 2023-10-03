import random


class Card:
    """
    A card consists of a suit (F, R, M, or B), a cost (a tuple where the first term
    is number of foxes, second rabbits, 3rd mice, and 4th any), a description (the
    actual text of the card) and a name (how the code stores it and knows what to do
    with it)
    """
    def __init__(self, suit, cost, description, name):
        self.suit = suit
        self.cost = cost
        self.description = description
        self.name = name

    def __repr__(self):
        return self.name


    def __str__(self):
        base = self.name + '\n' + self.description + '\n' + "suit: " + self.suit + '\n' + "Crafting Cost: "
        if self.cost[0] > 0:
            base += str(self.cost[0]) + ' Foxes '
        if self.cost[1] > 0:
            base += str(self.cost[1]) + ' Rabbits '
        if self.cost[2] > 0:
            base += str(self.cost[2]) + ' Mice '
        if self.cost[3] > 0:
            base += str(self.cost[3]) + ' of anything.'
        if self.cost == (0,0,0,0):
            base += "Free."
        return base



class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.shuffle()

    def draw(self):
        top = self.cards[0]
        del self.cards[0]
        return top

    def shuffle(self):
        random.shuffle(self.cards)

    def reset(self, discard):
        #Intended to put the discard back into the deck, could work for smaller numbers of cards though
        self.cards.extend(discard)
        self.shuffle()

    def __str__(self):
        #Just print the whole deck
        return str(self.cards)

cards = [Card('M',(0,1,0,0),"Gain a Boot and 1 VP, then discard.",'Travel Gear')]*1
cards = [Card('F',(1,0,0,0),"Gain a Boot and 1 VP, then discard.",'Travel Gear')]*1
cards+= [Card('R',(0,1,0,0),"Gain a Boot and 1 VP, then discard.","A Visit to Friends")]*1
cards+= [Card('B',(0,1,0,0),"Gain a Boot and 1 VP, then discard.","Woodland Runners")]*1
cards+= [Card('F',(0,2,0,0),"Gain a Coin and 3 VP, then discard.","Protection Racket")]*1
cards+= [Card('R',(0,2,0,0),"Gain a Coin and 3 VP, then discard.","Bake Sale")]*1
cards+= [Card('M',(0,2,0,0),"Gain a Coin and 3 VP, then discard.","Investments")]*1
cards+= [Card('M',(0,0,1,0),"Gain a Sack and 1 VP, then discard.","Mouse-in-a-Sack")]*1
cards+= [Card('B',(0,0,1,0),"Gain a Sack and 1 VP, then discard.","Birdy Bindle")]*1
cards+= [Card('F',(0,0,1,0),"Gain a Sack and 1 VP, then discard.","Gently Used Knapsack")]*1
cards+= [Card('R',(0,0,1,0),"Gain a Sack and 1 VP, then discard.","Smuggler\'s Trail")]*1
cards+= [Card('R',(0,0,1,0),"Gain a Tea and 2 VP, then discard.","Root Tea")]*1
cards+= [Card('F',(0,0,1,0),"Gain a Tea and 2 VP, then discard.","Root Tea")]*1
cards+= [Card('M',(0,0,1,0),"Gain a Tea and 2 VP, then discard.","Root Tea")]*1
cards+= [Card('F',(2,0,0,0),"Gain a Sword and 2 VP, then discard.","Foxfolk Steel")]*1
cards+= [Card('M',(2,0,0,0),"Gain a Sword and 2 VP, then discard.","Sword")]*1
cards+= [Card('B',(2,0,0,0),"Gain a Sword and 2 VP, then discard.","Arms Trader")]*1
cards+= [Card('M',(1,0,0,0),"Gain a Crossbow and 1 VP, then discard.","Crossbow")]*1
cards+= [Card('B',(1,0,0,0),"Gain a Crossbow and 1 VP, then discard.","Crossbow")]*1
cards+= [Card('F',(1,0,0,0),"Gain a Hammer and 2 VP, then disard.","Anvil")]*1

cards+= [Card('B',(0,0,0,0),"At start of battle, defender may play to deal two hits, then discard. Cancel if attacker plays matching ambush.","Ambush!")]*2
cards+= [Card('F',(0,0,0,0),"At start of battle, defender may play to deal two hits, then discard. Cancel if attacker plays matching ambush.","Ambush!")]*1
cards+= [Card('R',(0,0,0,0),"At start of battle, defender may play to deal two hits, then discard. Cancel if attacker plays matching ambush.","Ambush!")]*1
cards+= [Card('M',(0,0,0,0),"At start of battle, defender may play to deal two hits, then discard. Cancel if attacker plays matching ambush.","Ambush!")]*1



cards+= [Card('R',(0,2,0,0),"At start of Evening, may take a Move.","Cobbler")]*2

cards+= [Card('F',(3,0,0,0),"Remove all enemy pieces in Fox clearings, then discard.","Favor of the Foxes")]*1
cards+= [Card('R',(0,3,0,0),"Remove all enemy pieces in Rabbit clearings, then discard.","Favor of the Rabbits")]*1
cards+= [Card('M',(0,0,3,0),"Remove all enemy pieces in Mouse clearings, then discard.","Favor of the Mice")]*1

cards+= [Card('M',(0,0,2,0),"As attacker in battle, you are not affected by ambush cards.","Scouting Party")]*2
cards+= [Card('B',(1,0,0,0),"In battle, may discard this to ignore all rolled hits taken.","Armorers")]*2
cards+= [Card('B',(2,0,0,0),"In battle as attacker, may deal an extra hit, but defender scores one point.","Brutal Tactics")]*2
cards+= [Card('B',(0,0,1,0),"In battle as defender, may discard this to deal an extra hit.","Sappers")]*2

cards+= [Card('R',(0,2,0,0),"At start of Birdsong, you and another player draw a card.","Better Burrow Bank")]*2
cards+= [Card('B',(0,0,0,4),"In Birdsong, may discard this to score one point for each clearing you rule.","Royal Claim")]*1
cards+= [Card('F',(0,0,3,0),"In Birdsong, may take a random card from another player. That player scores one point.","Stand and Deliver!")]*2

cards+= [Card('M',(0,0,1,0),"Once in daylight, may look at another players hand.","Codebreakers")]*2
cards+= [Card('F',(1,1,1,0),"Once in Daylight, may remove one of your warriors from the map to draw a card.","Tax Collector")]*3
cards+= [Card('R',(0,2,0,0),"At start of Daylight, may initiate a battle.","Command Warren")]*2

#Dominance cards have to be played during daylight by a player with at least 10 points. Can be spent for suit, and are then made available.
#Also, they only enter the game with three players, so for now they don't exist.
# cards+= [Card('F',(0,0,0,0),"You win the game if you control three Fox clearings at the start of your Birdsong.","Dominance")]*1
# cards+= [Card('R',(0,0,0,0),"You win the game if you control three Rabbit clearings at the start of your Birdsong.","Dominance")]*1
# cards+= [Card('M',(0,0,0,0),"You win the game if you control three Mouse clearings at the start of your Birdsong.","Dominance")]*1
# cards+= [Card('B',(0,0,0,0),"You win the game if you control two opposite corners at the start of your Birdsong.","Dominance")]*1


DECK = Deck(cards)
DISCARD = Deck([])

if __name__ == '__main__':
    pass
