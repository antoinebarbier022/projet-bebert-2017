import pygame as pg
from settings import*
from pygame.locals import *

pg.init()

def gameOver():
    Game_Over = pg.image.load(imageGameOver).convert()
    fenetre.blit(Game_Over,(0,0))

    boutonMenu = False
    boutonRecommencer = False

    GameOver = False
    while not GameOver:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            sx,sy = pg.mouse.get_pos()


            if (sx > 306 and sx < 450) and (sy > 254 and sy < 304):
                boutonMenu = True
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    print('menu')
            else:
                boutonMenu = False

            if (sx > 532 and sx < 722) and (sy > 254 and sy < 304):
                boutonRecommencer = True
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    print('Recommencer')
            else:
                boutonRecommencer = False

        fenetre.blit(Game_Over,(0,0))


        if boutonRecommencer == True: #bouton recommencer
            surfaceBoutonRecommencer = pg.Surface((190,50))
            surfaceBoutonRecommencer.fill(vert)
            surfaceBoutonRecommencer.set_colorkey(vert)
            box_rect_BoutonRecomencer = surfaceBoutonRecommencer.get_rect()
            cadreBoutonRecommencer = pg.draw.rect(surfaceBoutonRecommencer,noir,box_rect_BoutonRecomencer,10)
            fenetre.blit(surfaceBoutonRecommencer,(522,254))

        if boutonMenu == True: #bouton retour menu
            surfaceBoutonMenu = pg.Surface((144,50))
            surfaceBoutonMenu.fill(vert)
            surfaceBoutonMenu.set_colorkey(vert)
            box_rect_BoutonMenu = surfaceBoutonMenu.get_rect()
            cadreBoutonMenu= pg.draw.rect(surfaceBoutonMenu,noir,box_rect_BoutonMenu,10)
            fenetre.blit(surfaceBoutonMenu,(306,254))

        pg.display.update()

if __name__ == '__main__':
    fenetre = pg.display.set_mode(taille)
    pg.display.set_caption(titre)
    gameOver()
    pg.quit()
    quit()
