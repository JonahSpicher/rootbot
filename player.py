from map import *
"""
Things to add:
- hand
- crafting
- building
- marching
- battling
- recruit
- overwork (/wood production in general)
- taking actions during daylight, bird cards to take more
- scoring points
- cards that just do points, items
- items


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

class CatPlayer:
    def __init__(self, player_num):
        self.hand = []
        self.items = []
        self.costs = [0,1,2,3,3,4]
        self.sawmill_points = [0,1,2,3,4,5]
        self.recruiter_points = [0,1,2,3,3,4]
        self.workshop_points = [0,2,2,3,4,5]
        self.building_nums = {'S':0, 'W':0, 'Re':0}
        self.player_num = player_num #For Rule purposes


        self.score = 0

    def build(self, clearing, building):
        """
        Makes sure it is allowed to build a building. If it is, builds it.
        """
        if CLEARINGS[clearing].build_slots > len(CLEARINGS[clearing].buildings) and CLEARINGS[clearing].rule == self.player_num:
            if self.collect_wood(building, clearing):
                self.building_score(building)
                CLEARINGS[clearing].add_building(building)
            else:
                print("Not enough wood for "+building+" in clearing "+str(clearing))
        else:
            print("No empty slot for "+building+" in clearing "+str(clearing))




    def is_connected(self, c1, c2, searched=None):
        """
        For the purposes of wood supply lines only
        """
        if searched is None:
            searched = [c1]
        else:
            searched.append(c1)
        if CLEARINGS[c1].rule == self.player_num and CLEARINGS[c2].rule == self.player_num:

            for c in CLEARINGS[c1].connections:
                if c not in searched:
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
        total_wood = 0
        for i in range(12):
            if 'W' in CLEARINGS[i].tokens:
                if self.is_connected(i, clearing)[0]:
                    total_wood += CLEARINGS[i].tokens.count('W')
                    CLEARINGS[i].tokens = list(filter(lambda x:x!='W', CLEARINGS[i].tokens))
                    if total_wood >= cost:
                        #Partially empty and stop
                        diff = total_wood - cost #if 0, thats fine
                        CLEARINGS[i].tokens.extend(['W']*diff) #Add wood back in if we took too much
                        break
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
    CLEARINGS[6].add_warrior(1, 1)
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
    status = True



    draw_map(CLEARINGS)
    while(status):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                status=False
    pygame.quit()
