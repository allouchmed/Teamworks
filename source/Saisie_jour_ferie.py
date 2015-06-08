#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#-----------------------------------------------------------
# Auteur:        Ivan LUCAS
# Copyright:    (c) 2008-09 Ivan LUCAS
# Licence:      Licence GNU GPL
#-----------------------------------------------------------

import wx
import GestionDB
import datetime
import FonctionsPerso


class MyFrame(wx.Frame):
    def __init__(self, parent, title="" , IDferie=0, type=""):
        wx.Frame.__init__(self, parent, -1, title=title, style=wx.DEFAULT_FRAME_STYLE)
        self.MakeModal(True)
        
        self.typeJour = type
        
        self.panel_base = wx.Panel(self, -1)
        self.staticBox_staticbox = wx.StaticBox(self.panel_base, -1, "")
        self.label_nom = wx.StaticText(self.panel_base, -1, "Nom :")
        self.text_ctrl_nom = wx.TextCtrl(self.panel_base, -1, "")
        self.label_jour_fixe = wx.StaticText(self.panel_base, -1, "Jour :")
        choices=[]
        for x in range(1, 32) : choices.append(str(x))
        self.choice_jour_fixe = wx.Choice(self.panel_base, -1, choices=choices)
        self.label_mois_fixe = wx.StaticText(self.panel_base, -1, "Mois :")
        self.choice_mois_fixe = wx.Choice(self.panel_base, -1, choices=["Janvier", u"F�vrier", "Mars", "Avril", "Mai", "Juin", "Juillet", u"Ao�t", "Septembre", "Octobre", "Novembre", u"D�cembre"])
        self.label_date_variable = wx.StaticText(self.panel_base, -1, "Date :")
        self.datepicker_date_variable = wx.DatePickerCtrl(self.panel_base, -1, style=wx.DP_DROPDOWN)
        
        self.bouton_aide = wx.BitmapButton(self.panel_base, -1, wx.Bitmap("Images/BoutonsImages/Aide_L72.png", wx.BITMAP_TYPE_ANY))
        self.bouton_ok = wx.BitmapButton(self.panel_base, -1, wx.Bitmap("Images/BoutonsImages/Ok_L72.png", wx.BITMAP_TYPE_ANY))
        self.bouton_annuler = wx.BitmapButton(self.panel_base, -1, wx.Bitmap("Images/BoutonsImages/Annuler_L72.png", wx.BITMAP_TYPE_ANY))
        
        self.IDferie = IDferie
        if IDferie != 0 : 
            self.Importation()

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnBoutonAide, self.bouton_aide)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonOk, self.bouton_ok)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAnnuler, self.bouton_annuler)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def __set_properties(self):
        self.SetTitle(u"Saisie d'un jour f�ri�")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("Images/16x16/Logo.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.choice_jour_fixe.SetMinSize((50, -1))
        self.choice_mois_fixe.SetMinSize((130, 21))
        self.bouton_aide.SetToolTipString("Cliquez ici pour obtenir de l'aide")
        self.bouton_aide.SetSize(self.bouton_aide.GetBestSize())
        self.bouton_ok.SetToolTipString("Cliquez ici pour valider")
        self.bouton_ok.SetSize(self.bouton_ok.GetBestSize())
        self.bouton_annuler.SetToolTipString("Cliquez ici pour annuler la saisie")
        self.bouton_annuler.SetSize(self.bouton_annuler.GetBestSize())

    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        sizer_base_2 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(rows=2, cols=1, vgap=0, hgap=0)
        grid_sizer_boutons = wx.FlexGridSizer(rows=1, cols=4, vgap=10, hgap=10)
        staticBox = wx.StaticBoxSizer(self.staticBox_staticbox, wx.VERTICAL)
        grid_sizer_staticBox = wx.FlexGridSizer(rows=3, cols=1, vgap=10, hgap=10)
        grid_sizer_variable = wx.FlexGridSizer(rows=1, cols=2, vgap=5, hgap=5)
        grid_sizer_fixe = wx.FlexGridSizer(rows=1, cols=5, vgap=5, hgap=5)
        grid_sizer_nom = wx.FlexGridSizer(rows=1, cols=2, vgap=5, hgap=5)
        grid_sizer_nom.Add(self.label_nom, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_nom.Add(self.text_ctrl_nom, 0, wx.EXPAND, 0)
        grid_sizer_nom.AddGrowableCol(1)
        grid_sizer_staticBox.Add(grid_sizer_nom, 1, wx.EXPAND, 0)
        grid_sizer_fixe.Add(self.label_jour_fixe, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_fixe.Add(self.choice_jour_fixe, 0, wx.RIGHT, 10)
        grid_sizer_fixe.Add(self.label_mois_fixe, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_fixe.Add(self.choice_mois_fixe, 0, wx.EXPAND, 0)
        grid_sizer_fixe.AddGrowableCol(4)
        grid_sizer_staticBox.Add(grid_sizer_fixe, 1, wx.EXPAND, 0)
        grid_sizer_variable.Add(self.label_date_variable, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_variable.Add(self.datepicker_date_variable, 0, 0, 0)
        grid_sizer_staticBox.Add(grid_sizer_variable, 1, wx.EXPAND, 0)
        grid_sizer_staticBox.AddGrowableCol(0)
        staticBox.Add(grid_sizer_staticBox, 1, wx.ALL|wx.EXPAND, 10)
        grid_sizer_base.Add(staticBox, 1, wx.ALL|wx.EXPAND, 10)
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.Add((20, 20), 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_ok, 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_annuler, 0, 0, 0)
        grid_sizer_boutons.AddGrowableCol(1)
        grid_sizer_base.Add(grid_sizer_boutons, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        sizer_base_2.Add(grid_sizer_base, 1, wx.EXPAND, 0)
        self.panel_base.SetSizer(sizer_base_2)
        sizer_base.Add(self.panel_base, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_base)
        
        # Affiche en fonction du type de de jour f�ri�
        if self.typeJour == "fixe" :
            self.label_date_variable.Show(False)
            self.datepicker_date_variable.Show(False)
        else:
            self.label_jour_fixe.Show(False)
            self.choice_jour_fixe.Show(False)
            self.label_mois_fixe.Show(False)
            self.choice_mois_fixe.Show(False)
        
        sizer_base.Fit(self)
        self.Layout()
        self.Centre()


    def Importation(self):
        DB = GestionDB.DB()
        req = "SELECT * FROM jours_feries WHERE IDferie=%d" % self.IDferie
        DB.ExecuterReq(req)
        donnees = DB.ResultatReq()[0]
        DB.Close()
        if len(donnees) == 0: return
        # R�cup�ration des donn�es
        type = donnees[1]
        nom = donnees[2]
        jour = donnees[3]
        mois = donnees[4]
        annee = donnees[5]
        
        # Place le nom
        self.text_ctrl_nom.SetValue(nom)
        # Place le jour et le mois si c'est un jour fixe
        if type == "fixe" :
            self.choice_jour_fixe.SetSelection(jour-1)
            self.choice_mois_fixe.SetSelection(mois-1)     
                
        # Place la date dans le cdatePicker si c'est une date variable
        else:
            date = wx.DateTime()
            date.Set(jour, mois-1, annee)
            self.datepicker_date_variable.SetValue(date)

    def Sauvegarde(self):
        """ Sauvegarde des donn�es dans la base de donn�es """
        
        # R�cup�ration ds valeurs saisies
        varNom = self.text_ctrl_nom.GetValue()
        if self.typeJour == "fixe" :
            varJour = self.choice_jour_fixe.GetSelection()+1
            varMois = self.choice_mois_fixe.GetSelection()+1
            varAnnee = 0
        else:
            date_tmp = self.datepicker_date_variable.GetValue()
            varJour = date_tmp.GetDay()
            varMois = date_tmp.GetMonth()+1
            varAnnee = date_tmp.GetYear()

        DB = GestionDB.DB()
        # Cr�ation de la liste des donn�es
        listeDonnees = [    ("type",   self.typeJour),  
                                    ("nom",   varNom),
                                    ("jour",   varJour),
                                    ("mois",   varMois),
                                    ("annee",    varAnnee), ]
        if self.IDferie == 0:
            # Enregistrement d'une nouvelle valeur
            newID = DB.ReqInsert("jours_feries", listeDonnees)
            ID = newID
        else:
            # Modification de la valeur
            DB.ReqMAJ("jours_feries", listeDonnees, "IDferie", self.IDferie)
            ID = self.IDferie
        DB.Commit()
        DB.Close()
        return ID

    def OnClose(self, event):
        self.MakeModal(False)
        FonctionsPerso.SetModalFrameParente(self)
        event.Skip()
        
    def OnBoutonAide(self, event):
        FonctionsPerso.Aide(39)

    def OnBoutonAnnuler(self, event):
        self.MakeModal(False)
        FonctionsPerso.SetModalFrameParente(self)
        self.Destroy()

    def OnBoutonOk(self, event):
        """ Validation des donn�es saisies """
        
        varNom = self.text_ctrl_nom.GetValue()
        if varNom == "" :
            dlg = wx.MessageDialog(self, u"Vous devez saisir un nom pour ce jour f�ri�. Par exemple : 'Lundi de P�ques'...", "Erreur", wx.OK)  
            dlg.ShowModal()
            dlg.Destroy()
            self.text_ctrl_nom.SetFocus()
            return
        
        if self.typeJour == "fixe" :
            varJour = self.choice_jour_fixe.GetSelection()
            if varJour == -1 or varJour == None :
                dlg = wx.MessageDialog(self, u"Vous devez s�lectionner un jour pour ce jour f�ri� !", "Erreur", wx.OK)  
                dlg.ShowModal()
                dlg.Destroy()
                self.choice_jour_fixe.SetFocus()
                return
            varMois = self.choice_mois_fixe.GetSelection()
            if varMois == -1 or varMois == None :
                dlg = wx.MessageDialog(self, u"Vous devez s�lectionner un mois pour ce jour f�ri� !", "Erreur", wx.OK)  
                dlg.ShowModal()
                dlg.Destroy()
                self.choice_mois_fixe.SetFocus()
                return

        # Sauvegarde
        self.Sauvegarde()
        
        # MAJ du listCtrl des valeurs de points
        if FonctionsPerso.FrameOuverte("Config_jours_feries_" + self.typeJour) != None :
            self.GetParent().MAJ_ListCtrl()

        # Fermeture
        self.MakeModal(False)
        FonctionsPerso.SetModalFrameParente(self)
        self.Destroy()

    
    
if __name__ == "__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, "", IDferie=1, type="fixe")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
