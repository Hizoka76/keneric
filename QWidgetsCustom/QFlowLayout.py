#!/bin/python3
# This Python file uses the following encoding: utf-8

try:
    # Modules PySide6
    from PySide6.QtWidgets import QLayout, QWidgetItem
    from PySide6.QtCore import Qt, QRect, QSize, QPoint

except:
    try:
        # Modules PySide2
        from PySide2.QtWidgets import QLayout, QWidgetItem
        from PySide2.QtCore import Qt, QRect, QSize, QPoint

    except:
        try:
            # Modules PyQt5
            from PyQt5.QtWidgets import QLayout, QWidgetItem
            from PyQt5.QtCore import Qt, QRect, QSize, QPoint

        except:
            print("QFlowLayout : Impossible de trouver PySide6 / PySide2 / PyQt5.")
            exit()




class QFlowLayout(QLayout):
    """QLayout personnalisé qui renvoie ses widgets à la ligne si besoin."""

    def __init__(self, parent=None, margin=0, spacing=0):
        # margin : Marge entre les items et et les bords du QLayout
        # spacing : marge entre les items

        super(QFlowLayout, self).__init__(parent)

        # Variables globales
        self.itemList = []
        self.margin = margin
        self.spacing = spacing
        self.index = 0


    #========================================================================
    def __del__(self):
        """Suppression des widgets du QLayout."""
        item = self.takeAt(0)
        while item: item = self.takeAt(0)


    #========================================================================
    def addItem(self, item):
        """Ajoute un item à la fin du QLayout, fonction appelée par addWidgetet qui va relancer doLayout."""
        # Permet de connaitre l'ordre d'insertion
        x = len(self.itemList) - 1
        if x < 0: x = 0

        # Remplissage de la liste avec des dictionnaires car ça permet de les ranger dans doLayout
        self.itemList.append({'index': x, 'widget': item, 'sort': self.index})

        # Réinitialisation de l'index pour qu'il ne soit pas utilisé lors d'un simple addWidget
        if self.index: self.index = 0


    #========================================================================
    def count(self):
        """Retourne le nombre d'item du QLayout."""
        return len(self.itemList)


    #========================================================================
    def itemAt(self, index):
        """Renvoi l'item demandé."""
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]['widget']

        return None


    #========================================================================
    def takeAt(self, index):
        """Supprime l'item indiqué du QLayout."""
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)['widget']

        return None


    #========================================================================
    def insertWidget(self, index, widget):
        """Insertion d'un widget à un emplacement."""
        self.index = index
        self.addWidget(widget)


    #========================================================================
    def expandingDirections(self):
        """Le QLayout ne s'étend qu'horizontalement."""
        return Qt.Orientations(Qt.Horizontal)


    #========================================================================
    def hasHeightForWidth(self):
        """If this layout's preferred height depends on its width."""
        return True


    #========================================================================
    def heightForWidth(self, width):
        """Get the preferred height a layout item with the given width."""
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height


    #========================================================================
    def setGeometry(self, rect):
        """Indique la taille du QLayout."""
        super(QFlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)


    #========================================================================
    def sizeHint(self):
        """Retourne la taille préférée du QLayout."""
        size = QSize()

        # Traite les items 1 par 1
        for item in self.itemList:
            size = size.expandedTo(item['widget'].minimumSize())

        return size


    #========================================================================
    def doLayout(self, rect, testOnly):
        """Mise en place des items."""
        # Ajout aussi la marge entre le QLayout et ses Items
        x = rect.x() + self.margin
        y = rect.y() + self.margin
        lineHeight = 0

        # Traite les items 1 par 1 en les rangeant
        for widget in sorted(self.itemList, key=lambda k: (k['sort'], k['index'])):
            item = widget['widget']

            # Emplacement x + largeur de l'item + marge
            nextX = x + item.sizeHint().width() + self.spacing

            # Si l'élément sans marge à la place de rentrer
            if nextX - self.spacing > rect.right() - self.margin and lineHeight > 0:
                # Nouvelles valeurs des variables
                x = rect.x() + self.margin
                y = y + lineHeight + self.spacing
                nextX = x + item.sizeHint().width() + self.spacing
                lineHeight = 0

            # Si ce n'est pas un test, envoie de l'emplacement de l'item
            if not testOnly: item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            # Décalage de x
            x = nextX

            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + self.margin
