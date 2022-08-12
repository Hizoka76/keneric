#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Fenêtre affichant le changelog demandé.
Le nom du soft est coloré comme tous les textes entre (), [] et <>.
"""

### Importation de gzip permettant de lire le fichier changelog compressé
import gzip
import sys

try:
    # Modules PySide6
    from PySide6.QtGui import QTextCursor
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QApplication, QTextEdit, QDialogButtonBox, QHBoxLayout
    from PySide6.QtCore import Qt, QFileInfo

except:
    try:
        # Modules PySide2
        from PySide2.QtGui import QTextCursor
        from PySide2.QtWidgets import QDialog, QVBoxLayout, QApplication, QTextEdit, QDialogButtonBox, QHBoxLayout
        from PySide2.QtCore import Qt, QFileInfo

    except:
        try:
            # Modules PyQt5
            from PyQt5.QtGui import QTextCursor
            from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication, QTextEdit, QDialogButtonBox, QHBoxLayout
            from PyQt5.QtCore import Qt, QFileInfo

        except:
            print("QDialogWhatsUp : Impossible de trouver PySide6 / PySide2 / PyQt5.")
            exit()




#############################################################################
class QDialogWhatsUp(QDialog):
    """Fenêtre affichant le changelog."""
    def __init__(self, File, SoftName, Title, Close=None, Parent=None):
        super().__init__(Parent)

        ### Création de la fenêtre
        Dialog = QDialog(self)
        Dialog.setWindowTitle(Title)
        Dialog.setAttribute(Qt.WA_DeleteOnClose)
        Dialog.setMinimumHeight(400)
        Dialog.setMinimumWidth(500)

        ### Création du QTextEdit
        Text = QTextEdit(Dialog)
        Text.setReadOnly(True)
        Text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        Text.setLineWrapMode(QTextEdit.WidgetWidth)

        ### Lecture du fichier changelog
        with gzip.open(File, 'rb') as f:
            file_content = f.read()

        ### Lecture ligne par ligne du texte
        for Line in file_content.decode('utf-8').split("\n"):
            NewLine = Line

            ## Coloration du nom du soft
            if SoftName in Line:
                NewLine = NewLine.replace(SoftName, '<span style="color:red">{}</span>'.format(SoftName))

            ## Coloration du texte entre parenthèses
            if "(" in Line:
                text = Line.split("(")[1].split(")")[0]
                NewLine = NewLine.replace(text, '<span style="color:blue">{}</span>'.format(text))

            ## Coloration du texte entre crochets
            if "[" in Line:
                text = Line.split("[")[1].split("]")[0]
                NewLine = NewLine.replace(text, '<span style="color:green">{}</span>'.format(text))

            ## Coloration du texte entre crochets
            if "<" in Line:
                text = Line.split("<")[1].split(">")[0]
                NewLine = NewLine.replace("<{}>".format(text), '&lt;<span style="color:gray">{}</span>&gt;'.format(text))

            ## Coloration du nom du créateur
            if "Belleguic Terence" in Line or "hizoka" in Line or "Hizoka" in Line:
                NewLine = NewLine.replace("Belleguic Terence", '<span style="color:darkblue">Belleguic Terence</span>')
                NewLine = NewLine.replace("Hizoka", '<span style="color:darkblue">Hizoka</span>')
                NewLine = NewLine.replace("hizoka", '<span style="color:darkblue">Hizoka</span>')

            ## Envoie de la ligne dans le widget
            Text.append(NewLine)

        ### Placement en haut du texte
        Text.moveCursor(QTextCursor.Start)

        ### Bouton de sortie
        Button = QDialogButtonBox(QDialogButtonBox.Close, Dialog)
        if Close: Button.button(Button.Close).setText(Close)
        Button.clicked.connect(Dialog.close)

        ### Présentation de la fenêtre
        Layout1 = QHBoxLayout()
        Layout1.addStretch()
        Layout1.addWidget(Button)

        Layout2 = QVBoxLayout()
        Layout2.addWidget(Text)
        Layout2.addLayout(Layout1)

        Dialog.setLayout(Layout2)

        ### Affichage de la fenêtre
        Dialog.exec()


#############################################################################
if __name__ == '__main__':
    ### Arg 1 : Nom du fichir gz à lire
    ### Arg 2 : Nom du paquet à colorer
    ### Arg 3 : Titre de la fenêtre
    ### Arg 4 : Parent pour bien placer la fenêtre et utiliser son icône

    ### Vérification du nombre d'argument
    if len(sys.argv) < 4:
        sys.exit(1)

    ### Vérification du fichier
    if not QFileInfo(sys.argv[1]).exists() or not QFileInfo(sys.argv[1]).isFile():
        sys.exit(1)

    ### Lancement du soft
    app = QApplication(sys.argv)
    app.setApplicationVersion("1.0")
    app.setApplicationName("WhatsUp")
    WhatsUpClass = QDialogWhatsUp(sys.argv[1], sys.argv[2], sys.argv[3])
    WhatsUpClass.setAttribute(Qt.WA_DeleteOnClose)
    sys.exit(app.exec())
