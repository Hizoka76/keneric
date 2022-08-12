#!/bin/python3

# Created by Belleguic Terence (hizo@free.fr)
# WebPage: https://github.com/Hizoka76/PyQt-Widgets
# Version: 21-11-04.0
# Based on: https://gis.stackexchange.com/questions/350148/qcombobox-multiple-selection-pyqt5


# modifier setDefaultValues pour utiliser tout simplement une liste de dictionnaires


# Version: 21-11-13.0
    # Ajout de la fonction currentInfo
    # updateLang => contextMenuUpdate
    # Mise en place de QUndoStack, QUndoCommand à la place du systeme maison
    # Utilisation de ctrl + maj ou les actions inverses
    # Utilisation de sous menus dans le menu context
    # Si les valeurs par défauts sont envoyés avant l'ajout des items, l'option est perdue
    # Ajout de setUndoEnabled et setCheckAllEnabled pour l'affichage ou non d'options dans le context menu
    # Ajout d'un argument dans setState* pour ne pas prendre en compte l'action dans l'historique
    # Changement de la fonction setIcons
    # Ajout de la selection multiple avec coloration
    # Utilisation d'une valeur par defaut à uncheck dans addItems


# Old :
    # Mise à jour du texte du lineEdit lors d'un changement d'état d'une case à cochée
    # utilisation de itemChanged et non de dataChanged qui ne précise pas l'item modifié
    #self.model().itemChanged.connect(self.dataItemChanged)
        # => Déconne avec le 1er élément de la liste, utilisation de highlighted + installEventFilter

    # Donne la même apparence au QLineEdit qu'un QPushButton
    #palette = qApp.palette()
    #palette.setBrush(QPalette.Base, palette.button())
    #self.lineEdit().setPalette(palette)
        # => Ne semble pas spécialement utile et plante en PyQt5

    # Prise en compte de la touche entrée
    #self.activated.connect(self.entryKeyUsed)
        # => Non fonctionnel, car il affiché le text et non le data, utilisation de : highlighted + installEventFilter


# Infos :
    # self : QComboBox
    # self.lineEdit() : QLineEdit
    # self.model() : QStandardItemModel
    # self.view() : QListView
    # self.view().viewport() : QWidget


try:
    # Modules PySide6
    from PySide6.QtGui import QPalette, QFontMetrics, QStandardItem, QAction, QIcon, QCursor, QKeySequence, QUndoStack, QUndoCommand, QBrush, QColor, QFont
    from PySide6.QtWidgets import QComboBox, QStyledItemDelegate, QLineEdit, QListView, QMenu, QApplication
    from PySide6.QtCore import QEvent, Qt, QCoreApplication, QSize, QFileInfo, QMimeDatabase, QMimeType

    PySideVersion = 6

except:
    try:
        # Modules PyQt6
        from PyQt6.QtGui import QPalette, QFontMetrics, QStandardItem, QAction, QIcon, QCursor, QKeySequence, QUndoStack, QUndoCommand, QBrush, QColor, QFont
        from PyQt6.QtWidgets import QComboBox, QStyledItemDelegate, QLineEdit, QListView, QMenu, QApplication
        from PyQt6.QtCore import QEvent, Qt, QCoreApplication, QSize, QFileInfo, QMimeDatabase, QMimeType

        PySideVersion = 6

    except:
        PySideVersion = 2

        try:
            # Modules PySide2
            from PySide2.QtGui import QPalette, QFontMetrics, QStandardItem, QIcon, QCursor, QKeySequence, QUndoStack, QUndoCommand, QBrush, QColor, QFont
            from PySide2.QtWidgets import QComboBox, QStyledItemDelegate, QLineEdit, QListView, QMenu, QApplication, QAction
            from PySide2.QtCore import QEvent, Qt, QCoreApplication, QSize, QFileInfo, QMimeDatabase, QMimeType

        except:
            try:
                # Modules PyQt5
                from PyQt5.QtGui import QPalette, QFontMetrics, QStandardItem, QIcon, QCursor, QKeySequence, QBrush, QColor, QFont
                from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QLineEdit, QListView, QMenu, QApplication, QAction, QUndoStack, QUndoCommand
                from PyQt5.QtCore import QEvent, Qt, QCoreApplication, QSize, QFileInfo, QMimeDatabase, QMimeType

            except:
                print("QCheckComboBox : Impossible de trouver PySide6 / PySide2 / PyQt5.")
                exit()



############################################
## Classe gérant l'historique des actions ##
############################################
class StoreCommand(QUndoCommand):
    def __init__(self, Item, OldValue, NewValue):
        super().__init__()

        # Item concerné
        self.Item = Item

        # Ancienne valeur
        self.OldValue = OldValue

        # Nouvelle valeur
        self.NewValue = NewValue


    #========================================================================
    def undo(self):
        """Fonction exécutant la commande inverse permettant un retour en arrière."""
        # Remet l'ancien état de la coche
        self.Item.setCheckState(self.OldValue)


    #========================================================================
    def redo(self):
        """Fonction exécutant la commande initiale permettant un retour en avant."""
        # (Re)met le nouvel état de la coche
        self.Item.setCheckState(self.NewValue)


class view(QListView):
    def __init__(self, Parent):
        super().__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, Event):
        print("mouseMoveEvent")


######################################
## Classe du QComboBox personnalisé ##
######################################
class QCheckComboBox(QComboBox):
    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size


    #========================================================================
    def __init__(self, Parent=None, *args, **kwargs):
        # Ne pas utiliser super().__init__(*args, **kwargs) car QComboBox ne connaît pas mes variables
        super().__init__()

        # Gestion de la coloration des lignes via shift + clic
        self.ColorEnabled = False
        self.brush = QBrush(QColor(255, 255, 125))
        self.brush.setStyle(Qt.SolidPattern)

        # Gestion de la pile des actions, la mise à jour du texte ne se fait qu'une fois par groupe d'action
        self.undoStack = QUndoStack()
        self.undoStack.indexChanged.connect(self.updateText)
        self.undoStackInProgress = False

        # Variables par défaut
        self.UndoEnabled = True
        self.CheckAllEnabled = True

        # Variable pour l'utilisation de shift + clic
        self.LastCheckBoxClicked = None

        # Liste des arguments possibles
        CamelArgs = ["TristateMode", "Icons", "Title", "TitleIcon", "Items", "DefaultValues", "UndoEnabled", "CheckAllEnabled"]

        # Retravaille le dictionnaire pour prise en compte d'une mauvais casse
        for Key, Value in dict(kwargs).items():
            # Si la clé est bien écrite, on continue
            if Key in CamelArgs:
                continue

            else:
                for Arg in CamelArgs:
                    # Si la clé existe mais avec la mauvaise casse, on ajoute la version camel
                    if Key.lower() == Arg.lower():
                        kwargs[Arg] = Value


        # La QComboBox est éditable pour afficher un texte mais est en lecture seule pour l'utilisateur
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        # Pour connaitre l'item surligné par la souris ou par le clavier'
        self.ItemHighlighted = None
        self.highlighted.connect(self.comboHighlighted)

        # Mode 3 états des cases à cocher
        self.TristateMode = False

        # Indicateur de la présence d'un titre pour ne pas prendre en compte le 1er élément
        self.TitleExists = False

        # Liste des valeurs par défaut
        self.DefaultValuesCase = False
        self.DefaultValues = {
            Qt.Checked: [],
            Qt.PartiallyChecked: []
            }

        # Use custom delegate
        self.setItemDelegate(QCheckComboBox.Delegate())

        # Mise en place de la surveillance des événements du lineEdit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Mise en place de la surveillance des événements du QWidget
        self.view().viewport().installEventFilter(self)
        self.view().viewport().setMouseTracking(True)
        self.model().installEventFilter(self)

        # Pour la gestion du clic droit sur la flèche et le blocage des touches flèches
        self.installEventFilter(self)

        # Pour la gestion du coche lors d'un clic
        self.view().installEventFilter(self)

        # Icônes par défaut du du menu
        self.MenuIcons = {
            "Copy": QIcon.fromTheme("edit-select-text"),
            "Undo": QIcon.fromTheme("edit-undo"),
            "Redo": QIcon.fromTheme("edit-redo"),
            "AllCheck": QIcon.fromTheme("edit-select-all"),
            "AllPatriallyCheck": QIcon.fromTheme("select-rectangular"),
            "AllUncheck": QIcon.fromTheme("edit-select-none"),
            "DefaultValues": QIcon.fromTheme("edit-reset")
            }

        # Récupération des icônes indiquées
        if "Icons" in kwargs:
            self.setIcons(kwargs["Icons"])

        # Si le mode TristateMode est passé lors de la création de la classe
        if "TristateMode" in kwargs:
            self.setTristateMode(kwargs["TristateMode"])

        # Si le titre est passé lors de la création de la classe
        if "Title" in kwargs:
            # L'icône est facultative
            self.setTitle(kwargs["Title"], IconChecker(kwargs.get("TitleIcon")))

        # Si des items sont passées lors de la création de la classe
        if "Items" in kwargs:
            self.addItems(kwargs["Items"])

        # Si des valeurs par défaut ont été données
        if "DefaultValues" in kwargs:
            self.setDefaultValues(kwargs["DefaultValues"])

        # Chargement des textes de base
        self.contextMenuUpdate()


    #========================================================================
    def setUndoEnabled(self, Value):
        """Mise à jour la variable UndoEnabled."""
        try:
            self.UndoEnabled = bool(Value)
        except:
            return

        self.contextMenuUpdate()


    #========================================================================
    def setCheckAllEnabled(self, Value):
        """Mise à jour la variable CheckAllEnabled."""
        try:
            self.CheckAllEnabled = bool(Value)
        except:
            return

        self.contextMenuUpdate()


    #========================================================================
    def setIcons(self, Icons):
        """Fonction permettant de changer les icônes par défaut.
        Icons doit être un dictionnaire."""
        if isinstance(Icons, dict):
            # Permet de ne pas prendre en compte la casse
            IconNames = {}
            for Icon in self.MenuIcons.keys():
                IconNames[Icon.lower()] = Icon

            # Mise à jour des icônes
            for Key, Value in Icons.items():
                if Key.lower() in IconNames.keys():
                    IconName = IconNames[Key.lower()]
                    self.MenuIcons[IconName] = IconChecker(Value)

            # Mise à jour du menu
            self.contextMenuUpdate()


    #========================================================================
    def setTristateMode(self, TristateMode):
        """Fonction permettant d'activer ou non le mode 3états des cases à cocher."""
        # Si le type de valeur reçue n'est pas celle attendue, on stoppe
        if not isinstance(TristateMode, bool) and TristateMode not in [0, 1, "0", "1", "True", "False"]:
            return

        # Force le bool
        self.TristateMode = bool(TristateMode)

        # (Dés)active le mode 3 états des cases à cocher
        for i in range(self.model().rowCount()):
            if self.model().item(i) is not None:
                self.model().item(i).setUserTristate(TristateMode)
                self.model().item(i).setAutoTristate(TristateMode)

        # Mise à jour du menu
        self.contextMenuUpdate()


    #========================================================================
    def newCheckState(self, ActualState):
        """Fonction indiquant le nouvel état d'une case à cocher."""
        if ActualState == Qt.Checked:
            NewState = Qt.Unchecked

        elif ActualState == Qt.Unchecked:
            # Mode 3 états
            if self.TristateMode:
                NewState = Qt.PartiallyChecked

            # Mode 2 états
            else:
                NewState = Qt.Checked

        elif ActualState == Qt.PartiallyChecked:
            NewState = Qt.Checked

        return NewState


    #========================================================================
    def contextMenuUpdate(self):
        """Fonction permettant de mettre à jour les textes lors des changements de langue."""
        # Création d'un menu vide
        self.contextMenu = QMenu()
        self.contextMenu.installEventFilter(self)

        # Création et ajout de l'action de copie du texte
        CopyAction = QAction(self.MenuIcons["Copy"], QCoreApplication.translate("QCheckComboBox", "Copy values choosen"), self.contextMenu)
        CopyAction.setShortcut(QKeySequence("Ctrl+C"))
        CopyAction.setShortcutContext(Qt.ApplicationShortcut)
        CopyAction.triggered.connect(self.copyText)
        self.contextMenu.addAction(CopyAction)


        self.UndoAction = self.undoStack.createUndoAction(self.contextMenu, QCoreApplication.translate("QCheckComboBox", "Undo Action"))
        self.RedoAction = self.undoStack.createRedoAction(self.contextMenu, QCoreApplication.translate("QCheckComboBox", "Redo Action"))

        if self.UndoEnabled:
            self.contextMenu.addSection(QCoreApplication.translate("QCheckComboBox", "UnRedo Actions"))

            # Création et ajout de l'action d'annulation d'action
            self.UndoAction.setIcon(self.MenuIcons["Undo"])
            self.UndoAction.setShortcut(QKeySequence("Ctrl+Z"))
            self.contextMenu.addAction(self.UndoAction)

            # Création et ajout de l'action d'annulation d'action
            self.RedoAction.setIcon(self.MenuIcons["Redo"])
            self.RedoAction.setShortcut(QKeySequence("Ctrl+Shift+Z"))
            self.contextMenu.addAction(self.RedoAction)


        if self.CheckAllEnabled:
            self.contextMenu.addSection(QCoreApplication.translate("QCheckComboBox", "Check Boxes"))

            # Création et ajout de l'action de cochage
            AllCheck = QAction(self.MenuIcons["AllCheck"], QCoreApplication.translate("QCheckComboBox", "Check All Items"), self.contextMenu)
            AllCheck.triggered.connect(lambda: self.setStateAll(Qt.Checked))
            AllCheck.setShortcut(QKeySequence("Ctrl+A"))
            self.contextMenu.addAction(AllCheck)

            # Création et ajout de l'action de semi cochage
            if self.TristateMode:
                AllSemiCheck = QAction(self.MenuIcons["AllPatriallyCheck"], QCoreApplication.translate("QCheckComboBox", "Partially Check All Items"), self.contextMenu)
                AllSemiCheck.triggered.connect(lambda: self.setStateAll(Qt.PartiallyChecked))
                AllSemiCheck.setShortcut(QKeySequence("Ctrl+P"))
                self.contextMenu.addAction(AllSemiCheck)

            # Création et ajout de l'action de décochage
            AllUncheck = QAction(self.MenuIcons["AllUncheck"], QCoreApplication.translate("QCheckComboBox", "Uncheck All Items"), self.contextMenu)
            AllUncheck.triggered.connect(lambda: self.setStateAll(Qt.Unchecked))
            AllUncheck.setShortcut(QKeySequence("Ctrl+Shift+A"))
            self.contextMenu.addAction(AllUncheck)


        # Création de l'action de restauration des données par défaut
        if self.DefaultValues[Qt.Checked] or self.DefaultValues[Qt.PartiallyChecked]:
            self.contextMenu.addSection(QCoreApplication.translate("QCheckComboBox", "Default Values"))

            ResetDefaultValues = QAction(self.MenuIcons["DefaultValues"], QCoreApplication.translate("QCheckComboBox", "Restore the default values"), self.contextMenu)
            ResetDefaultValues.triggered.connect(self.resetDefaultValues)
            ResetDefaultValues.setShortcut(QKeySequence("Ctrl+R"))
            self.contextMenu.addAction(ResetDefaultValues)


    #========================================================================
    def comboHighlighted(self, Index):
        """Fonction conservant l'item actuellement surligné, utile lors de l'utilisation du clavier."""
        self.ItemHighlighted = Index


    #========================================================================
    def resizeEvent(self, Event):
        # Recompute text to elide as needed
        super().resizeEvent(Event)

        # La mise  à jour doit se faire après le resize
        self.updateText()


    #========================================================================
    def eventFilter(self, Object, Event):
        """Fonction surveillant toutes les évènements des widgets mis sur écoute."""
        # Cas de la combobox
        if Object == self:
            # Si on utilise les touches des flèches pour naviguer, ça inverse l'état des cases
            # 1 clic sur la combobox, un 2e pour fermer la fenêtre puis utilisation des flèches pour une navigation invisible

            # Les touches affichent le menu ou ne font rien pour ne pas cocher des cases sans le voir
            if Event.type() == QEvent.KeyPress:
                # Prise en compte des raccourcis claviers, mieux géré ainsi qu'avec QShortcut
                if self.shortcutEvent(Event):
                    return True

                elif Event.key() in [Qt.Key_Down, Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab]:
                    self.popupEvent()

                return True

            # Si c'est un clic droit sur la petite flèche, on affiche un menu modifié
            elif Event.type() == QEvent.ContextMenu:
                self.menuEvent()

                # Bloque l'événement
                return True


        # Cas du lineEdit
        elif Object == self.lineEdit():
            # Si l'événement est le relâchement d'un clic (Event.button() pour savoir lequel)
            if Event.type() == QEvent.MouseButtonRelease:
                self.popupEvent()

                # Bloque l'événement
                return True

            # Si c'est un clic droit, on affiche un menu modifié
            elif Event.type() == QEvent.ContextMenu:
                self.menuEvent()

                # Bloque l'événement
                return True


        # Cas du viewport
        elif Object == self.view().viewport():
            if Event.type() == QEvent.MouseMove:
                if Event.modifiers() == Qt.ShiftModifier and self.LastCheckBoxClicked is not None:
                    # Coloration des lignes lors de l'utilisation de shift après un clic
                    self.colorizeRow(Event.pos())

                else:
                    # Remise en place des couleurs
                    self.uncolorizeRow()


            # Si l'événement est le relâchement d'un clic (Event.button() si besoin pour savoir lequel)
            elif Event.type() == QEvent.MouseButtonRelease:
                # Si c'est un clic gauche, on modifie l'état de la case à cocher
                if Event.button() == Qt.MouseButton.LeftButton:
                    # S'il y a shift + clic pour sélection multiple
                    if Event.modifiers() == Qt.ShiftModifier and self.LastCheckBoxClicked is not None:
                        self.multiCheck(Event.pos())

                    else:
                        # Récupération de la case à cocher concernée
                        Index = self.view().indexAt(Event.pos())
                        Row = Index.row()
                        Item = self.model().item(Row)

                        # Bloque les actions de la 1ere ligne s'il y a un titre
                        if Row == 0 and self.TitleExists:
                            return True

                        # Nouvel état à donner à la case à cocher
                        State = self.newCheckState(Item.checkState())

                        # Mise à jour de l'item
                        self.setStateItem(State, Row)

                        self.LastCheckBoxClicked = Row

                # Si c'est un clic droit, on affiche le menu d'action
                elif Event.button() == Qt.MouseButton.RightButton:
                    self.menuEvent()

                # Bloque l'événement
                return True


        # Cas du view
        elif Object == self.view():
            if Event.type() == QEvent.KeyPress:
                # Prise en compte des raccourcis claviers, mieux géré ainsi qu'avec QShortcut
                if self.shortcutEvent(Event):
                    return True

                # Lors de l'utilisation des touches espace, entrée x 2
                elif Event.key() in [Qt.Key_Space, Qt.Key_Enter, Qt.Key_Return]:
                    # Bloque les actions de la 1ere ligne s'il y a un titre
                    if self.ItemHighlighted == 0 and self.TitleExists:
                        return True

                    # Nouvel état à donner à la case à cocher
                    State = self.newCheckState(self.model().item(self.ItemHighlighted).checkState())

                    # Si les touches entrées ont été utilisées et qu'il y a un titre, on remet le titre pour conserver son icône
                    if Event.key() in [Qt.Key_Enter, Qt.Key_Return] and self.TitleExists:
                        self.setCurrentIndex(0)

                    # Mise à jour de l'item
                    self.setStateItem(State, self.ItemHighlighted)

                    # Bloque l'événement
                    return True


                # Coloration des lignes lors de l'utilisation de shift après un clic
                elif Event.modifiers() == Qt.ShiftModifier and self.LastCheckBoxClicked is not None and Event.key() == Qt.Key_Shift:
                    # Coloration des lignes lors de l'utilisation de shift après un clic
                    self.colorizeRow(self.mapFromGlobal(QCursor.pos()), -1)


            # Remise en place des couleurs
            elif Event.type() == QEvent.KeyRelease:
                if Event.key() == Qt.Key_Shift :
                    self.uncolorizeRow()


        # Dans le cas du QMenu
        elif Object == self.contextMenu:
            if Event.type() == QEvent.KeyPress:
                # Prise en compte des raccourcis claviers, mieux géré ainsi qu'avec QShortcut
                if self.shortcutEvent(Event):
                    # Fermeture du menu
                    self.contextMenu.close()

                    # Bloque l'événement
                    return True


        ### Autorise l'événement
        return False


    #========================================================================
    def shortcutEvent(self, Event):
        """Fonction de gestion des raccourcis clavier."""
        # S'il y a combinaison de ctrl + maj + une des touches suivantes, on exécute la commande associée
        if Event.modifiers() == Qt.ShiftModifier | Qt.ControlModifier and Event.key() in [Qt.Key_A, Qt.Key_Z]:
            if Event.key() == Qt.Key_A and self.CheckAllEnabled:
                self.setStateAll(Qt.Unchecked)

            elif Event.key() == Qt.Key_Z and self.UndoEnabled:
                self.RedoAction.trigger()


        # S'il y a combinaison de ctrl + une des touches suivantes, on exécute la commande associée
        if Event.modifiers() == Qt.ControlModifier and Event.key() in [Qt.Key_A, Qt.Key_C, Qt.Key_P, Qt.Key_R, Qt.Key_Z]:
            if Event.key() == Qt.Key_A and self.CheckAllEnabled:
                self.setStateAll(Qt.Checked)

            elif Event.key() == Qt.Key_C:
                self.copyText()

            elif Event.key() == Qt.Key_P and self.TristateMode and self.CheckAllEnabled:
                self.setStateAll(Qt.PartiallyChecked)

            elif Event.key() == Qt.Key_R and (self.DefaultValues[Qt.Checked] or self.DefaultValues[Qt.PartiallyChecked]):
                self.resetDefaultValues()

            elif Event.key() == Qt.Key_Z and self.UndoEnabled:
                self.UndoAction.trigger()

            return True

        return False


    #========================================================================
    def popupEvent(self):
        """Fonction gérant l'affichage ou son contraire de la liste des propositions."""
        # Si la popup est visible, on la case sinon on l'affiche
        if self.closeOnLineEditClick:
            self.hidePopup()

        else:
            self.showPopup()


    #========================================================================
    def menuEvent(self):
        """Fonction gérant l'affichage de la liste des actions."""
        if PySideVersion == 6:
            self.contextMenu.exec(QCursor.pos())

        else:
            self.contextMenu.exec_(QCursor.pos())


    #========================================================================
    def colorizeRow(self, Position, Decalage=0):
        """Fonction colorant les lignes comprises entre la dernière case modifiée
        et l'emplacement actuel lors de l'utilisation de la touche shift pour une modification d'état de case multiple."""
        # Si la souris est dans le viewport
        if self.view().viewport().underMouse():
            Index = self.view().indexAt(Position)
            Row = Index.row() + Decalage
            Item = self.model().item(Row)

            # Si on trouve bien un item
            if Item:
                # Détermine les valeurs de départ et d'arriver
                if Row < self.LastCheckBoxClicked:
                    Start = Row
                    End = self.LastCheckBoxClicked
                else:
                    Start = self.LastCheckBoxClicked
                    End = Row

                # Empêche la sélection du titre
                if self.TitleExists and Start == 0:
                    Start = 1

                self.ColorEnabled = True

                # Effet gras du texte
                Font = QFont()
                Font.setBold(True)

                for Idx in range(self.count()):
                    # Colore les lignes concernées
                    if Start <= Idx <= End:
                        self.model().item(Idx).setBackground(self.brush)
                        self.model().item(Idx).setData(Font, Qt.FontRole)

                    # Réinitialise les autres lignes
                    else:
                        self.model().item(Idx).setBackground(QStandardItem().background())
                        self.model().item(Idx).setData(QFont(), Qt.FontRole)


    #========================================================================
    def uncolorizeRow(self):
        """Fonction réinitialisant la couleur de toutes les lignes après utilisation de la touche shift."""
        if self.ColorEnabled:
            self.ColorEnabled = False

            # Remise en place de la couleur de base
            for Idx in range(self.model().rowCount()):
                self.model().item(Idx).setBackground(QStandardItem().background())
                self.model().item(Idx).setData(QFont(), Qt.FontRole)


    #========================================================================
    def multiCheck(self, Position):
        # Récupération de la case à cocher concernée
        Index = self.view().indexAt(Position)
        Row = Index.row()
        Item = self.model().item(Row)

        StartIndex = self.LastCheckBoxClicked
        StateCheckState = self.model().item(StartIndex).checkState()

        if StartIndex < Row + 1:
            Start = StartIndex
            End = Row + 1
        else:
            Start = Row
            End = StartIndex

        self.undoStackInProgress = True
        self.undoStack.beginMacro('')

        for Index in range(Start, End):
            Item = self.model().item(Index)
            ItemCheckState = Item.checkState()
            self.setStateItem(StateCheckState, Index)

        self.undoStackInProgress = False
        self.undoStack.endMacro()


    #========================================================================
    def showPopup(self):
        """Fonction affichant la liste des propositions."""
        super().showPopup()

        # Item survolé à l'affichage de la liste
        self.ItemHighlighted = 0

        # Variable permettant à l’évènement de savoir s'il doit afficher ou cacher la popup
        self.closeOnLineEditClick = True


    #========================================================================
    def hidePopup(self):
        """Fonction cachant la liste des propositions."""
        super().hidePopup()

        # Permet d'éviter la réouverture immédiate lors d'un clic sur le lineEdit
        self.startTimer(100)

        # Met à jour le texte visible du lineEdit
        self.updateText()


    #========================================================================
    def timerEvent(self, Event):
        # Après le timeout, kill le timer, et réactive le clic sur le lineEdit
        self.killTimer(Event.timerId())

        self.closeOnLineEditClick = False


    #========================================================================
    def updateText(self, Index=None):
        """Fonction d'affichage des data cochés. L'index est donné par QUndoStack."""
        # Récupération du texte
        text = self.currentText()

        # Gestion de l'ajout du ... en fonction de la place dispo
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)


    #========================================================================
    def addItem(self, Text, Data=None, State=None, Icon=None, ToolTip=None):
        """Fonction de création de l'item."""
        # Création de l'item de base avec son texte et ses flags
        Item = QStandardItem()
        Item.setEditable(False)
        Item.setText(Text)
        Item.setData(Qt.Unchecked, Qt.CheckStateRole)

        if self.TristateMode:
            Item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsUserTristate)

        else:
            Item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)

        # Utilisation de la data indiquée ou du texte
        if Data is None:
            Data = Text

        Item.setData(Data, Qt.UserRole)

        # Utilisation de la data indiquée ou du texte
        if ToolTip is not None:
            Item.setToolTip(ToolTip)

        if Icon is not None and not Icon.isNull():
            Item.setIcon(Icon)

        # Si l'état de la case à cocher est précisée
        if State is not None:
            Item.setCheckState(State)
        else:
            Item.setCheckState(Qt.Unchecked)

        # Ajout de l'item
        self.model().appendRow(Item)


    #========================================================================
    def addItems(self, Items):
        """Fonction de chargement d'item depuis une liste de dictionnaire.
        Les items sont de type : {text, data, state, icon}"""
        # Traite les dictionnaires un à un
        for Item in Items:
            # Remplace les clés par des clés.lower()
            ItemCase = {}
            for Key, Value in Item.items():
                ItemCase[Key.lower()] = Value

            # Si ni data ni texte, on le saute
            if "data" not in ItemCase.keys() and "text" not in ItemCase.keys():
                continue

            # Si une donnée est manquante, on met une valeur de base
            if "text" not in ItemCase.keys():
                ItemCase["text"] = ItemCase["data"]

            #if Item != Items[-1]:
                #ItemCase["default"] = False
            #else:
                #ItemCase["default"] = True

            # Création de la ligne
            self.addItem(ItemCase["text"], ItemCase.get("data"), ItemCase.get("state"), ItemCase.get("icon"), ItemCase.get("tooltip"))


    #========================================================================
    def setStateItem(self, State, Indexes, Undo=True):
        """Fonction de modification de l'état de la case à cocher.
        Cette fonction est appelée par les fonctions de modifications
        de l'état des cases à cocher mais aussi lors du clic sur une case."""

        # Si Indexes n'est pas une liste, on la change
        if not isinstance(Indexes, list):
            if isinstance(Indexes, (str, int)):
                Indexes = [Indexes]

        # Permet de regrouper toutes les actions ci dessous en une
        if Undo and not self.undoStackInProgress:
            self.undoStack.beginMacro('')

        for Index in Indexes:
            # Ne met à jour l'item que si besoin, ne prend pas en compte le titre
            if self.model().item(Index).checkState() != State and self.model().item(Index).data(Qt.UserRole):
                # Valeur actuelle de la case
                ActualState = self.model().item(Index).checkState()

                if Undo:
                    # Création de la commande d'historisation
                    command = StoreCommand(self.model().item(Index), ActualState, State)

                    # Envoie de la commande dans la pile des actions, elle est exécutée par défaut
                    self.undoStack.push(command)

                else:
                    self.model().item(Index).setCheckState(State)

        # Fin du regroupement des actions
        if Undo and not self.undoStackInProgress:
            self.undoStack.endMacro()

        # Mise à jour du texte de la QLineEdit, une seule fois et non 1 fois par index
        self.updateText()


    #========================================================================
    def setStateItems(self, State, Values, CaseSensitive=False, Undo=True):
        """Fonction de modification de l'état de la case à cocher en se basant sur sa data."""
        Indexes = []

        # Utilisation d'une liste obligatoire
        if not isinstance(Values, list):
            if isinstance(Values, (str, int)):
                Values = [Values]

        # Traitement des valeurs
        for Value in Values:
            # Si la valeur est un  nombre, on le considère comme un index
            if isinstance(Value, int):
                if self.TitleExists:
                    Indexes.append(Value + 1)

                else:
                    Indexes.append(Value)

            # Si c'est un texte, on le recherche dans les data et les textes
            elif isinstance(Value, str):
                for Index in range(self.model().rowCount()):
                    Item = self.model().item(Index)

                    # Mode avec prise en compte de la casse
                    if CaseSensitive:
                        if Value in (Item.data(Qt.UserRole), Item.text()):
                            Indexes.append(Index)
                            break

                    # Mode sans prise en compte de la casse
                    else:
                        if Value.lower() in (Item.data(Qt.UserRole).lower(), Item.text().lower()):
                            Indexes.append(Index)
                            break


        # Traite les indexes retournés
        if Indexes:
            self.setStateItem(State, Indexes, Undo)


    #========================================================================
    def setStateAll(self, State, Undo=True):
        """Fonction de modification de l'état de la case à cocher de tous les items."""
        Indexes = []

        # Traite tous les items un à un
        for Index in range(self.model().rowCount()):
            Indexes.append(Index)

        # Traite les cases retournées
        if Indexes:
            self.setStateItem(State, Indexes, Undo)


    #========================================================================
    def setTitle(self, Text, Icon=None):
        """Fonction créant un item en début de liste afin d'utiliser son icône dans le QLineEdit."""
        # Création et configuration de l'item
        FirstItem = QStandardItem()
        FirstItem.setText(Text)
        FirstItem.setFlags(Qt.NoItemFlags)
        FirstItem.setData("", Qt.UserRole)
        FirstItem.setTextAlignment(Qt.AlignHCenter)

        if isinstance(Icon, QIcon):
            FirstItem.setIcon(Icon)

        elif isinstance(Icon, str):
            FirstItem.setIcon(Icon)

        # S'il y a déjà un titre, on l'efface
        if self.TitleExists:
            self.model().removeRow(0)

        # Insertion du titre
        self.model().insertRow(0, FirstItem)

        # Utilisation du titre pour utiliser l'icône
        if Icon is not None:
            self.setCurrentIndex(0)

        # Mise à jour de la variable indiquant qu'il y a un titre
        self.TitleExists = True


    #========================================================================
    def setDefaultValues(self, Values):
        """Fonction prenant les valeurs par défaut. Values est une liste de dictionnaires.
        Les dictionnaires doivent contenir les clés value, state et case (facultatif).
        value (int/str) peut être l'index ou le texte.
        state (Qt.Checked, Qt.PartiallyChecked) correspond à l'état de la case à cocher.
        case (1) indique si la recherche de value est sensible à la casse."""
        # Bloque la fonction s'il n'y a pas encore de choix, les valeurs par défaut sont perdues
        if self.model().rowCount() == 0 or (self.model().rowCount() == 1 and self.TitleExists):
            print("setDefaultValues use before items added, DefautlValues lost.")
            return

        # Si la valeur n'est ni une liste ni un dictionnaire
        if not isinstance(Values, (dict, list)):
            return

        # Si c'est un dictionnaire, on le place dans une liste
        if isinstance(Values, dict):
            Values = [Values]

        # Traite chaque item
        for Item in Values:
            # Si ce n'est pas un dictionnaire, on le saute
            if not isinstance(Item, dict):
                continue

            # Si l'état de la case à cocher n'existe pas, on arrête là
            State = Item.get("state")
            if State not in [Qt.Checked, Qt.PartiallyChecked]:
                return

            # Si la valeur est un  nombre, on le considère comme un index
            Value = Item.get("value")
            if isinstance(Value, int):
                if self.TitleExists:
                    self.DefaultValues[State].append(self.model().item(Value + 1))
                else:
                    self.DefaultValues[State].append(self.model().item(Value))

            # Si c'est un texte, on le recherche dans les data et les textes
            elif isinstance(Value, str):
                for Index in range(self.model().rowCount()):
                    SubItem = self.model().item(Index)

                    # Mode avec prise en compte de la casse
                    if Item.get("case"):
                        if Value in (SubItem.data(Qt.UserRole), SubItem.text()):
                            self.DefaultValues[State].append(SubItem)
                            break

                    # Mode sans prise en compte de la casse
                    else:
                        if Value.lower() in (SubItem.data(Qt.UserRole).lower(), SubItem.text().lower()):
                            self.DefaultValues[State].append(SubItem)
                            break


        # Déblocage de l'action
        if self.DefaultValues[Qt.Checked] or self.DefaultValues[Qt.PartiallyChecked]:
            self.contextMenuUpdate()


    #========================================================================
    def resetDefaultValues(self):
        """Fonction de remise en état des valeurs par défaut."""
        if self.DefaultValues[Qt.Checked] or self.DefaultValues[Qt.PartiallyChecked]:
            # Rassemble le décochage massif et le cochage sélectif en une action
            self.undoStackInProgress = True
            self.undoStack.beginMacro('')

            # Décoche tout
            self.setStateAll(Qt.Unchecked)

            # Coche les différentes cases
            for State, Items in self.DefaultValues.items():
                Indexes = []

                for Item in Items:
                    if Item:
                        Indexes.append(Item.index().row())

                if Indexes:
                    self.setStateItem(State, Indexes)

            # Fin du rassemblage
            self.undoStack.endMacro()
            self.undoStackInProgress = False


    #========================================================================
    def copyText(self):
        """Fonction renvoyant le texte affiché sur le QLineEdit dans le presse papier."""
        QApplication.clipboard().setText(self.currentText())


    #========================================================================
    def currentText(self, Separator=', '):
        """Fonction renvoyant le texte affiché sur le QLineEdit."""
        return Separator.join(self.currentData())


    #========================================================================
    def currentData(self):
        """Fonction renvoyant les data des cases cochées."""
        # Data des cases à cocher
        CheckOK = []

        # Tourne sur toutes les cases à cocher
        for i in range(self.model().rowCount()):
            # Saute les éléments vides
            if self.model().item(i) is None:
                continue

            data = self.model().item(i).data(Qt.UserRole)

            # Ne traite que les cases cochées
            if self.model().item(i).checkState() == Qt.Checked:
                # Ajoute sa data à la liste
                CheckOK.append(data)

            elif self.model().item(i).checkState() == Qt.PartiallyChecked:
                # Ajoute sa data à la liste
                CheckOK.append('[' + data + ']')

        # Envoi de la liste des cases cochées
        return CheckOK



    #========================================================================
    def currentInfo(self):
        """Fonction renvoyant les data des cases cochées."""
        # Infos des cases à cocher
        CheckOK = []

        # Tourne sur toutes les cases à cocher
        for i in range(self.model().rowCount()):
            # Saute les éléments vides
            if self.model().item(i) is None:
                continue

            # Récupération des infos
            Data = self.model().item(i).data(Qt.UserRole)
            Text = self.model().item(i).text()
            State = self.model().item(i).checkState()

            # Index en fonction de la présence d'un titre ou non
            Index = i
            if self.TitleExists:
                Index -= 1

            # Ne traite que les cases cochées
            if State in [Qt.Checked, Qt.PartiallyChecked]:
                # Ajoute la case et ses infos à la liste
                CheckOK.append({"Index":Index, "Data":Data, "Text":Text, "State":State})

        # Envoi de la liste des cases cochées
        return CheckOK


#========================================================================
def IconChecker(Icon):
    """Fonction renvoyant une QIcon depuis une QIcon ou un texte."""
    if Icon is None:
        return QIcon()

    # Si la valeur est déjà une QIcon, on la renvoie directement
    if isinstance(Icon, QIcon):
        return Icon

    # Si c'est un texte, on la transforme en QIcon avant de le renvoyer
    elif isinstance(Icon, str):
        File = QFileInfo(Icon)
        MimeBase = QMimeDatabase()
        MimeType = MimeBase.mimeTypeForFile(Icon).name().split("/")[0].lower()

        # Si l'image existe
        if File.exists() and MimeType == "image":
            return QIcon(Icon)

        # Si le texte n'a pas d'extension ni de path
        if not File.completeSuffix() and File.filePath() == Icon:
            return QIcon.fromTheme(Icon)

        # Si ce n'est pas une image on renvoie un QIcon vide
        if MimeType != "image":
            return QIcon()
