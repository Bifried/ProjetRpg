#imports
from pygame import mixer
from random import randint
import credits
import pygame

#Création d'une classe avec plusieurs attributs pour les personnages du combat:
#Les coordonnées du personnages, son nom, ses hp max, sa force, son nombre de potion,son level, ses mp, rajouts des attributs screen et ennemis pour débuger les autres combats ou la classe est appelée
class Fighter():
    def __init__(self, x, y, name, max_hp, strenght, potions, level, max_mp, screen, enemy=None):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strenght = strenght
        self.level = level
        self.max_mp = max_mp
        self.mp = max_mp
        self.start_potions = potions
        self.potions = potions
        self.screen = screen
        self.enemy = enemy
        self.alive = True
        self.animation_list = [] #Liste qui va contenir d'autres listes temporaires contenant nos animations faites à partir des sprites du dossier correspondant
        self.frame_index = 0 #variable utilisé pour l'animation des actions
        self.action = 0 # chaque action d'un personnage correspondra à un chiffre de 0 à 7, 0 pour l'animation de base, 1 pour l'attaque, 2 pour animation suite à des dégats reçu, 3 pour heal, 4 pour mort, 5 pour win, 6 pour attaque special, 7 pour animation suite aux dégats d'attaque spéciale reçu
        self.update_time = pygame.time.get_ticks() #variable qui va servir à définir le temps lors d'une animation pour passer d'une image dans la liste de l'animation à l'autre

        #Images d'animation de base
        temp_list = []#liste temporaire qui va récupérer les images d'un dossier en fonction de l'action en question
        for i in range(8):#le range de l'animation correspond au nombre d'images dans le dossier de l'animation
            img = pygame.image.load(f'images/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #Images d'animations d'attaque
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'images/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #Images d'animations de dégats reçus
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'images/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #Images d'animations de heal(potion)
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'images/{self.name}/Heal/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #Images d'animations de mort
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'images/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
            temp_list.append(img)
        self.animation_list.append(temp_list)


        #Images d'animations de victoire
        temp_list = []
        for i in range(13):
            img = pygame.image.load(f'images/Hero/Win/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #Création d'un rectangle de collision à partir des images du personnage
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #Images d'animations d'attaque spéciale
        temp_list = []
        for i in range(30):
            img = pygame.image.load(f'images/{self.name}/Special/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        #Images d'animations de dgts d'attaque spéciale
        temp_list = []
        for i in range(29):
            img = pygame.image.load(f'images/{self.name}/HurtSpecial/{i}.png')
            img = pygame.transform.scale(img, (img.get_width()*2, img.get_height()*2))
            temp_list.append(img)
        self.animation_list.append(temp_list)
    
    #fonction pour mettre à jour l'apparence du joueur régulièrement
    def update(self, frombattle="battle"): 
        import rpg #imports ajoutés dans la fonction à cause de bugs
        import congratulations 
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown: #création d'une condition pour avoir un temps avant d'update l'image du joueur entre chaque images d'une animation
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 4:
                self.frame_index = len(self.animation_list[self.action]) - 1 #-1 pour éviter que l'animation ne redémarre lorsqu'elle arrive à son dernier index 
            elif self.action == 5:
                self.frame_index = len(self.animation_list[self.action]) - 1
                if frombattle == "battle":
                   rpg.game(self)
                elif frombattle == "bossbattle":#renvoyer le jeu sur une fenêtre différente lors de la victoire du combat de boss
                    congratulations.congratulations()
    
            else:
                self.idle() #retour à l'animation idle


    #Fonction servant à afficher le personnage sur l'écran
    def draw(self):
        self.screen.blit(self.image, self.rect)

    #Fonctions de chaques animations, idle (position basique), hurt (dégats reçus), hurt special (dégats d'une atk spéciale), heal (potions utilisée), death (mort), victoires et atks/atks spéciales
   #animation de base
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        if self.enemy is not None: #pour éviter un bug dû au nonetype qui ne peux avoir l'attribut alive
            win_condition = self.alive == True and self.enemy.alive == False #condition de victoire, si on est en vie et l'ennemi est mort on fait l'animation de victoire
            if win_condition == True:
                self.win()
                
    #animation de dégats reçus
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    #animation d'utilisation de potion
    def heal(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    #animation de mort
    def death(self):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    #animation de victoire
    def win(self):
        self.action = 5
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        if self.enemy.level == 5: #Système d'expérience et de gain de stats du joueur en fonction du niveau de l'ennemi
            self.level += 5
            self.strenght += 5
            self.max_hp += 100
            self.hp = self.max_hp
            self.max_mp += 10
            self.mp = self.max_mp
        elif self.enemy.level == 15:
            self.level += 7
            self.strenght += 7
            self.max_hp += 170
            self.hp = self.max_hp
            self.max_mp += 17
            self.mp = self.max_mp    
        elif self.enemy.level >=25:
            self.level += 10
            self.strenght += 10
            self.max_hp += 200
            self.hp = self.max_hp
            self.max_mp += 20
            self.mp = self.max_mp           
        drop = randint(0,4) #fonction de drop en fin de combat suite à une victoire pour récupérer un nombre aléatoire de potions mais la quantité max de potion que le joueur peu transporter ne dépassera pas 3
        self.potions = self.potions + drop
        if self.potions >= 3:
           self.potions = 3
        

    #Fonction servant à calculer les dégats d'une attaque
    def attack(self, target):
        rand = randint(-5, 5) #Pour créer un combat avec + de tension les dégats infligés sont déterminé par un calcul de la force du personnage -5 ou +5 aléatoirement
        damage = self.strenght + rand
        target.hp -= damage
        target.hurt() #animation dé dégats reçu pour la cible de l'attaque
        if target.hp <1: #condition pour déclencher l'animation de mort à la place de l'animation de dégats reçus
            target.hp = 0
            target.alive = False
            target.death()
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    #Fonction servant à calculer les dégats d'une attaque spéciale et condition d'animation de mort également
    def special(self, target):
        rand = randint(-5, 5) 
        special = 2
        damage = (self.strenght + rand) *special
        target.hp -= damage
        target.hurt_special()
        if target.hp <1:
            target.hp = 0
            target.alive = False
            target.death()
        self.action = 6
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    #animation de dégats reçu d'une attaque spéciale
    def hurt_special(self):
        self.action = 7
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()




#fonction appelé lors d'une collision avec un ennemi sur la carte
def fight(hero=None):
    import rpg

    pygame.init()
    
#Variables pour l'UI de combat (l'écran et le panneau avec les vies, potions, attaques spéciales et informations des personnages)
    bottom_panel = 150
    screen_width = 900
    screen_height = 450 + bottom_panel

#Fenêtre de combat
    screen = pygame.display.set_mode((screen_width, screen_height))


#Variables pour le code du combat en tour par tour
    fighter_turn = 1 #Tour du personnage pour selectionner une action
    total_fighter = 2 #Nombres de personnages
    action_cooldown = 0 #variable pour créer un délais entre les actions du joueurs et de l'IA
    action_wait_time = 100 #Pareil
    attack = False #Action attaqué (on démarre par un boolean faux pour l'activer lors d'un clique)
    potion = False #Action potion (pareil)
    potion_heal = 100 #La quantité de soin d'une potion
    target = None #Cible lors d'une attaque (peux servir également lorsque l'on voudra mettre plusieurs ennemis)
    special = False #Action attaque spéciale (pareil que pour les potion)
    hero_mana_restored = 15 #Mp qui seront restaurés par le joueur après chaques attaques "basiques" 
    enemy_mana_restored = 25 #Même chose pour l'ennemi
    game_over = 0 #Variable pour la condition de fin du combat et l'affichage du game over

#Variables pour la police de texte et les couleurs principalements utilisés lors du combat (pour le text et les barres de vie)
    font = pygame.font.Font('VT323-Regular.ttf', 26)
    black = (0,0,0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    purple = (240,0,255)

#Sons que l'ont veux utiliser lors du combats
    hero_hurt_snd = pygame.mixer.Sound('audio/herohurt.wav')
    enemy_hurt_snd = pygame.mixer.Sound('audio/alienhurt.wav')
    hero_atk_snd = pygame.mixer.Sound('audio/swordslashsound.wav')
    enemy_atk_snd = pygame.mixer.Sound('audio/lightsabersound.wav')
    healing_sound = pygame.mixer.Sound('audio/healingsound.wav')
    enemy_spec_sound1 = pygame.mixer.Sound('audio/enemyspecial1.wav')
    enemy_spec_sound2 = pygame.mixer.Sound('audio/enemyspecial2.wav')
    hero_spec_sound1 = pygame.mixer.Sound('audio/specialhero1.wav')
    hero_spec_sound2 = pygame.mixer.Sound('audio/specialhero2.wav')


#Images que l'on veux utiliser dans la fenêtre
    background_img = pygame.image.load('images/battle.png').convert_alpha()

    panel_img = pygame.image.load('images/panel1.png').convert_alpha()
   
    potion_img = pygame.image.load('images/potion.png').convert_alpha()

    special_img = pygame.image.load('images/special.png').convert_alpha()

    victory_img = pygame.image.load('images/victory.png').convert_alpha()

    defeat_img = pygame.image.load('images/game_over.png').convert_alpha()

#Création de la classe des barre de vie, requiert une position un nombre actuel de hp et les hp max
    class HealthBar():
        def __init__(self, x, y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp
#Fonction pour afficher les barres de vie sur l'écran
        def draw(self, hp):
            self.hp = hp
            ratio = self.hp / self.max_hp #sert à recouvrir les hp max de rouge puis de vert et réduire la barre verte en fonction des hp actuels perdus
            pygame.draw.rect(screen, red, (self.x, self.y, 150, 20)) #création des rectangles de vie colorés
            pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


#Création de la classe des barre de mp, requiert une position un nombre actuel de mp et les mp max (pareil que pour la vie mais en utilisant les mp)
    class ManaBar():
        def __init__(self, x, y, mp, max_mp):
            self.x = x
            self.y = y
            self.mp = mp
            self.max_mp = max_mp
#Fonction pour afficher les barres de mp
        def draw(self, mp):
            self.mp = mp
            ratio = self.mp / self.max_mp #sert à recouvrir les mp max de noir puis de violet et réduire la barre verte en fonction des hp actuels perdus
            pygame.draw.rect(screen, black, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, purple, (self.x, self.y, 150 * ratio, 20))
            


#Création de la classe des boutons (pour les potions et les attaques spéciales)
    class Button():
        def __init__(self, x, y, image, size_x, size_y):
            self.image = pygame.transform.scale(image, (size_x, size_y)) #redimension de l'image
            self.rect = self.image.get_rect() #création d'un rectangle pour pouvoir cliquer sur les boutons
            self.rect.topleft = (x, y)
            self.clicked = False

#afficher les boutons sur l'écran
        def draw(self):
            action = False
#Rajout de la position de la souris
            pos = pygame.mouse.get_pos()

#Vérifier si la souris est sur un bouton et si elle clique dessus
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #Si clique gauche sur un bouton
                    self.clicked = True
                    action = True
#Détecter que la souris ne clique plus
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked == False

            screen.blit(self.image, (self.rect.x, self.rect.y))
            return action #Pour activer une fonction dans la boucle lorsqu'un bouton sera cliqué

    
#variables de la classe fighters, le héro et l'ennemi
 #positionnement du personnage, son nom, ses hp, sa force, son nombre de potion, son level, ses mp (les fonctions screens et enemy sont ajoutés pour éviter des bugs lorsqu'on les appels dans d'autres fenêtre ou les ennemis sont différents)
    enemy = Fighter(-50, 85, 'Enemy', 120, 13, 1, 5, 250, screen)

    if hero is None:
        hero = Fighter(330, 260, 'Hero', 100, 16, 3, 5, 250, screen, enemy)

    hero.screen = screen #redéfinition des variables lorsque l'on est dans la fonction
    hero.enemy = enemy #n'est plus un nonetype
    hero.hp = hero.max_hp
    hero.mp = hero.max_mp
    hero.alive = True
    hero.frame_index = 0 #reset l'index du joueur à la première frame (évite un bug ou le joueur est en frame de victoire suite à un combat précédant)
    hero.action = 0 #reset les actions du joueur en idle
    hero.update_time = pygame.time.get_ticks()
    
#variables de la classe barre de vie et barre de mp, la vie et les mp du héro et de l'ennemi
    hero_health_bar = HealthBar(100, screen_height - bottom_panel + 45, hero.hp, hero.max_hp)
    enemy_health_bar = HealthBar(500, screen_height - bottom_panel + 45, enemy.hp, enemy.max_hp)
    hero_mana_bar = ManaBar(100, screen_height - bottom_panel + 70, hero.mp, hero.max_mp)
    enemy_mana_bar = ManaBar(500, screen_height - bottom_panel + 70, enemy.mp, enemy.max_mp)

#Fonction pour mettre du texte sur l'écran
    def draw_text(text, font, text_col, x, y):
        img = font.render(text,True, text_col)
        screen.blit(img, (x, y))
#Fonction pour afficher le fond d'écran
    def draw_bg():
        screen.blit(background_img, (0, 0))
#Fonction pour afficher l'UI en bas de l'écran de combat avec les informations des personnages
    def draw_panel():
        screen.blit(panel_img, (0, screen_height - bottom_panel-19))
        draw_text(f'{hero.name} HP: {hero.hp}/{hero.max_hp}', font, black, 100, screen_height - bottom_panel -5) #Utilisation directe des attributs de la classe fighter pr définir les noms et la valeur des hp des personnages
        draw_text(f'{enemy.name} HP: {enemy.hp}/{enemy.max_hp}', font, black, 500, screen_height - bottom_panel -5)
        draw_text(f'Level: {hero.level}', font, black, 100, screen_height - bottom_panel + 15)
        draw_text(f'Level: {enemy.level}', font, black, 500, screen_height - bottom_panel + 15)
        draw_text(f'Mana: {hero.mp}/{hero.max_mp}', font, purple, 250, screen_height - bottom_panel + 15)
        draw_text(f'Mana: {enemy.mp}/{enemy.max_mp}', font, purple, 650, screen_height - bottom_panel + 15)
#variable de la classe bouton
    potion_button = Button(100, screen_height - bottom_panel + 100, potion_img, 40, 40)
    special_button = Button(200,screen_height - bottom_panel + 100, special_img, 40, 40)

#création de la boucle
    run = True

#ajout musique
    mixer.init()
    mixer.music.load("musiques/fight.mp3")
    mixer.music.play(loops=-1) #Pour que la musique se répète

    while run:

#Affichage des différentes images et du texte

        draw_bg() #Fond d'écran

        draw_panel() #UI en bas
        hero_health_bar.draw(hero.hp)
        enemy_health_bar.draw(enemy.hp)
        hero_mana_bar.draw(hero.mp)
        enemy_mana_bar.draw(enemy.mp)

        hero.update() #mise à jour du joueur
        hero.draw() #affichage du personnage joueur

        enemy.update() #mise à jour de l'ennemi
        enemy.draw() #affichage de l'ennemi
        
        potion_button.draw() #affichages des Potions du joueur
        special_button.draw() #affichages special du joueur

        draw_text(str(hero.potions),font, red, 130, screen_height - bottom_panel + 100) #affichage pour avoir le nombre de potions du joueurs affichées
  
#Condition de victoire ou défaites pour afficher le game over ou la victoire  
        if game_over != 0:
            if game_over == 1:
               screen.blit(victory_img, (330, 50))
            if game_over == -1:
                screen.blit(defeat_img, (0, 100))
#condition de clique et de fermeture de la fenêtre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
                    
        pygame.display.update() #mise à jour de l'écran
#Réitération des variables liés aux choix d'action dans la boucle
        attack = False
        potion = False
        special = False
        target = None


#Position + affichage de la souris
        pos = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)

#Condition de clique lorsque l'on choisit d'attaquer un ennemi et éviter bug ou cliquer sur un boutton et le rectangle d'un ennemi lançait 2 actions simultanément (dû à un rognage des images de sprites trop grands)  
        if enemy.rect.collidepoint(pos) and potion_button.rect.collidepoint(pos) == False and special_button.rect.collidepoint(pos) == False:
            if clicked == True and enemy.alive == True:
                attack = True
                target = enemy

#Condition de clique lorsque l'ont choisit d'utiliser une potion       
        if potion_button.rect.collidepoint(pos):
            if clicked == True:
                potion = True
            else:
                potion = False

#Condition de clique lorsque l'ont choisit d'utiliser une attaque spéciale     
        if special_button.rect.collidepoint(pos):
            if clicked == True:
                special = True
            else:
                special = False
                


#Création des actions au tour par tour en fonction des choix du joueur
        if game_over == 0:
            if hero.alive == True:
                if fighter_turn == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        if attack == True and target == enemy:
                            hero_atk_snd.play()
                            hero.attack(enemy)
                            enemy_hurt_snd.play()
                            
                            if hero.mp < hero.max_mp and hero.mp + hero_mana_restored < hero.max_mp:
                                hero.mp += hero_mana_restored
                            else:
                                hero.mp = hero.max_mp     
                            fighter_turn +=1
                            action_cooldown = 0

                        if potion == True: #Choix d'utiliser la potion + éviter que le heal soit supérieur aux hp max
                            if hero.potions > 0  and enemy.alive == True:
                                healing_sound.play()
                                hero.heal()
                                if hero.max_hp - hero.hp > potion_heal:
                                    heal_amount = potion_heal
                                else:
                                    heal_amount = hero.max_hp - hero.hp
                                hero.hp += heal_amount
                                hero.potions -=1
                                fighter_turn += 1
                                action_cooldown = 0
                        if special == True and hero.mp >= 250:
                            hero.special(enemy)
                            hero_atk_snd.play()
                            hero_spec_sound1.play()
                            hero_spec_sound2.play()
                            enemy_hurt_snd.play()
                            hero.mp -= 250
                            fighter_turn += 1
                            action_cooldown = -200 #cooldown augmenté pour éviter que 2 animations s'overlap parce que les animations d'attaques spéciales sont longues

            else:
                game_over = -1
                
            


            
#Action de L'IA qui joue après le joueur, se heal lorsqu'il passe à la moitié de ses pv et atk spéciale si il n'a pu de potions et assez de mp            
            if fighter_turn == 2:
                if enemy.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
                            healing_sound.play()
                            enemy.heal()
                            if enemy.max_hp - enemy.hp > potion_heal:
                                    heal_amount = potion_heal
                            else:
                                heal_amount = enemy.max_hp - enemy.hp
                            enemy.hp += heal_amount
                            enemy.potions -=1
                            fighter_turn += 1
                            action_cooldown = 0
                        elif (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions == 0 and enemy.mp >= 250:
                            enemy_spec_sound1.play()
                            enemy_spec_sound2.play()
                            enemy.special(hero)
                            hero_hurt_snd.play()
                            enemy.mp -= 250
                            fighter_turn += 1
                            action_cooldown = -200
                        else:
                            enemy_atk_snd.play()
                            enemy.attack(hero)
                            hero_hurt_snd.play()
                            fighter_turn += 1
                            action_cooldown = 0

                            if enemy.mp < enemy.max_mp and enemy.mp + enemy_mana_restored < enemy.max_mp:
                                enemy.mp += enemy_mana_restored
                                fighter_turn += 1
                                action_cooldown = 0
                            else:
                                enemy.mp = enemy.max_mp
                            fighter_turn +=1
                            action_cooldown = 0
                else:
                    fighter_turn += 1

            if fighter_turn > total_fighter:
                fighter_turn = 1

            if not enemy.alive:
                game_over = 1
        
                
            

        keys = pygame.key.get_pressed()
        #Lancement de l'écran aventure si barre espace est utilisée
        if keys[pygame.K_SPACE]:
            rpg.game(hero)
        if keys[pygame.K_a]: #relancer le combat
            return fight


    