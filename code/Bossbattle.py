from pygame import mixer
from random import randint
import pygame
from Battle import Fighter
#commentaires mal détaillé par manque de temps, mieux détaillés dans Battle.py
def bossfight(hero=None):
    import rpg

    pygame.init()
    
#Variables pour l'UI de combat
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
    special = False
    hero_mana_restored = 15
    boss_mana_restored = 30
    game_over = 0 #Variable pour la condition de fin du combat

#Variables pour la police de texte et les deux couleurs principalement utilisé lors du combat (pour le text et les barres de vie)
    font = pygame.font.Font('VT323-Regular.ttf', 26)
    black = (0,0,0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    purple = (240,0,255)

#Sons que l'ont veux utiliser
    hero_hurt_snd = pygame.mixer.Sound('audio/herohurt.wav')
    boss_hurt_snd = pygame.mixer.Sound('audio/alienhurt.wav')
    hero_atk_snd = pygame.mixer.Sound('audio/swordslashsound.wav')
    boss_atk_snd = pygame.mixer.Sound('audio/laserriflesound.wav')
    healing_sound = pygame.mixer.Sound('audio/healingsound.wav')
    boss_spec_sound1 = pygame.mixer.Sound('audio/energywavesound.wav')
    hero_spec_sound1 = pygame.mixer.Sound('audio/specialhero1.wav')
    hero_spec_sound2 = pygame.mixer.Sound('audio/specialhero2.wav')


#Images que l'on veux utiliser
    background_img = pygame.image.load('images/bossbattle.png').convert_alpha()

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
#Fonction pour dessiner les barres de vie
        def draw(self, hp):
            self.hp = hp
            ratio = self.hp / self.max_hp #sert à recouvrir les hp max de rouge puis de vert et réduire la barre verte en fonction des hp actuels perdus
            pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


#Création de la classe des barre de mp, requiert une position un nombre actuel de mp et les mp max
    class ManaBar():
        def __init__(self, x, y, mp, max_mp):
            self.x = x
            self.y = y
            self.mp = mp
            self.max_mp = max_mp
#Fonction pour dessiner les barres de mp
        def draw(self, mp):
            self.mp = mp
            ratio = self.mp / self.max_mp #sert à recouvrir les mp max de noir puis de violet et réduire la barre verte en fonction des hp actuels perdus
            pygame.draw.rect(screen, black, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, purple, (self.x, self.y, 150 * ratio, 20))
            


#Création de la classe des boutons
    class Button():
        def __init__(self, x, y, image, size_x, size_y):
            self.image = pygame.transform.scale(image, (size_x, size_y))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
            self.clicked = False

#Dessiner les boutons sur l'écran
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
 #positionnement du personnage, son nom, ses hp, sa force, son nombre de potion et son lvl
    boss = Fighter(-480, 283, 'Boss', 700, 40, 2, 30, 300, screen)

    if hero is None:
        hero = Fighter(330, 260, 'Hero', 100, 16, 3, 5, 250, screen, boss)

    hero.screen = screen
    hero.enemy = boss
    hero.hp = hero.max_hp
    hero.mp = hero.max_mp
    hero.alive = True
    hero.frame_index = 0
    hero.action = 0 #0 pour l'animation de base, 1 pour l'attaque, 2 pour dégats reçu, 3 pour heal, 4 pour mort, 5 pour win, 6 pour special
    hero.update_time = pygame.time.get_ticks()
    
#variables de la classe barre de vie, la vie du héro et la vie de l'ennemi
    hero_health_bar = HealthBar(100, screen_height - bottom_panel + 45, hero.hp, hero.max_hp)
    boss_health_bar = HealthBar(500, screen_height - bottom_panel + 45, boss.hp, boss.max_hp)
    hero_mana_bar = ManaBar(100, screen_height - bottom_panel + 70, hero.mp, hero.max_mp)
    boss_mana_bar = ManaBar(500, screen_height - bottom_panel + 70, boss.mp, boss.max_mp)

#Fonction pour mettre du texte sur l'écran
    def draw_text(text, font, text_col, x, y):
        img = font.render(text,True, text_col)
        screen.blit(img, (x, y))
#Fonction pour afficher le fond d'écran
    def draw_bg():
        screen.blit(background_img, (0, 0))
#Fonction pour afficher l'UI en bas de l'écran de combat
    def draw_panel():
        screen.blit(panel_img, (0, screen_height - bottom_panel-19))
        draw_text(f'{hero.name} HP: {hero.hp}/{hero.max_hp}', font, black, 100, screen_height - bottom_panel -5) #Utilisation directe des attributs de la classe fighter pr définir les noms et la valeur des hp des personnages
        draw_text(f'{boss.name} HP: {boss.hp}/{boss.max_hp}', font, black, 500, screen_height - bottom_panel -5)
        draw_text(f'Level: {hero.level}', font, black, 100, screen_height - bottom_panel + 15)
        draw_text(f'Level: {boss.level}', font, black, 500, screen_height - bottom_panel + 15)
        draw_text(f'Mana: {hero.mp}/{hero.max_mp}', font, purple, 250, screen_height - bottom_panel + 15)
        draw_text(f'Mana: {boss.mp}/{boss.max_mp}', font, purple, 650, screen_height - bottom_panel + 15)
#variable de la classe bouton
    potion_button = Button(100, screen_height - bottom_panel + 100, potion_img, 40, 40)
    special_button = Button(200,screen_height - bottom_panel + 100, special_img, 40, 40)

#création de la boucle
    run = True

#ajout musique
    mixer.init()
    mixer.music.load("musiques/finalboss.mp3")
    mixer.music.play(loops=-1) #Pour que la musique se répète

    while run:

#Affichage des différentes images et du texte

        draw_bg() #Fond d'écran

        draw_panel() #UI en bas
        hero_health_bar.draw(hero.hp)
        boss_health_bar.draw(boss.hp)
        hero_mana_bar.draw(hero.mp)
        boss_mana_bar.draw(boss.mp)

        hero.update("bossbattle")
        hero.draw() #Personnage joueur

        boss.update("bossbattle")
        boss.draw() #IA
        
        potion_button.draw() #Potions du joueur
        special_button.draw() #special du joueur

        draw_text(str(hero.potions),font, red, 130, screen_height - bottom_panel + 100) #Pour avoir le nombre de potions du joueurs affichées
  
#Condition de victoire ou défaites     
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
                    
        pygame.display.update()
#Réitération des variables liés aux choix d'action dans la boucle
        attack = False
        potion = False
        special = False
        target = None


#Position + affichage de la souris
        pos = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)

#Condition de clique lorsque l'on choisit d'attaquer un ennemi        
        if boss.rect.collidepoint(pos) and potion_button.rect.collidepoint(pos) == False and special_button.rect.collidepoint(pos) == False:
            if clicked == True and boss.alive == True:
                attack = True
                target = boss

#Condition de clique lorsque l'ont choisit d'utiliser une potion       
        if potion_button.rect.collidepoint(pos):
            if clicked == True:
                potion = True
            else:
                potion = False

#Condition de clique lorsque l'ont choisit d'utiliser une potion       
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
                        if attack == True and target == boss:
                            hero_atk_snd.play()
                            hero.attack(boss)
                            boss_hurt_snd.play()
                            
                            if hero.mp < hero.max_mp and hero.mp + hero_mana_restored < hero.max_mp:
                                hero.mp += hero_mana_restored
                            else:
                                hero.mp = hero.max_mp     
                            fighter_turn +=1
                            action_cooldown = 0

                        if potion == True: #Choix d'utiliser la potion + éviter que le heal soit supérieur aux hp max
                            if hero.potions > 0  and boss.alive == True:
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
                            hero.special(boss)
                            hero_atk_snd.play()
                            hero_spec_sound1.play()
                            hero_spec_sound2.play()
                            boss_hurt_snd.play()
                            hero.mp -= 250
                            fighter_turn += 1
                            action_cooldown = -200

            else:
                game_over = -1
                
            


            
#Action de L'IA qui joue après le joueur, se heal lorsqu'il passe à la moitié de ses pv                
            if fighter_turn == 2:
                if boss.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        if (boss.hp / boss.max_hp) < 0.5 and boss.potions > 0:
                            healing_sound.play()
                            boss.heal()
                            if boss.max_hp - boss.hp > potion_heal:
                                    heal_amount = potion_heal
                            else:
                                heal_amount = boss.max_hp - boss.hp
                            boss.hp += heal_amount
                            boss.potions -=1
                            fighter_turn += 1
                            action_cooldown = 0
                        elif (boss.hp / boss.max_hp) < 0.5 and boss.potions == 0 and boss.mp >= 250:
                            boss_spec_sound1.play()
                            boss.special(hero)
                            hero_hurt_snd.play()
                            boss.mp -= 250
                            fighter_turn += 1
                            action_cooldown = -200
                        else:
                            boss_atk_snd.play()
                            boss.attack(hero)
                            hero_hurt_snd.play()
                            fighter_turn += 1
                            action_cooldown = 0

                            if boss.mp < boss.max_mp and boss.mp + boss_mana_restored < boss.max_mp:
                                boss.mp += boss_mana_restored
                                fighter_turn += 1
                                action_cooldown = 0
                            else:
                                boss.mp = boss.max_mp
                            fighter_turn +=1
                            action_cooldown = 0
                else:
                    fighter_turn += 1

            if fighter_turn > total_fighter:
                fighter_turn = 1

            if not boss.alive:
                game_over = 1
        
                
            
            #Mouvement du personnage via les touches que l'utilisateur presse
        keys = pygame.key.get_pressed()
        #Lancement de l'écran aventure si barre espace est utilisée
        if keys[pygame.K_SPACE]:
            rpg.game(hero)
        if keys[pygame.K_a]: #relancer le combat
            return bossfight


    