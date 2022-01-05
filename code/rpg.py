
# import pygame module in this program 
import Battle
import Battle2
import Bossbattle
import pygame
from pygame import mixer
from random import randint

def game(hero=Battle.Fighter(330, 260, 'Hero', 100, 16, 3, 5, 250, None, None)): #pour garder les stats du joueurs après un combats
    from menu import main_menu


#activation de pygame
    pygame.init()
    
    #création de la fenêtre  
    win = pygame.display.set_mode((900, 600))  
    
    #coordonées des personnages,
    #perso
    x = 200
    y = 100
#ennemi1
    x2 = 100
    y2 = 490
#enemy 2
    x3 = 500
    y3 = 400
#boss
    x4 = 800
    y4 = 500

#pnj
    x5 = 200
    y5 = 250
    
    #dimension du personnage
    width = 30
    height = 30


    #vitesse
    vel = 3
    
    


   
    run = True

    #ajout musique
    mixer.init()
    mixer.music.load("musiques/adventuring.mp3")
    mixer.music.play(loops=-1) #Pour que la musique se répète
    dialog = pygame.image.load("images/dialog_box.png")
    menu_help = pygame.image.load("images/menu_help.png")

    #boucle
    while run:
        #création d'un délais
        pygame.time.delay(10)

        #affichage des images et création de rectangle de collision à partir des images pour chaque personnages
        
        hero_img = pygame.image.load("images/character.png") 
        hero_small = pygame.transform.scale(hero_img,(60,60))  
        hero_rect = hero_img.get_rect()
        hero_rect.center = (x, y)

        enemy = pygame.image.load("images/enemy.png") 
        enemy_small = pygame.transform.scale(enemy,(70,70))  
        enemy_rect = enemy.get_rect()
        enemy_rect.center = (x2, y2)

        enemy2 = pygame.image.load("images/enemy2.png") 
        enemy2_small = pygame.transform.scale(enemy2,(90,90))  
        enemy2_rect = enemy2.get_rect()
        enemy2_rect.center = (x3, y3)

        enemy3 = pygame.image.load("images/boss.png") 
        enemy3_small = pygame.transform.scale(enemy3,(90,90))  
        enemy3_rect = enemy3.get_rect()
        enemy3_rect.center = (x4, y4)

        pnj = pygame.image.load("images/pnj.png") 
        pnj_small = pygame.transform.scale(pnj,(90,90))  
        pnj_rect = pnj.get_rect()
        pnj_rect.center = (x5, y5)
#chargement de l'image de la map
        background = pygame.image.load("images/map.jpg")
        
        
        win.blit(background,(0,0))
        win.blit(hero_small, (x,y, width, height))
        win.blit(enemy_small, (x2,y2, width, height))
        win.blit(enemy2_small, (x3,y3, width, height))
        win.blit(enemy3_small, (x4,y4, width, height))
        win.blit(pnj_small,(x5,y5, width, height))

  
        for event in pygame.event.get():
            
#quitter fermeture de fenêtre
            if event.type == pygame.QUIT:
                
                #Sortie de boucle
                run = False
        #Mouvement du personnage via les touches que l'utilisateur presse
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_LEFT] and x>-10:
            
            #Désincrémentation de x
            x -= vel
            
       
        if keys[pygame.K_RIGHT] and x<870-width:
            
            #Incrémentation de x
            x += vel
            
           
        if keys[pygame.K_UP] and y>0:
            
            #Désincrémentation de y
            y -= vel
            
           
        if keys[pygame.K_DOWN] and y<560-height:
            #Incrémentation d'y
            y += vel
        #menu aide quand on appuie sur la touche "m"
        if keys[pygame.K_m] and hero_rect.colliderect(pnj_rect) == False:
            win.blit(menu_help,(0,450, 0,0))

        #retour au menu si touche echap est utilisée
        if keys[pygame.K_ESCAPE]:
            mixer.music.stop()
            main_menu()
        #lancement d'un combat en fonction de l'ennemi avec lequel le joueur à une collision
        if hero_rect.colliderect(enemy_rect):
            Battle.fight(hero)
        elif hero_rect.colliderect(enemy2_rect):
            Battle2.second_fight(hero)
        elif hero_rect.colliderect(enemy3_rect):
            Bossbattle.bossfight(hero)
        
        if hero_rect.colliderect(pnj_rect):
            win.blit(dialog, (0, 400, 0, 0))

      

        
        #Mise à jour de la fenêtre
        pygame.display.update() 
    
    #Fermeture de la fenêtre
    pygame.quit()