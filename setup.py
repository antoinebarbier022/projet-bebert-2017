"""Fichier d'installation de notre script salut.py."""
import os
import cx_Freeze
#
os.environ['TCL_LIBRARY'] = "C:\Python 3.6\Tcl\Tcl8.6"
os.environ['TK_LIBRARY'] = "C:\Python 3.6\Tcl\Tk8.6"

executables = [cx_Freeze.Executable("main.py")]
# On appelle la fonction setup
cx_Freeze.setup(
    name = "Bébert's Aventure",
    version = "0.1",
    options = {"build_exe": {"packages": ["pygame"],
                                          "include_files": ["font\OCRAEXT.TTF",
                                                             "image\Background\i1.png",
                                                             "image\Background\i2.png",
                                                             "image\Background\i3.png",
                                                             "image\Bebert\BebertCours1.png",
                                                             "image\Bebert\BebertCours2.png",
                                                             "image\Bebert\BebertDebout.png",
                                                             "image\Bebert\BebertDroite.png",
                                                             "image\Bebert\BebertJump.png",
                                                             "image\editeur_niveau\Jump_bloc.png",
                                                             "image\editeur_niveau\L_bloc.png",
                                                             "image\editeur_niveau\LT_bloc.png",
                                                             "image\editeur_niveau\M_bloc.png",
                                                             "image\editeur_niveau\Mouvement_bloc.png",
                                                             "image\editeur_niveau\P_bloc.png",
                                                             "image\editeur_niveau\R_bloc.png",
                                                             "image\editeur_niveau\RT_bloc.png",
                                                             "image\editeur_niveau\WallJump_bloc.png",
                                                             "image\editeur_niveau\Background1_600px.png",
                                                             "image\editeur_niveau\Background2_600px.png",
                                                             "image\editeur_niveau\Background3_600px.png",
                                                             "image\editeur_niveau\croixRouge.png",
                                                             "image\editeur_niveau\grille.png",
                                                             "image\game_over\game_over.png",
                                                             "image\menu\menu.png",
                                                             "image\menu\menu_principale.png",
                                                             "image\plateforme\pJ.png",
                                                             "image\plateforme\pLR.png",
                                                             "image\plateforme\pLRF.png",
                                                             "image\plateforme\pM.png",
                                                             "image\plateforme\pMF.png",
                                                             "image\plateforme\pRR.png",
                                                             "image\plateforme\pRRF.png",
                                                             "image\plateforme\pW.png",
                                                             "image\plateforme\pWJ.png",
                                                             "image\plateforme\pX.png",
                                                             "image\plateforme\signExit.png",
                                                             "music\Atmosphere.ogg",
                                                             "music\main_music.ogg",
                                                             "niveau\l1.txt",
                                                             "niveau\l2.txt",
                                                             "niveau\l3.txt",
                                                             "niveau\l4.txt",
                                                             "niveau\l5.txt",
                                                             "niveau\lvlPerso.txt",
                                                             "settings.py"]}},


    description = "This truly is the only game you need",
    executables = executables
)
