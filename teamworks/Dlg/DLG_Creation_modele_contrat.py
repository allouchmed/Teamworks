#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#-----------------------------------------------------------
# Auteur:        Ivan LUCAS
# Copyright:    (c) 2008-09 Ivan LUCAS
# Licence:      Licence GNU GPL
#-----------------------------------------------------------

import Chemins
from Utils.UTILS_Traduction import _
import wx
from Ctrl import CTRL_Bouton_image
import GestionDB
import FonctionsPerso

from Ctrl.CTRL_Creation_modele_contrat_p1 import Page as Page1
from Ctrl.CTRL_Creation_modele_contrat_p2 import Page as Page2
from Ctrl.CTRL_Creation_modele_contrat_p3 import Page as Page3


class Dialog(wx.Dialog):
    def __init__(self, parent, title="", IDmodele=0):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX)
        self.parent = parent
        self.listePages = ("Page1", "Page2", "Page3")
        
        self.panel_base = wx.Panel(self, -1)
        self.static_line = wx.StaticLine(self.panel_base, -1)
        self.bouton_aide = CTRL_Bouton_image.CTRL(self.panel_base, texte=_(u"Aide"), cheminImage=Chemins.GetStaticPath("Images/32x32/Aide.png"))
        self.bouton_retour = wx.BitmapButton(self.panel_base, -1, wx.Bitmap(Chemins.GetStaticPath("Images/BoutonsImages/Retour_L72.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_suite = wx.BitmapButton(self.panel_base, -1, wx.Bitmap(Chemins.GetStaticPath("Images/BoutonsImages/Suite_L72.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_annuler = CTRL_Bouton_image.CTRL(self.panel_base, texte=_(u"Annuler"), cheminImage=Chemins.GetStaticPath("Images/32x32/Annuler.png"))
        self.__set_properties()
        self.__do_layout()
                
        self.Bind(wx.EVT_BUTTON, self.Onbouton_aide, self.bouton_aide)
        self.Bind(wx.EVT_BUTTON, self.Onbouton_retour, self.bouton_retour)
        self.Bind(wx.EVT_BUTTON, self.Onbouton_suite, self.bouton_suite)
        self.Bind(wx.EVT_BUTTON, self.Onbouton_annuler, self.bouton_annuler)

        self.bouton_retour.Enable(False)
        self.nbrePages = len(self.listePages)    
        self.pageVisible = 1
                
        # Initialisation de la liste de r�cup�ration des donn�es
        self.dictModeles = {
                                            "IDmodele" : IDmodele,
                                            "IDclassification" : None,
                                            "IDtype" : None,
                                            "nom" : "",
                                            "description" : "",
                                    }
                                    
        self.dictChamps = {} 
        
        if IDmodele != 0 : self.Importation(IDmodele)
        
        # Cr�ation des pages
        self.Creation_Pages()
        
    def Importation(self, IDmodele=0):
        # R�cup�ration des donn�es
        DB = GestionDB.DB()
        
        # Importe les donn�es MODELES
        req = "SELECT nom, description, IDclassification, IDtype FROM contrats_modeles WHERE IDmodele=%d ;" % IDmodele
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()[0]
        self.dictModeles["nom"] = listeDonnees[0]
        self.dictModeles["description"] = listeDonnees[1]        
        self.dictModeles["IDclassification"] = listeDonnees[2]
        self.dictModeles["IDtype"] = listeDonnees[3]
        
        # Importe les donn�es CHAMPS
        req = "SELECT IDchamp, valeur FROM contrats_valchamps WHERE (IDmodele=%d AND type='modele')  ;" % IDmodele
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()

        for item in listeDonnees :
            self.dictChamps[item[0]] = item[1]

        DB.Close()

    def Creation_Pages(self):
        """ Creation des pages """
        for numPage in range(1, self.nbrePages+1) :
            exec( "self.page" + str(numPage) + " = " + self.listePages[numPage-1] + "(self.panel_base)" )
            exec( "self.sizer_pages.Add(self.page" + str(numPage) + ", 1, wx.EXPAND, 0)" )
            self.sizer_pages.Layout()
            exec( "self.page" + str(numPage) + ".Show(False)" )
        self.page1.Show(True)
        self.sizer_pages.Layout()

    def __set_properties(self):
        self.SetTitle(_(u"Cr�ation d'un mod�le de contrat"))
        if 'phoenix' in wx.PlatformInfo:
            _icon = wx.Icon()
        else :
            _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Logo.png"), wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.bouton_aide.SetToolTip(wx.ToolTip("Cliquez ici pour obtenir de l'aide"))
        self.bouton_retour.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour revenir � la page pr�c�dente")))
        self.bouton_suite.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour passer � l'�tape suivante")))
        self.bouton_annuler.SetToolTip(wx.ToolTip(_(u"Cliquez pour annuler la cr�ation du contrat")))
        self.SetMinSize((470, 500))

    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(rows=3, cols=1, vgap=0, hgap=0)
        grid_sizer_boutons = wx.FlexGridSizer(rows=1, cols=6, vgap=10, hgap=10)
        sizer_pages = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base.Add(sizer_pages, 1, wx.ALL|wx.EXPAND, 10)
        grid_sizer_base.Add(self.static_line, 0, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_boutons.Add(self.bouton_retour, 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_suite, 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_annuler, 0, wx.LEFT, 10)
        grid_sizer_boutons.AddGrowableCol(1)
        grid_sizer_base.Add(grid_sizer_boutons, 1, wx.ALL|wx.EXPAND, 10)
        self.panel_base.SetSizer(grid_sizer_base)
        grid_sizer_base.AddGrowableRow(0)
        grid_sizer_base.AddGrowableCol(0)
        sizer_base.Add(self.panel_base, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Centre()
        self.sizer_pages = sizer_pages

    def Onbouton_aide(self, event):
        from Utils import UTILS_Aide
        UTILS_Aide.Aide("Lesmodlesdecontrats")

    def Onbouton_retour(self, event):
        # rend invisible la page affich�e
        pageCible = eval("self.page"+str(self.pageVisible))
        pageCible.Show(False)
        # Fait appara�tre nouvelle page
        self.pageVisible -= 1
        pageCible = eval("self.page"+str(self.pageVisible))
        pageCible.Show(True)
        self.sizer_pages.Layout()
        # Si on quitte la derni�re page, on active le bouton Suivant
        if self.pageVisible == self.nbrePages-1 :
            self.bouton_suite.Enable(True)
            self.bouton_suite.SetBitmapLabel(wx.Bitmap(Chemins.GetStaticPath("Images/BoutonsImages/Suite_L72.png"), wx.BITMAP_TYPE_ANY))
        # Si on revient � la premi�re page, on d�sactive le bouton Retour
        if self.pageVisible == 1 :
            self.bouton_retour.Enable(False)

    def Onbouton_suite(self, event):
        # V�rifie que les donn�es de la page en cours sont valides
        validation = self.ValidationPages()
        if validation == False : return
        # Si on est d�j� sur la derni�re page : on termine
        if self.pageVisible == self.nbrePages :
            self.Terminer()
            return
        # Rend invisible la page affich�e
        pageCible = eval("self.page"+str(self.pageVisible))
        pageCible.Show(False)
        # Fait appara�tre nouvelle page
        self.pageVisible += 1
        pageCible = eval("self.page"+str(self.pageVisible))
        pageCible.Show(True)
        self.sizer_pages.Layout()
        # Si on arrive � la derni�re page, on d�sactive le bouton Suivant
        if self.pageVisible == self.nbrePages :
            self.bouton_suite.SetBitmapLabel(wx.Bitmap(Chemins.GetStaticPath("Images/BoutonsImages/Valider_L72.png"), wx.BITMAP_TYPE_ANY))
        # Si on quitte la premi�re page, on active le bouton Retour
        if self.pageVisible > 1 :
            self.bouton_retour.Enable(True)
            
    def Onbouton_annuler(self, event):
        self.EndModal(wx.ID_CANCEL)
        
    def ValidationPages(self) :
        """ Validation des donn�es avant changement de pages """
        validation = getattr(self, "page%s" % self.pageVisible).Validation()
        return validation
    
    def Terminer(self):
        self.EndModal(wx.ID_OK)

        
if __name__ == "__main__":
    app = wx.App(0)
    dlg = Dialog(None, "", IDmodele=4)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
