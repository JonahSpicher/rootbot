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



if __name__ == '__main__':
    pass
    print("this is a test")
