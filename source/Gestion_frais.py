#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#-----------------------------------------------------------
# Auteur:        Ivan LUCAS
# Copyright:    (c) 2008-09 Ivan LUCAS
# Licence:      Licence GNU GPL
#-----------------------------------------------------------

import wx
import FonctionsPerso
import os
import GestionDB
import PageFrais
import wx.lib.mixins.listctrl  as  listmix


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, name="frm_gestion_frais", style=wx.DEFAULT_FRAME_STYLE)
        self.MakeModal(True)
        self.parent = parent
        self.IDpersonne = None
        self.nomPersonne = None
        
        self.panel_base = wx.Panel(self, -1)
        self.label_intro = wx.StaticText(self.panel_base, -1, u"Veuillez s�lectionner une personne dans la liste pour afficher les d�placements et remboursements correspondants :")
        self.staticBox_selection = wx.StaticBox(self.panel_base, -1, u"S�lection")
        
        # Filtres d'affichage
        self.label_check_tous = wx.StaticText(self.panel_base, -1, u"Afficher toutes les personnes" )
        self.ctrl_check_tous = wx.RadioButton(self.panel_base, -1, "", style = wx.RB_GROUP )
        self.label_check_nonRembourses = wx.StaticText(self.panel_base, -1, u"Afficher uniquement les \npersonnes ayant au moins un \nd�placement non rembours�" )
        self.ctrl_check_nonRembourses = wx.RadioButton(self.panel_base, -1, "")
        self.ctrl_check_nonRembourses.SetValue(True)
        
        # ListCtrl Personnes
        self.ctrl_personnes = ListCtrl_personnes(self.panel_base)
        
        # Page Frais � importer
        self.panel_pageFrais = PageFrais.Panel(self.panel_base,  IDpersonne=self.IDpersonne)
        
        self.bouton_aide = wx.BitmapButton(self.panel_base, -1, wx.Bitmap("Images/BoutonsImages/Aide_L72.png", wx.BITMAP_TYPE_ANY))
        self.bouton_ok = wx.BitmapButton(self.panel_base, -1, wx.Bitmap("Images/BoutonsImages/Fermer_L72.png", wx.BITMAP_TYPE_ANY))

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAide, self.bouton_aide)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonOk, self.bouton_ok)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Bind(wx.EVT_RADIOBUTTON, self.OnCheckTous, self.ctrl_check_tous )
        self.Bind(wx.EVT_RADIOBUTTON, self.OnCheckNonRembourses, self.ctrl_check_nonRembourses )
        
        # Si aucune personne n'a de d�placements � rembourser, on affiche tout le monde
        if len(self.ctrl_personnes.donnees) == 0 :
            self.ctrl_check_tous.SetValue(True)
            self.ctrl_personnes.MAJListeCtrl()
        
        
    def __set_properties(self):
        self.SetTitle(u"Gestion des frais de d�placement")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("Images/16x16/Logo.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.bouton_aide.SetToolTipString("Cliquez ici pour obtenir de l'aide")
        self.bouton_aide.SetSize(self.bouton_aide.GetBestSize())
        self.bouton_ok.SetToolTipString("Cliquez ici pour fermer")
        self.bouton_ok.SetSize(self.bouton_ok.GetBestSize())
        self.SetMinSize((760, 600))

    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(rows=6, cols=1, vgap=0, hgap=0)
        grid_sizer_boutons = wx.FlexGridSizer(rows=1, cols=4, vgap=10, hgap=10)
        grid_sizer_base.Add(self.label_intro, 1, wx.LEFT|wx.TOP|wx.RIGHT|wx.EXPAND, 10)
        
        # Filtre
        grid_sizer_filtre = wx.FlexGridSizer(rows=2, cols=2, vgap=10, hgap=5)
        grid_sizer_filtre.Add(self.ctrl_check_tous, 1, 0, 0)
        grid_sizer_filtre.Add(self.label_check_tous, 1, 0, 0)
        grid_sizer_filtre.Add(self.ctrl_check_nonRembourses, 1, 0, 0)
        grid_sizer_filtre.Add(self.label_check_nonRembourses, 1, 0, 0)
        
        # StaticBox selection
        staticBox_selection = wx.StaticBoxSizer(self.staticBox_selection, wx.HORIZONTAL)
        staticBox_selection.Add(self.ctrl_personnes, 1, wx.ALL|wx.EXPAND, 5)
        staticBox_selection.Add(grid_sizer_filtre, 0, wx.ALL, 5)
        grid_sizer_base.Add(staticBox_selection, 1, wx.ALL|wx.EXPAND, 10)
        
        # Panel frais
        grid_sizer_base.Add(self.panel_pageFrais, 1, wx.EXPAND | wx.LEFT|wx.RIGHT|wx.TOP, 5)
        grid_sizer_base.Add((10, 10), 1, wx.EXPAND | wx.ALL, 0)
        
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_boutons.Add(self.bouton_ok, 0, 0, 0)
        grid_sizer_boutons.AddGrowableCol(1)
        
        grid_sizer_base.AddGrowableCol(0)
        grid_sizer_base.AddGrowableRow(1)
        grid_sizer_base.AddGrowableRow(2)
        
        grid_sizer_base.Add(grid_sizer_boutons, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        self.panel_base.SetSizer(grid_sizer_base)
        sizer_base.Add(self.panel_base, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Centre()       
    
    def OnCheckTous(self, event):
        self.ctrl_personnes.MAJListeCtrl()
        self.IDpersonne = None
        self.nomPersonne = None
        self.MAJlistes()
        
    def OnCheckNonRembourses(self, event):
        self.ctrl_personnes.MAJListeCtrl()
        self.IDpersonne = None
        self.nomPersonne = None
        self.MAJlistes()
        
    def MAJlistes(self):
        # MAJ du IDpersonne si demand�
        if self.IDpersonne != 0 :
            self.panel_pageFrais.IDpersonne = self.IDpersonne
            if self.IDpersonne == None : self.panel_pageFrais.staticBox_deplacements.SetLabel(u"D�placements")
            else : self.panel_pageFrais.staticBox_deplacements.SetLabel(u"D�placements de %s" % self.nomPersonne)
            self.panel_pageFrais.ctrl_deplacements.IDpersonne = self.IDpersonne
            if self.IDpersonne == None : self.panel_pageFrais.staticBox_remboursements.SetLabel(u"Remboursements")
            else : self.panel_pageFrais.staticBox_remboursements.SetLabel(u"Remboursements de %s" % self.nomPersonne)
            self.panel_pageFrais.ctrl_remboursements.IDpersonne = self.IDpersonne
        # MAJ des listCtrl
        self.panel_pageFrais.ctrl_deplacements.MAJListeCtrl()
        self.panel_pageFrais.ctrl_remboursements.MAJListeCtrl()

    def OnClose(self, event):
        self.MakeModal(False)
        event.Skip()
        
    def OnBoutonAide(self, event):
        FonctionsPerso.Aide(25)

    def OnBoutonOk(self, event):        
        # Fermeture
        self.MakeModal(False)
        self.Destroy()




# ----------- LISTCTRL PERSONNES  ---------------------------------------------------------------------------------------------------

class ListCtrl_personnes(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    def __init__(self, parent, IDpersonne=None):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_SINGLE_SEL|wx.LC_HRULES|wx.LC_VRULES)
        self.IDpersonne = 1
        self.parent = parent
        self.selection = (0, None)

        # Initialisation des images
        tailleIcones = 16
        self.il = wx.ImageList(tailleIcones, tailleIcones)
        self.imgTriAz= self.il.Add(wx.Bitmap("Images/16x16/Tri_az.png", wx.BITMAP_TYPE_PNG))
        self.imgTriZa= self.il.Add(wx.Bitmap("Images/16x16/Tri_za.png", wx.BITMAP_TYPE_PNG))
        self.imgOk = self.il.Add(wx.Bitmap("Images/16x16/Ok.png", wx.BITMAP_TYPE_PNG))
        self.imgPasOk = self.il.Add(wx.Bitmap("Images/16x16/Interdit.png", wx.BITMAP_TYPE_PNG))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        #adding some attributes (colourful background for each item rows)
        self.attr1 = wx.ListItemAttr()
        self.attr1.SetBackgroundColour("#EEF4FB") # Vert = #F0FBED
        
        # Remplissage
        self.Remplissage()
        
        #events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

    def Remplissage(self):
        
        # R�cup�ration des donn�es dans la base de donn�es
        self.Importation()
        
        # Cr�ation des colonnes
        self.nbreColonnes = 4
        self.InsertColumn(0, u"ID")
        self.SetColumnWidth(0, 0)
        self.InsertColumn(1, u"Nom et pr�nom")
        self.SetColumnWidth(1, 200)
        self.InsertColumn(2, u"D�plac. rembours�s")
        self.SetColumnWidth(2, 120)
        self.InsertColumn(3, u"D�plac. non rembours�s")
        self.SetColumnWidth(3, 150)

        #These two should probably be passed to init more cleanly
        #setting the numbers of items = number of elements in the dictionary
        self.itemDataMap = self.donnees
        self.itemIndexMap = self.donnees.keys()
        self.SetItemCount(self.nbreLignes)
        
        #mixins
##        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ColumnSorterMixin.__init__(self, self.nbreColonnes)

        #sort by genre (column 1), A->Z ascending order (1)
        self.SortListItems(1, 1)

    def OnItemSelected(self, event):
        if self.GetFirstSelected() == -1: return False
        index = self.GetFirstSelected()
        IDpersonne= int(self.getColumnText(index, 0))
        nomPersonne = self.getColumnText(index, 1)
        # MAJ de l'affichage
        self.GetGrandParent().IDpersonne = IDpersonne
        self.GetGrandParent().nomPersonne = nomPersonne
        self.GetGrandParent().MAJlistes()
        event.Skip()
    
    def Importation(self):
        dictDonnees = {}
        # R�cup�ration de la liste des personnes
        DB = GestionDB.DB()        
        req = """SELECT IDpersonne, nom, prenom FROM personnes ORDER BY nom, prenom; """
        DB.ExecuterReq(req)
        listePersonnes = DB.ResultatReq()
        DB.Close()
        
        for IDpersonne, nom, prenom in listePersonnes :
            dictDonnees[IDpersonne] = [IDpersonne, nom + " " + prenom, 0, 0, 0, 0] # Nbre_rembours�s, montant_rembours�s, nbre_non_rembours�s, montant_non_rembours�s
        
        # R�cup�ration des d�placements
        DB = GestionDB.DB()        
        req = """SELECT IDdeplacement, IDpersonne, distance, tarif_km, IDremboursement FROM deplacements; """
        DB.ExecuterReq(req)
        listeDeplacements = DB.ResultatReq()
        DB.Close()
        
        # Cr�ation de la liste de donn�es
        for IDdeplacement, IDpersonne, distance, tarif_km, IDremboursement in listeDeplacements :
            montant = float(distance) * float(tarif_km)
            
            if IDremboursement == 0 :
                dictDonnees[IDpersonne][4] = dictDonnees[IDpersonne][4] + 1
                dictDonnees[IDpersonne][5] = dictDonnees[IDpersonne][5] + montant
            else:
                dictDonnees[IDpersonne][2] = dictDonnees[IDpersonne][2] + 1
                dictDonnees[IDpersonne][3] = dictDonnees[IDpersonne][3] + montant

        self.donnees = {}
        index = 0
        for key,  valeurs in dictDonnees.iteritems() :
            IDpersonne = key
            nom = valeurs[1]
            nbreRembourses = valeurs[2]
            montantRembourses = valeurs[3]
            nbreNonRembourses = valeurs[4]
            montantNonRembourses = valeurs[5]
            if nbreRembourses == 0 : txtRembourses = ""
            else : txtRembourses = str(nbreRembourses) + u" (soit %.2f �) " % montantRembourses
            if nbreNonRembourses == 0 : txtNonRembourses = ""
            else : txtNonRembourses = str(nbreNonRembourses) + u" (soit %.2f �) " % montantNonRembourses
            
            if self.GetGrandParent().ctrl_check_nonRembourses.GetValue() == True :
                if nbreNonRembourses > 0 :
                    self.donnees[index] = (IDpersonne, nom, txtRembourses, txtNonRembourses)
                    index += 1
            else :
                self.donnees[index] = (IDpersonne, nom, txtRembourses, txtNonRembourses)
                index += 1
        
        self.nbreLignes = len(self.donnees)
            
    def MAJListeCtrl(self):
        self.ClearAll()
        self.Remplissage()
        listmix.ColumnSorterMixin.__init__(self, self.nbreColonnes)
           
        
    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    #---------------------------------------------------
    # These methods are callbacks for implementing the
    # "virtualness" of the list...

    def OnGetItemText(self, item, col):
        """ Affichage des valeurs dans chaque case du ListCtrl """
        index=self.itemIndexMap[item]
        valeur = unicode(self.itemDataMap[index][col])
        # Reformate une valeur date en version fran�aise
##        if col == 1 :
##            if valeur[4:5]=="-" and valeur[7:8]=="-":
##                valeur = str(valeur[8:10])+"/"+str(valeur[5:7])+"/"+str(valeur[0:4])
        return valeur

    def OnGetItemImage(self, item):
        """ Affichage des images en d�but de ligne """
        index=self.itemIndexMap[item]
        valeur =self.itemDataMap[index][0]
        return -1

    def OnGetItemAttr(self, item):
        """ Application d'une couleur de fond pour une ligne sur deux """
        # Cr�ation d'une ligne de couleur 1 ligne sur 2
        if item % 2 == 1:
            return self.attr1
        else:
            return None
       
    #-----------------------------------------------------------
    # Matt C, 2006/02/22
    # Here's a better SortItems() method --
    # the ColumnSorterMixin.__ColumnSorter() method already handles the ascending/descending,
    # and it knows to sort on another column if the chosen columns have the same value.

    def SortItems(self,sorter=cmp):
        items = list(self.itemDataMap.keys())
        items.sort(sorter)
        self.itemIndexMap = items
        # redraw the list
        self.Refresh()

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.imgTriAz, self.imgTriZa)

    
    
    
if __name__ == "__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    frame_1 = MyFrame(None)
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()