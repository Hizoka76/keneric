#! /usr/bin/python3
# This Python file uses the following encoding: utf-8

# Créer un mode commande ?

# revoir pour charger toutes les pages en même temps

# Teste le titre et le titre original

# Mise à jour de QCheckComboBox

# ThreadStop supprimé
# Chargement de Slot supprimé

#############
## Modules ##
#############
# Modules Python
from os import execl, popen
from shutil import copyfileobj, which
from time import sleep
from unidecode import unidecode
import sys
import requests


try:
    # PySide6
    from PySide6.QtGui import QIcon, QPixmap, QDesktopServices, QCursor, QPalette, QBrush, QColor, QTextCursor, QAction

    from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QFileDialog, QProgressBar, QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel, QLineEdit, QGroupBox, QComboBox, QCheckBox, QSpinBox, QTextEdit, QSpacerItem, QSizePolicy, QSplitter, QTabWidget, QWidget, QMainWindow, QScrollArea, QFormLayout, QStatusBar, QProxyStyle, QStyle

    from PySide6.QtCore import QObject, Signal, QTranslator, QCoreApplication, QEvent, Qt, QLocale, QTemporaryDir, QDir, QUrl, QSize, QSettings, QFileInfo, QRunnable, QThreadPool

    PySideVersion = 6

except:
    try:
        # PyQt6
        from PyQt6.QtGui import QIcon, QPixmap, QDesktopServices, QCursor, QPalette, QBrush, QColor, QTextCursor, QAction

        from PyQt6.QtWidgets import QApplication, QMessageBox, QPushButton, QFileDialog, QProgressBar, QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel, QLineEdit, QGroupBox, QComboBox, QCheckBox, QSpinBox, QTextEdit, QSpacerItem, QSizePolicy, QSplitter, QTabWidget, QWidget, QMainWindow, QScrollArea, QFormLayout, QStatusBar, QProxyStyle, QStyle

        from PyQt6.QtCore import QObject, pyqtSignal as Signal, QTranslator, QCoreApplication, QEvent, Qt, QLocale, QTemporaryDir, QDir, QUrl, QSize, QSettings, QFileInfo, QRunnable, QThreadPool

        PySideVersion = 6

    except:
        PySideVersion = 2

        try:
            # PySide2
            from PySide2.QtGui import QIcon, QPixmap, QDesktopServices, QCursor, QPalette, QBrush, QColor, QTextCursor

            from PySide2.QtWidgets import QApplication, QMessageBox, QPushButton, QFileDialog, QProgressBar, QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel, QLineEdit, QGroupBox, QComboBox, QCheckBox, QSpinBox, QTextEdit, QSpacerItem, QSizePolicy, QSplitter, QTabWidget, QWidget, QMainWindow, QScrollArea, QFormLayout, QStatusBar, QProxyStyle, QStyle, QAction

            from PySide2.QtCore import QObject, Signal, QTranslator, QCoreApplication, QEvent, Qt, QLocale, QTemporaryDir, QDir, QUrl, QSize, QSettings, QFileInfo, QRunnable, QThreadPool

        except:
            try:
                # PyQt5
                from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QCursor, QPalette, QBrush, QColor, QTextCursor

                from PyQt5.QtWidgets import QApplication, QMessageBox, QPushButton, QFileDialog, QProgressBar, QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel, QLineEdit, QGroupBox, QComboBox, QCheckBox, QSpinBox, QTextEdit, QSpacerItem, QSizePolicy, QSplitter, QTabWidget, QWidget, QMainWindow, QScrollArea, QFormLayout, QStatusBar, QProxyStyle, QStyle, QAction

                from PyQt5.QtCore import QObject, pyqtSignal as Signal, QTranslator, QCoreApplication, QEvent, Qt, QLocale, QTemporaryDir, QDir, QUrl, QSize, QSettings, QFileInfo, QRunnable, QThreadPool

            except:
                print("Impossible to find PySide6 / PyQt6 / PySide2 / PyQt5.<br>You need to install one of them !<br><br>PySide6: <b>pip3 install pyside6</b><br>PySide2: <b>sudo apt install python3-pyside2</b><br>PyQt5: <b>sudo apt install python3-pyqt5</b>")

                if which("kdialog"):
                    popen("""kdialog --error "Impossible to find PySide6 / PyQt6 / PySide2 / PyQt5.<br>You need to install one of them:<br><br>PySide6: <b>pip3 install pyside6</b><br>PySide2: <b>sudo apt install python3-pyside2</b><br>PyQt5: <b>sudo apt install python3-pyqt5</b>" """)

                elif which("zenity"):
                    popen("""zenity --error --no-wrap --text "Impossible to find PySide6 / PyQt6 / PySide2 / PyQt5.\nYou need to install one of them:\n\nPySide6: <b>pip3 install pyside6</b>\nPySide2: <b>sudo apt install python3-pyside2</b>\nPyQt5: <b>sudo apt install python3-pyqt5</b>" """)

                exit()


# Widgets personnalisés
from QWidgetsCustom.QCheckComboBox import QCheckComboBox
from QWidgetsCustom.QToolButtonCustom import QToolButtonCustom
from QWidgetsCustom.QPushQuitButton import QPushQuitButton
from QWidgetsCustom.QFlowLayout import QFlowLayout
from QWidgetsCustom.QDialogWhatsUp import QDialogWhatsUp



#############################################################################
## Fonction permettant d'améliorer la lisibilité des lignes de traductions ##
#############################################################################
translate = QCoreApplication.translate



##########################################################################
## Classe permettant de pas attendre avant l'affichage des infos bulles ##
##########################################################################
class MyProxyStyle(QProxyStyle):
    def styleHint(self, hint, option = None, widget = None, returnData = None):
        # On peut ajouter des conditions de fonctionnement sur certains widgets uniquement
        if hint == QStyle.SH_ToolTip_WakeUpDelay: return 0

        return QProxyStyle().styleHint(hint, option, widget, returnData);




########################################
## Classe travaillant en arrière plan ##
########################################
class ThreadSignals(QObject):
    # Indication de la valeur maximale de la barre de progression
    ProgressMax = Signal(int)

    # Incrémentation de la barre de progression
    ProgressPlus = Signal()

    # Message d'information à afficher
    Info = Signal(str)

    # Fin du travail demandé
    Finish = Signal()

    # Demande de création d'un onglet de recherche
    AddTab = Signal(str, int)

    # Demande de création d'un bouton de film
    AddMovie = Signal(str, object, int, int)

    # Affiche téléchargée
    DlFinish = Signal(str, object)



class ThreadActions(QRunnable):
    # https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    #========================================================================
    def __init__(self, *args, **kwargs):
        super(ThreadActions, self).__init__()

        ### Chargement des signaux
        self.Signals = ThreadSignals()

        ### Vérification qu'il y a bien une action
        if 'Action' not in kwargs.keys():
            self.Signals.Info.emit(GlobalTr["ActionMissing"].format(GlobalTr["Error"]))
            self.Action = None

        else:
            self.Action = kwargs['Action']

        ### Vérifications
        # Vérifie que l'action est connue
        if self.Action not in ["Movies", "MoviePictures", "DownloadPictures"]:
            self.Signals.Info.emit(GlobalTr["ActionUnknow"].format(GlobalTr["Error"]))

        # Vérifie les présences des arguments pour l'action Movies
        if self.Action == "Movies":
            if 'Names' not in kwargs.keys() or not len(kwargs['Names']):
                self.Signals.Info.emit(GlobalTr["NameMissing"].format(GlobalTr["Error"]))
                self.Action = None

            self.Names = kwargs['Names']

        # Vérifie les présences des arguments pour l'action MoviePictures
        elif self.Action == "MoviePictures":
            for Arg in ['Id','Name', 'DownloadFolder']:
                if Arg not in kwargs.keys() or not kwargs[Arg]:
                    self.Signals.Info.emit(GlobalTr["ArgMissing"].format(GlobalTr["Error"], "MoviePictures", GlobalTr[Arg]))
                    self.Action = None

            self.Id = kwargs['Id']
            self.Name = kwargs['Name']
            self.DownloadFolder = kwargs['DownloadFolder']

        # Vérifie les présences des arguments pour l'action DownloadPictures
        elif self.Action == "DownloadPictures":
            for Arg in ['Folder','URLBase', 'Name']:
                if Arg not in kwargs.keys() or not kwargs[Arg]:
                    self.Signals.Info.emit(GlobalTr["ArgMissing"].format(GlobalTr["Error"], "DownloadPictures", GlobalTr[Arg]))
                    self.Action = None

            self.Folder = kwargs['Folder']
            self.URLBase = kwargs['URLBase']
            self.Name = kwargs['Name']

            if 'Data' in kwargs.keys() and kwargs['Data']: self.Data = kwargs['Data']
            else: self.Data = None

            if 'Search' in kwargs.keys() and kwargs['Search']: self.Search = kwargs['Search']
            else: self.Search = None

            if 'Index' in kwargs.keys() and kwargs['Index']: self.Index = kwargs['Index']
            else: self.Index = None

            if 'NbMovie' in kwargs.keys() and kwargs['NbMovie']: self.NbMovie = kwargs['NbMovie']
            else: self.NbMovie = 0


        ### Headers pour les requêtes
        self.Headers = { 'Authorization': f"Bearer {Global['Token']}", 'Content-Type': "application/json;charset=utf-8" }
        self.TimeOut = (2, 2)


    #========================================================================
    def run(self):
        # Lancement de la fonction demandée
        if self.Action == "Movies":
            self.threadpool = QThreadPool()
            self.Movies()

        elif self.Action == "MoviePictures":
            self.threadpool = QThreadPool()
            self.MoviePictures()

        elif self.Action == "DownloadPictures":
            self.DownloadPictures()

        if self.Action != "DownloadPictures" and not Global['StopThread']:
            # Signal indiquant la fin du travail
            self.Signals.Finish.emit()


    #========================================================================
    ### Fonction de recherche des films
    def Movies(self):
        # Recherche des films 1 à 1
        for Name in self.Names:
            self.Signals.Info.emit(GlobalTr["SearchStarts"].format(GlobalTr["InfoBlue"], Name))

            # Liste des films regroupés si plusieurs pages
            AllMovies = []

            # Nettoyage du nom et des accents
            NameFinded = Name.lower().replace("*", "")
            NameFinded = unidecode(NameFinded)

            # Langue du texte
            Language = "fr-FR" if Global["Language"] == "Français" else "en_US"

            # Nombre de page à télécharger
            for Page in range(1, Global["NbPage"] + 1):
                # Stoppe le travail si clic sur le bouton stop
                if Global['StopThread']: return

                self.Signals.Info.emit(GlobalTr["ReadingPage"].format(GlobalTr["InfoBlue"], Page))

                Try = 0
                while True:
                    # Nombre de tentative
                    Try += 1
                    if Try > Global['TryMax']:
                        self.Signals.Info.emit("{} {} {}".format(GlobalTr["Error"], GlobalTr['ErrorMovies'], GlobalTr['TryMax']))
                        break

                    # Envoi de la requête à l'API de TMDB
                    try:
                        Requete = requests.get("https://api.themoviedb.org/4/search/movie?language={}&query={}&page={}".format(Language, NameFinded.replace(" ", "%20"), Page), headers=self.Headers, timeout=self.TimeOut)

                    # En cas d'échec de connexion, on relance la fonction
                    except:
                        self.Signals.Info.emit("{} {} {}".format(GlobalTr["Error"], GlobalTr['ErrorMovies'], GlobalTr['TryAgain']))
                        continue

                    # Si le code retour n'est pas 200, on relance la fonction
                    if Requete.status_code != 200:
                        self.Signals.Info.emit("{} {} {}".format(GlobalTr["Error"], GlobalTr['ErrorMovies'], GlobalTr['TryAgain']))
                        continue

                    break

                # Remplissage de la liste des films retournés
                for Movie in Requete.json()['results']:
                    # Stoppe le travail si clic sur le bouton stop
                    if Global['StopThread']: return

                    MovieOK = False
                    for Title in ["title", "original_title"]:
                        # Nettoyage du nom
                        TitleFinded = Movie[Title].lower()
                        TitleFinded = unidecode(TitleFinded)

                        # Si l'étoile est utilisée dans la recherche
                        if "*" in Name:
                            # Si le nom est entouré, on le reprend
                            if Name[0] != "*" or Name[-1] != "*":
                                # Si le nom doit commencer par... (Iron*)
                                if Name[-1] == "*" and not TitleFinded.startswith(NameFinded): continue

                                # Si le nom doit finir par... (Iron*)
                                if Name[0] == "*" and not TitleFinded.endswith(NameFinded): continue

                        # Sinon, c'est qu'on veut le nom exacte
                        else:
                            if NameFinded != TitleFinded: continue

                        MovieOK = True
                        break

                    if not MovieOK:
                        continue

                    # Ne traite pas les films sans poster
                    if 'poster_path' not in Movie.keys() or not Movie['poster_path']: continue

                    # indique une date par défaut
                    if 'release_date' not in Movie.keys() or not Movie['release_date']: Movie['release_date'] = "9999-99-99"

                    AllMovies.append(Movie)

                # Si on a atteint le nombre de page possible
                if Requete.json()['total_pages'] == Page: break


            # Nombre de film renvoyé
            NbMovie = len(AllMovies)

            # Si aucun film n'a été renvoyé
            if not NbMovie:
                self.Signals.Info.emit(GlobalTr["NoMovieReturns"].format(GlobalTr["InfoOrange"], Name))
                self.Signals.ProgressPlus.emit()
                continue

            # Signal de création
            self.Signals.AddTab.emit(Name, NbMovie)

            # Traitement du retour, la variable est rangée par date et nom
            Global["WorkChecker"] = []
            for Index, Movie in enumerate(sorted(AllMovies, key=lambda k: (k['release_date'], k['title']))):
                # Stoppe le travail si clic sur le bouton stop
                if Global['StopThread']: return

                Global["WorkChecker"].append(Movie['poster_path'])

                # Création et lancement des téléchargement d'image en parallèle
                # Attention, les signaux doivent renvoyer vers les mêmes du parent, impossible d'en changer ?!
                Work = ThreadActions(Action = "DownloadPictures", Folder = Global['TempFolder'], URLBase = "https://image.tmdb.org/t/p/w500", Name = Movie['poster_path'], Search = Name, Data = Movie, Index = Index, NbMovie = NbMovie)
                Work.Signals.Info.connect(self.Signals.Info)
                Work.Signals.AddMovie.connect(self.Signals.AddMovie)
                self.threadpool.start(Work)

            # Attend que tous les fichiers soient traités
            while len(Global["WorkChecker"]):
                # Stoppe le travail si clic sur le bouton stop
                if Global['StopThread']: break

                # Micro sleep
                sleep(0.2)

            # Attend avec PySide2 qui est plus long ?!!
            if PySideVersion != 6: sleep(5)


            # Quand la recherche a été traitée, on fait progresser la barre
            self.Signals.ProgressPlus.emit()


            # Envoi du signal indiquant que les recherches sont terminées
            self.Signals.Info.emit(GlobalTr["SearchFinish"].format(GlobalTr["InfoBlue"], Name))


    #========================================================================
    ### Fonction de recherche des films
    def MoviePictures(self):
        # Stoppe le travail si clic sur le bouton stop
        if Global['StopThread']: return

        # Recherche des posters du film
        self.Signals.Info.emit(GlobalTr["SearchPosters"].format(GlobalTr["InfoBlue"], self.Name, self.Id))

        Try = 0
        while True:
            # Nombre de tentative
            Try += 1
            if Try > Global['TryMax']:
                self.Signals.Info.emit("{} {} {}".format(GlobalTr["Error"], GlobalTr['MoviePictures'], GlobalTr['TryMax']))
                return

            # Envoi de la requête à l'API de TMDB
            try:
                Requete = requests.get("https://api.themoviedb.org/3/movie/{}/images?language=fr-FR&include_image_language={}".format(self.Id, ','.join(Global['ImagesLanguages'])), headers=self.Headers, timeout=self.TimeOut)

            # En cas d'échec de connexion, on relance la fonction
            except:
                self.Signals.Info.emit("{} {} {}".format(GlobalTr["Error"], GlobalTr['MoviePictures'], GlobalTr['TryAgain']))
                continue

            # Si le code retour n'est pas 200, on relance la fonction
            if Requete.status_code != 200:
                self.Signals.Info.emit("{} {} {}".format(GlobalTr["Error"], GlobalTr['MoviePictures'], GlobalTr['TryAgain']))
                continue

            break

        # Dossier de téléchargement, DownloadFolder est un str
        QDir().mkpath(self.DownloadFolder)
        DownloadSubFolder = QDir(self.DownloadFolder)

        # Arrêt de la fonction si aucune image à dl
        if not len(Requete.json()['posters']):
            # Bar de progression
            self.Signals.ProgressPlus.emit()

            return

        # Précise le nombre de poster pour la barre de progression
        self.Signals.ProgressMax.emit(len(Requete.json()['posters']))

        # Traitement du retour, la variable est rangée par date et nom
        Global["WorkChecker"] = []
        for Return in Requete.json()['posters']:
            # Stoppe le travail si clic sur le bouton stop
            if Global['StopThread']: return

            Global["WorkChecker"].append(Return['file_path'])

            # Télécharge les affiches en parallèle
            Work = ThreadActions(Action = "DownloadPictures", Folder = DownloadSubFolder, URLBase = "https://image.tmdb.org/t/p/original", Name = Return['file_path'])
            Work.Signals.ProgressPlus.connect(self.Signals.ProgressPlus)
            Work.Signals.Info.connect(self.Signals.Info)
            self.threadpool.start(Work)


        # Attend que tous les fichiers soient traités
        while len(Global["WorkChecker"]):
            # Stoppe le travail si clic sur le bouton stop
            if Global['StopThread']: break

            # Micro sleep
            sleep(0.2)


        # Ouverture automatique du dossier l'option est active'
        if Global['AutoOpenDownloadFolder']:
            self.Signals.Info.emit(GlobalTr["AutoOpenFolder"].format(GlobalTr["InfoBlue"], self.Name))
            QDesktopServices.openUrl(QUrl.fromLocalFile(DownloadSubFolder.absolutePath()))

        else:
            self.Signals.Info.emit(GlobalTr["SearchPostersFinish"].format(GlobalTr["InfoBlue"], self.Name))


    #========================================================================
    ## Fonction de téléchargement des images
    def DownloadPictures(self):
        # Stoppe le travail si clic sur le bouton stop
        if Global['StopThread']: return

        if not self.Folder.exists():
            self.Signals.Info.emit(GlobalTr["FolderNotExists"].format(GlobalTr["Error"], self.Folder.absolutePath()))
            Global["WorkChecker"].remove(self.Name)
            self.Signals.AddMovie.emit(self.Name, self.Data, self.Index, 0)
            return

        Name = self.Name[1:]

        Try = 0
        while True:
            # Nombre de tentative
            Try += 1
            if Try > Global['TryMax']:
                self.Signals.Info.emit("{} {}: {} {}".format(GlobalTr["Error"], Name, GlobalTr['ErrorDownloadPictures'], GlobalTr['TryMax']))
                return

            # Stoppe le travail si clic sur le bouton stop
            if Global['StopThread']: return

            # Envoi de la requête à l'API de TMDB
            try:
                Requete = requests.get(self.URLBase + self.Name, headers=self.Headers, stream=True, timeout=self.TimeOut)

            # En cas d'échec de connexion, on relance la fonction
            except:
                self.Signals.Info.emit("{} {}: {} {}".format(GlobalTr["Error"], Name, GlobalTr['ErrorDownloadPictures'], GlobalTr['TryAgain']))
                continue

            # Si le code retour n'est pas 200, on relance la fonction
            if Requete.status_code != 200:
                self.Signals.Info.emit("{} {}: {} {}".format(GlobalTr["Error"], Name, GlobalTr['ErrorDownloadPictures'], GlobalTr['TryAgain']))
                continue

            # Sauvegarde du poster sur le disque
            with open(f"{self.Folder.absolutePath()}/{self.Name}", 'wb') as out_file:
                copyfileobj(Requete.raw, out_file)

            # Signaux pas forcément utilisés
            self.Signals.AddMovie.emit(self.Search, self.Data, self.Index, self.NbMovie)
            self.Signals.Info.emit(GlobalTr["PosterDownloaded"].format(GlobalTr["InfoGreen"], self.Name[1:], self.Folder.absolutePath()))
            self.Signals.ProgressPlus.emit()

            Global["WorkChecker"].remove(self.Name)

            break



#############################################################################
class WinHizoTMDB(QMainWindow):
    """Fenêtre de configuration du code."""
    def __init__(self, Parent=None):
        super().__init__(Parent)

        # Obligé de le mettre là sinon la création des QPixmap avant le self font planter...
        from LanguageList import LanguageList

        # Variables
        self.AutoDlToolButton = None
        self.threadpool = QThreadPool()
        self.MoviesTab = {}

        ### Fenêtre
        self.setWindowFlags(Qt.WindowTitleHint)
        self.setMinimumWidth(840)
        self.setMinimumHeight(400)
        self.resize(Global['WinWidth'], Global['WinHeight'])
        self.setWindowTitle("{} v{}".format(QCoreApplication.applicationName(), QCoreApplication.applicationVersion()))
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Acceptation du glisser déposer
        self.setAcceptDrops(True)

        # Status Bar
        self.StatusBar = QStatusBar(self)
        self.setStatusBar(self.StatusBar)

        # Ajout d'un bouton quitter dans la status bar
        self.ButtonQuit = QPushQuitButton(None)
        self.ButtonQuit.setIcon(QIcon.fromTheme("application-exit", QIcon("Ressources:application-exit.svg")))
        self.ButtonQuit.clicked.connect(self.close)
        self.ButtonQuit.rebootSignal.connect(self.rebootEvent)
        self.StatusBar.addPermanentWidget(self.ButtonQuit)
        self.StatusBar.setSizeGripEnabled(False)

        # Ajout du bouton A propos dans la status bar
        self.AboutButton = QPushButton()
        self.AboutButton.setIcon(QIcon.fromTheme("help-about", QIcon("Ressources:application-exit.svg")))
        self.AboutButton.clicked.connect(self.About)
        self.StatusBar.addWidget(self.AboutButton)

        # Layout principal
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        WinVLayout = QVBoxLayout(self.centralwidget)

        # Grand splitter
        self.WinSplitter = QSplitter(Qt.Vertical, self.centralwidget)
        self.WinSplitter.setChildrenCollapsible(False)
        WinVLayout.addWidget(self.WinSplitter)

        ### Partie haute avec le splitter et son layout
        self.TopSplitter = QSplitter(self.WinSplitter)
        self.TopSplitter.setChildrenCollapsible(False)

        ### Gestion de la box des noms de film à rechercher
        # Box
        self.MoviesSearchedBox = QGroupBox(self.TopSplitter)
        self.MoviesSearchedBox.setMinimumWidth(200)
        MoviesSearchedVLayout = QVBoxLayout(self.MoviesSearchedBox)

        # Zone de texte
        self.MoviesSearchedTextEdit = QPlainTextEdit(self.MoviesSearchedBox)
        #self.MoviesSearchedTextEdit.setAcceptDrops(True)
        MoviesSearchedVLayout.addWidget(self.MoviesSearchedTextEdit)

        MoviesSearchedHLayout = QHBoxLayout(None)
        MoviesSearchedVLayout.addLayout(MoviesSearchedHLayout)

        # Icône d'aide
        Icon = QIcon.fromTheme("documentinfo", QIcon("Ressources:documentinfo.svg")).pixmap(24, 24)
        self.MoviesSearchedLabel = QLabel()
        self.MoviesSearchedLabel.setPixmap(Icon)
        MoviesSearchedHLayout.addWidget(self.MoviesSearchedLabel)

        MoviesSearchedSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        MoviesSearchedHLayout.addItem(MoviesSearchedSpacer2)

        # Bouton de recherche
        self.MoviesSearchedButton = QPushButton(QIcon.fromTheme("edit-find", QIcon("Ressources:edit-find.svg")), "")
        MoviesSearchedHLayout.addWidget(self.MoviesSearchedButton)
        self.MoviesSearchedButton.clicked.connect(self.LaunchMovieSearch)


        ### Gestion de la box des retours et de la progression
        # Box
        self.ProgressBox = QGroupBox(self.TopSplitter)
        ProgressVLayout = QVBoxLayout(self.ProgressBox)

        # Zone de texte
        self.ProgressTextEdit = QTextEdit(self.ProgressBox)
        self.ProgressTextEdit.setAcceptDrops(False)
        self.ProgressTextEdit.setReadOnly(True)
        self.ProgressTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ProgressTextEdit.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        ProgressVLayout.addWidget(self.ProgressTextEdit)


        # Barre de progression
        ProgressHLayout = QHBoxLayout(None)
        ProgressVLayout.addLayout(ProgressHLayout)
        self.ProgressBar = QProgressBar(self.ProgressBox)
        self.ProgressBar.setFormat("%v / %m")
        ProgressHLayout.addWidget(self.ProgressBar)

        # Bouton d'annulation
        self.ProgressButton = QPushButton(QIcon.fromTheme("dialog-cancel", QIcon("Ressources:dialog-cancel.svg")), "")
        self.ProgressButton.clicked.connect(self.StopWorkinProgress)
        self.ProgressButton.setEnabled(False)
        ProgressHLayout.addWidget(self.ProgressButton)


        ### Gestion de la box des configs, utilisation de labels pour permettre leur traduction
        self.ConfigsBox = QGroupBox(self.TopSplitter)
        self.ConfigsBox.setMinimumWidth(375)
        ConfigLayout1 = QVBoxLayout(self.ConfigsBox)

        ConfigWidget = QWidget(None)

        ConfigScroll = QScrollArea(self.ConfigsBox)
        ConfigScroll.setWidgetResizable(True)
        ConfigScroll.setWidget(ConfigWidget)
        ConfigLayout1.addWidget(ConfigScroll)

        ProgressFLayout = QFormLayout(ConfigWidget)

        self.TokenWidget = QLineEdit(Global['Token'], self.ConfigsBox)
        self.TokenWidget.setClearButtonEnabled(True)
        self.TokenWidget.textChanged.connect(self.UpadeToken)
        self.TokenLabel = QLabel()
        ProgressFLayout.addRow(self.TokenLabel, self.TokenWidget)

        self.DownloadFolderWidget = QLineEdit(DownloadFolder.absolutePath(), self.ConfigsBox)
        self.DownloadFolderAction = QAction(QIcon.fromTheme("folder", QIcon("Ressources:folder.svg")), "", self.DownloadFolderWidget)
        self.DownloadFolderAction.triggered.connect(self.SelectOutputFolder)
        self.DownloadFolderWidget.addAction(self.DownloadFolderAction, QLineEdit.LeadingPosition)
        self.DownloadFolderWidget.setClearButtonEnabled(True)
        self.DownloadFolderWidget.setText(Global['DownloadFolder'].absolutePath())
        self.DownloadFolderWidget.textEdited.connect(self.UpadeDownloadFolder)
        self.DownloadFolderWidget.setMinimumWidth(150)
        self.DownloadFolderLabel = QLabel()
        ProgressFLayout.addRow(self.DownloadFolderLabel, self.DownloadFolderWidget)

        self.ImagesLanguagesWidget = QCheckComboBox(self.ConfigsBox)
        self.ImagesLanguagesWidget.addItems(LanguageList + [{"text": 'null - Aucune', "data": "null"}])
        self.ImagesLanguagesWidget.setStateItems(Qt.Checked, Global['ImagesLanguages'], False, False)
        self.ImagesLanguagesWidget.currentTextChanged.connect(self.UpadeImagesLanguages)
        self.ImagesLanguagesWidget.setMinimumWidth(150)

        self.ImagesLanguagesWidget.setDefaultValues([
            {"value": "fr", "state":Qt.Checked},
            {"value": "en", "state":Qt.Checked},
            {"value": "null", "state":Qt.Checked},
            ])

        self.ImagesLanguagesWidget.setIcons({
            "Copy": QIcon.fromTheme("edit-select-text", QIcon("Ressources:edit-select-text")),
            "Undo": QIcon.fromTheme("edit-undo", QIcon("Ressources:edit-undo")),
            "Redo": QIcon.fromTheme("edit-redo", QIcon("Ressources:edit-redo")),
            "AllCheck": QIcon.fromTheme("edit-select-all", QIcon("Ressources:edit-select-all")),
            "AllUncheck": QIcon.fromTheme("edit-select-none", QIcon("Ressources:edit-select-none")),
            "DefaultValues": QIcon.fromTheme("edit-reset", QIcon("Ressources:edit-reset"))
            })

        self.ImagesLanguagesLabel = QLabel()
        ProgressFLayout.addRow(self.ImagesLanguagesLabel, self.ImagesLanguagesWidget)

        self.ImageSizeWidget = QSpinBox(self.ConfigsBox)
        self.ImageSizeWidget.setMinimum(50)
        self.ImageSizeWidget.setMaximum(500)
        self.ImageSizeWidget.setSuffix("px")
        self.ImageSizeWidget.setValue(Global['ImageSize'])
        self.ImageSizeWidget.valueChanged.connect(self.UpadeImageSize)
        self.ImageSizeWidget.setMinimumWidth(150)
        self.ImageSizeLabel = QLabel()
        ProgressFLayout.addRow(self.ImageSizeLabel, self.ImageSizeWidget)

        self.NbPageWidget = QSpinBox(self.ConfigsBox)
        self.NbPageWidget.setMinimum(1)
        self.NbPageWidget.setMaximum(20)
        self.NbPageWidget.setValue(Global['NbPage'])
        self.NbPageWidget.valueChanged.connect(self.UpadeNbPage)
        self.NbPageWidget.setMinimumWidth(150)
        self.NbPageLabel = QLabel()
        ProgressFLayout.addRow(self.NbPageLabel, self.NbPageWidget)

        self.TryMaxWidget = QSpinBox(self.ConfigsBox)
        self.TryMaxWidget.setMinimum(1)
        self.TryMaxWidget.setMaximum(20)
        self.TryMaxWidget.setValue(Global['TryMax'])
        self.TryMaxWidget.valueChanged.connect(self.UpadeTryMax)
        self.TryMaxWidget.setMinimumWidth(150)
        self.TryMaxLabel = QLabel()
        ProgressFLayout.addRow(self.TryMaxLabel, self.TryMaxWidget)

        self.AutoOpenDownloadFolderWidget = QCheckBox(self.ConfigsBox)
        self.AutoOpenDownloadFolderWidget.setChecked(Global['AutoOpenDownloadFolder'])
        self.AutoOpenDownloadFolderWidget.stateChanged.connect(self.UpdateAutoOpenDownloadFolder)
        self.AutoOpenDownloadFolderLabel = QLabel()
        ProgressFLayout.addRow(self.AutoOpenDownloadFolderLabel, self.AutoOpenDownloadFolderWidget)

        self.AutoDlWidget = QCheckBox(self.ConfigsBox)
        self.AutoDlWidget.setChecked(Global['AutoDl'])
        self.AutoDlWidget.stateChanged.connect(self.UpdateAutoDlWidget)
        self.AutoDlLabel = QLabel()
        ProgressFLayout.addRow(self.AutoDlLabel, self.AutoDlWidget)

        self.AutoSearchWidget = QCheckBox(self.ConfigsBox)
        self.AutoSearchWidget.setChecked(Global['AutoSearch'])
        self.AutoSearchWidget.stateChanged.connect(self.UpdateAutoSearchWidget)
        self.AutoSearchLabel = QLabel()
        ProgressFLayout.addRow(self.AutoSearchLabel, self.AutoSearchWidget)

        self.LanguageWidget = QComboBox(self.ConfigsBox)
        self.LanguageWidget.addItem(QIcon("Flags:en.svg"), "English")
        self.LanguageWidget.addItem(QIcon("Flags:fr.svg"), "Français")
        self.LanguageWidget.currentTextChanged.connect(self.UpdateLanguage)
        self.LanguageWidget.setMinimumWidth(150)
        self.LanguageLabel = QLabel()
        ProgressFLayout.addRow(self.LanguageLabel, self.LanguageWidget)


        ### Gestion de la box de la liste des films
        self.MoviesFindedBox = QGroupBox(self.WinSplitter)
        self.MoviesFindedBox.setMinimumHeight(200)
        MoviesFindedHLayout = QVBoxLayout(self.MoviesFindedBox)

        # Onglets des films
        self.MoviesFindedTab = QTabWidget(self.MoviesFindedBox)
        self.MoviesFindedTab.setTabsClosable(True)
        self.MoviesFindedTab.tabCloseRequested.connect(self.RemoveMovieTab)
        MoviesFindedHLayout.addWidget(self.MoviesFindedTab)

        # Répartition du WinSplitter
        if Global['WinSplitter'] == [0, 0]:
            # 25% pour le TopSplitter dans la limite de 300px
            SubWinSplitter1 = (self.width() * 25) / 100
            if SubWinSplitter1 > 300: SubWinSplitter1 = 300
            SubWinSplitter2 = self.width() - SubWinSplitter1
            self.WinSplitter.setSizes([SubWinSplitter1, SubWinSplitter2])

        else:
            self.WinSplitter.setSizes(Global['WinSplitter'])

        # Répartition du TopSplitter
        if Global['TopSplitter'] == [0, 0]:
            #45% pour le MoviesSearchedBox dans la limite de 400px
            SubTopSplitter1 = (self.width() * 45) / 100
            if SubTopSplitter1 > 400: SubTopSplitter1 = 400
            SubTopSplitter2 = self.width() - SubTopSplitter1
            self.TopSplitter.setSizes([SubTopSplitter1, SubTopSplitter2])

        else:
            self.TopSplitter.setSizes(Global['TopSplitter'])


        # Installation des filtres des événements
        self.MoviesFindedTab.installEventFilter(self)
        self.MoviesSearchedTextEdit.installEventFilter(self)

        # Chargement de la langues, force l'anglais
        if Global["Language"] == "Français": self.LanguageWidget.setCurrentText("Français")
        else: self.UpdateLanguage("English")


        # Si des arguments ont été reçus
        if len(sys.argv) > 1: self.MovieNamesCleaner(sys.argv[1:])

        # Affichage de la fenêtre
        self.show()

        # Mise à jour du texte avec ...
        #self.ImagesLanguagesWidget.updateText()

        ## Débloque ou non les actions si les variables sont OK
        self.UnlockActions()

        # Lancement automatique de la recherche
        if Global['AutoSearch']:
            self.LaunchMovieSearch()


    #========================================================================
    def eventFilter(self, Object, Event):
        """Filtre sur les événements."""
        # Fermeture des onglets eu clic molette
        if Object == self.MoviesFindedTab:
            if Event.type() == QEvent.Type.MouseButtonRelease:
                if Event.button() == Qt.MouseButton.MiddleButton:
                    TabIndex = self.MoviesFindedTab.tabBar().tabAt(Event.position().toPoint())
                    self.RemoveMovieTab(TabIndex)

        # Lors de l'utilisation de ctrl + entrée dans QTextEdit des noms de films
        elif Object == self.MoviesSearchedTextEdit:
            if Event.type() == QEvent.Type.KeyRelease:
                if Event.modifiers() == Qt.ControlModifier:
                    # Il semble que la touche entrée du pavé numérique ne se cumule pas avec ctrl
                    if Event.key() in [Qt.Key_Enter, Qt.Key_Return]:
                        self.MoviesSearchedButton.click()

        return False


    #========================================================================
    def MovieNamesCleaner(self, Values):
        """Fonction de nettoyage des noms de film."""
        for Value in Values:
            if type(Value) == QUrl: Value = Value.toDisplayString()

            # Supprime l'adresse du dossier
            NameWithExt = Value
            if "/" in Value: NameWithExt = Value.split("/")[-1]

            # Supprime l'extension
            Name = NameWithExt
            if "." in NameWithExt: Name = ''.join(NameWithExt.split(".")[0:-1])

            # Ajout du nom
            self.MoviesSearchedTextEdit.appendPlainText(Name)


    #========================================================================
    def UnlockActions(self):
        """Fonction débloquant le bouton de recherche."""
        if Global['Token'] and Global['ImagesLanguages'] and Global['DownloadFolder']:
            self.MoviesSearchedButton.setEnabled(True)

            # Bloque les boutons des films
            for MovieName in self.MoviesTab.keys():
                if "QToolButton" in self.MoviesTab[MovieName]:
                    for Button in self.MoviesTab[MovieName]['QToolButton']:
                        Button.setEnabled(True)

        else:
            self.MoviesSearchedButton.setEnabled(False)

            # Bloque les boutons des films
            for MovieName in self.MoviesTab.keys():
                if "QToolButton" in self.MoviesTab[MovieName]:
                    for Button in self.MoviesTab[MovieName]['QToolButton']:
                        Button.setEnabled(False)


    #========================================================================
    def LaunchMovieSearch(self):
        """Fonction de lancement de la recherche des films."""
        # Récupération des noms de films séparés par un saut de ligne
        Names = self.MoviesSearchedTextEdit.toPlainText().split('\n')

        # Suppression des lignes vides
        while True:
            try: Names.remove('')
            except: break

        # Vérifie qu'il y a bien au moins une recherche à effectuer
        if not len(Names): return

        # Indique le nombre de recherche à effectuer à la barre de progression
        self.ProgressBar.setMaximum(len(Names))

        # Grisage des widgets
        self.WorkInProgress()

        # Recrée le dossier si besoin
        if not Global['TempFolder'].exists(): QDir().mkpath(Global['TempFolder'].absolutePath())

        # Création et exécution du thread
        Work = ThreadActions(Action = "Movies", Names = Names)
        Work.Signals.AddTab.connect(self.AddMovieTab)
        Work.Signals.AddMovie.connect(self.AddMovieButton)
        Work.Signals.Info.connect(self.ViewInformations)
        Work.Signals.ProgressPlus.connect(self.ProgressBarValue)
        Work.Signals.Finish.connect(self.StopWorkinProgress)
        self.threadpool.start(Work)


    #========================================================================
    def AddMovieTab(self, MovieName, NbMovie):
        """Fonction ajoutant les retours des recherches."""
        # Suppression de l'ancien onglet si besoin
        if MovieName in self.MoviesTab.keys():
            self.RemoveMovieTab(MovieName)

        # Création de l'onglet
        self.MoviesTab[MovieName] = {}
        self.MoviesTab[MovieName]['QWidget1'] = QWidget(None)
        self.MoviesTab[MovieName]['QHBoxLayout1'] = QHBoxLayout(self.MoviesTab[MovieName]['QWidget1'])

        self.MoviesTab[MovieName]['QScrollArea'] = QScrollArea(self.MoviesTab[MovieName]['QWidget1'])
        self.MoviesTab[MovieName]['QScrollArea'].setWidgetResizable(True)
        self.MoviesTab[MovieName]['QHBoxLayout1'].addWidget(self.MoviesTab[MovieName]['QScrollArea'])

        self.MoviesTab[MovieName]['QWidget2'] = QWidget(self.MoviesTab[MovieName]['QScrollArea'])
        self.MoviesTab[MovieName]['QFlowLayout'] = QFlowLayout(self.MoviesTab[MovieName]['QWidget2'], 5, 5)

        self.MoviesTab[MovieName]['QScrollArea'].setWidget(self.MoviesTab[MovieName]['QWidget2'])

        self.MoviesTab[MovieName]['QToolButton'] = []

        # Ajout de l'onglet de la recherche
        self.MoviesTab[MovieName]['Index'] = self.MoviesFindedTab.addTab(self.MoviesTab[MovieName]['QWidget1'], GlobalTr["TabName"].format(MovieName, NbMovie))
        self.MoviesFindedTab.setTabWhatsThis(self.MoviesTab[MovieName]['Index'], MovieName)


    #========================================================================
    def AddMovieButton(self, MovieName, MovieInfos, Index, NbMovie = 0):
        """Fonction ajoutant les retours des recherches."""
        if MovieInfos['release_date'] == "9999-99-99": MovieInfos['release_date'] = GlobalTr["DateUnknow"]

        # Création du bouton
        QToolButton = QToolButtonCustom(self.MoviesTab[MovieName]['QWidget2'],
                                        ImageSize = Global['ImageSize'],
                                        id = MovieInfos['id'],
                                        icon = Global['TempFolder'].absolutePath() + MovieInfos['poster_path'],
                                        title = MovieInfos['title'],
                                        text = f"{MovieInfos['original_title']}\n{MovieInfos['release_date']}",
                                        tooltip = MovieInfos['overview'],
                                        DownloadFolder = Global['DownloadFolder'].absolutePath())

        QToolButton.clicked.connect(lambda: self.LaunchImagesDownload(QToolButton))
        self.MoviesTab[MovieName]['QFlowLayout'].insertWidget(Index, QToolButton)
        self.MoviesTab[MovieName]['QToolButton'] += [QToolButton]

        # Mode auto dl
        if NbMovie == 1 and Global['AutoDl']:
            self.AutoDlToolButton = QToolButton


    #========================================================================
    def RemoveMovieTab(self, Index):
        """Fonction supprimant les onglets des films au clic sur l'icône."""
        # Lorsque Appelée par AddMovieTab
        if isinstance(Index, str):
            for i in range(self.MoviesFindedTab.count()):
                MovieSearch = self.MoviesFindedTab.tabWhatsThis(i)
                if MovieSearch == Index:
                    Index = i
                    break

        # Récupération du nom de la recherche
        else:
            MovieSearch = self.MoviesFindedTab.tabWhatsThis(Index)

        # Supprime les widgets pour ne pas les recharger si on relance la même recherche
        if MovieSearch in self.MoviesTab.keys():
            self.MoviesTab[MovieSearch]['QWidget1'].deleteLater()
            del self.MoviesTab[MovieSearch]

        # Supprime l'onglet
        self.MoviesFindedTab.removeTab(Index)


    #========================================================================
    def LaunchImagesDownload(self, Widget):
        # Génère un nouveau dossier
        Widget.downloadFolder(Global["DownloadFolder"].absolutePath())

        # Grisage des widgets
        self.WorkInProgress()

        # Recrée le dossier si besoin
        if not Global['TempFolder'].exists():
            QDir().mkpath(Global['TempFolder'].absolutePath())

        # Création et exécution du thread
        Work = ThreadActions(Action = "MoviePictures", Id = Widget.id, Name = Widget.title, DownloadFolder = Widget.DownloadFolder)
        Work.Signals.Info.connect(self.ViewInformations)
        Work.Signals.ProgressMax.connect(self.ProgressBarMax)
        Work.Signals.ProgressPlus.connect(self.ProgressBarValue)
        Work.Signals.Finish.connect(self.StopWorkinProgress)
        self.threadpool.start(Work)


    #========================================================================
    def ViewInformations(self, Text):
        """Fonction affichant les retours du thread dans le QTextEdit."""
        self.ProgressTextEdit.append(Text)

        self.ProgressTextEdit.moveCursor(QTextCursor.End)


    #========================================================================
    def UpdateAutoDlWidget(self, AutoDlWidgetUpdated):
        """Fonction de mise à jour de l'option de téléchargement des posters s'il n'y a qu'un film trouvé."""
        # Mise à jour de la variable
        Global['AutoDl'] = AutoDlWidgetUpdated

        # Sauvegarde de la valeur dans le fichier de config
        Configs.setValue("hizo-tmdb/AutoDl", AutoDlWidgetUpdated)


    #========================================================================
    def UpdateAutoOpenDownloadFolder(self, AutoOpenDownloadFolderUpdated):
        """Fonction de mise à jour de l'option d'ouverture automatique des dossiers en fin de téléchargement."""
        # Mise à jour de la variable
        Global['AutoOpenDownloadFolder'] = AutoOpenDownloadFolderUpdated

        # Sauvegarde de la valeur dans le fichier de config
        Configs.setValue("hizo-tmdb/AutoOpenDownloadFolder", AutoOpenDownloadFolderUpdated)


    #========================================================================
    def UpdateAutoSearchWidget(self, AutoSearchWidgetUpdated):
        """Fonction de mise à jour de l'option de recherche automatique au lancement du logiciel."""
        # Mise à jour de la variable
        Global['AutoSearch'] = AutoSearchWidgetUpdated

        # Sauvegarde de la valeur dans le fichier de config
        Configs.setValue("hizo-tmdb/AutoSearch", AutoSearchWidgetUpdated)


    #========================================================================
    def UpadeImageSize(self, ImageSizeUpdated):
        """Fonction de mise à jour de la taille des vignettes."""
        # Mise à jour de la variable
        Global['ImageSize'] = ImageSizeUpdated

        # Sauvegarde de la valeur dans le fichier de config
        Configs.setValue("hizo-tmdb/ImageSize", ImageSizeUpdated)

        ## Mise à jour de la taille mini
        #self.MoviesFindedTab.setMinimumHeight(Global['ImageSize'] + 160)

        ## 940 by 685 pour des vignettes de 200px
        #self.setMinimumHeight(450 + ImageSizeUpdated)

        for MovieName in self.MoviesTab.keys():
            if "QToolButton" in self.MoviesTab[MovieName]:
                for Button in self.MoviesTab[MovieName]['QToolButton']:
                    Button.setIconSize(QSize(ImageSizeUpdated, ImageSizeUpdated))
                    Button.setMinimumWidth(ImageSizeUpdated)
                    Button.setMinimumHeight(ImageSizeUpdated)
                    Button.setMaximumWidth(ImageSizeUpdated)


    #========================================================================
    def UpadeNbPage(self, NbPageUpdated):
        """Fonction de mise à jour du nombre de page à télécharger."""
        # Mise à jour de la variable
        Global['NbPage'] = NbPageUpdated

        # Sauvegarde de la valeur dans le fichier de config
        Configs.setValue("hizo-tmdb/NbPage", NbPageUpdated)


    #========================================================================
    def UpadeTryMax(self, TryMaxUpdated):
        """Fonction de mise à jour du nombre de tentative de connexion."""
        # Mise à jour de la variable
        Global['TryMax'] = TryMaxUpdated

        # Sauvegarde de la valeur dans le fichier de config
        Configs.setValue("hizo-tmdb/TryMax", TryMaxUpdated)


    #========================================================================
    def UpadeToken(self, TokenUpdated):
        """Fonction de mise à jour du token."""
        if TokenUpdated:
            # Mise à jour de la variable
            Global['Token'] = TokenUpdated

            # Sauvegarde de la valeur dans le fichier de config
            Configs.setValue("hizo-tmdb/Token", TokenUpdated)

            # Remise en couleur normale
            self.TokenWidget.setPalette(self.TokenWidget.style().standardPalette())

        else:
            Global['Token'] = None

            # Colore le widget car la valeur n'est pas bonne
            self.TokenWidget.setPalette(PalettesWigets["LineEdit"])

        # Fonction de déblocage du bouton de lancement de la recherche de film
        self.UnlockActions()


    #========================================================================
    def UpadeImagesLanguages(self, ImagesLanguagesUpdated):
        """Fonction de mise à jour des langues des affiches."""
        # Si c'est le titre lors de la création, on le bloque
        if ImagesLanguagesUpdated == translate("ConfigBox", "Languages available:"):
            return

        # Si la sélection du dossier est OK
        if ImagesLanguagesUpdated:
            # Mise à jour de la variable
            Global['ImagesLanguages'] = self.ImagesLanguagesWidget.currentData()

            # Sauvegarde de la valeur dans le fichier de config
            Configs.setValue("hizo-tmdb/ImagesLanguages", Global['ImagesLanguages'])

            # Remise en couleur normale
            self.ImagesLanguagesWidget.setPalette(self.ImagesLanguagesWidget.style().standardPalette())

        else:
            Global['ImagesLanguages'] = None

            # Colore le widget car la valeur n'est pas bonne
            self.ImagesLanguagesWidget.setPalette(PalettesWigets["LineEdit"])

        # Fonction de déblocage du bouton de lancement de la recherche de film
        self.UnlockActions()


    #========================================================================
    def UpadeDownloadFolder(self, DownloadFolderUpdated):
        """Fonction de mise à jour du dossier de téléchargement."""
        # Si la sélection du dossier est OK
        if DownloadFolderUpdated:
            # Mise à jour de la variable
            Global['DownloadFolder'] = QDir(DownloadFolderUpdated)

            # Sauvegarde de la valeur dans le fichier de config
            Configs.setValue("hizo-tmdb/DownloadFolder", DownloadFolderUpdated)

            # Remise en couleur normale
            self.DownloadFolderWidget.setPalette(self.DownloadFolderWidget.style().standardPalette())

        else:
            Global['DownloadFolder'] = None

            # Colore le widget car la valeur n'est pas bonne
            self.DownloadFolderWidget.setPalette(PalettesWigets["LineEdit"])

        # Fonction de déblocage du bouton de lancement de la recherche de film
        self.UnlockActions()


    #========================================================================
    def UpdateLanguage(self, Value):
        """Fonction appelée via la combobox de la langue du soft ou au début du script qui recharge les traductions."""
        # pylupdate5 *.py -ts Languages/hizo-tmdb_fr_FR.ts Languages/hizo-tmdb_en_EN.ts # -noobsolete
        # lrelease Languages/*.ts

        # Suppression de la traduction actuelle
        HizoTMDB.removeTranslator(Global["QTranslator"])

        # Langue à utiliser
        File = "hizo-tmdb_fr_FR" if Value in (1, "Français") else "hizo-tmdb_en_EN"

        # Mise à jour du fichier langage de Qt, ne semble pas fonctionner... du coup traduction des quelques mots manuellement

        # Mise à jour de la langue du logiciel
        if Global["QTranslator"].load(File, f"{AbsoluteFolder}/Languages"):
            HizoTMDB.installTranslator(Global["QTranslator"])

        # En cas d'erreur de chargement de la traduction
        else:
            QMessageBox(QMessageBox.Critical, translate("UpdateLanguage", "Translation error"), translate("UpdateLanguage", "No <b>French</b> translation files found.<br/>Use of <b>English language</b>."), QMessageBox.Close, None, Qt.WindowSystemMenuHint).exec()


        # Mise à jour de la variable
        Global["Language"] = "Français" if Value in (1, "Français") else "English"

        # Sauvegarde de la valeur dans le fichier de config
        Configs.setValue("hizo-tmdb/Language", Value)


        # Le changement de langue exécute l'événement changeEvent
        # Cela crée un décalage, l'event est traité plus tard
        # il vaut mieux le faire ici

        # Widgets de la fenêtre principale
        self.ButtonQuit.setText(translate("MainWindow", "Exit"))
        self.AboutButton.setText(translate("MainWindow", "About"))

        # Widgets de la SearchBox
        self.MoviesSearchedButton.setText(translate("SearchBox", "Start search"))
        self.MoviesSearchedBox.setTitle(translate("SearchBox", "Movie names searched:"))
        self.MoviesSearchedButton.setStatusTip(translate("SearchBox", "Start the movies searching."))
        self.MoviesSearchedLabel.setToolTip(translate("SearchBox", "Movie's names to search on <b>The Movie Data Base</b>.<br><br>Rules:<br> - Only one search per line.<br> - Exact names (not case sensitive).<br> - Use *'s for extended search.<br> - Name must be completed enough to be found. <br><br>Examples:<br> - Iron Man: Will return movies with the name iron man.<br> - Iron*: Will return all movies whose name starts with iron.<br> - *Man: Will return all movies whose name ends with man.<br> - *Man*: Will return all movies whose name includes man.<br><br>ctrl + enter launches the search."))

        # Widgets de la ProgressBox
        self.ProgressButton.setStatusTip(translate("ProgressBox", "Stop the work in progress..."))
        self.ProgressButton.setText(translate("ProgressBox", "Stop work"))
        self.ProgressBox.setTitle(translate("ProgressBox", "Returns and progression:"))

        ### Widgets de la ConfigBox
        self.ConfigsBox.setTitle(translate("ConfigBox", "Configuration:"))

        self.NbPageLabel.setText(translate("ConfigBox", "Nb Page to Download:"))
        self.NbPageWidget.setSuffix(translate("ConfigBox", " page(s)"))
        self.NbPageWidget.setStatusTip(translate("ConfigBox", "Number of page to download during the movies search. Between 1 page and 20 pages."))

        self.TryMaxLabel.setText(translate("ConfigBox", "Max Connection Try:"))
        self.TryMaxWidget.setStatusTip(translate("ConfigBox", "Number of connection attempts to the TMDB's API. Between 1 and 20 try."))

        self.DownloadFolderLabel.setText(translate("ConfigBox", "Download Folder:"))
        self.DownloadFolderAction.setText(translate("ConfigBox", "Folder Selector"))
        self.DownloadFolderWidget.setStatusTip(translate("ConfigBox", "Mandatory: The folder where create the movie folders uses to download posters."))

        self.TokenLabel.setText(translate("ConfigBox", "Token:"))
        self.TokenWidget.setStatusTip(translate("ConfigBox", "Mandatory: The token to connect at the The Movie Data Base API v4."))

        self.ImageSizeLabel.setText(translate("ConfigBox", "Thumb Size:"))
        self.ImageSizeWidget.setStatusTip(translate("ConfigBox", "The size of the thumbnails' movie. Between 50px and 500px."))

        self.AutoOpenDownloadFolderLabel.setText(translate("ConfigBox", "Auto Open Folder:"))
        self.AutoOpenDownloadFolderWidget.setStatusTip(translate("ConfigBox", "Enable/disable the auto open download folder when posters' download finished."))

        self.AutoDlLabel.setText(translate("ConfigBox", "Auto Download Posters:"))
        self.AutoDlWidget.setStatusTip(translate("ConfigBox", "Enable/disable the auto download of the posters when only one movie finded."))

        self.AutoSearchLabel.setText(translate("ConfigBox", "Auto Search Starter:"))
        self.AutoSearchWidget.setStatusTip(translate("ConfigBox", "Enable/disable the auto search at software start if there is search value."))

        self.LanguageLabel.setText(translate("ConfigBox", "GUI Language:"))
        self.LanguageWidget.setStatusTip(translate("ConfigBox", "Language of the GUI. The texts are changed in live."))

        self.ImagesLanguagesLabel.setText(translate("ConfigBox", "Posters' Languages:"))
        self.ImagesLanguagesWidget.setStatusTip(translate("ConfigBox", "Mandatory: The posters' languages to download."))
        # Les icônes plantent PyQt5
        if PySideVersion == 6: self.ImagesLanguagesWidget.setTitle(translate("ConfigBox", "Languages available:"), QIcon.fromTheme("languages", QIcon("Ressources:edit-undo.svg")))
        self.ImagesLanguagesWidget.contextMenuUpdate()
        self.ImagesLanguagesWidget.updateText()

        # Widgets de la ReturnBox
        self.MoviesFindedBox.setTitle(translate("ReturnBox", "Movies finded:"))

        # Mise à jour des textes des QToolButtonCustom
        for MovieName in self.MoviesTab.keys():
            if "QToolButton" in self.MoviesTab[MovieName]:
                for Button in self.MoviesTab[MovieName]['QToolButton']:
                    Button.updateLang()

        # QStatusTip en cours
        self.StatusBar.clearMessage()

        # Dictionnaire de traduction global pour les messages d'erreur
        GlobalTr["Error"] = translate("ErrorMessage", "[<span style='color:red;'>ERROR</span>]")
        GlobalTr["InfoGreen"] = translate("InfoMessage", "[<span style='color:green;'>INFO</span>]")
        GlobalTr["InfoBlue"] = translate("InfoMessage", "[<span style='color:blue;'>INFO</span>]")
        GlobalTr["InfoOrange"] = translate("InfoMessage", "[<span style='color:orange;'>INFO</span>]")
        GlobalTr["ErrorMovies"] = translate("InfoMessage", "An error occurred during the search for the film,")
        GlobalTr["ErrorLanguages"] = translate("InfoMessage", "An error occurred while searching for the languages,")
        GlobalTr["MoviePictures"] = translate("InfoMessage", "An error occurred while searching for the posters of the film,")
        GlobalTr['ErrorDownloadPictures'] = translate("InfoMessage", "An error occurred while downloading this poster,")
        GlobalTr["TryAgain"] = translate("InfoMessage", "try again...")
        GlobalTr["TryMax"] = translate("InfoMessage", "max number of try reached.")
        GlobalTr["TabName"] = translate("InfoMessage", "{} ({} results)", "{Name of the movie} ({Number of movie returns by the search} results)")
        GlobalTr["DateUnknow"] = translate("InfoMessage", "Date unknow")
        GlobalTr["DownloadFolderTitle"] = translate("ConfigBox", "Select the download folder")
        GlobalTr["AutoDl"] = translate("InfoMessage", "{} Auto download the movie's posters.<br>", "[INFO] Auto download the movie's posters.<br>")
        GlobalTr["AboutQt"] = translate("About", "About Qt")
        GlobalTr["WhatsUp"] = translate("About", "What's up ?")
        GlobalTr["Changelog"] = translate("About", "Changelog of hizo-tmdb")
        GlobalTr["About"] = translate("About", "About hizo-tmdb")
        GlobalTr["Close"] = translate("About", "Close")
        GlobalTr["hizo-tmdb"] = translate("About", """<html><head/><body><p align="center"><span style=" font-size:12pt; font-weight:600;">hizo-tmdb v{}</span></p><p><span style=" font-size:10pt;">GUI to download movie's posters from the <a href="https://www.themoviedb.org/"><b>TMDB</b> website</a>.</span></p><p><span style=" font-size:10pt;">This software is programed in python3 + QT6 (PySide6) and is licensed under </span><span style=" font-size:8pt; font-weight:600;"><a href="{}">GNU GPL v3</a></span><span style=" font-size:8pt;">.</span></p><p>&nbsp;</p><p align="right">Created by <span style=" font-weight:600;">Belleguic Terence</span> (<a href="mailto:hizo@free.fr">Hizoka</a>), 2021</p></body></html>""")

        GlobalTr["ActionMissing"] = translate("ErrorMessage", "{} An error occurred while using the thread, <b>it is missing the action</b>.", "{} = [ERROR]")
        GlobalTr["ActionUnknow"] = translate("ErrorMessage", "{} An error occurred while using the thread, <b>the action is unknown</b>.", "{} = [ERROR]")
        GlobalTr["NameMissing"] = translate("ErrorMessage", "{} An error occurred when using the Movies function, <b>the movie names</b> are missing.", "{} = [ERROR]")
        GlobalTr["ArgMissing"] = translate("ErrorMessage", "{0} An error occurred while using the MoviePictures function, <b>{1}</b> is missing.", "{0} = [ERROR], {1} = function name, {2} = Argument name")
        GlobalTr["SearchStarts"] = translate("InfoMessage", "{0} Launching the search for <b>{1}</b>.", "{0} = [INFO], {1} = ")
        GlobalTr["ReadingPage"] = translate("InfoMessage", "{0} Reading of the <b>page n°{1}</b>.", "{0} = [INFO], {1} = Page number")
        GlobalTr["NoMovieReturns"] = translate("InfoMessage", "{0} Searching for <b>{1}</b> did not return any movies.<br>", "{0} = [INFO], {1} = Text searched")
        GlobalTr["SearchFinish"] = translate("InfoMessage", "{0} Search for the <b>{1}</b> movie completed.<br>", "{0} = [INFO], {1} = Text searched")
        GlobalTr["SearchPosters"] = translate("InfoMessage", "{0} Search the posters of the movie: <b>{1}</b> ({2}).", "{0} = [INFO], {1} = Movie name, {2} = Movie id")
        GlobalTr["AutoOpenFolder"] = translate("InfoMessage", "{0} Search for {1} movie posters completed, automatic opening of folder.<br>", "{0} = [INFO], {1} = Number of poster downloaded")
        GlobalTr["SearchPostersFinish"] = translate("InfoMessage", "{0} Search for posters of the film {1} completed.<br>", "{0} = [INFO], {1} = Movie name")
        GlobalTr["FolderNotExists"] = translate("ErrorMessage", "{0} The folder {1} <b>does not exist</b> !", "{0} = [ERROR], {1} = Folder path")
        GlobalTr["PosterDownloaded"] = translate("InfoMessage", "{0} {1} donwloaded into the folder {2}.", "{0} = [INFO], {1} = Poster name, {2} = Download folder path")
        GlobalTr["Id"] = translate("ErrorMessage", "the id")
        GlobalTr["Name"] = translate("ErrorMessage", "the name")
        GlobalTr["DownloadFolder"] = translate("ErrorMessage", "the download folder")
        GlobalTr["Folder"] = translate("ErrorMessage", "the download folder")
        GlobalTr["URLBase"] = translate("ErrorMessage", "the url base")


    #========================================================================
    def SelectOutputFolder(self):
        """Fonction de modification du dossier d'enregistrement des images."""
        # fenêtre de sélection du dossier de téléchargement
        DownloadFolderTemp = QFileDialog.getExistingDirectory(self, GlobalTr["DownloadFolderTitle"], Global['DownloadFolder'].absolutePath(), QFileDialog.ShowDirsOnly)

        # Si la sélection du dossier est OK
        if DownloadFolderTemp:
            # Mise à jour du widget
            self.DownloadFolderWidget.setText(DownloadFolderTemp)


    #========================================================================
    def ProgressBarMax(self, Value):
        """Fonction mettant à jour la valeur maximale de la barre de progression."""
        self.ProgressBar.setMaximum(Value)


    #========================================================================
    def ProgressBarValue(self):
        """Fonction incrémentant d'1 la barre de progression."""
        self.ProgressBar.setValue(self.ProgressBar.value() + 1)


    #========================================================================
    def WorkInProgress(self):
        """Fonction Appelée au lancement d'un travail afin de (dé)bloquer les widgets."""
        # Variable en cas de demande d'arrêt du travail en cours
        Global['StopThread'] = False

        # Remise à 0 de la barre de progression
        self.ProgressBar.setValue(0)

        # (Dé)Bloque différents widgets
        self.MoviesSearchedTextEdit.setEnabled(False)
        self.MoviesSearchedButton.setEnabled(False)
        self.ProgressButton.setEnabled(True)

        # Bloque les options
        for Widget in self.ConfigsBox.children(): Widget.setEnabled(False)

        # Bloque les boutons des films
        for MovieName in self.MoviesTab.keys():
            if "QToolButton" in self.MoviesTab[MovieName]:
                for Button in self.MoviesTab[MovieName]['QToolButton']:
                    Button.setEnabled(False)


    #========================================================================
    def StopWorkinProgress(self):
        """Fonction Appelée à l'arrêt d'un travail afin de (dé)bloquer les widgets."""
        # Mode auto download
        if self.AutoDlToolButton:
            self.ViewInformations(GlobalTr["AutoDl"].format(GlobalTr["InfoBlue"]))
            self.LaunchImagesDownload(self.AutoDlToolButton)
            self.AutoDlToolButton = None
            return

        # Variable permettant au travail en cours de s'arrêter
        Global['StopThread'] = True

        # (Dé)Bloque différents widgets
        self.MoviesSearchedTextEdit.setEnabled(True)
        self.MoviesSearchedButton.setEnabled(True)
        self.ProgressButton.setEnabled(False)

        # Débloque les options
        for Widget in self.ConfigsBox.children(): Widget.setEnabled(True)

        # Débloque les boutons des films
        for MovieName in self.MoviesTab.keys():
            if "QToolButton" in self.MoviesTab[MovieName]:
                for Button in self.MoviesTab[MovieName]['QToolButton']:
                    Button.setEnabled(True)


    #========================================================================
    def About(self):
        """Fonction affichant une fenêtre d'information sur le soft."""
        ### Bouton Qt
        AboutQt = QPushButton(QIcon.fromTheme("qt", QIcon("Ressources:qt.png")), GlobalTr["AboutQt"], self)
        AboutQt.clicked.connect(lambda: QMessageBox.aboutQt(self))

        ### Bouton Changelog
        WhatUpButton = QPushButton(QIcon.fromTheme("text-x-texinfo", QIcon("Ressources:text-x-texinfo.svg")), GlobalTr["WhatsUp"], self)
        WhatUpButton.clicked.connect(lambda: QDialogWhatsUp('/usr/share/doc/hizo-tmdb/changelog.Debian.gz', 'hizo-tmdb', GlobalTr["Changelog"], GlobalTr["Close"], self))


        ### Fenêtre d'info
        Win = QMessageBox(QMessageBox.NoIcon,
                          GlobalTr["About"],
                          GlobalTr["hizo-tmdb"].format(HizoTMDB.applicationVersion(), "http://www.gnu.org/copyleft/gpl.html"),
                          QMessageBox.Close, self)

        Win.setIconPixmap(QPixmap(QIcon.fromTheme("hizo-tmdb", QIcon("Ressources:hizo-tmdb.png")).pixmap(175)))
        Win.setMinimumWidth(800)
        Win.addButton(AboutQt, QMessageBox.HelpRole)
        Win.setDefaultButton(QMessageBox.Close)
        Win.button(Win.Close).setText(GlobalTr["Close"])

        # Ajoute le bouton quoi de neuf si le fichier existe
        if QDir().exists('/usr/share/doc/hizo-tmdb/changelog.Debian.gz'): Win.addButton(WhatUpButton, QMessageBox.HelpRole)

        Win.exec()

        ### Relance la fenêtre si on a cliqué sur les boutons AboutQt ou WhatUpButton
        if Win.clickedButton() in (AboutQt, WhatUpButton): self.About()


    #========================================================================
    def dragEnterEvent(self, event):
        """Fonction acceptant de glisser des fichiers sur la fenêtre."""
        event.accept()


    #========================================================================
    def dropEvent(self, event):
        """Fonction traitant les déposer de fichiers sur la fenêtre pour les ajouter à la liste des recherches."""
        self.MovieNamesCleaner(event.mimeData().urls())

        event.accept()


    #========================================================================
    def preClose(self):
        # Curseur de chargement
        self.setCursor(Qt.WaitCursor)

        # Arrêt du travail en cours
        Global['StopThread'] = True
        #if "ExtractionThread" in dir(self) and self.ExtractionThread.isRunning():
            #self.ExtractionThread.terminate()
            #Global['StopThread'] = True
            #self.ExtractionThread.wait()

        # Sauvegarde de la taille de la fenêtre
        Configs.setValue("hizo-tmdb/WinWidth", self.width())
        Configs.setValue("hizo-tmdb/WinHeight", self.height())

        # Sauvegarde de la taille des Splitters
        Configs.setValue("hizo-tmdb/WinSplitter", self.WinSplitter.sizes())
        Configs.setValue("hizo-tmdb/TopSplitter", self.TopSplitter.sizes())

        # Force l'écriture dans le fichier de config'
        Configs.sync()

        # Suppression du dossier temporaire
        if Global['TempFolder'].exists(): Global['TempFolder'].removeRecursively()

        # Curseur normal
        self.setCursor(Qt.ArrowCursor)


    #========================================================================
    def closeEvent(self, event):
        # Traitement avant la fermeture
        self.preClose()

        # Acceptation de la fermeture
        event.accept()


    #========================================================================
    def rebootEvent(self):
        """Ce n'est pas un vrai event, il est émit par le clic droit du bouton quitter."""
        # Traitement avant la fermeture
        self.preClose()

        # Restart de la commande
        python = sys.executable
        execl(python, python, * sys.argv)


#############################################################################
if __name__ == '__main__':
    ####################
    ### QApplication ###
    ####################
    ### Gestion de l'emplacement du script
    FileURL = QFileInfo(sys.argv[0])

    while FileURL.isSymLink():
        FileURL = QFileInfo(FileURL.symLinkTarget())

    AbsoluteFolder = FileURL.absolutePath()

    ### Gestion des ressources
    QDir.addSearchPath('Ressources', f"{AbsoluteFolder}/Ressources/")
    QDir.addSearchPath('Flags', f"{AbsoluteFolder}/Flags/")

    # Ajout du chargement de la feuille de style
    args = list(sys.argv)
    args[1:1] = ['-stylesheet', f'{AbsoluteFolder}/Styles.qss']

    # Création de l'application
    HizoTMDB = QApplication(args)
    HizoTMDB.setApplicationVersion("22-08-12.0") # Version de l'application
    HizoTMDB.setApplicationName("HizoTMDB") # Nom de l'application
    HizoTMDB.setWindowIcon(QIcon.fromTheme("hizo-tmdb", QIcon("Ressources:hizo-tmdb.png"))) # Icône de l'application

    MyStyle = MyProxyStyle()
    HizoTMDB.setStyle(MyStyle)

    ### Système de gestion des configurations QSettings
    ## Création ou ouverture du fichier de config
    Configs = QSettings(QSettings.NativeFormat, QSettings.UserScope, "hizo-service-menus")

    # Ne conserve que les valeurs du bloc hizo-tmdb, les autres ne sont pas pour ce soft
    # utilisation d'un Dictionnaire car ils sont globaux de base, donc pas besoin d'utiliser global
    Global = {}
    Global['StopThread'] = False

    Global['Token'] = Configs.value("hizo-tmdb/Token")
    Global['ImageSize'] = int(Configs.value("hizo-tmdb/ImageSize", 200))
    Global['NbPage'] = int(Configs.value("hizo-tmdb/NbPage", 1))
    Global['WinWidth'] = int(Configs.value("hizo-tmdb/WinWidth", 650))
    Global['WinHeight'] = int(Configs.value("hizo-tmdb/WinHeight", 550))
    Global['AutoOpenDownloadFolder'] = int(Configs.value("hizo-tmdb/AutoOpenDownloadFolder", 0))
    Global['AutoDl'] = int(Configs.value("hizo-tmdb/AutoDl", 0))
    Global['AutoSearch'] = int(Configs.value("hizo-tmdb/AutoSearch", 1))
    Global['TryMax'] = int(Configs.value("hizo-tmdb/TryMax", 5))

    # Langues des affiches
    Global['ImagesLanguages'] = Configs.value("hizo-tmdb/ImagesLanguages", ["en", "fr", "null"])
    if isinstance(Global['ImagesLanguages'], str):
        Global['ImagesLanguages'] = Global['ImagesLanguages'].split(", ")

    # Pour ces valeurs, il faut que ce soit des int et non des str
    Global['WinSplitter'] = list(Configs.value("hizo-tmdb/WinSplitter", [0, 0]))
    for i, element in enumerate(Global['WinSplitter']): Global['WinSplitter'][i] = int(element)

    Global['TopSplitter'] = list(Configs.value("hizo-tmdb/TopSplitter", [0, 0]))
    for i, element in enumerate(Global['TopSplitter']): Global['TopSplitter'][i] = int(element)


    ### Dossiers
    # Création du dossier temporaire
    TempFolder = QTemporaryDir(QDir.tempPath() + "/HizoTMDB").path()
    QDir().mkpath(TempFolder)
    Global['TempFolder'] = QDir(TempFolder)

    # Dossier de téléchargement
    DownloadFolder = Configs.value("hizo-tmdb/DownloadFolder")

    if not DownloadFolder:
        DownloadFolder = QDir(QDir().absolutePath())
        if not DownloadFolder.absolutePath().startswith("/home"): DownloadFolder = QDir(QDir().homePath())

    else:
        DownloadFolder = QDir(DownloadFolder)

    Global['DownloadFolder'] = DownloadFolder


    ### Traductions
    # pylupdate5 *.py QWidgetsCustom/*.py -ts Languages/hizo-tmdb_fr_FR.ts Languages/hizo-tmdb_en_EN.ts # -noobsolete
    # lrelease Languages/*.ts
    Global['Language'] = Configs.value("hizo-tmdb/Language", QLocale().nativeLanguageName().capitalize())
    Global["QTranslator"] = QTranslator() # Création d'un QTranslator
    GlobalTr = {}


    ### Dictionnaires permettant de mettre en avant certains widgets
    PalettesWigets = {}
    PalettesWigets["LineEdit"] = QPalette()
    brush = QBrush(QColor(255, 255, 125))
    brush.setStyle(Qt.SolidPattern)
    PalettesWigets["LineEdit"].setBrush(QPalette.Active, QPalette.Base, brush)


    ### Permet d'éviter les fameux Erreur de segmentation (core dumped)
    QCoreApplication.processEvents()

    HizoTMDBClass = WinHizoTMDB()

    QCoreApplication.processEvents()

    if PySideVersion == 6:
        # PySide6
        sys.exit(HizoTMDB.exec())

    else:
        # PySide2
        sys.exit(HizoTMDB.exec_())
