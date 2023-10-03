from map import *
from cards import Card, Deck
import random
"""
Things to add:
- crafting
- cards that just do points, items
- ambush cards
- more complicated cards
- Field Hospitals???
- The draw and discard pile

Known bugs:
- daylight prints weird
- One time when I did an action wrong the whole thing crashed it was weird
- Hired birds not discarding

"""



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

        self.phase = 0 #Track point in turn, 0 birdsong, 1 daylight, 2 evening
        self.dstage = 0 #During daylight, keep track of current status while waiting for commands
        self.current_action = 10
        self.actions = 0
        self.max_actions = 3




    ######################  PHASES ##########################

    def birdsong(self):
        """
        Very straightforward, just places a wood on each sawmill
        """
        print("Placing wood for birdsong...")
        total = 0
        for c in CLEARINGS:
            if 'S' in c.buildings:
                total += 1
                c.tokens.append('W')
        print("Placed %d wood."%total)
        print("Currently have %d points."%self.score)



    def daylight(self, command=None):
        """
        For now, this is going to accept player input. Can be modified later for bots.
        First, offers crafting.
        """
        # print("Beginning daylight, dstage:", self.dstage)
        # print("Action:", self.current_action)
        # print("Command: ", command)
        if self.dstage == 0:
            print("Starting Daylight...")
            #print(self.hand)
            #print("Setting dstage to 1")
            self.dstage = 1

        #Crafting loop
        if self.dstage == 1: #For crafting

            if len(self.hand)==0:
                print("No cards available for crafting. Moving on to Actions.")
                print("Setting dstage to 2")
                self.dstage = 2
                return 0
            i = 0
            print('\n')
            for card in self.hand:
                print(i, card)
                i+=1
            print('\n')
            print("Would you like to craft any cards? Your hand is printed above. Type no to move on, or the matching index to craft a card.\n")
            if command is None:
                return 0
            if command == 'no':
                print("Moving on to actions.")
                self.dstage = 2
                return 0
            try:
                selected = int(command)
                valid = True
            except ValueError:
                valid = False
            if valid:
                if selected < len(self.hand):
                    self.craft(selected)
                    self.dstage=0
                    return 0
                else:
                    print("Not a valid card index, try again.")
                    return 0
            else:
                print("Type the number printed before the card")
                return 0




        if self.dstage == 2 and self.actions == self.max_actions:
            self.dstage = 6
        if self.dstage < 6:
            print("Action number ", self.actions+1)
            print("Select your action from this list:\n0 Build\n1 Battle\n2 March\n3 Overwork\n4 Recruit\n5 Pass\n")


        if self.dstage == 2:
            self.dstage = 3
            return 0
        if self.dstage == 3:
            choice = command
            try:
                self.current_action = int(choice)
                self.dstage = 4
            except ValueError:
                self.current_action = 10

        if self.dstage <6:
            if self.current_action == 0: #Build - works
                if self.dstage == 4:
                    print("Sawmill Cost: ", self.costs[self.building_nums['S']])
                    print("Workshop Cost: ", self.costs[self.building_nums['W']])
                    print("Recruiter Cost: ", self.costs[self.building_nums['Re']])
                    print("Enter clearing (0-11) and building (S for sawmill, Re for recruiter, and W for workshop) in format C,B")
                    self.dstage = 5
                    return 0
                if self.dstage == 5:
                    try:
                        c,b = command.split(',')
                        c = int(c)

                        if c<0 or c>11 or b not in ['S', 'Re', 'W']:
                            print("Not a valid entry.\nEnter clearing (0-11) and building (S for sawmill, Re for recruiter, and W for workshop) in format C,B")
                            return 0
                    except ValueError:
                        print("Not a valid entry.\nEnter clearing (0-11) and building (S for sawmill, Re for recruiter, and W for workshop) in format C,B")
                        return 0

                    if (self.build(c, b)):
                        self.actions += 1
                        self.dstage = 2
                        self.current_action = 10
                        return 0
                    else:
                        print("Failed to build, try again.")
                        self.dstage = 2
                        self.current_action = 10
                        return 0

            elif self.current_action == 1: #Battle - works
                if self.dstage == 4:
                    print("Enter clearing (0-11).")
                    self.dstage = 5
                    return 0
                if self.dstage == 5:
                    try:
                        c = int(command)

                        if c<0 or c>11:
                            print("Not a valid entry.\nEnter clearing (0-11) and building (S for sawmill, Re for recruiter, and W for workshop) in format C,B")
                            return 0
                    except ValueError:
                        print("Not a valid entry.\nEnter clearing (0-11) and building (S for sawmill, Re for recruiter, and W for workshop) in format C,B")
                        return 0

                    if (self.battle(c)):
                        self.actions += 1
                        self.dstage = 2
                        self.current_action = 10
                        return 0
                    else:
                        print("Failed to battle, try again.")
                        self.dstage = 2
                        self.current_action = 10
                        return 0

            elif self.current_action == 2: #March - works
                if self.dstage == 4:
                    print("Enter clearings (0-11) and troop count for two moves, in format c1,c2,num1,c3,c4,num2 (moving num1 troops from c1->c2, then num2 troops from c3->c4).")
                    self.dstage = 5
                    return 0
                if self.dstage == 5:
                    try:
                        c1,c2,num1,c3,c4,num2 = command.split(',')
                        c1 = int(c1)
                        c2 = int(c2)
                        num1 = int(num1)
                        c3 = int(c3)
                        c4 = int(c4)
                        num2 = int(num2)

                        if c1<0 or c1>11 or c2<0 or c2>11 or c3<0 or c3>11 or c4<0 or c4>11:
                            print("Not a valid entry.")
                            print("Enter clearings (0-11) and troop count for two moves, in format c1,c2,num1,c3,c4,num2 (moving num1 troops from c1->c2, then num2 troops from c3->c4).")

                            return 0
                    except ValueError:
                        print("Not a valid entry.")
                        print("Enter clearings (0-11) and troop count for two moves, in format c1,c2,num1,c3,c4,num2 (moving num1 troops from c1->c2, then num2 troops from c3->c4).")

                        return 0

                    if (self.march((c1,c2,num1),(c3,c4,num2))):
                        self.actions += 1
                        self.dstage = 2
                        self.current_action = 10
                        return 0
                    else:
                        print("Failed to march, try again.")
                        self.dstage = 2
                        self.current_action = 10
                        return 0

            elif self.current_action == 3: #Overwork
                if self.dstage == 4:
                    i = 0
                    print('\n')
                    for card in self.hand:
                        print(i, card)
                        i+=1
                    print('\n')

                    print("Enter clearing (0-11) and card to discard (index in hand of card with matching suit) in format c,card.")
                    self.dstage = 5
                    return 0
                if self.dstage == 5:
                    try:
                        c, card = command.split(',')
                        c = int(c)
                        card = int(card)

                        if c<0 or c>11 or card<0 or card>len(self.hand):
                            print("Not a valid entry.\nEnter clearing (0-11) and building (S for sawmill, Re for recruiter, and W for workshop) in format C,B")
                            return 0
                    except ValueError:
                        print("Not a valid entry.\nEnter clearing (0-11) and building (S for sawmill, Re for recruiter, and W for workshop) in format C,B")
                        return 0

                    if (self.overwork(c, card)):
                        self.actions += 1
                        self.dstage = 2
                        self.current_action = 10
                        print("Placed wood in clearing %d"%c)
                        return 0
                    else:
                        print("Failed to overwork, try again.")
                        self.dstage = 2
                        self.current_action = 10
                        return 0

            elif self.current_action == 4: #Recruit - works
                if self.recruit():
                    self.actions += 1
                    self.dstage = 2
                    self.current_action = 10
                    print("Troops placed.")
                else:
                    print("Failed to recruit, try again")
                    self.dstage=2
                    self.current_action=10
                    return 0
            elif self.current_action == 5: #Pass
                self.actions=self.max_actions
                self.dstage=2
                self.current_action = 0
                print("Skipping daylight")
            else:
                print("Enter a number from 0 through 5 to select an action.")


        #####BIRDS
        if self.dstage == 6:
            num_birds = 0
            bird_indexes = []
            for i in range(len(self.hand)):
                c = self.hand[i]
                if c.suit == 'B':
                    num_birds += 1
                    bird_indexes.append(i)
            if num_birds > 0:
                print("Would you like to spend a bird card to take an extra action?")
                print("Available bird cards:")
                for i in bird_indexes:
                    print(i, self.hand[i].name)
                print("\nEnter the number to the left of the card to spend, or \"no\" to skip.")
                self.dstage = 7
                return 0
            else:
                print("Hired mercenaries not available, ending daylight")
                self.phase = 2
                self.dstage = 0
                self.current_action = 10
                self.max_actions = 3
                self.actions = 0
                return 0

        if self.dstage == 7:
            if command=='no':
                #Actually exit, end daylight
                print("Ending daylight")
                self.phase = 2
                self.dstage = 0
                self.current_action = 10
                self.max_actions = 3
                self.actions = 0
                return 0
            try:
                selected = int(command)

            except ValueError:
                print("Invalid entry, enter the number associated with a bird card, or enter no to cancel.")
                return 0
            if selected < len(self.hand) and self.hand[selected].suit == 'B':
                #Successfully played a bird card!
                del self.hand[selected] #Discard the bird card, will later go into the discard pile
                self.max_actions += 1
                self.dstage = 2
            else:
                print("Entry does not match bird card, enter the number associated with a bird card, or enter no to cancel.")
                return 0

    def evening(self, command=None):
        #print("EVENING START")
        if self.dstage == 0:
            num_cards = 1 + self.building_nums['Re']//2 #Number of cards to draw
            self.draw(num_cards)
            if len(self.hand) <= 5:
                print("Evening ended, end of turn.")
                print("Currently have %d points."%self.score)
                self.phase = 0
                self.dstage = 0
            else:
                print('\n')
                i = 0
                for card in self.hand: #Why is this like this ahhhh
                    print(i, card)
                    i+=1
                print('\n')
                print("Need to discard cards. Select card to discard from above hand.")
                self.dstage = 1
                return 0
        else: #Should only be possible with a command? I hope so
            try:
                c = int(command)
                if c <0 or c >= len(self.hand):
                    print("Enter the index of the card to discard.")
                    return 0
            except ValueError:
                print("Enter the index of the card to discard.")
                return 0

            #Now discard
            card = self.hand[c]
            DISCARD.cards.append(card)
            print("Successfully discarded", card)
            del self.hand[c]
            if len(self.hand) <= 5:
                print("Evening ended, end of turn.")
                print("Currently have %d points."%self.score)
                self.phase = 0
                self.dstage = 0
            else:
                print('\n')
                i = 0
                for card in self.hand:
                    print(i, card)
                    i+=1
                print('\n')
                "Need to discard cards. Select card to discard from above hand."
                self.dstage = 1
                return 0






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
                    print("Destroyed Roost! Scored one point")
                    self.score +=1
            if bird_hits <= c.cat_count:
                c.add_warrior(-1*bird_hits, 1)
            else: #here we go
                remainder = bird_hits - c.cat_count
                c.add_warrior(-1*c.cat_count, 1)
                for i in range(remainder):
                    #Fix: eventually birds should score points here
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

                if c2 in CLEARINGS[c1].connections:

                    CLEARINGS[c1].add_warrior(-1*max(0,num), 1)
                    CLEARINGS[c2].add_warrior(max(0,num),1)
                    return True

                else:
                    print("Cannot make move, clearings not connected")

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
                    self.workshop_suits[CLEARINGS[clearing].suit]+= 1
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
        if self.hand[card].suit != c.suit and self.hand[card].suit != 'B':
            print("Card suit must match clearing")
            return False
        c.tokens.append('W')
        del self.hand[card] #When discard pile is necessary, fix this
        return True




    ######################  UTILITIES  ##########################

    def craft(self, card):
        """
        Basically just make sure that the cost is covered by workshops and then boom
        """
        # check that cost is paid
        print("Oh yes definitely crafting this card:")
        print(self.hand[card])
        del self.hand[card]
        # if yes, activate card effect and then discard
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

    def draw(self, n):
        #Just taken the top n cards from the deck
        for i in range(n):
            self.hand.append(DECK.draw())
        print(self.hand)

"""
Ugh, players need set of crafted cards.
Permanent effects:
    Battle:
        Scouting Party - As attacker in battle, you are not affected by ambush cards.
        Armorers - In battle, may discard this to ignore all rolled hits taken.
        Brutal Tactics - deal an extra hit as attacker, gives opponent 1 point.
        Sappers - as defender, discard to deal an extra hit
    Birdsong:
        Better Burrow Bank - At start of Birdsong, you and another player draw a card
        Stand and deliver - take a random card from another player in birdsong, they score one point
        Royal Claim - discard to score one point per ruled clearing
    Daylight:
        Codebreakers - once in daylight look at another players hand
        Tax Collector - Once in Daylight, may remove one of your warriors from the map to draw a card.
        Command Warren - At start of daylight, may initiate a battle.
    Evening:
        Cobbler - At start of evening, may take a move


"""

if __name__ == '__main__':
    #All setup For testing

    #CLEARINGS[6].add_warrior(1, 1)
    for i in range(len(CLEARINGS)):
        if i%2==0 and i!=0:
            CLEARINGS[i].add_warrior(i+1, 2)
            CLEARINGS[i].add_building('Ro') #Random bird nonsense for testing
        if i!=11:
            CLEARINGS[i].add_warrior(1, 1) #Place initial cats

    marquise = CatPlayer(1)
    marquise.build(0, 'S')
    marquise.build(1, 'Re')
    marquise.build(3,'W')
    CLEARINGS[0].tokens.append('K')
    marquise.hand = [DECK.draw(), DECK.draw(), DECK.draw()]
    print(marquise.hand)



    #### Actual pygame code
    input_ready = False
    usr_txt = ''
    command = ''
    input_font = pygame.font.SysFont(None, 30)
    txt_surface = input_font.render("Input: "+usr_txt, True, (255,255,255))

    draw_map(CLEARINGS)
    scrn.blit(txt_surface, (50,850))
    pygame.display.flip()
    pygame.display.update()

    status = True







    while(status):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                status=False
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_BACKSPACE:
                    usr_txt = usr_txt[:-1]
                    draw_map(CLEARINGS)
                elif i.key == pygame.K_RETURN:
                    input_ready = True
                    command = usr_txt
                    usr_txt = ''
                    draw_map(CLEARINGS)

                else:
                    usr_txt += i.unicode
                txt_surface = input_font.render("Input: "+usr_txt, True, (255,255,255))
                #print(usr_txt)

                #draw_map(CLEARINGS)
                scrn.blit(txt_surface, (50,850))
                pygame.display.flip()
                pygame.display.update()

        if marquise.score >= 30:
            print("You win!")
            break

        if marquise.phase == 0:
            marquise.birdsong()
            draw_map(CLEARINGS)
            scrn.blit(txt_surface, (50,850))
            pygame.display.flip()
            pygame.display.update()
            marquise.phase = 1

        if marquise.phase == 1:
            if marquise.dstage ==  0 or marquise.dstage == 2 or marquise.dstage == 4:
                marquise.daylight()
                draw_map(CLEARINGS)
                scrn.blit(txt_surface, (50,850))
                pygame.display.flip()
                pygame.display.update()

        if marquise.phase == 2:
            if marquise.dstage == 0:
                marquise.evening()


        if input_ready:
            input_ready = False
            if marquise.phase == 1:
                marquise.daylight(command)
            elif marquise.phase == 2:
                marquise.evening(command)
            draw_map(CLEARINGS)
            scrn.blit(txt_surface, (50,850))
            pygame.display.flip()
            pygame.display.update()







    pygame.quit()
