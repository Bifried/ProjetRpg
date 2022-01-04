
def credits():
    #import de pygame et de la fonction menu
    from pygame import mixer
    import pygame
    from menu import main_menu
    #initialise tout les modules apportés de pygame
    pygame.init()
    
    #création de la fenêtre, taille
    win = pygame.display.set_mode((900, 600))   
    
    #Variable pour la boucle
    run = True

    #ajout de la musique
    mixer.init()
    mixer.music.load("musiques/credits.mp3")
    mixer.music.play(loops=-1) #Pour que la musique se répète
    
    #boucle
    while run:  
        for event in pygame.event.get():
            
            #si l'utilisateur quitte la fenêtre, ça quitte 
            if event.type == pygame.QUIT:
                
                #termine la boucle 
                run = False
            #retour au menu
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                main_menu()

        #Remplissage du fond avec l'image de crédits en plein écran
        background = pygame.image.load("images/merci.jpg")
        win.blit(background,(0,0))

       
        #Met à jour la fenêtre
        pygame.display.update()
    
    #Ferme la fenêtre
    pygame.quit()