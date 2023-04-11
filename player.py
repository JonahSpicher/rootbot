from map import *
import random
"""
Things to add:
- crafting
- taking actions during daylight, bird cards to take more
- cards that just do points, items
- ambush cards
- more complicated cards
- Field Hospitals???


"""

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
        return self.name + '\n' + self.description

class CatPlayer:
    def __init__(self, player_num):
        self.hand = []
        self.items = []
        self.costs = [0,1,2,3,3,4]
        self.sawmill_points = [0,1,2,3,4,5]
        self.recruiter_points = [0,1,2,3,3,4]
        self.workshop_points = [0,2,2,3,4,5]
        self.workshop_suits = {'F':0, 'R':0, 'M':0}
        self.building_nums = {'S':0, 'W':0, 'Re':0}
        self.player_num = player_num #For Rule purposes


        self.score = 0



    ######################  PHASES ##########################

    def birdsong(self):
        print("PLacing wood for birdsong...")
        total = 0
        for c in CLEARINGS:
            if 'S' in c.buildings:
                total += 1
                c.tokens.append('W')
        print("Placed %d wood."%total)

    def daylight(self):
        """
        For now, this is going to accept player input. Can be modified later for bots.

        """

        for card in self.hand:
            print(i, card)
        craft_selection = input("Would you like to craft any cards? Your hand is printed above. Type no to move on, or the matching index to craft a card.\n")
        if craft_selection == 'no':
            print("Moving on to actions.")

        else:
            self.craft(craft_selection)
            #Very much a work in progress but I am tired 







    ######################  ACTIONS  ##########################







    def battle(self, clearing):
        """
        ACTION
        choose clearing and faction to battle (kinda silly for now)
        Eventually, need to track faction, only one right now though
        Also add ambush, and other possibilities
        """
        c = CLEARINGS[clearing]
        if (c.cat_count >= 1) and (('Ro' in c.buildings) or (c.bird_count >= 1) ):
            roll1 = random.randint(0,3)
            roll2 = random.randint(0,3) #Eventually might want this to be a thing we can input
            print(roll1, roll2)
            cat_hits = max(roll1, roll2) #First, attacker gets higher roll
            bird_hits = min(roll1, roll2)
            cat_hits = min(cat_hits, c.cat_count) #if more hits than warriors, capped at warriors
            bird_hits = min(bird_hits, c.bird_count)
            if c.bird_count == 0:
                cat_hits += 1 #For helpless
            print("Adjusted Hits: ", cat_hits, bird_hits)
            #Finally, assign hits
            if cat_hits <= c.bird_count:
                c.add_warrior(-1*cat_hits, 2) #subtract warriors actually lol
            else: #Must be greater
                c.add_warrior(-1*c.bird_count, 2)
                #In the cats case, the only thing that could be left to attack is a roost
                if 'Ro' in c.buildings:
                    c.buildings.remove('Ro')
            if bird_hits <= c.cat_count:
                c.add_warrior(-1*bird_hits, 1)
            else: #here we go
                remainder = bird_hits - c.cat_count
                c.add_warrior(-1*c.cat_count, 1)
                for i in range(remainder):
                    if 'W' in c.tokens:
                        c.tokens.remove('W')
                    elif 'S' in c.buildings:
                        c.buildings.remove('S')
                        self.building_nums['S'] -= 1
                    elif 'W' in c.buildings:
                        c.buildings.remove('W')
                        self.building_nums['W'] -= 1
                        self.workshop_suits[c.suit] -= 1
                    elif 'Re' in c.buildings:
                        c.buildings.remove('R')
                        self.building_nums['Re'] -= 1
                    elif 'K' in c.tokens:
                        c.tokens.remove('K')
                        break
            return True


        else:
            print("Both sides must be present to battle")
            return False



    def recruit(self):
        #ACTION
        #literally cant imagine how this one could fail? I guess if there are no recruiters?
        if self.building_nums['Re'] == 0:
            print("Yikes")
            return False
        for c in CLEARINGS:
            if 'Re' in c.buildings:
                c.add_warrior(1,1)
        return True

    def move(self, c1, c2, num):
        if num <= CLEARINGS[c1].cat_count:
            if CLEARINGS[c1].rule == self.player_num or CLEARINGS[c2].rule == self.player_num:
                CLEARINGS[c1].add_warrior(-1*max(0,num), 1)
                CLEARINGS[c2].add_warrior(max(0,num),1)
                return True
            else:
                print("Cannot make move, rule conditions not met")
        else:
            print("Cannot make move, not enough warriors present")
        return False


    def march(self, m1, m2):
        #ACTION
        r1 = self.move(*m1)
        if r1:
            r2 = self.move(*m2)
            return r2
        return False

    def build(self, clearing, building):
        """
        ACTION
        Makes sure it is allowed to build a building. If it is, builds it.
        """
        if CLEARINGS[clearing].build_slots > len(CLEARINGS[clearing].buildings) and CLEARINGS[clearing].rule == self.player_num:
            if self.collect_wood(building, clearing):
                self.building_score(building)
                CLEARINGS[clearing].add_building(building)
                if building == 'W':
                    self.workshop_suits[CLEARINGS[clearing.suit]]+= 1
                return True
            else:
                print("Not enough wood for "+building+" in clearing "+str(clearing))
        else:
            print("No empty slot for "+building+" in clearing "+str(clearing))
            print("(Or you dont rule it lol)")
        return False


    def overwork(self, clearing, card):
        # ACTION
        c = CLEARINGS[clearing]
        if self.cards[card].suit != c.suit and self.cards[card].suit != 'B':
            print("Card suit must match clearing")
            return False
        c.tokens.append('W')
        del self.cards[card] #When discard pile is necessary, fix this
        return True




    ######################  UTILITIES  ##########################

    def craft(self, card):
        """
        Basically just make sure that the cost is covered by workshops and then boom
        """
        return True


    def is_connected(self, c1, c2, searched=None):
        """
        For the purposes of wood supply lines only
        """
        #print("Searching for connection between clearings %d and %d"%(c1,c2))
        #print("Have already searched:", searched)
        if searched is None:
            searched = [c1]
        else:
            searched.append(c1)
        if c1 == c2:
            return True, searched

        #print("Rule check:")
        #print(CLEARINGS[c1].rule, CLEARINGS[c2].rule, self.player_num)
        if CLEARINGS[c1].rule == self.player_num and CLEARINGS[c2].rule == self.player_num:
            #print("Both ends ruled")
            for c in CLEARINGS[c1].connections:
                if c not in searched:
                    #print("Moving down to next level with clearing ", c)
                    res, searched = self.is_connected(c, c2, searched)
                    if res:
                        return True, searched
            return False, searched

        else: #We don't rule endpoint
            return False, searched

    def collect_wood(self, building, clearing):
        """
        Make sure enough wood is present to build the given building (check cost),
        if yes then remove that amount of wood
        """
        cost = self.costs[self.building_nums[building]]
        #print("Cost: ", cost)
        total_wood = 0
        for i in range(12):
            #print(CLEARINGS[i].tokens)
            if 'W' in CLEARINGS[i].tokens:
                if self.is_connected(i, clearing)[0]:
                    #print("Connection found")
                    total_wood += CLEARINGS[i].tokens.count('W')
                    CLEARINGS[i].tokens = list(filter(lambda x:x!='W', CLEARINGS[i].tokens))
                    #print("Wood comparison:")
                    #print(total_wood, cost)
                    if total_wood >= cost:
                        #Partially empty and stop
                        #print("Found too much")
                        diff = total_wood - cost #if 0, thats fine
                        CLEARINGS[i].tokens.extend(['W']*diff) #Add wood back in if we took too much
                        break
                #print(i)
        if total_wood >= cost:
            return True
        else:
            #OH NO PUT IT ALL BACK
            for i in range(12):
                if 'S' in CLEARINGS[i].buildings:
                    CLEARINGS[i].tokens.extend(['W']*total_wood) #Just like throw it in the first sawmill for now I dont know
                    break
            return False


    def building_score(self, building):
        """
        Find number of points awarded for this building, then add 1 to number built
        """
        if building == 'W':
            points = self.workshop_points[self.building_nums['W']]
            self.score += points
            self.building_nums['W']+=1
            print("Built workshop for "+str(points)+" points")
        elif building == 'Re':
            points = self.recruiter_points[self.building_nums['Re']]
            self.score += points
            self.building_nums['Re']+=1
            print("Built recruiter for "+str(points)+" points")
        elif building == 'S':
            points = self.sawmill_points[self.building_nums['S']]
            self.score += points
            self.building_nums['S']+=1
            print("Built sawmill for "+str(points)+" points")







if __name__ == '__main__':
#For testing

    # CLEARINGS[0].add_building('W')
    # CLEARINGS[1].add_building('Re')
    # CLEARINGS[3].add_building('S')
    #CLEARINGS[6].add_warrior(1, 1)
    for i in range(len(CLEARINGS)):
        if i%2==0 and i!=0:
            CLEARINGS[i].add_warrior(i+1, 2)
            CLEARINGS[i].add_building('Ro')
        if i!=11:
            CLEARINGS[i].add_warrior(1, 1)
        if i < 5:
            CLEARINGS[i].tokens.append('W')

    marquise = CatPlayer(1)
    CLEARINGS[0].tokens.append('K')
    marquise.build(0, 'W')
    marquise.build(1, 'Re')
    marquise.build(3, 'S')

    marquise.build(7, 'S')
    marquise.build(3, 'Re')
    marquise.recruit()
    marquise.march((1,2,2),(10,11,1))

    marquise.battle(2)
    status = True



    draw_map(CLEARINGS)
    while(status):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                status=False
    pygame.quit()
