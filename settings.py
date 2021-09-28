import pygame as pg

pg.init()

#principaux paramètres
taille = (1000, 500)
titre = '''The Bebert's Aventures'''
fenetre = pg.display.set_mode(taille)
icone = pg.image.load('image/icone.png').convert_alpha()

#----- Nom du fichier niveau à modifier (editeur de niveau)
nomFichierEdition = 'niveau/lvlPerso.txt'

#image background
bg = ["image/Background/i1.png", #0
      "image/Background/i2.png", #1
      "image/Background/i3.png", #2
      "image/Background/i4.png", #3
      "image/Background/i5.png" #4
      ]
backgroundJeu = pg.image.load(bg[0]).convert()

FPS = 60

boucleGlobale = True
boucleMenu = True
boucleJeu = False
boucleGO = False

fichierNiveau = ['niveau/l1.txt', #0
                'niveau/l2.txt', #1
                'niveau/l3.txt', #2
                'niveau/l4.txt', #3
                'niveau/l5.txt', #4
                nomFichierEdition #5
                ]

niveau = fichierNiveau[0]


imageB = "image/Bebert/BebertDebout.png"
imageBR = "image/Bebert/BebertDroite.png"
imageBJ = "image/Bebert/BebertJump.png"
imageBR1 ="image/Bebert/BebertCours1.png"
imageBR2 ="image/Bebert/BebertCours2.png"


imageP = ["image/plateforme/pM.png", #0 bloc normal milieu avec herbe
          "image/plateforme/pLR.png", #1 bloc normal coté gauche avec herbe
          "image/plateforme/pRR.png", #2 bloc normal coté droit avec herbe
          "image/plateforme/pW.png", #3 bloc normal avec herbe coté droit et gauche
          "image/plateforme/pWJ.png", #4 bloc wall jump
          "image/plateforme/pLRF.png", #5 bloc normal coté gauche sans herbe
          "image/plateforme/pRRF.png", #6 bloc normal coté droit sans herbe
          "image/plateforme/pMF.png", #7 bloc normal milieu sans herbe
          "image/plateforme/pJ.png", #8 bloc Jump
          "image/plateforme/pX.png", #9 bloc Mouvement
          "image/plateforme/signExit.png", #10 bloc pancarte fin du jeu
        #   "image/plateforme/",
        ]

#----- COULEURS
noir = (0,0,0)
blanc = (255,255,255)

grisF = (22,22,22)
gris = (70,70,70)
grisClair = (200,200,200)

rouge = (200,0,0)
orange = (255,100,50)
bleu = (85,180,205)
vert = (80,230,70)
jaune = (235,255,55)



'''-------------------------------------------------------------------------'''
'''--------------------------SETTING MENU ----------------------------------'''
'''----------------------ET EDITEUR DE NIVEAU ------------------------------'''

#------importation des images
imageBackgroundIntro = 'image/menu/menu_principale.png'
imageBackgroundNiveau ='image/menu/menu.png'
imageGrille = 'image/editeur_niveau/grille.png'

imageDecors = ['image/editeur_niveau/background1_600px.png', #0
      "image/editeur_niveau/background2_600px.png", #1
      "image/editeur_niveau/background3_600px.png", #2
      "image/editeur_niveau/background4_600px.png", #2
      "image/editeur_niveau/background5_600px.png" #2
      ]
imageCroixReinitialiser = 'image/editeur_niveau/croixRouge.png'

imageGameOver = 'image/game_over/game_over2.png'

#----- Nom des images des blocs
imageBlocNormalMilieu = 'image/editeur_niveau/M_bloc.png'
imageBlocNormalDroit = 'image/editeur_niveau/R_bloc.png'
imageBlocNormalGauche = 'image/editeur_niveau/L_bloc.png'
imageBlocNormalDroitTerre = 'image/editeur_niveau/RT_bloc.png'
imageBlocNormalGaucheTerre = 'image/editeur_niveau/LT_bloc.png'
imageBlocNormalMilieuTerre = 'image/editeur_niveau/P_bloc.png'

imageBlocJump = 'image/editeur_niveau/Jump_bloc.png'
imageBlocWallJump = 'image/editeur_niveau/WallJump_bloc.png'
imageBlocMouvement = 'image/editeur_niveau/Mouvement_bloc.png'

# ----- configuration des décors
nomDecors = ['Plaine', 'Montagne', 'Brouillard', 'Nuage', 'Espace']



#----- Code pour coder les fichiers niveaux
codeVide = '0'
codeBlocNormal = 'M'
codeBlocJump = 'J'
codeBlocWallJump = 'W'
codeBlocMouvement = 'X'


#------Configuration du niveau
nombreCaseAxeOrdonnee = 10+1#on ajoute une ligne pour pouvoir mettre les effets( c'est a dire que c'est une ligne pour eviter les erreurs)
nombreCaseAxeAbscisse = 1000
nombreFenetreMax = nombreCaseAxeAbscisse/20
nombreFenetreMin =1

#-------Dimensions des blocs
blocW = 270
blocH = 100
dimensionImageNiveau = (blocW, blocH)
sizeBlocGrille = 30

#-----liste
listePointOrigineGrilleX = [[65,100],[363,100],[665,100],[65,300],[363,300],[665,300]]


#----- quelque couleurs des elements de l'éditeur de niveau
couleurFenetre = gris
couleurTexteAvertissement = blanc
couleurSurfaceAvertissement = noir
couleurFondBlockSelect = grisClair
couleurLigneSousSurfaceHaut = gris
couleurNumeroFenetreEdition = blanc

#----- TAILLE POLICE D'ECRITURE
taillePolice_titre = 24
taillePolice_normal = 20
taillePolice_petit = 17

#----- TAILLE DES SURFACES
sizeSurfaceGauche = (300,500)
sizeSurfaceHaut = (1000,50)
sizeSurfaceEdition = (600,300)
sizeParent4Blocs = (240,50)
sizeSurfaceBloc = (50,50)
sizeSurfaceMessageAvertissement = (480,90)


#----- TAILLE DES BOUTONS
sizeBoutonRetour = (200,50)
sizeBoutonDecors = (200,40)
sizeBoutonTesterNiveau = (240,30)

#------ POSITIONS
positionFenetreEdition = (350,125)
positionBoutonDecors = (50,110)

positionBoutonTesterNiveau = (530,450)
