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
from Utils import UTILS_Adaptations
import GestionDB
import FonctionsPerso
from Dlg import DLG_Saisie_cat_presences
import six


class Panel(wx.Panel):
    def __init__(self, parent, ID=-1):
        wx.Panel.__init__(self, parent, ID, style=wx.TAB_TRAVERSAL)
        
        self.barreTitre = FonctionsPerso.BarreTitre(self,  _(u"Les cat�gories de pr�sence"), u"")
        texteIntro = _(u"Vous pouvez ici ajouter, modifier ou supprimer des cat�gories de pr�sence. Vous pouvez utiliser autant de\ncat�gories et sous-cat�gories que vous souhaitez. Exemples : 'R�union', 'Cong�s pay�s', 'Formation'...")
        self.label_introduction = FonctionsPerso.StaticWrapText(self, -1, texteIntro)

        self.treeSelection = 0
        self.treeCtrl_categories = TreeCtrlCategories(self, self.treeSelection)
        
        self.bouton_ajouter = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Ajouter.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_modifier = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Modifier.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_supprimer = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Supprimer.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_haut = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Fleche_haut.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_bas = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Fleche_bas.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_aide = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Aide.png"), wx.BITMAP_TYPE_ANY))
        if parent.GetName() != "treebook_configuration" :
            self.bouton_aide.Show(False)

##        self.label_conclusion = wx.StaticText(self, -1, "Remarques...")

        self.__set_properties()
        self.__do_layout()
        
        # Binds
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAjouter, self.bouton_ajouter)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonModifier, self.bouton_modifier)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonSupprimer, self.bouton_supprimer)
        self.Bind(wx.EVT_BUTTON, self.treeCtrl_categories.Menu_Haut, self.bouton_haut)
        self.Bind(wx.EVT_BUTTON, self.treeCtrl_categories.Menu_Bas, self.bouton_bas)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAide, self.bouton_aide)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
    def __set_properties(self):
        self.bouton_ajouter.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour cr�er une nouvelle cat�gorie de pr�sences")))
        self.bouton_ajouter.SetSize(self.bouton_ajouter.GetBestSize())
        self.bouton_modifier.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour modifier une cat�gorie de pr�sences")))
        self.bouton_modifier.SetSize(self.bouton_modifier.GetBestSize())
        self.bouton_supprimer.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour supprimer une cat�gorie de pr�sences")))
        self.bouton_supprimer.SetSize(self.bouton_supprimer.GetBestSize())
        self.bouton_haut.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour d�placer la cat�gorie s�lectionn�e vers le haut")))
        self.bouton_haut.SetSize(self.bouton_haut.GetBestSize())
        self.bouton_bas.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour d�placer la cat�gorie s�lectionn�e vers le bas")))
        self.bouton_bas.SetSize(self.bouton_bas.GetBestSize())
        self.bouton_aide.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour obtenir de l'aide")))

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=5, cols=1, vgap=10, hgap=10)
        grid_sizer_base2 = wx.FlexGridSizer(rows=1, cols=2, vgap=10, hgap=10)
        grid_sizer_boutons = wx.FlexGridSizer(rows=8, cols=1, vgap=5, hgap=10)
        grid_sizer_base.Add(self.barreTitre, 0, wx.EXPAND, 0)
        grid_sizer_base.Add(self.label_introduction, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        grid_sizer_base2.Add(self.treeCtrl_categories, 1, wx.EXPAND, 0)
        grid_sizer_boutons.Add(self.bouton_ajouter, 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_modifier, 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_supprimer, 0, 0, 0)
        grid_sizer_boutons.Add((15, 15), 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_haut, 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_bas, 0, 0, 0)
        grid_sizer_boutons.Add((5, 5), 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.AddGrowableRow(6)
        grid_sizer_base2.Add(grid_sizer_boutons, 1, wx.EXPAND, 0)
        grid_sizer_base2.AddGrowableRow(0)
        grid_sizer_base2.AddGrowableCol(0)
        grid_sizer_base.Add(grid_sizer_base2, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
##        grid_sizer_base.Add(self.label_conclusion, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        grid_sizer_base.AddGrowableRow(2)
        grid_sizer_base.AddGrowableCol(0)
        self.SetAutoLayout(True)
        self.grid_sizer_base = grid_sizer_base
        self.grid_sizer_base2 = grid_sizer_base2
        
    def OnSize(self, event) :
        self.treeCtrl_categories.Layout()
        self.grid_sizer_base.Layout()
        self.grid_sizer_base2.Layout()
        event.Skip()
        
    def OnBoutonAjouter(self, event):
        self.Ajouter()

    def Ajouter(self):
        """ Cr�er une nouvelle cat�gorie """
        dlg = DLG_Saisie_cat_presences.Dialog(self, -1, IDcat_parent=self.treeSelection)
        dlg.ShowModal()
        dlg.Destroy()

    def OnBoutonModifier(self, event):
        self.Modifier()

    def Modifier(self):
        """ Modification d'une cat�gorie """
        IDcategorie = self.treeSelection

        # V�rifie qu'un item a bien �t� s�lectionn�
        if IDcategorie == 0:
            dlg = wx.MessageDialog(self, _(u"Vous devez d'abord s�lectionner une cat�gorie � modifier dans la liste."), "Information", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # V�rifie que cette cat�gorie n'est pas attribu�e � une pr�sence
        DB = GestionDB.DB()
        req = "SELECT IDpresence FROM presences WHERE IDcategorie=%d" % IDcategorie
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()
        DB.Close()
        if len(listeDonnees) != 0 :
            dlg = wx.MessageDialog(self, _(u"Cette cat�gorie a d�j� �t� attribu�e � ") + str(len(listeDonnees)) + _(u" pr�sences.\nEtes-vous s�r de vouloir la modifier ?"), "Confirmation", wx.YES_NO|wx.NO_DEFAULT|wx.ICON_EXCLAMATION)
            reponse = dlg.ShowModal()
            if reponse == wx.ID_NO:
                dlg.Destroy()
                return
            else: dlg.Destroy()

        
        # V�rifie que cette cat�gorie n'est pas attribu�e � un mod�le de pr�sences
        DB = GestionDB.DB()
        req = "SELECT IDtache FROM modeles_taches WHERE IDcategorie=%d" % IDcategorie
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()
        DB.Close()
        if len(listeDonnees) != 0 :
            dlg = wx.MessageDialog(self, _(u"Cette cat�gorie a d�j� �t� attribu�e � ") + str(len(listeDonnees)) + _(u" mod�le(s) de pr�sences.\nEtes-vous s�r de vouloir la modifier ?"), "Confirmation", wx.YES_NO|wx.NO_DEFAULT|wx.ICON_EXCLAMATION)
            reponse = dlg.ShowModal()
            if reponse == wx.ID_NO:
                dlg.Destroy()
                return
            else: dlg.Destroy()
                
        dlg = DLG_Saisie_cat_presences.Dialog(self, -1, IDcategorie=IDcategorie)
        dlg.ShowModal()
        dlg.Destroy()

    def OnBoutonSupprimer(self, event):
        self.Supprimer()

    def Supprimer(self):
        """ Suppression d'une coordonn�e """
        IDcategorie = self.treeSelection

        # V�rifie qu'un item a bien �t� s�lectionn�
        if IDcategorie == 0:
            dlg = wx.MessageDialog(self, _(u"Vous devez d'abord s�lectionner une cat�gorie � supprimer dans la liste."), "Information", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return


        # V�rifie que cette cat�gorie n'a pas de sous-cat�gorie
        DB = GestionDB.DB()
        req = "SELECT IDcategorie FROM cat_presences WHERE IDcat_parent=%d" % IDcategorie
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()
        DB.Close()
        if len(listeDonnees) != 0 :
            dlg = wx.MessageDialog(self, _(u"Vous ne pouvez pas supprimer une cat�gorie sans en avoir supprim� au pr�alable toutes les sous-cat�gories."), "Information", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # V�rifie que cette cat�gorie n'est pas attribu�e � une pr�sence
        DB = GestionDB.DB()
        req = "SELECT IDpresence FROM presences WHERE IDcategorie=%d" % IDcategorie
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()
        DB.Close()
        if len(listeDonnees) != 0 :
            dlg = wx.MessageDialog(self, _(u"Vous avez d�j� enregistr� ") + str(len(listeDonnees)) + _(u" pr�sences avec cette cat�gorie. \nVous ne pouvez donc pas la supprimer."), "Information", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # V�rifie que cette cat�gorie n'est pas attribu�e � un mod�le de pr�sences
        DB = GestionDB.DB()
        req = "SELECT IDtache FROM modeles_taches WHERE IDcategorie=%d" % IDcategorie
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()
        DB.Close()
        if len(listeDonnees) != 0 :
            dlg = wx.MessageDialog(self, _(u"Vous avez d�j� cr�� ") + str(len(listeDonnees)) + _(u" mod�le(s) de planning avec cette cat�gorie. \nVous ne pouvez donc pas la supprimer."), "Information", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # Demande de confirmation
        NomCategorie = self.treeCtrl_categories.treeSelection[1]
        txtMessage = six.text_type((_(u"Voulez-vous vraiment supprimer cette cat�gorie ? \n\n> ") + NomCategorie))
        dlgConfirm = wx.MessageDialog(self, txtMessage, _(u"Confirmation de suppression"), wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)
        reponse = dlgConfirm.ShowModal()
        dlgConfirm.Destroy()
        if reponse == wx.ID_NO:
            return
        
        # Suppression de la cat�gorie
        self.DB = GestionDB.DB()
        self.DB.ReqDEL("cat_presences", "IDcategorie", IDcategorie)

        # Suppression des enfants de cette cat�gorie
        self.boucleSuppression(IDcategorie)
        
        # Fermeture de la DB
        self.DB.Close()


        # MAJ du TreeCTrl du panel CONFIG
        self.treeCtrl_categories.select2 = None
        self.treeCtrl_categories.treeSelection = (0, 0, 0)
        self.treeCtrl_categories.MAJtree()
        self.treeCtrl_categories.SetFocus()


    def boucleSuppression(self, IDcategorie):
        req = """
        SELECT IDcategorie, IDcat_parent
        FROM cat_presences
        WHERE cat_presences.IDcat_parent=%d;
        """ % IDcategorie
        self.DB.ExecuterReq(req)
        listeCategories = self.DB.ResultatReq()

        for categorie in listeCategories:
            self.DB.ReqDEL("cat_presences", "IDcategorie", categorie[0])
            self.boucleSuppression(categorie[0])
            
    def MAJpanel(self):
        self.treeCtrl_categories.MAJtree()

    def OnBoutonAide(self, event):
        from Utils import UTILS_Aide
        UTILS_Aide.Aide("Lescatgoriesdeprsences")



class TreeCtrlCategories(wx.TreeCtrl):
    def __init__(self, parent, treeSelection):
        wx.TreeCtrl.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize, style=wx.TR_DEFAULT_STYLE)
        # Autres styles possibles = wx.TR_HAS_BUTTONS|wx.TR_EDIT_LABELS| wx.TR_MULTIPLE|wx.TR_HIDE_ROOT
        self.parent = parent
        self.treeSelection = (0, 0, treeSelection)
        self.select2 = None

        if self.GetGrandParent().GetName() != "treebook_configuration" :
            self.Remplissage()

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnContextMenu)

    def FormateCouleur(self, texte):
        pos1 = texte.index(",")
        pos2 = texte.index(",", pos1+1)
        r = int(texte[1:pos1])
        v = int(texte[pos1+2:pos2])
        b = int(texte[pos2+2:-1])
        return (r, v, b)

    def CreationImage(self, tailleImages, r, v, b):
        """ Cr�ation des images pour le TreeCtrl """
        if 'phoenix' in wx.PlatformInfo:
            bmp = wx.Image(tailleImages[0], tailleImages[1], True)
            bmp.SetRGB((0, 0, 16, 16), 255, 255, 255)
            bmp.SetRGB((6, 4, 8, 8), r, v, b)
        else:
            bmp = wx.EmptyImage(tailleImages[0], tailleImages[1], True)
            bmp.SetRGBRect((0, 0, 16, 16), 255, 255, 255)
            bmp.SetRGBRect((6, 4, 8, 8), r, v, b)
        return bmp.ConvertToBitmap()

    def Remplissage(self):

        self.listeCategories = self.Importation()
        tailleImages = (16,16)
        il = wx.ImageList(tailleImages[0], tailleImages[1])
        if 'phoenix' in wx.PlatformInfo:
            self.imgRoot = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, tailleImages))
        else:
            self.imgRoot = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, tailleImages))
        for categorie in self.listeCategories:
            ID = categorie[0]
            couleur = self.FormateCouleur(categorie[4])
            r = couleur[0]
            v = couleur[1]
            b = couleur[2]
            exec("self.img" + str(ID) +  "= il.Add(self.CreationImage(tailleImages, " + str(r) + ", " + str(v) + ", " + str(b) + "))")

        self.SetImageList(il)
        self.il = il

        self.root = self.AddRoot(_(u"Cat�gories"))
        if 'phoenix' in wx.PlatformInfo:
            self.SetItemData(self.root, 0)
        else:
            self.SetPyData(self.root, 0)
        self.SetItemImage(self.root, self.imgRoot, wx.TreeItemIcon_Normal)

        self.nbreCategories = len(self.listeCategories)
        if self.nbreCategories == 0:
            return
        self.nbreBranches = 0
        self.Boucle(0, self.root)
        
        self.Expand(self.root)

    def Boucle(self, IDparent, itemParent):
        """ Boucle de remplissage du TreeCtrl """
        for item in self.listeCategories :
            if item[2] == IDparent:

                # Cr�ation de la branche
                newItem = self.AppendItem(itemParent, item[1])
                if 'phoenix' in wx.PlatformInfo:
                    self.SetItemData(newItem, item[0])
                else:
                    self.SetPyData(newItem, item[0])
                exec("self.SetItemImage(newItem, self.img" + str(item[0]) + ", wx.TreeItemIcon_Normal)")

                # S�lection de l'item s'il s�lectionn� est par d�faut
                if self.select2 != None:
                    if int(item[0]) == self.select2 :
                        self.EnsureVisible(newItem)
                        self.SelectItem(newItem)
                        self.select2 = None
                else:
                    if int(item[0]) == self.treeSelection[2] :
                        self.EnsureVisible(newItem)
                        self.SelectItem(newItem)
                    
                self.nbreBranches += 1

                # Recherche des branches enfants
                self.Boucle(item[0], newItem)

    def MAJtree(self):
        self.DeleteAllItems()
        self.Remplissage()

    def Importation(self):
        """ R�cup�ration de la liste des cat�gories dans la base """

        # Initialisation de la connexion avec la Base de donn�es
        DB = GestionDB.DB()
        req = "SELECT * FROM cat_presences ORDER BY IDcat_parent, ordre"
        DB.ExecuterReq(req)
        listeCategories = DB.ResultatReq()
        DB.Close()
        return listeCategories               
            

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        textItem = self.GetItemText(self.item)
        if 'phoenix' in wx.PlatformInfo:
            data = self.GetItemData(self.item)
        else:
            data = self.GetPyData(self.item)
        self.treeSelection = (self.item, textItem, data)
        self.parent.treeSelection = data
        event.Skip()


    def OnContextMenu(self, event):
        """Ouverture du menu contextuel """

        # Recherche et s�lection de l'item point� avec la souris
        item = self.FindTreeItem(event.GetPosition())
        if item == None:
            return
        self.SelectItem(item, True)
        
        # Cr�ation du menu contextuel
        menuPop = UTILS_Adaptations.Menu()

        # Item Ajouter
        item = wx.MenuItem(menuPop, 10, _(u"Ajouter"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Ajouter.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Menu_Ajouter, id=10)
        
        menuPop.AppendSeparator()

        # Item Modifier
        item = wx.MenuItem(menuPop, 20, _(u"Modifier"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Modifier.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Menu_Modifier, id=20)

        # Item Supprimer
        item = wx.MenuItem(menuPop, 30, _(u"Supprimer"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Supprimer.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Menu_Supprimer, id=30)

        menuPop.AppendSeparator()

        # Item Deplacer vers le haut
        item = wx.MenuItem(menuPop, 40, _(u"D�placer vers le haut"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Fleche_haut.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Menu_Haut, id=40)

        # Item D�placer vers le bas
        item = wx.MenuItem(menuPop, 50, _(u"D�placer vers le bas"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Fleche_bas.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Menu_Bas, id=50)
        
        self.PopupMenu(menuPop)
        menuPop.Destroy()

    def FindTreeItem(self, position):
        """ Permet de retrouver l'item point� dans le TreeCtrl """
        item, flags = self.HitTest(position)
        if item and flags & (wx.TREE_HITTEST_ONITEMLABEL |
                             wx.TREE_HITTEST_ONITEMICON):
            return item
        return None
    
    def Menu_Ajouter(self, event):
        self.parent.Ajouter()
        
    def Menu_Modifier(self, event):
        self.parent.Modifier()

    def Menu_Supprimer(self, event):
        self.parent.Supprimer()

    def Menu_Haut(self, event):
        
        if self.treeSelection[2] == 0:
            return
        
        # On recherche si c'est n'est pas le seul enfant
        itemParent = self.GetItemParent(self.treeSelection[0])
        IDitemParent = self.GetPyData(itemParent)
        nbreEnfants = self.GetChildrenCount(itemParent, False)
        if nbreEnfants < 2:
            dlg = wx.MessageDialog(self, _(u"Cet item est la seule dans sa cat�gorie. Vous ne pouvez donc pas le d�placer."), "Information", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # On le d�place vers le haut
        IDcategorie = self.GetPyData(self.treeSelection[0])        
        DB = GestionDB.DB()

        # R�cup�ration de l'ordre
        req = """
        SELECT IDcategorie, nom_categorie, ordre
        FROM cat_presences
        WHERE cat_presences.IDcat_parent=%d
        ORDER BY cat_presences.ordre DESC;
        """ % IDitemParent
        DB.ExecuterReq(req)
        listeCategories = DB.ResultatReq()

        ordreTemp = None
        for categorie in listeCategories :

            # Si c'est d�j� le premier, on laisse tomber
            if categorie[0] == IDcategorie and categorie[2] == 1:
                dlg = wx.MessageDialog(self, _(u"Cet item est le premier de sa cat�gorie. Vous ne pouvez donc pas le d�placer vers le haut."), "Information", wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                return

            # On cherche les places
            if categorie[0] == IDcategorie:
                ordreTemp = categorie[2]
                # On modifie l'enregistrement
                listeDonnees = [("ordre", ordreTemp-1),]
                DB.ReqMAJ("cat_presences", listeDonnees, "IDcategorie", categorie[0])

            if ordreTemp != None:
                if categorie[2] == ordreTemp-1:
                    listeDonnees = [("ordre", ordreTemp),]
                    DB.ReqMAJ("cat_presences", listeDonnees, "IDcategorie", categorie[0])

        # Finalisation
        DB.Commit()
        DB.Close()

        # M�J du treeCtrl
        self.select2 = IDcategorie
        self.MAJtree()
        self.SetFocus()
       

    def Menu_Bas(self, event):
        
        if self.treeSelection[2] == 0:
            return
        
        # On recherche si c'est n'est pas le seul enfant
        itemParent = self.GetItemParent(self.treeSelection[0])
        IDitemParent = self.GetPyData(itemParent)
        nbreEnfants = self.GetChildrenCount(itemParent, False)
        if nbreEnfants < 2:
            dlg = wx.MessageDialog(self, _(u"Cet item est la seule dans sa cat�gorie. Vous ne pouvez donc pas le d�placer."), "Information", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return

        # On le d�place vers le haut
        IDcategorie = self.GetPyData(self.treeSelection[0])        
        DB = GestionDB.DB()

        # R�cup�ration de l'ordre
        req = """
        SELECT IDcategorie, nom_categorie, ordre
        FROM cat_presences
        WHERE cat_presences.IDcat_parent=%d
        ORDER BY cat_presences.ordre;
        """ % IDitemParent
        DB.ExecuterReq(req)
        listeCategories = DB.ResultatReq()

        ordreTemp = None
        for categorie in listeCategories :

            # Si c'est d�j� le premier, on laisse tomber
            if categorie[0] == IDcategorie and categorie[2] == len(listeCategories):
                dlg = wx.MessageDialog(self, _(u"Cet item est le dernier de sa cat�gorie. Vous ne pouvez donc pas le d�placer vers le bas."), "Information", wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                return

            # On cherche les places
            if categorie[0] == IDcategorie:
                ordreTemp = categorie[2]
                # On modifie l'enregistrement
                listeDonnees = [("ordre", ordreTemp+1),]
                DB.ReqMAJ("cat_presences", listeDonnees, "IDcategorie", categorie[0])

            if ordreTemp != None:
                if categorie[2] == ordreTemp+1:
                    listeDonnees = [("ordre", ordreTemp),]
                    DB.ReqMAJ("cat_presences", listeDonnees, "IDcategorie", categorie[0])

        # Finalisation
        DB.Commit()
        DB.Close()

        # M�J du treeCtrl
        self.select2 = IDcategorie
        self.MAJtree()
        self.SetFocus()


class Dialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        self.parent = parent

        self.panel_base = wx.Panel(self, -1)
        self.panel_contenu = Panel(self.panel_base)
        self.panel_contenu.barreTitre.Show(False)
        self.bouton_aide = CTRL_Bouton_image.CTRL(self.panel_base, texte=_(u"Aide"), cheminImage=Chemins.GetStaticPath("Images/32x32/Aide.png"))
        self.bouton_fermer = CTRL_Bouton_image.CTRL(self.panel_base, texte=_(u"Fermer"), cheminImage=Chemins.GetStaticPath("Images/32x32/Fermer.png"))
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.Onbouton_aide, self.bouton_aide)
        self.Bind(wx.EVT_BUTTON, self.Onbouton_annuler, self.bouton_fermer)

    def __set_properties(self):
        self.SetTitle(_(u"Gestion des cat�gories de pr�sences"))
        self.bouton_aide.SetToolTip(wx.ToolTip("Cliquez ici pour obtenir de l'aide"))
        self.bouton_fermer.SetToolTip(wx.ToolTip(_(u"Cliquez pour annuler et fermer")))
        self.SetMinSize((600, 500))

    def __do_layout(self):
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(rows=3, cols=1, vgap=0, hgap=0)
        sizer_pages = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base.Add(sizer_pages, 1, wx.ALL | wx.EXPAND, 0)
        sizer_pages.Add(self.panel_contenu, 1, wx.EXPAND | wx.TOP, 10)
        grid_sizer_boutons = wx.FlexGridSizer(rows=1, cols=6, vgap=10, hgap=10)
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_boutons.Add(self.bouton_fermer, 0, 0, 0)
        grid_sizer_boutons.AddGrowableCol(1)
        grid_sizer_base.Add(grid_sizer_boutons, 1, wx.LEFT | wx.BOTTOM | wx.RIGHT | wx.EXPAND, 10)
        self.panel_base.SetSizer(grid_sizer_base)
        grid_sizer_base.AddGrowableRow(0)
        grid_sizer_base.AddGrowableCol(0)
        sizer_base.Add(self.panel_base, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.sizer_pages = sizer_pages
        self.CenterOnScreen()

    def Onbouton_aide(self, event):
        from Utils import UTILS_Aide
        UTILS_Aide.Aide("Lescatgoriesdeprsences")

    def Onbouton_annuler(self, event):
        self.EndModal(wx.ID_CANCEL)


if __name__ == "__main__":
    app = wx.App(0)
    dlg = Dialog(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
