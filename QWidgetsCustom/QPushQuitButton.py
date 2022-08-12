#!/bin/python3
# This Python file uses the following encoding: utf-8

try:
    # Modules PySide6
    from PySide6.QtWidgets import QApplication, QPushButton
    from PySide6.QtCore import Qt, Signal

except:
    try:
        # Modules PySide2
        from PySide2.QtWidgets import QApplication, QPushButton
        from PySide2.QtCore import Qt, Signal

    except:
        try:
            # Modules PyQt5
            from PyQt5.QtWidgets import QApplication, QPushButton
            from PyQt5.QtCore import Qt, pyqtSignal as Signal

        except:
            print("QPushQuitButton : Impossible de trouver PySide6 / PySide2 / PyQt5.")
            exit()



class QPushQuitButton(QPushButton):
    """QPushButton prenant en compte un clic droit et renvoyant un signal."""
    rebootSignal = Signal()

    def __init__(self, Parent=None):
        super().__init__(Parent)


    def mouseReleaseEvent(self, event):
        """Fonction de récup des clics souris utilisées."""

        ### Envoi du signal si c'est un clic droit qui a été relâché
        if event.button() == Qt.RightButton: self.rebootSignal.emit()

        # Acceptation de l'événement'
        super().mouseReleaseEvent(event)
