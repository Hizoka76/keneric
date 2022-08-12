#!/bin/python3
# This Python file uses the following encoding: utf-8

try:
    # Modules PySide6
    from PySide6.QtGui import QIcon, QAction, QDesktopServices, QCursor
    from PySide6.QtWidgets import QToolButton, QMenu
    from PySide6.QtCore import Qt, QSize, QCoreApplication, QDir, QTemporaryDir, QEvent, QUrl

    PySideVersion = 6

except:
    PySideVersion = 2

    try:
        # Modules PySide2
        from PySide2.QtGui import QIcon, QDesktopServices, QCursor
        from PySide2.QtWidgets import QToolButton, QMenu, QAction
        from PySide2.QtCore import Qt, QSize, QCoreApplication, QDir, QTemporaryDir, QEvent, QUrl

    except:
        try:
            # Modules PyQt5
            from PyQt5.QtGui import QIcon, QDesktopServices, QCursor
            from PyQt5.QtWidgets import QToolButton, QMenu, QAction
            from PyQt5.QtCore import Qt, QSize, QCoreApplication, QDir, QTemporaryDir, QEvent, QUrl

        except:
            print("QToolButtonCustom : Impossible de trouver PySide6 / PySide2 / PyQt5.")
            exit()



# Fonction permettant d'améliorer la lisibilité des lignes de traductions
def translate(Groupe, Text):
    return QCoreApplication.translate(Groupe, Text)


#############################################################################
class QToolButtonCustom(QToolButton):
    def __init__(self, parent=None, id=None, icon=None, temp=None, ImageSize=200, text=None, tooltip=None, title=None, DownloadFolder=None):
        QToolButton.__init__(self, parent)

        # Variables
        self.TemporaryImage = icon
        self.title = title
        self.id = id
        self.downloadFolder(DownloadFolder)

        # Config par défaut
        self.setEnabled(False)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Gestion de la taille du bouton en fonction de celle de l'image'
        self.setMinimumWidth(ImageSize)
        self.setMinimumHeight(ImageSize)
        self.setMaximumWidth(ImageSize)
        self.setIconSize(QSize(ImageSize, ImageSize))

        # Gestion du texte
        self.setText(f"{id}\n{title}\n{text}")

        # Gestion de l'icône
        if icon: self.setIcon(QIcon(icon))

        # Gestion de l'info bulle
        if tooltip: self.setToolTip(f"<div style='width: 500px;'>{tooltip}</div>")

        # Chargement des textes de base
        self.updateLang()


    #========================================================================
    def updateLang(self):
        """Fonction permettant de mettre à jour les textes lors des changements de langue."""
        # Maj du status tip
        self.setStatusTip(translate("QToolButtonCustom", "There is a context menu with right click."))

        # Recréation du menu
        self.menuCreation()


    #========================================================================
    def menuCreation(self):
        """Création du context menu."""
        self.contextMenu = QMenu(self)

        DownloadAction =  QAction(QIcon.fromTheme("folder-download", QIcon("Ressources:folder-download.svg")), translate("QToolButtonCustom", "Open the download folder"), self.contextMenu)
        DownloadAction.triggered.connect(self.openDownloadFolder)
        self.contextMenu.addAction(DownloadAction)

        ViewImageAction =  QAction(QIcon.fromTheme("viewimage", QIcon("Ressources:viewimage.svg")), translate("QToolButtonCustom", "Open the temporary poster"), self.contextMenu)
        ViewImageAction.triggered.connect(self.openTemporaryPoster)
        self.contextMenu.addAction(ViewImageAction)

        self.contextMenu.addSeparator()

        GoWebSiteAction =  QAction(QIcon.fromTheme("link", QIcon("Ressources:link.svg")), translate("QToolButtonCustom", "Go to the movie page on TMDB"), self.contextMenu)
        GoWebSiteAction.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(f"https://www.themoviedb.org/movie/{self.id}")))
        self.contextMenu.addAction(GoWebSiteAction)


    #========================================================================
    def openTemporaryPoster(self):
        """Fonction ouvrant le poster temporaire."""
        if QDir().exists(self.TemporaryImage):
            temp = QDesktopServices.openUrl(QUrl(self.TemporaryImage))


    #========================================================================
    def openDownloadFolder(self):
        """Fonction ouvrant le dossier de téléchargement."""
        if QDir().exists(self.DownloadFolder):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.DownloadFolder))


    #========================================================================
    def downloadFolder(self, DownloadFolder):
        """Fonction générant un nom de dossier de téléchargement."""
        self.DownloadFolder = QTemporaryDir(DownloadFolder + "/" + self.title).path()


    #========================================================================
    def mousePressEvent(self, event):
        """Fonction de récupération des touches souris utilisées."""
        # Affichage du menu au clic droit
        if event.button() == Qt.RightButton:
            if PySideVersion == 6:
                # PySide6
                self.contextMenu.exec(QCursor.pos())

            else:
                # PySide2
                self.contextMenu.exec_(QCursor.pos())

        # Accepte l'événement
        super().mousePressEvent(event)
