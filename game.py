from map import *
from cards import *
from player import *
import random
"""
Things to add:
- crafting
    - Birdsong cards
    - Daylight cards
    - Evening cards
    - Battle cards
- ambush cards

- Field Hospitals???
- The draw and discard pile

Known bugs:
- One time when I did an action wrong the whole thing crashed it was weird
    - Does this count as known?

- Ok it draws  the screen too many times whats goin on
    - Fixing this would require doing things completely differently at a very basic level. It is
    not important.

"""

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

class Game:
    def __init__(self):
        #Runs necessary pygame initialization
        self.input_ready = False
        self.usr_txt = ''
        self.command = ''
        self.input_font = pygame.font.SysFont(None, 30)
        self.txt_surface = self.input_font.render("Input: "+self.usr_txt, True, (255,255,255))

        draw_map(CLEARINGS)
        scrn.blit(self.txt_surface, (50,850))
        pygame.display.flip()
        pygame.display.update()

        self.status = True

    def setup(self):
        #Temporary stuff here for now, eventually runs all board and player setup

        for i in range(len(CLEARINGS)):
            if i%2==0 and i!=0:
                CLEARINGS[i].add_warrior(i+1, 2)
                CLEARINGS[i].add_building('Ro') #Random bird nonsense for testing
            if i!=11:
                CLEARINGS[i].add_warrior(1, 1) #Place initial cats

        self.marquise = CatPlayer(1)
        self.marquise.build(0, 'S')
        self.marquise.build(1, 'Re')
        self.marquise.build(3,'W')
        CLEARINGS[0].tokens.append('K')
        DECK.shuffle()
        self.marquise.hand = [DECK.draw(), DECK.draw(), DECK.draw()]
        #For testing
        self.marquise.hand.append(Card('M',(0,0,3,0),"Remove all enemy pieces in Mouse clearings, then discard.","Favor of the Mice"))


    def screen_updates(self):
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                self.status=False
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_BACKSPACE:
                    self.usr_txt = self.usr_txt[:-1]
                    draw_map(CLEARINGS)
                elif i.key == pygame.K_RETURN:
                    self.input_ready = True
                    self.command = self.usr_txt
                    self.usr_txt = ''
                    draw_map(CLEARINGS)

                else:
                    self.usr_txt += i.unicode
                self.txt_surface = self.input_font.render("Input: "+self.usr_txt, True, (255,255,255))
                #print(usr_txt)

                #draw_map(CLEARINGS)
                scrn.blit(self.txt_surface, (50,850))
                pygame.display.flip()
                pygame.display.update()

    def check_wins(self):
        if self.marquise.score >= 30:
            print("You win!")
            self.status=False

    def turn(self):
        if self.marquise.phase == 0:
            self.marquise.birdsong()
            draw_map(CLEARINGS)
            scrn.blit(self.txt_surface, (50,850))
            pygame.display.flip()
            pygame.display.update()
            self.marquise.phase = 1

        if self.marquise.phase == 1:
            if self.marquise.dstage ==  0 or self.marquise.dstage == 2 or self.marquise.dstage == 4:
                self.marquise.daylight()
                draw_map(CLEARINGS)
                scrn.blit(self.txt_surface, (50,850))
                pygame.display.flip()
                pygame.display.update()

        if self.marquise.phase == 2:
            if self.marquise.dstage == 0:
                self.marquise.evening()

    def check_inputs(self):
        if self.input_ready:
            if self.command == 'bye':
                self.status = False
            self.input_ready = False
            if self.marquise.phase == 1:
                self.marquise.daylight(self.command)
            elif self.marquise.phase == 2:
                self.marquise.evening(self.command)
            draw_map(CLEARINGS)
            scrn.blit(self.txt_surface, (50,850))
            pygame.display.flip()
            pygame.display.update()

if __name__ == '__main__':
    root = Game()
    root.setup()





    while(root.status):
        root.screen_updates()
        root.check_wins()
        root.turn()
        root.check_inputs()

    pygame.quit()
