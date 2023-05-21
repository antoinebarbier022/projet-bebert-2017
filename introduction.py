import pygame as pg
from settings import*
from pygame.locals import *

pg.init()

# Police_ecriture = pg.font.Font("font/OCRAEXT.TTF", 24)

Police_ecriture = pg.font.SysFont("monospace", 15)

def objet_texte(text, couleur):
    textSurface = Police_ecriture.render(text, True, couleur)
    return textSurface, textSurface.get_rect()

def message(message, couleur,x,y):
    textSurface, textRect = objet_texte(message,couleur)
    textRect.center = (x,y)
    fenetre.blit(textSurface,textRect)

def intro():

    #importation image de fond, introduction
    background_intro = pg.image.load(imageBackgroundIntro).convert()
    fenetre.blit(background_intro,(0,0))

    intro = True
    compteur = 10
    introFPS = 30

    clock = pg.time.Clock()
    while intro:
        clock.tick(introFPS) #la boucle tourne 30 fois par seconde
        for event in pg.event.get():
            if event.type == pg.QUIT: #quitter le jeu si on appuie sur croix
                intro = False
                SortiChoixNiv = True
                pg.quit()
                quit()
            #si appuie sur une touche : on sort de la boucle
            if event.type == pg.KEYDOWN:
                intro = False
        #afficher à l'écran
        fenetre.blit(background_intro,(0,0))
        #afficher le texte quand le compteur est plus petit que 60
        if compteur < 50:
            message('Appuyer sur une touche', blanc, 500,460)
        if compteur == 60:
            compteur = 0
        compteur += 1
        pg.display.update()

if __name__ == '__main__':
    fenetre = pg.display.set_mode(taille)
    pg.display.set_caption(titre)
    intro()
