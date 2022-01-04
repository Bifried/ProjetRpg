import pygame
from rpg import game
from pygame import image
from credits import credits
from pygame import mixer
#initialise tout les modules importés de pygame
pygame.init()

#Fonction du menu
def main_menu():
    #Generer la fenetre de notre jeu
    pygame.display.set_caption("Dream")
    screen = pygame.display.set_mode((900, 600))

    #On utilise nos images pour les buttons et le fond
    background = pygame.image.load("images/reve.jpg")
    new_game_img = pygame.image.load("images/new_game.png")
    credit_img = pygame.image.load("images/credits.png")
    quit_img = pygame.image.load("images/quit.png")

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

    #Les boutons
    new_game_button = Button(365, 190, new_game_img, 150,60)
    credit_button = Button(365, 260, credit_img, 150,60)
    quit_button = Button(365, 330, quit_img, 150,60)


    running = True
    #Ajout de la musique
    mixer.init()
    mixer.music.load("musiques/menu.mp3")
    mixer.music.play(loops=-1) #Pour que la musique se répète

    #Tant que running est vrai
    while running:
        

        #Appliquer l'arrière plan de notre jeu
        screen.blit(background, (0, 0))

        #Afficher les boutons sur le menu et créer les conditions de clique
        if new_game_button.draw() == True:
            mixer.music.stop()
            game()
        if credit_button.draw() == True:
            mixer.music.stop()
            credits()
        if quit_button.draw() == True:
            running = False
            pygame.quit()

        credit_button.draw()
        quit_button.draw()

        #Mettre a jour l'ecran
        pygame.display.flip()

        #Si le joueur ferme cette fenêtre
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

main_menu()
        