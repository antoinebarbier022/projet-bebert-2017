import pygame as pg
import random
from settings import *
from introduction import *
# from menu import *

#initialisation de la fenêtre et du jeu
pg.init()
pg.mixer.init()
pg.display.set_caption(titre)
pg.display.set_icon(icone)
clock = pg.time.Clock()


'''----------------------------------CLASS--------------------------------'''

########## Création du groupe pour le joueur, l'environnement et le décor ##########

class Joueur(pg.sprite.Sprite):
    """docstring for joueur."""

    ########## Mise en place des paramètres de base ##########

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.wallJumpTimer = 0
        self.load_images()
        self.image = self.standing_frames[0] # on charge l'image de Bébert
        self.rect = self.image.get_rect() # on récupère le rectangle de l'image
        self.rect.center = (taille[0] / 2, taille[1] - 100) # position de base de Bébert
        self.vitesseH = 0
        self.vitesseV = 0


    ########## Mise à jour des paramètres du personnage ##########
    def update(self):
        now = pg.time.get_ticks() # variable prenant en compte le temps écoulé
        self.animate()
        self.grav()

        ########## Mise en place de la collision joueur / environnement ##########
        self.rect.x += self.vitesseH # on rajoute à la coordonné x du personnage la vitesse horizontale

        collision = pg.sprite.spritecollide(bebert, environnement, False) # Création d'une liste notant tous les objets en collision avec le joueur
        for e in collision:
            if self.vitesseH > 0: # s'il va à droite et qu'il rencontre un objet, stoppper son déplacement
                self.rect.right = e.rect.left
            elif self.vitesseH < 0: # inversement
                self.rect.left = e.rect.right


        self.rect.y += self.vitesseV # on rajoute à la coordonnée y du personnage la vitesse verticale
        collision = pg.sprite.spritecollide(bebert, environnement, False)
        for e in collision:
            if self.vitesseV >= 0: # s'il tombe et qu'il rencontre un objet, stoppper son déplacement
                self.rect.bottom = e.rect.top
            elif self.vitesseV < 0 : # inversement
                self.rect.top = e.rect.bottom
            self.jumping = False # Boolean qui permet de changer l'animation
            self.vitesseV = 0 # réinitialiser sa vitesse verticale pour qu'il reste sur la plateforme


        if now - self.wallJumpTimer >= 400: # on calcule un intervalle durant lequel il ne pourra pas refaire l'action

            self.rect.x -= 1
            collision = pg.sprite.spritecollide(bebert, plateformeWallJump, False) # On regarde si Bébert rentre en collision avec ce groupe de plateformes
            self.rect.x += 1
            for obj in collision:
                if self.rect.left >= obj.rect.right: # s'il rencontre une plateforme du groupe plateformeWallJump, faire sauter le personnage
                    self.vitesseV = -13
                    self.jumping = True
                    self.wallJumpTimer = now # on réinitialise le timer

            self.rect.x += 1
            collision = pg.sprite.spritecollide(bebert, plateformeWallJump, False)
            self.rect.x -= 1
            for obj in collision:
                if self.rect.right >= obj.rect.left:
                    self.vitesseV = -13
                    self.jumping = True
                    self.wallJumpTimer = now

        self.rect.y += 1
        collision = pg.sprite.spritecollide(bebert, plateformeSaut, False)
        self.rect.y -= 1
        for e in collision:
            if self.rect.bottom == e.rect.top:
                self.vitesseV = -20
                self.jumping = True




    ######### Préparation des listes d'images utilisées pour faire les animations ##########
    def load_images(self):
        self.standing_frames = [pg.image.load(imageB).convert_alpha()]

        self.walk_frames_r = [pg.image.load(imageBR).convert_alpha(),
                              pg.image.load(imageBR1).convert_alpha(),
                              pg.image.load(imageBR).convert_alpha(),
                              pg.image.load(imageBR2).convert_alpha()]

        self.walk_frames_l = [pg.transform.flip(self.walk_frames_r[0], True, False),
                              pg.transform.flip(self.walk_frames_r[1], True, False),
                              pg.transform.flip(self.walk_frames_r[2], True, False),
                              pg.transform.flip(self.walk_frames_r[3], True, False)]

        self.jump_frame = pg.image.load(imageBJ).convert_alpha()

    ########## On vérifie  que le joueur soit sur une plateforme avant de le laisser sauter #########
    def jump(self):
        self.rect.y += 2
        collision = pg.sprite.spritecollide(bebert, environnement, False)
        self.rect.y -= 2
        if len(collision) > 0:
            self.vitesseV = -12
            self.jumping = True


    ########## On met en place les mouvements et la gravité ##########
    def right(self):
        self.vitesseH = 5

    def left(self):
        self.vitesseH = -5

    def stop(self):
        self.vitesseH = 0

    def grav(self):
        # si Bébert ne possède pas de vitesse verticale, mettre la valeur 1 pour qu'il tombe.
        # Sinon on rajoute progressivement 0.65 afin d'augmenter sa vitesse
        if self.vitesseV == 0:
            self.vitesseV = 1
        else:
            self.vitesseV += 0.65

    ########## Animation du personnage ##########
    def animate(self):
        now = pg.time.get_ticks() # on trace le temps

        #-- On cherche à savoir si le personnage possède une vitesse horizontale et se trouve au sol --#
        if self.vitesseH != 0 and self.vitesseV >= 0:
            self.walking = True # Si c'est le cas la variable prend la valeur True
        else:
            self.walking = False

        #-- Dans chaque bloc on vérifie les paramètres de mouvement du personnage et on attribue une animation différente en fonction --#
        if not self.jumping and not self.walking: # s'il est immobile
            if now - self.last_update > 100: # on calcule le temps entre chaque image
                self.last_update = now # on remet le temps à zéro
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
                #-- ici on fait en sorte que le personnage garde toujours le même 'centre de gravité' en fonction de l'image --#
                rectCenter = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = rectCenter

        elif self.jumping and not self.walking: # s'il saute
            if now - self.last_update > 1:
                self.image = self.jump_frame
                collision = pg.sprite.spritecollide(bebert, environnement, False)
                rectCenter = self.rect.center
                rectRight = self.rect.midright
                rectLeft = self.rect.midleft
                self.rect = self.image.get_rect()
                self.rect.center = rectCenter

                #tentative de debugging
                # for e in collision:
                #     if self.rect.bottom == e.rect.top:
                #         self.rect = self.image.get_rect()
                #         self.rect.center = rectCenter
                #     elif self.rect.right == e.rect.midleft:
                #         self.rect = self.image.get_rect()
                #         self.rect.midright = rectRight
                #     elif self.rect.left == e.rect.midright:
                #         self.rect = self.image.get_rect()
                #         self.rect.midleft = rectLeft



        elif not self.jumping and self.walking: # s'il marche
            if now - self.last_update > 150 and self.vitesseH > 0: # à droite
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                self.image = self.walk_frames_r[self.current_frame]
                rectCenter = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = rectCenter

            elif now - self.last_update > 150 and self.vitesseH < 0: # à gauche
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                self.image = self.walk_frames_l[self.current_frame]
                rectCenter = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = rectCenter


########## Création d'une plateforme se déplacant ###########
class PlateformeMouvante(pg.sprite.Sprite):
    """Classe pour les plateformes se déplancant"""
    def __init__(self, x, y, imageP, mouvement):
        super(PlateformeMouvante, self).__init__()
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(imageP).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mouvementH = 2
        self.mouvementV = 2
        self.varCompteur = 60
        self.varMouvement = False
        self.choixMouvement = mouvement #Boolean permettant de choisir la direction de la plateforme

    def update(self):

        if self.varMouvement:
            self.varCompteur += 1
        else:
            self.varCompteur -= 1

        # Si le Boolean = True, alors la plateforme aura un mouvement horizontal
        if self.choixMouvement:
            self.rect.x += self.mouvementH
            if self.varCompteur >= 60:
                self.mouvementH = 2
                self.varMouvement = False
            elif self.varCompteur <= -60:
                self.mouvementH = -2
                self.varMouvement = True

        # Sinon elle aura un mouvement vertical
        elif not self.choixMouvement:
            self.rect.y += self.mouvementV
            if self.varCompteur >= 60:
                self.mouvementV = 2
                self.varMouvement = False
            elif self.varCompteur <= -60:
                self.mouvementV = -2
                self.varMouvement = True


class Environnement(pg.sprite.Sprite):
    """docstring for environnement."""
    def __init__(self, x, y, imageP):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(imageP).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



########## Fin des groupes ##########


'''------------------------------------CLASS--------------------------'''



def shift_world(shift_x):
    world_shift = 0
    world_shift += shift_x

    for e in environnement:
        e.rect.x += shift_x


    # for p in plateformeSaut:
    #     p.rect.x += shift_x

    for p in flag:
        p.rect.x += shift_x

def creationNiveau():
    global groupeSprites, environnement, bebert, plateformeSaut, plateformeWallJump, flag

    groupeSprites = pg.sprite.Group()
    environnement = pg.sprite.Group()
    plateformeSaut = pg.sprite.Group()
    plateformeWallJump = pg.sprite.Group()
    flag = pg.sprite.Group()
    bebert = Joueur()
    groupeSprites.add(bebert)

    with open(niveau, "r") as fichier:

        structure_niveau = []
            #On parcourt les lignes du fichier
        for ligne in fichier:
            ligne_niveau = []
            #On parcourt les sprites (lettres) contenus dans le fichier
            for sprite in ligne:
                #On ignore les "\n" de fin de ligne
                if sprite != '\n':
                    #On ajoute le sprite à la liste de la ligne
                    ligne_niveau.append(sprite)
            #On ajoute la ligne à la liste du niveau
            structure_niveau.append(ligne_niveau)
        #On sauvegarde cette structure
        structure = structure_niveau
    num_ligne = 0

    for ligne in structure:
        #On parcourt les listes de lignes
        num_case = 0
        for sprite in ligne:
            #On calcule la position réelle en pixels
            x = num_case * 50
            y = num_ligne * 50

            if sprite == 'M':
                # si il n'y a rien à gauche et un bloc à droite et que le bloc dessous est différent d'un bloc normal
                if ligne[num_case - 1] == '0' and ligne[num_case + 1] == 'M' and structure[num_ligne + 1][num_case] != 'M' and structure[num_ligne + 1][num_case] != 'W':
                    p = Environnement(x, y, imageP[5])
                    environnement.add(p)
                    groupeSprites.add(p)
                    #s'il n'y a pas de bloc au dessus
                    if structure[num_ligne - 1][num_case] == '0' :
                        p = Environnement(x, y, imageP[1])
                        environnement.add(p)
                        groupeSprites.add(p)
                # en dessous ou au dessus d'un bloc wall Jump, affichage d'un bloc de terre plein
                elif structure[num_ligne + 1][num_case] == 'W':
                    p = Environnement(x, y, imageP[7])
                    environnement.add(p)
                    groupeSprites.add(p)
                elif structure[num_ligne - 1][num_case] == 'W':
                    if ligne[num_case - 1] == '0' and ligne[num_case + 1] == 'M' and structure[num_ligne + 1][num_case] == '0':
                        p = Environnement(x, y, imageP[5])
                        environnement.add(p)
                        groupeSprites.add(p)
                    if ligne[num_case - 1] == 'M' and ligne[num_case + 1] == '0' and structure[num_ligne + 1][num_case] == '0':
                        p = Environnement(x, y, imageP[6])
                        environnement.add(p)
                        groupeSprites.add(p)
                    else:
                        p = Environnement(x, y, imageP[7])
                        environnement.add(p)
                        groupeSprites.add(p)



                elif ligne[num_case - 1] == 'M' and ligne[num_case + 1] == '0' and structure[num_ligne + 1][num_case] != 'M' :
                    p = Environnement(x, y, imageP[6])
                    environnement.add(p)
                    groupeSprites.add(p)
                    if structure[num_ligne - 1][num_case] == '0' :
                        p = Environnement(x, y, imageP[2])
                        environnement.add(p)
                        groupeSprites.add(p)
                #si le bloc au dessus est un bloc alors on met un bloc plein de terre
                elif structure[num_ligne - 1][num_case] != '0':
                    p = Environnement(x, y, imageP[7 ])
                    environnement.add(p)
                    groupeSprites.add(p)

                else:
                    p = Environnement(x, y, imageP[0])
                    environnement.add(p)
                    groupeSprites.add(p)

            if sprite == 'J':          #J = Bloc Saut
                p = Environnement(x, y, imageP[8])
                environnement.add(p)
                plateformeSaut.add(p)
                groupeSprites.add(p)

            if sprite == 'W':          #W = Bloc WallJump
                p = Environnement(x, y, imageP[4])
                environnement.add(p)
                plateformeWallJump.add(p)
                groupeSprites.add(p)

            if sprite == 'X':          #X = Plateforme Mouvante
                p = PlateformeMouvante(x, y, imageP[9], True)
                environnement.add(p)
                groupeSprites.add(p)

            if sprite == 'F': #F = Pancarte de fin de niveau
                p = Environnement(x, y, imageP[10],)
                # environnement.add(p)
                flag.add(p)
                groupeSprites.add(p)

            if sprite == ' ':          #  = ne pas prendre en compte
                num_case -=1

            num_case += 1
        num_ligne += 1

 #   pg.mixer.music.load("music\main_music.ogg")
    corps()

def corps():
    global boucleInterne, boucleJeu, boucleGO
    boucleInterne = True
 #   pg.mixer.music.play(loops=-1)
    while boucleInterne:
        clock.tick(FPS)
        fenetre.blit(backgroundJeu, (0, 0))
        miseAJour()
        evenement()
        dessiner()
        if bebert.rect.y >= taille[1]:
            boucleInterne = False
    boucleJeu = False
    boucleGO = True
 #   pg.mixer.music.fadeout(500)

def miseAJour():
    groupeSprites.update()

    if bebert.rect.right >= 600:
        diff = bebert.rect.right - 600
        bebert.rect.right = 600
        shift_world(-diff)

    if bebert.rect.right <= 250:
        diff = bebert.rect.right - 250
        bebert.rect.right = 250
        shift_world(-diff)

def evenement():
    global boucleInterne, boucleJeu, boucleGlobale, boucleGO
    for event in pg.event.get():
        if event.type == pg.QUIT:
            if boucleInterne:
                boucleInterne = False
            boucleJeu = False
            boucleGO = False
            boucleGlobale = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                bebert.jump()

    key = pg.key.get_pressed()

    if key[pg.K_LEFT]:
        bebert.left()
    elif key[pg.K_RIGHT]:
        bebert.right()
    else:
        bebert.stop()
        bebert.walking = False


    collision = pg.sprite.spritecollide(bebert, flag, False)
    if collision:
        if boucleInterne:
            boucleInterne = False
        boucleJeu = False
        boucleGO = False

def dessiner():
    groupeSprites.draw(fenetre)
    pg.display.update()




    '''-----------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    -----------------------FONCTION MENU -------------------------------------------
    ------------------------------------------------------------------------------'''

def menu():
    global boucleMenu, boucleGlobale

    #image de fond, choix du niveau
    background = pg.image.load(imageBackgroundNiveau).convert()
    fenetre.blit(background,(0,0))

    # création de la surfaces des niveaux
    surface_box_cadre_niv = pg.Surface(dimensionImageNiveau)
    surface_box_cadre_niv.fill(noir)
    surface_box_cadre_niv.set_colorkey(noir)

    # création de la bordure sur la surface
    box_rect = surface_box_cadre_niv.get_rect()
    mon_rect = pg.draw.rect(surface_box_cadre_niv, blanc,box_rect,10)

    #initialisation
    afficher = False
    SortiChoixNiv = False

    while not SortiChoixNiv:
        global boucleJeu, boucleMenu, backgroundJeu, bg, niveau, fichierNiveau

        #afficher background
        fenetre.blit(background,(0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            #on releve les coordonnées x et y de la souris
            sx,sy = pg.mouse.get_pos()

            #lors du clique gauche sur le niveau choisie, cela le lance
            for i in range(6):
                if  (sx > listePointOrigineGrilleX[i][0] and sx < listePointOrigineGrilleX[i][0]+blocW) and (sy > listePointOrigineGrilleX[i][1] and sy < listePointOrigineGrilleX[i][1]+blocH):
                    afficher = True
                    coordonner = (listePointOrigineGrilleX[i][0],listePointOrigineGrilleX[i][1])
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        #on lance les niveaux en sortant de la boucle et en changant le fichier et le background
                        if i+1 == 1:
                            niveau = fichierNiveau[0]
                            backgroundJeu = pg.image.load(bg[0]).convert()
                            boucleJeu = True
                            boucleMenu = False
                            SortiChoixNiv = True
                        if i+1 == 2:
                            niveau = fichierNiveau[1]
                            backgroundJeu = pg.image.load(bg[1]).convert()
                            boucleJeu = True
                            boucleMenu = False
                            SortiChoixNiv = True
                        if i+1 == 3:
                            niveau = fichierNiveau[2]
                            backgroundJeu = pg.image.load(bg[2]).convert()
                            boucleJeu = True
                            boucleMenu = False
                            SortiChoixNiv = True
                        if i+1 == 4: print('chargement niveau 4')
                        if i+1 == 5:
                            niveau = fichierNiveau[4]
                            backgroundJeu = pg.image.load(bg[4]).convert()
                            boucleJeu = True
                            boucleMenu = False
                            SortiChoixNiv = True
                        if i+1 == 6: Editeur_Niveau()
                    #afficher les contours des images lors du survol de la souris
                    if afficher == True:
                        fenetre.blit(surface_box_cadre_niv,coordonner)
                else:
                    afficher = False

            #rafraichir la fenetre / mise à jour
            pg.display.update()


        ''' --------------------------------------------------- '''
        ''' ----------------EDITEUR DE NIVEAU ----------------- '''
        ''' --------------------------------------------------- '''

        def Editeur_Niveau():

            #surface bloc couleur dans la grille (en attendant de mettre les images)
            surfaceBlocCouleur = pg.Surface((30,30))

            # creation des surface des mini bloc pour afficher dans la grille
            M_bloc = pg.image.load(imageBlocNormalMilieu).convert()
            L_bloc = pg.image.load(imageBlocNormalGauche).convert()
            R_bloc = pg.image.load(imageBlocNormalDroit).convert()

            MT_bloc = pg.image.load(imageBlocNormalMilieuTerre).convert()
            RT_bloc = pg.image.load(imageBlocNormalDroitTerre).convert()
            LT_bloc = pg.image.load(imageBlocNormalGaucheTerre).convert()

            Jump_bloc = pg.image.load(imageBlocJump).convert()
            WallJump_bloc = pg.image.load(imageBlocWallJump).convert()
            Mouvement_bloc = pg.image.load(imageBlocMouvement).convert()


            #surface des bloc de selection du type de bloc
            surfaceBloc1 = pg.Surface(sizeSurfaceBloc)
            surfaceBloc1.fill(blanc)

            surfaceBloc2 = pg.Surface(sizeSurfaceBloc)
            surfaceBloc2.fill(blanc)

            surfaceBloc3 = pg.Surface(sizeSurfaceBloc)
            surfaceBloc3.fill(blanc)

            surfaceBloc4 = pg.Surface(sizeSurfaceBloc)
            surfaceBloc4.fill(blanc)

            #----------------------

            surfaceGauche = pg.Surface(sizeSurfaceGauche)
            surfaceGauche.fill(grisF)

            surfaceHaut = pg.Surface(sizeSurfaceHaut)
            surfaceHaut.fill(grisF)

            surfaceEdition = pg.Surface(sizeSurfaceEdition)
            surfaceEdition.fill(blanc)

            #bouton retour, (celui pour retourner sur le choix des niveaux)
            surfaceButtonRetour = pg.Surface(sizeBoutonRetour)
            surfaceButtonRetour.fill(gris)

            #creation de la grille d'edition
            grilleEdition = pg.image.load(imageGrille).convert()
            fenetre.blit(grilleEdition,(0,0))

            #creation bouton background
            surfaceBoutonDecors = pg.Surface(sizeBoutonDecors)
            surfaceBoutonDecors.fill(blanc)

            #creation de la surface qui contiendra les differents blocs
            surfaceParent4Blocs = pg.Surface(sizeParent4Blocs)
            surfaceParent4Blocs.fill(grisF)

            #creation du bouton "tester le niveau"
            surfaceBoutonTesterNiveau = pg.Surface(sizeBoutonTesterNiveau)
            surfaceBoutonTesterNiveau.fill(blanc)

            #surface message avertissement reinitialisation
            surfaceAvertissementReinitialisation = pg.Surface(sizeSurfaceMessageAvertissement)
            surfaceAvertissementReinitialisation.fill(couleurSurfaceAvertissement)

            #configuration de la police
            Police_titre = pg.font.Font("font/OCRAEXT.TTF",taillePolice_titre)
            Police_normal = pg.font.Font("font/OCRAEXT.TTF",taillePolice_normal)
            Police_petit = pg.font.Font("font/OCRAEXT.TTF",taillePolice_petit)

            def objet_texte(text, couleur,taille):
                if taille == 'titre':
                    textSurface = Police_titre.render(text, True, couleur)
                elif taille == 'normal':
                    textSurface = Police_normal.render(text, True, couleur)
                elif taille == 'petit':
                    textSurface = Police_petit.render(text, True, couleur)
                else:
                    textSurface = Police_normal.render(text, True, couleur)

                return textSurface, textSurface.get_rect()

            def message(message,taille, couleur,x,y,position ='center'):
                textSurface, textRect = objet_texte(message,couleur,taille)
                if position == 'center':
                    textRect.center = (x,y)
                else:
                    textRect.x = x
                    if taille == 'titre':
                        textRect.y = y-(taillePolice_titre/2)
                    elif taille == 'normal':
                        textRect.y = y-(taillePolice_normal/2)
                    elif taille == 'petit':
                        textRect.y = y-(taillePolice_petit/2)

                fenetre.blit(textSurface,textRect)

            #on prend le fichier niveau et on le met dans une liste
            structure_niveau = []
            fichier = open(nomFichierEdition,'r')
            for ligne in fichier:
                ligne_niveau = []
                for code in ligne:
                    if code != '\n':
                        ligne_niveau.append(code)
                structure_niveau.append(ligne_niveau)
            #structure_niveau = [[codeVide for x in range(nombreCaseAxeAbscisse)]for y in range(nombreCaseAxeOrdonnee)]

        #______________________________________________________________
        #----------------------DEBUT DE LA BOUCLE----------------------

            afficherblocGrille = False
            afficherRegle = 1
            afficherGrille = 1
            numeroDuDecorsEdition = 1
            boutonBlocSelect = 1
            changementCouleurBoutonReinitialiser = False
            boutonReinitialiserActionner = False
            afficherMessageAvertissement = False
            desactivationDesBoutons = False


            afficherButtonRetour = False
            numeroFenetreEdition = 1
            textureBloc = codeBlocNormal
            afficherGameOver = False

            Exit_Edit_Niveau = False

            while not Exit_Edit_Niveau:
                global niveau, fichierNiveau, boucleGO, backgroundJeu, bg

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()

                    sx,sy = pg.mouse.get_pos()

                    #pour desactiver la recherche d'événement
                    if desactivationDesBoutons == False:

                        #------ Bouton Retour -----
                        if (sx > 0 and sx < 200) and (sy > 0 and sy < 50):
                            afficherButtonRetour = True
                            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                                Exit_Edit_Niveau = True
                        else: afficherButtonRetour = False

                        #------- Bouton "Tester le Niveau" ------
                        if (sx > 530 and sx < 530+240) and (sy > 450 and sy < 450+30):
                            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                                print('Tester le Niveau')
                                niveau = fichierNiveau[5]
                                creationNiveau()
                                boucleGO = False

                        #------- Bouton Background -------
                        if (sx > 50 and sx < 250) and (sy > 110 and sy < 150):
                            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                                numeroDuDecorsEdition += 1

                        #------- Bouton afficher la grille ------
                        if (sx > 30 and sx < 250) and (sy > 335 and sy < 365):
                            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                                afficherGrille +=1

                        #------- Bouton afficher les regles ------
                        if (sx > 30 and sx < 250) and (sy > 375 and sy < 405):
                            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                                afficherRegle +=1


                        #------- lors du click afficher et supprimer mini bloc ------
                        #liste qui contient les coordonner entre 0 et 600
                        positionDepart = 0
                        test = [e*sizeBlocGrille for e in range(20)]
                        for y in range(10):
                            for x in range(20):
                                if  (sx > test[x]+350 and sx < (test[x])+350+sizeBlocGrille) and (sy > test[y]+125 and sy < test[y]+125+sizeBlocGrille):
                                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                                        #remplacement des bloc dans la liste
                                        positionDepart = (numeroFenetreEdition*20)-20
                                        x = positionDepart+x
                                        #les if permettent de savoir quelle bloc il y a et le supprime, ensuite le else de fin change la texture
                                        if structure_niveau[y][x] == codeBlocNormal :
                                            structure_niveau[y][x] = codeVide
                                        elif structure_niveau[y][x] == codeBlocJump :
                                            structure_niveau[y][x] = codeVide
                                        elif structure_niveau[y][x] == codeBlocMouvement :
                                            structure_niveau[y][x] = codeVide
                                        elif structure_niveau[y][x] == codeBlocWallJump :
                                            structure_niveau[y][x] = codeVide
                                        else:
                                            structure_niveau[y][x] = textureBloc #changer la texture en fonction des boutons blocs

                        #------- Creation des boutons selection des blocs avec changement de la texture ------
                        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                            if (sx > 30 and sx < 80) and (sy > 230 and sy < 280): #clique de la souris sur le 1er bloc
                                boutonBlocSelect = 1
                                textureBloc = codeBlocNormal#la texture change en fonction du bouton selectionner
                            elif (sx > 30+63 and sx < 80+63) and (sy > 230 and sy < 280): #2eme bloc
                                boutonBlocSelect = 2
                                textureBloc = codeBlocJump
                            elif (sx > 30+126 and sx < 80+126) and (sy > 230 and sy < 280): #3eme bloc
                                boutonBlocSelect = 3
                                textureBloc = codeBlocWallJump
                            elif (sx > 30+190 and sx < 80+190) and (sy > 230 and sy < 280): #4eme bloc
                                boutonBlocSelect = 4
                                textureBloc = codeBlocMouvement

                        #-------- CHANGEMENT DE FENETRE (evenement clavier avec les touches right et left)
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_RIGHT and numeroFenetreEdition < nombreFenetreMax:
                                #lorsque l'on appuie sur la touche droite, changement de fenetre
                                numeroFenetreEdition +=1
                            if event.key == pg.K_LEFT and numeroFenetreEdition > nombreFenetreMin:
                                #lorsque l'on appuie sur la touche droite, changement de fenetre
                                numeroFenetreEdition -=1

                    #------- Bouton Reinitialiser le niveau ------
                    if (sx > 800 and sx < 800+30) and (sy > 450 and sy < 450+30):
                        if desactivationDesBoutons == False: changementCouleurBoutonReinitialiser = True
                        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                            afficherMessageAvertissement = True
                            boutonReinitialiserActionner = True
                            desactivationDesBoutons = True
                    else: changementCouleurBoutonReinitialiser = False



                    #si bouton rehinitialiser actionner (on desactive tout les boutons)
                    if event.type == pg.KEYDOWN and event.key == pg.K_DELETE and boutonReinitialiserActionner == True:
                        print('niveau réinitialisé')
                        structure_niveau = [[codeVide for x in range(nombreCaseAxeAbscisse)]for y in range(nombreCaseAxeOrdonnee)]
                        afficherMessageAvertissement = False
                        boutonReinitialiserActionner = False
                        desactivationDesBoutons = False
                    elif event.type == pg.KEYDOWN and event.key != pg.K_DELETE and boutonReinitialiserActionner == True:
                        afficherMessageAvertissement = False
                        boutonReinitialiserActionner = False
                        desactivationDesBoutons = False


                '''affichage dans la fenetre des differents elements'''

                fenetre.fill(couleurFenetre)
                fenetre.blit(surfaceGauche,(0,0))
                fenetre.blit(surfaceHaut,(0,0))
                fenetre.blit(surfaceEdition,positionFenetreEdition)


                if afficherButtonRetour == True:
                    fenetre.blit(surfaceButtonRetour,(0,0))

                #ligne sous la surface du haut
                ligne = pg.draw.line(fenetre,couleurLigneSousSurfaceHaut,(0,50),(1000,50),4)

                #rectangle sous le texte "background"
                fenetre.blit(surfaceBoutonDecors,positionBoutonDecors)

                #changement du texte background et mise en place de l'image dans le cadre edition

                if numeroDuDecorsEdition == 1:
                    message(nomDecors[0],'normal', noir,150,130)
                    decors1 = pg.image.load(imageDecors[0]).convert()
                    surfaceEdition.blit(decors1,(0,0))
                    backgroundJeu = pg.image.load(bg[0]).convert()
                if numeroDuDecorsEdition == 2:
                    message(nomDecors[1],'normal', noir,150,130)
                    decors2 = pg.image.load(imageDecors[1]).convert()
                    surfaceEdition.blit(decors2,(0,0))
                    backgroundJeu = pg.image.load(bg[1]).convert()
                if numeroDuDecorsEdition == 3:
                    message(nomDecors[2],'normal', noir,150,130)
                    decors3 = pg.image.load(imageDecors[2]).convert()
                    surfaceEdition.blit(decors3,(0,0))
                    backgroundJeu = pg.image.load(bg[2]).convert()
                if numeroDuDecorsEdition == 4:
                    message(nomDecors[3],'normal', noir,150,130)
                    decors3 = pg.image.load(imageDecors[3]).convert()
                    surfaceEdition.blit(decors3,(0,0))
                    backgroundJeu = pg.image.load(bg[3]).convert()
                if numeroDuDecorsEdition == 5:
                    message(nomDecors[4],'normal', noir,150,130)
                    decors3 = pg.image.load(imageDecors[4]).convert()
                    surfaceEdition.blit(decors3,(0,0))
                    backgroundJeu = pg.image.load(bg[4]).convert()
                if numeroDuDecorsEdition == 6: numeroDuDecorsEdition = 1



                #--------------------affichage des blocs dans la grille d'edition-----------------------------
                try:
                    y =0 #init à 0 puis on rajoute 1 jusqu'à 10 (c'est le y qui parcours la liste niveau pour obtenir la position)
                    for num_ligne in range(11):
                        for num_case in range(20):
                            #remplacement des bloc dans la liste
                            positionDepart = (numeroFenetreEdition*20)-20 #le chiffre 20 est la longeur de la fenetre en case
                            x = positionDepart+num_case
                            xt = sizeBlocGrille*num_case
                            yt = sizeBlocGrille*num_ligne

                            #si le bloc selectionner est un bloc normal
                            if structure_niveau[y][x] == codeBlocNormal :

                                #si le bloc situé à gauche est vide et que celui à droite droite est un bloc normal et celui en dessus il y a du vide
                                if structure_niveau[y][x-1] == codeVide and structure_niveau[y][x+1] == codeBlocNormal and structure_niveau[y+1][x] == codeVide:
                                    # alors on affiche le bloc normal en terre et en position gauche
                                    surfaceEdition.blit(LT_bloc,(xt,yt))
                                    #si le bloc au dessus est vide
                                    if structure_niveau[y-1][x] == codeVide :
                                        #alors on affiche le bloc de gauche avec herbe en position gauche
                                        surfaceEdition.blit(L_bloc,(xt,yt))

                                #sinon si le bloc situé à droite est vide et que celui à gauche droite est un bloc normal et celui en dessus est different d'un bloc normal
                                elif structure_niveau[y][x+1] == codeVide and structure_niveau[y][x-1] == codeBlocNormal and structure_niveau[y+1][x] == codeVide:
                                    # # alors on affiche le bloc normal en terre et en position droite
                                    surfaceEdition.blit(RT_bloc,(xt,yt))
                                    #si le bloc au dessus est vide
                                    if structure_niveau[y-1][x] == codeVide:
                                        #alors on affiche un bloc normal avec herbe en position droite
                                        surfaceEdition.blit(R_bloc,(xt,yt))


                                #si le bloc au dessus est un bloc
                                elif structure_niveau[y-1][x] != codeVide:
                                    #alors on affiche un bloc de terre plein
                                    surfaceEdition.blit(MT_bloc,(xt,yt))

                                #sinon on affiche un bloc de terre avec de l'herbe
                                else:
                                    surfaceEdition.blit(M_bloc,(xt,yt))

                            #affichage bloc jump
                            if structure_niveau[y][x] == codeBlocJump :
                                surfaceEdition.blit(Jump_bloc,(xt,yt))

                            #affichage bloc Walljump
                            if structure_niveau[y][x] == codeBlocWallJump :
                                surfaceEdition.blit(WallJump_bloc,(xt,yt))

                            #affichage bloc Mouvement
                            if structure_niveau[y][x] == codeBlocMouvement :
                                surfaceBlocCouleur.fill(orange)
                                surfaceEdition.blit(Mouvement_bloc,(xt,yt))
                        y+=1
                except IndexError:
                    print('Un ou plusieurs caractères manquant dans le fichier texte')
                    print('Le niveau a été réinitialisé')
                    structure_niveau = [[codeVide for x in range(nombreCaseAxeAbscisse)]for y in range(nombreCaseAxeOrdonnee)]


                #affichage grille d'edition
                if afficherGrille == 1:
                    message('| Grille : oui','normal', blanc,30,350,'justifier')
                    surfaceEdition.blit(grilleEdition,(0,0))
                else:
                    afficherGrille = 0
                    message('| Grille : non','normal', blanc,30,350,'justifier')

                #affichage message avertissement de la suppresion du niveau
                if afficherMessageAvertissement == True:
                    surfaceEdition.blit(surfaceAvertissementReinitialisation,(60,60))
                    message('ATTENTION !','normal', couleurTexteAvertissement,650,200)
                    message('Si vous souhaitez réinitialiser le niveau','petit', couleurTexteAvertissement,650,220)
                    message('appuyer sur la touche |suppr|','petit', couleurTexteAvertissement,650,240)

                #affichage bouton reinitialiser le niveau
                rect = pg.draw.rect(fenetre,blanc,(800,450,30,30))
                boutonReinitialiser = pg.image.load(imageCroixReinitialiser).convert()
                fenetre.blit(boutonReinitialiser,(800,450))


                #affichage de la regle
                if afficherRegle == 1:
                    message('| Règles : oui','normal', blanc,30,390,'justifier')
                    # creation la numerotation des cases
                    e = 0
                    for i in range(1,11):
                        message(str(i),'normal', grisClair,330,140+e)
                        e +=30
                    #creation alphabet numerotation
                    e = 0
                    lettre = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T']
                    for i in lettre:
                        message(str(i),'normal', grisClair,365+e,110)
                        e +=30
                else:
                    afficherRegle = 0
                    message('| Règles : non','normal', blanc,30,390,'justifier')


                #surface et rectangle sous le texte "bloc"
                fenetre.blit(surfaceParent4Blocs,(30,230))
                surfaceParent4Blocs.blit(surfaceBloc1,(0,0))
                surfaceParent4Blocs.blit(surfaceBloc2,(63,0))
                surfaceParent4Blocs.blit(surfaceBloc3,(126,0))
                surfaceParent4Blocs.blit(surfaceBloc4,(190,0))
                if boutonBlocSelect == 1 : surfaceBloc1.fill(couleurFondBlockSelect)
                else: surfaceBloc1.fill(blanc)
                if boutonBlocSelect == 2 : surfaceBloc2.fill(couleurFondBlockSelect)
                else: surfaceBloc2.fill(blanc)
                if boutonBlocSelect == 3 : surfaceBloc3.fill(couleurFondBlockSelect)
                else: surfaceBloc3.fill(blanc)
                if boutonBlocSelect == 4 : surfaceBloc4.fill(couleurFondBlockSelect)
                else: surfaceBloc4.fill(blanc)


                #affichage des images des blocs dans les 4 cases de selection de bloc
                surfaceBloc1.blit(M_bloc,(10,10))
                surfaceBloc2.blit(Jump_bloc,(10,10))
                surfaceBloc3.blit(WallJump_bloc,(10,10))
                surfaceBloc4.blit(Mouvement_bloc,(10,10))

                #bouton "tester le niveau"
                fenetre.blit(surfaceBoutonTesterNiveau,positionBoutonTesterNiveau)
                message('Tester le niveau','normal', grisF,650,465)

                #textes dans la surface du haut
                message('EDITEUR DE NIVEAU | fenetre ','titre', blanc,650,25)
                surfaceNumFenetre = pg.Surface((40,50))
                surfaceNumFenetre.fill(couleurLigneSousSurfaceHaut)
                fenetre.blit(surfaceNumFenetre,(860,0))
                message(str(numeroFenetreEdition) ,'titre',couleurNumeroFenetreEdition,880,25)
                message('RETOUR','titre', blanc,30,25,'justifier')

                #texte dans la surface de gauche
                message('Décors','normal', blanc,150,80)
                message('Blocs','normal', blanc,150,200)


                #on ecrit dans le fichier pour mettre les modification mise dans l'editeur, à l'interrieur du fichier niveau
                try:
                    fichier_editeurNiveau = open(nomFichierEdition,'w')
                    for y in range(nombreCaseAxeOrdonnee):
                        for x in range(nombreCaseAxeAbscisse):
                            fichier_editeurNiveau.write(structure_niveau[y][x])
                        fichier_editeurNiveau.write('\n')
                except IndexError:
                    print('Un ou plusieurs caractères manquant dans le fichier texte')
                    print('On execute la réinitialisation automatique du niveau')
                    structure_niveau = [[codeVide for x in range(nombreCaseAxeAbscisse)]for y in range(nombreCaseAxeOrdonnee)]
                fichier_editeurNiveau.close()


                pg.display.update()

def gameOver():
    Game_Over = pg.image.load(imageGameOver).convert_alpha()
    fenetre.blit(Game_Over,(0,0))

    boutonMenu = False
    boutonRecommencer = False

    GameOver = False
    while not GameOver:
        global boucleMenu, boucleGO, boucleJeu
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            sx,sy = pg.mouse.get_pos()


            if (sx > 306 and sx < 450) and (sy > 254 and sy < 304):
                boutonMenu = True
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    print('menu')
                    boucleGO = False
                    boucleMenu = True
                    GameOver = True
            else:
                boutonMenu = False

            if (sx > 532 and sx < 722) and (sy > 254 and sy < 304):
                boutonRecommencer = True
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    print('Recommencer')
                    boucleGO = False
                    boucleMenu = False
                    boucleJeu = True
                    GameOver = True
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

########## Boucle comprenant la totalité du jeu ##########

global boucleGlobale, boucleMenu, boucleJeu
intro()
while boucleGlobale:
    while boucleMenu :
        menu()
    while boucleGO:
        gameOver()
    while boucleJeu:
        creationNiveau()

pg.quit()
