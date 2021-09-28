import pygame as pg
from settings import *

class Joueur(pg.sprite.Sprite):
    """classe pour l'objet joueur"""
    def __init__(self):
        super(joueur, self).__init__()
        self.arg = arg


class Environnement(pg.sprite.Sprite):
    """classe pour les plateformes"""
    def __init__(self):
        super(Plateforme, self).__init__()
        self.arg = arg


class PlateformeMouvante(pg.sprite.Sprite):
    """Classe pour les plateformes se déplancant"""
    def __init__(self):
        super(PlateformeMouvante, self).__init__()
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(pTaille).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mouvementH = 3
        self.varCompteur = 0
        self.varMouvement = True

    def update(self):
        if self.varMouvement:
            self.varCompteur += 1
        else:
            self.varCompteur -= 1

        self.rect.x += self.mouvementH
        if self.varCompteur >= 2:
            self.mouvementH = 3
            self.varMouvement = False
        elif self.varCompteur >= -2:
            self.varMouvement = -3
            self.varMouvement = True





class Ennemis(pg.sprite.Sprite):
    """Classe pour les objets Ennemis"""
    def __init__(self):
        super(Ennemis, self).__init__()
        self.arg = arg
