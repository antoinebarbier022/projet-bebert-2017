import pygame as pg
from settings import *
from pygame.locals import *

pg.init()

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
        global boucleJeu, boucleMenu

        #afficher background
        fenetre.blit(background,(0,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        #on releve les coordonnées x et y de la souris
        sx,sy = pg.mouse.get_pos()


        #on verifie que la souris ne se trouve pas au dessus d'un bloc, si c'est le cas on renvoie True pour pouvoir afficher les bordures
        for i in range(6):
            if  (sx > listePointOrigineGrilleX[i][0] and sx < listePointOrigineGrilleX[i][0]+blocW) and (sy > listePointOrigineGrilleX[i][1] and sy < listePointOrigineGrilleX[i][1]+blocH):
                afficher = True
                coordonner = (listePointOrigineGrilleX[i][0],listePointOrigineGrilleX[i][1])
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if i+1 == 2: print('chargement niveau 2')
                    if i+1 == 3: print('chargement niveau 3')
                    if i+1 == 4: print('chargement niveau 4')
                    if i+1 == 5: print('chargement niveau 5')
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
            fondEcran = 1
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
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()

                    sx,sy = pg.mouse.get_pos()
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
                                NiveauTest()

                        #------- Bouton Background -------
                        if (sx > 50 and sx < 250) and (sy > 110 and sy < 150):
                            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                                fondEcran += 1

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
                ligne = pg.draw.line(fenetre,gris,(0,50),(1000,50),4)

                #rectangle sous le texte "background"
                fenetre.blit(surfaceBoutonDecors,positionBoutonDecors)

                #changement du texte background et mise en place de l'image dans le cadre edition
                if fondEcran == 1:
                    message(nomDecors[0],'normal', noir,150,130)
                    decors1 = pg.image.load(imageDecors[0]).convert()
                    surfaceEdition.blit(decors1,(0,0))
                if fondEcran == 2:
                    message(nomDecors[1],'normal', noir,150,130)
                    decors2 = pg.image.load(imageDecors[1]).convert()
                    surfaceEdition.blit(decors2,(0,0))
                if fondEcran == 3:
                    message(nomDecors[2],'normal', noir,150,130)
                    decors3 = pg.image.load(imageDecors[2]).convert()
                    surfaceEdition.blit(decors3,(0,0))
                if fondEcran == 4: fondEcran = 1


                #--------------------affichage des blocs dans la grille d'edition-----------------------------
                try:
                    y =0 #init à 0 puis on rajoute 1 jusqu'à 10 (c'est le y qui parcours la liste niveau pour obtenir la position)
                    for num_ligne in range(11):
                        for num_case in range(20):
                            #remplacement des bloc dans la liste
                            positionDepart = (numeroFenetreEdition*20)-20
                            x = positionDepart+num_case
                            xt = sizeBlocGrille*num_case
                            yt = sizeBlocGrille*num_ligne

                            #si le bloc selectionner est un bloc normal
                            if structure_niveau[y][x] == codeBlocNormal :

                                #si le bloc situé à gauche est vide et que celui à droite droite est un bloc normal et celui en dessus il y a du vide
                                if structure_niveau[y][x-1] == codeVide and structure_niveau[y][x+1] == codeBlocNormal and structure_niveau[y+1][x] == codeVide :
                                    # alors on affiche le bloc normal en terre et en position gauche
                                    surfaceEdition.blit(LT_bloc,(xt,yt))
                                    #si le bloc au dessus est vide
                                    if structure_niveau[y-1][x] == codeVide :
                                        #alors on affiche le bloc de gauche avec herbe en position gauche
                                        surfaceEdition.blit(L_bloc,(xt,yt))

                                #sinon si le bloc situé à droite est vide et que celui à gauche droite est un bloc normal et celui en dessus est different d'un bloc normal
                                elif structure_niveau[y][x+1] == codeVide and structure_niveau[y][x-1] == codeBlocNormal and structure_niveau[y+1][x] == codeVide :
                                    # # alors on affiche le bloc normal en terre et en position droite
                                    surfaceEdition.blit(RT_bloc,(xt,yt))
                                    #si le bloc au dessus est vide
                                    if structure_niveau[y-1][x] == codeVide:
                                        #alors on affiche un bloc normal avec herbe en position droite
                                        surfaceEdition.blit(R_bloc,(xt,yt))


                                #si le bloc au dessus est un bloc de terre
                                elif structure_niveau[y-1][x] == codeBlocNormal:
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
                    print('On execute la réinitialisation automatique du niveau')
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
                surfaceNumFenetre.fill(gris)
                fenetre.blit(surfaceNumFenetre,(860,0))
                message(str(numeroFenetreEdition) ,'titre',blanc,880,25)
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


if __name__ == '__main__':
    fenetre = pg.display.set_mode(taille)
    pg.display.set_caption(titre)
    menu()
