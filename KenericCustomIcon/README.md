# KenericCustomIcon

## Version Française :
### Présentation :
Ce service menu permet de seléctionner une image à utiliser comme vignette personnalisée.

Il modifie le fichier ~/.config/keneric.conf

### Installation :
Le fichier keneric-custom-icon.desktop doit être mis dans un dossier du path de kde5 :
```
kf5-config --path services
```
Le fichier keneric-custom-icon doit être mis dans le path :
```
echo "$PATH"
```

### Utilisation :
Faire un clic droit sur les éléments (fichiers ou dossiers) puis de choisir "Keneric Actions" et enfin "Choisir une vignette personnalisée".
Chercher l'image à utiliser comme vignette dans le selécteur de fichier.
Si KenericRemoveThumbnails est installé il sera exécuté afin de supprimer l'ancienne vignette du fichier, dans le cas contraire, c'est à vous de la supprimer.


## English version:
### Presentation:
This service menu allows you to delete custom thumbnails of selected items.

It changes the ~/.config/keneric.conf file.

### Installation:
The keneric-custom-icon.desktop file should be put in a folder in the kde5 path:
```
kf5-config --path services
```
The keneric-custom-icon must be put in the path :
```
echo "$PATH"
```

### Usage:
Right-click on items (files or folders) then choose "Keneric Actions" and finally "Choose a custom thumbnail".
Search for the image you wish to use as a thumbnail in the file browser.
If KenericRemoveThumbnails is installed, it will be run to remove the old thumbnail from the file; otherwise, it's up to you to remove it.
