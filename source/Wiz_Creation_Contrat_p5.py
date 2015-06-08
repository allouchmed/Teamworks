#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#-----------------------------------------------------------
# Auteur:        Ivan LUCAS
# Copyright:    (c) 2008-09 Ivan LUCAS
# Licence:      Licence GNU GPL
#-----------------------------------------------------------

import wx
import  wx.lib.scrolledpanel as scrolled

class PanelDefilant(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        self.Creation_champs()
    
    def Creation_champs(self):       
        # R�cup�ration des donn�es
        self.dicoChampsTous = self.GetGrandParent().GetParent().page4.listCtrl_champs.dictChamps
        self.selections = self.GetGrandParent().GetParent().page4.listCtrl_champs.selections
        self.dicoChamps = {}
        for ID, valeurs in self.dicoChampsTous.iteritems() :
            if ID in self.selections :
                self.dicoChamps[ID] = valeurs
                
        # Modification du texte d'intro du panel
        if len(self.dicoChamps) == 0 :
            self.GetParent().label_intro.SetLabel(u"Vous n'avez aucun champ � remplir. Cliquez sur 'Suite'...")
        else:
            self.GetParent().label_intro.SetLabel(u"Vous pouvez maintenant remplir vos champs personnalis�s :")
        
        # Cr�ation des champs dans l'interface
        grid_sizer = wx.FlexGridSizer(rows=4, cols=1, vgap=10, hgap=10)
        
        for ID, valeurs in self.dicoChamps.iteritems() : 
            nom = "champ" + str(ID)
            label = valeurs[1]
            infoBulle = valeurs[2]
            motCle = valeurs[3]
            valeur = valeurs[4]
            exemple = valeurs[5]
            
            # Importation de la valeur si le contrat est en modification
            d = self.GetGrandParent().GetParent().dictChamps
            if ID in d.keys() : valeur = d[ID]
            
            # TextCtrl pour r�ponse
            self.sizer_champs = wx.StaticBox(self, -1, label)
            sizer_champ = wx.StaticBoxSizer(self.sizer_champs, wx.VERTICAL)
            exec( "self.text_" + nom + " = wx.TextCtrl(self, -1, valeur)" )
            exec( "self.text_" + nom + ".SetToolTipString(infoBulle)")
            exec( "sizer_champ.Add(self.text_" + nom + ", 0, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 0)")
            
            # Exemple :
            if exemple != "" :
                txtExemple = "Ex. : " + exemple[:60]
                exec( "self.label_" + nom + "EX = wx.StaticText(self, -1, txtExemple)")
                exec( "self.label_" + nom + "EX.SetFont(wx.Font(7, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ''))")
                exec( "self.label_" + nom + "EX.SetForegroundColour((120, 120, 120))")
                exec( "sizer_champ.Add(self.label_" + nom + "EX, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)")
            
            grid_sizer.Add(sizer_champ, 1, wx.RIGHT|wx.EXPAND, 10)

        grid_sizer.AddGrowableCol(0)
        self.SetSizer(grid_sizer)
        
        # Initialisation des barres de d�filement
        self.SetupScrolling()
        
        
class Page(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.label_titre = wx.StaticText(self, -1, u"4. Remplissage des champs personnalis�s")
        self.label_intro = wx.StaticText(self, -1, u"Vous pouvez maintenant remplir vos champs personnalis�s :")
        self.panelDefilant = wx.Panel(self, -1)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.label_titre.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=3, cols=1, vgap=10, hgap=10)
        grid_sizer_base.Add(self.label_titre, 0, 0, 0)
        grid_sizer_base.Add(self.label_intro, 0, wx.LEFT, 20)
        sizer_pages = wx.BoxSizer(wx.VERTICAL)
        sizer_pages.Add(self.panelDefilant, 1, wx.LEFT|wx.EXPAND, 20)
        grid_sizer_base.Add(sizer_pages, 1, wx.LEFT|wx.EXPAND, 20)
        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        grid_sizer_base.AddGrowableRow(2)
        grid_sizer_base.AddGrowableCol(0)
        self.sizer_pages = sizer_pages

    def MAJ_panelDefilant(self):
        # Destruction du panel actuel
        self.panelDefilant.Destroy()
        # Recontruction avec les nouveaux contr�les
        self.panelDefilant = PanelDefilant(self)
        self.sizer_pages.Add(self.panelDefilant, 1, wx.LEFT|wx.EXPAND, 20)
        self.sizer_pages.Layout()


    def Validation(self):
        
        # V�rifie que les champs ont �t� remplis
        listeInvalides = []
        dictChamps = {}
        for ID, valeurs in self.panelDefilant.dicoChamps.iteritems() : 
            nom = "champ" + str(ID)
            label = valeurs[1]
            exec( "texte = self.panelDefilant.text_" + nom + ".GetValue()" )
                        
            # Crit�res de validation
            if texte == "" :
                listeInvalides.append(label)
            else:
                # M�morisation pour enr. base de donn�es (cf plus bas)
                dictChamps[ID] = texte

        if len(listeInvalides) == 1 :
            txtMessage = u"Vous n'avez pas rempli le champ suivant : '" + listeInvalides[0]
            txtMessage += u"'\n\nSouhaitez-vous continuer quand m�me ?"
            dlg = wx.MessageDialog(self, txtMessage, u"Demande de confirmation", wx.ICON_QUESTION | wx.YES_NO | wx.NO_DEFAULT)
            if dlg.ShowModal() == wx.ID_NO :
                dlg.Destroy() 
                return False
                    
        if len(listeInvalides) > 1 :
            txtMessage = u"Vous n'avez pas rempli les champs suivants : \n\n"
            for item in listeInvalides :
                txtMessage += "      - " + item + "\n"
            txtMessage += u"\nSouhaitez-vous continuer quand m�me ?"
            dlg = wx.MessageDialog(self, txtMessage, u"Demande de confirmation", wx.ICON_QUESTION | wx.YES_NO | wx.NO_DEFAULT)
            if dlg.ShowModal() == wx.ID_NO :
                dlg.Destroy() 
                return False
        
        # M�morisation des donn�es pour l'enregistrement dans la base de donn�es
        self.GetGrandParent().dictChamps = dictChamps
            
        return True