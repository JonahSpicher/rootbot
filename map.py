#hello forest
import pygame
from pygame.locals import *

#Set up pygame and the screen
pygame.init()
X = 1000
Y = 915

scrn = pygame.display.set_mode((X,Y))
pygame.display.set_caption('The Forest')

map = pygame.image.load('./map2.jpg').convert()
height = map.get_height()
width = map.get_width()
s_factor = X/width
map = pygame.transform.scale(map, (width*s_factor, height*s_factor))
scrn.blit(map, (0,0))

cat = pygame.image.load('./catlabel.png').convert_alpha()
bird = pygame.image.load('./birdlabel.png').convert_alpha()
wood = pygame.image.load('./wood.png').convert_alpha()
keep = pygame.image.load('./keep.png').convert_alpha()
slot = pygame.image.load('./slot.png').convert_alpha()
wood = pygame.transform.scale(wood, (20, 21))
keep = pygame.transform.scale(keep, (20, 21))
slot = pygame.transform.scale(slot, (25,24))

troop_count_font = pygame.font.SysFont(None, 20)





class Clearing:
    def __init__(self, suit, connections, corner, build_slots, ruin, cat_loc, label, show_num=False):
        self.suit = suit
        self.connections = connections
        self.corner = corner
        self.build_slots = build_slots;
        self.buildings = []
        self.tokens = []

        self.cat_count = 0
        self.bird_count = 0
        self.rule = 0 #0 for none, 1 for cats, 2 for birds
        self.cat_loc=cat_loc
        self.bird_loc= (cat_loc[0], cat_loc[1]+31)
        self.token_loc = (self.cat_loc[0], self.cat_loc[1]-24)
        self.catnum_loc = (self.cat_loc[0]+21, self.cat_loc[1]+4)
        self.birdnum_loc = (self.bird_loc[0]+21, self.bird_loc[1]+4)
        self.build_loc = (self.cat_loc[0]+45, self.cat_loc[1]-5)
        if ruin:
            self.buildings.append('ruin')
        self.label = label
        if show_num:
            self.label_loc = (self.cat_loc[0]+80, self.cat_loc[1])
        else:
            self.label_loc = None


    def draw_contents(self):
        slot_x = self.build_loc[0]
        slot_y = self.build_loc[1]
        for i in range(self.build_slots):
            scrn.blit(slot, (slot_x, slot_y+(20*i)))

        if self.cat_count > 0:
            scrn.blit(cat, self.cat_loc)
            num = troop_count_font.render('x'+str(self.cat_count), True, (0,0,0))
            scrn.blit(num, self.catnum_loc)
            #Also a number
        if self.bird_count > 0:
            scrn.blit(bird, self.bird_loc)
            num = troop_count_font.render('x'+str(self.bird_count), True, (0,0,0))
            scrn.blit(num, self.birdnum_loc)
        if len(self.tokens) > 0:
            print(self.tokens)
            for i in range(len(self.tokens)):
                print(i)
                target = (self.token_loc[0]+(22*i), self.token_loc[1])
                if self.tokens[i] == 'K':
                    scrn.blit(keep, target)
                if self.tokens[i] == 'W':
                    scrn.blit(wood, target)

        if self.label_loc != None:
            clearing_num = troop_count_font.render(str(self.label), True, (255,255,255))
            scrn.blit(clearing_num, self.label_loc)

clearings = [Clearing('F', [1,3,4],      True, 1, False, (70,90),0),
             Clearing('R', [0,2],        False, 2, False, (513,58),1),
             Clearing('M', [1,4,7],      True, 2, False, (825,190),2),
             Clearing('M', [0,5,8],      False, 2, False, (65,330),3),
             Clearing('R', [0,2,5],      False, 2, True, (375,240),4),
             Clearing('F', [3,4,6,8,10], False, 2, True, (280,475),5),
             Clearing('M', [5,7,11],     False, 3, True, (595,425),6),
             Clearing('F', [2,6,11],     False, 2, True, (860,455),7),
             Clearing('R', [3,5,9],      True, 1, False, (65,710),8),
             Clearing('F', [8,10],       False, 2, False, (310,780),9),
             Clearing('M', [5,9,11],     False, 2, False, (535,680),10),
             Clearing('R', [6,7,10],     True, 1, False, (790,765),11)]


#Place pieces
# clearings[0].tokens.append('K')
# for i in range(len(clearings)):
#     if i%2==0:
#         clearings[i].bird_count=i+1
#     if i%3==0:
#         clearings[i].cat_count=i+1
#     if i < 5:
#         print(i)
#         clearings[i].tokens.append('W')
#

#Draw all clearings
for i in range(len(clearings)):
    clearings[i].draw_contents()

pygame.display.flip()
status = True
while(status):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status=False
pygame.quit()