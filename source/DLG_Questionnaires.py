#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Teamworks
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-11 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------

import wx

import GestionDB
import CTRL_Bandeau
import CTRL_Questionnaire


class Dialog(wx.Dialog):
    def __init__(self, parent, type="individu"):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.THICK_FRAME)
        self.parent = parent      
        self.type = type
        
        intro = u"Vous pouvez ici concevoir des questionnaires personnalis�s pour les fiches individuelles. Commencez par cr�er des cat�gories puis param�trez des questions bas�es sur les contr�les de votre choix en fonction des donn�es � saisir : texte, liste, entier, etc..."
        titre = u"Questionnaires"
        self.SetTitle(titre)
        self.ctrl_bandeau = CTRL_Bandeau.Bandeau(self, titre=titre, texte=intro, hauteurHtml=30, nomImage="Images/32x32/Questionnaire.png")
                
        # Questionnaire
        self.box_questionnaire_staticbox = wx.StaticBox(self, -1, u"Questionnaire")
        self.ctrl_questionnaire = CTRL_Questionnaire.CTRL(self, type=type, menuActif=True, afficherInvisibles=True)
        
        self.bouton_ajouter = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Ajouter.png", wx.BITMAP_TYPE_ANY))
        self.bouton_modifier = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Modifier.png", wx.BITMAP_TYPE_ANY))
        self.bouton_supprimer = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Supprimer.png", wx.BITMAP_TYPE_ANY))
        self.bouton_monter = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Fleche_haut.png", wx.BITMAP_TYPE_ANY))
        self.bouton_descendre = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/16x16/Fleche_bas.png", wx.BITMAP_TYPE_ANY))
        
        # Boutons
        self.bouton_aide = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/BoutonsImages/Aide_L72.png", wx.BITMAP_TYPE_ANY))
        self.bouton_fermer = wx.BitmapButton(self, -1, wx.Bitmap(u"Images/BoutonsImages/Fermer_L72.png", wx.BITMAP_TYPE_ANY))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnBoutonAjouter, self.bouton_ajouter)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonModifier, self.bouton_modifier)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonSupprimer, self.bouton_supprimer)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonMonter, self.bouton_monter)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonDescendre, self.bouton_descendre)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAide, self.bouton_aide)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonFermer, self.bouton_fermer)
        
        # Init contr�les
        self.ctrl_questionnaire.MAJ() 
        

    def __set_properties(self):
        self.bouton_ajouter.SetToolTipString(u"Cliquez ici pour ajouter une cat�gorie ou une question")
        self.bouton_modifier.SetToolTipString(u"Cliquez ici pour modifier la cat�gorie ou la question s�lectionn�e")
        self.bouton_supprimer.SetToolTipString(u"Cliquez ici pour supprimer la cat�gorie ou la question s�lectionn�e")
        self.bouton_monter.SetToolTipString(u"Cliquez ici pour monter la cat�gorie ou la question s�lectionn�e")
        self.bouton_descendre.SetToolTipString(u"Cliquez ici pour descendre la cat�gorie ou la question s�lectionn�e")
        self.bouton_aide.SetToolTipString(u"Cliquez ici pour obtenir de l'aide")
        self.bouton_fermer.SetToolTipString(u"Cliquez ici pour fermer")
        self.SetMinSize((690, 700))

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=4, cols=1, vgap=10, hgap=10)
        grid_sizer_boutons = wx.FlexGridSizer(rows=1, cols=4, vgap=10, hgap=10)
        box_questionnaire = wx.StaticBoxSizer(self.box_questionnaire_staticbox, wx.VERTICAL)
        grid_sizer_questionnaire = wx.FlexGridSizer(rows=1, cols=2, vgap=5, hgap=5)
        grid_sizer_boutons_questionnaire = wx.FlexGridSizer(rows=8, cols=1, vgap=5, hgap=5)
        grid_sizer_base.Add(self.ctrl_bandeau, 0, wx.EXPAND, 0)
        grid_sizer_questionnaire.Add(self.ctrl_questionnaire, 1, wx.EXPAND, 0)
        grid_sizer_boutons_questionnaire.Add(self.bouton_ajouter, 0, 0, 0)
        grid_sizer_boutons_questionnaire.Add(self.bouton_modifier, 0, 0, 0)
        grid_sizer_boutons_questionnaire.Add(self.bouton_supprimer, 0, 0, 0)
        grid_sizer_boutons_questionnaire.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_boutons_questionnaire.Add(self.bouton_monter, 0, 0, 0)
        grid_sizer_boutons_questionnaire.Add(self.bouton_descendre, 0, 0, 0)
        grid_sizer_questionnaire.Add(grid_sizer_boutons_questionnaire, 1, wx.EXPAND, 0)
        grid_sizer_questionnaire.AddGrowableRow(0)
        grid_sizer_questionnaire.AddGrowableCol(0)
        box_questionnaire.Add(grid_sizer_questionnaire, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_base.Add(box_questionnaire, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_boutons.Add(self.bouton_fermer, 0, 0, 0)
        grid_sizer_boutons.AddGrowableCol(1)
        grid_sizer_base.Add(grid_sizer_boutons, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        grid_sizer_base.AddGrowableRow(1)
        grid_sizer_base.AddGrowableCol(0)
        self.Layout()
        self.CenterOnScreen() 

    def OnBoutonAjouter(self, event): 
        self.ctrl_questionnaire.Ajouter()

    def OnBoutonModifier(self, event): 
        self.ctrl_questionnaire.Modifier()

    def OnBoutonSupprimer(self, event):
        self.ctrl_questionnaire.Supprimer()

    def OnBoutonMonter(self, event): 
        self.ctrl_questionnaire.Monter()

    def OnBoutonDescendre(self, event): 
        self.ctrl_questionnaire.Descendre()

    def OnBoutonAide(self, event): 
        print "Aide..."

    def OnBoutonFermer(self, event): 
        self.EndModal(wx.ID_OK)



if __name__ == u"__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    dialog_1 = Dialog(None, type="individu")
    app.SetTopWindow(dialog_1)
    dialog_1.ShowModal()
    app.MainLoop()
