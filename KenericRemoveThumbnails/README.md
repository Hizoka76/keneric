# KenericRemoveThumbnails

## Version Française :
### Présentation :
Ce service menu permet de supprimer les vignettes des éléments sélectionnés etde recharger l'affichage de Dolphin.

### Installation :
Le fichier keneric-remove-thumbnails.desktop doit être mis dans un dossier du path de kde5 :
```
kf5-config --path services
```
Le fichier keneric-remove-thumbnails doit être mis dans le path :
```
echo "$PATH"
```

### Utilisation :
Il suffit de faire un clic droit sur l'élément (fichier ou dossier) puis de choisir "Keneric Actions" et enfin "Copier le hash md5 du fichier".


## English version:
### Presentation:
This menu service allows to copy in the clipboard the md5 hash of the selected item.

Thus, it is easy to find the thumbnail in the ~/.cache/thumbnails folder or to customize the icon of the item in the Keneric config file.

### Installation:
The keneric-hash-file.desktop file should be put in a folder in the kde5 path:
```
kf5-config --path services
```
The keneric-hash-file must be put in the path :
```
echo "$PATH"
```

### Usage:
Just right click on the item (file or folder) then choose "Keneric Actions" and finally "Copy the md5 hash of the file".
