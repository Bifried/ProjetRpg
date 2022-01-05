import pygame
import random

pygame.init()

screen = pygame.display.set_mode((500,500))


#image des items, pour l'instant des cercles, à voir pour mettre les vrai images
items = [pygame.Surface((50,50),pygame.SRCALPHA) for x in range(4)]


pygame.draw.circle(items[0],(0,255,255),(25,25),25)
pygame.draw.circle(items[1],(0,255,0),(25,25),25)
pygame.draw.circle(items[2],(255,255,0),(25,25),25)
pygame.draw.circle(items[3],(0,0,255),(25,25),25)


font = pygame.font.Font(pygame.font.match_font("calibri"),26)
#class pour les items du jeux
class item:
    def __init__(self,id):
        self.id = id
        self.surface = items[id]
    
    def resize(self,size):
        return pygame.transform.scale(self.surface,(size,size))

#inventaire du joueur ( a redéfinir )
class inventory:
    def __init__(self):
        self.rows = 3
        self.col = 9
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 40
        self.x = 50
        self.y = 50
        self.border = 3
    
    #permet de dessiner l'invenataire
    def draw(self):
        pygame.draw.rect(screen,(100, 100, 100),
                         (self.x,self.y,(self.box_size + self.border)*self.col + self.border,(self.box_size + self.border)*self.rows + self.border))
        # x et y correspondes aux absyces et ordonnés
        for x in range(self.col):
            for y in range(self.rows):
                rect = (self.x + (self.box_size + self.border)*x + self.border,self.x + (self.box_size + self.border)*y + self.border,self.box_size,self.box_size )
                pygame.draw.rect(screen,(180,180,180),rect)
                if self.items[x][y]:
                    screen.blit(self.items[x][y][0].resize(self.box_size),rect)
                    obj = font.render(str(self.items[x][y][1]),True,(0,0,0))
                    screen.blit(obj,(rect[0] + self.box_size//2, rect[1] + self.box_size//2))
                    
    # détecte où la souris se trouve pour selectionner un emplacement d'inventaire
    def get_pos(self):
        mouse = pygame.mouse.get_pos()
        
        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x//(self.box_size + self.border)
        y = y//(self.box_size + self.border)
        return (x,y)
    
    # permets d'ajouter des items dans l'inventaire
    def add(self,Item,xy):
        x, y = xy
        if self.items[x][y]:
            if self.items[x][y][0].id == Item[0].id: # si dans la case il n'y a pas l'item selectionner -> ajoute dans la case
                self.items[x][y][1] += Item[1] # si item selectionner est dans la case AJOUTE stack a l'items ( 2 fois le même item dans la case )
            else:
                temp = self.items[x][y]
                self.items[x][y] = Item
                return temp
        else:
            self.items[x][y] = Item
    
    # vérifie si la souris est dans la grille
    def in_grid(self,x,y):
        if 0 > x > self.col-1:
            return False
        if 0 > y > self.rows-1:
            return False
        return True
    
    
player_inventory = inventory()

# l'objet que le joueur a selectionner
selected = None

running = True
while running:
    # couleur du fond 
    screen.fill((255,255,255))
    player_inventory.draw()
    
    mousex, mousey = pygame.mouse.get_pos()
    
    # lorsque le joueur selectionne un objet, le déssine à coter de la souris
    if selected:
        screen.blit(selected[0].resize(30),(mousex,mousey))
        obj = font.render(str(selected[1]),True,(0,0,0))
        screen.blit(obj,(mousex + 15, mousey + 15))        
    
    # TEST 
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONUP:
            #quand le joueur fait un clic droit donne un item aléatoire TEST
            if event.button == 3:
                selected = [item(random.randint(0,0)),1]
            elif event.button == 1:
                pos = player_inventory.get_pos()
                if player_inventory.in_grid(pos[0],pos[1]):
                    if selected:
                        selected = player_inventory.add(selected,pos)
                    elif player_inventory.items[pos[0]][pos[1]]:
                        selected = player_inventory.items[pos[0]][pos[1]]
                        player_inventory.items[pos[0]][pos[1]] = None