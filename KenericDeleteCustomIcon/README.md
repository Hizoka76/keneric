# KenericDeleteCustomIcon

## Version Française :
### Présentation :
Ce service menu permet de supprimer les vignettes personnalisées des éléments sélectionnés.

Il modifie le fichier ~/.config/keneric.conf

### Installation :
Le fichier keneric-delete-custom-icon.desktop doit être mis dans un dossier du path de kde5 :
```
kf5-config --path services
```
Le fichier keneric-delete-custom-icon doit être mis dans le path :
```
echo "$PATH"
```

### Utilisation :
Il suffit de faire un clic droit sur l'élément (fichier ou dossier) puis de choisir "Keneric Actions" et enfin "Supprimer le lien de la vignette personnalisée".


## English version:
### Presentation:
This service menu allows to copy in the clipboard the md5 hash of the selected item.

Thus, it is easy to find the thumbnail in the ~/.cache/thumbnails folder or to customize the icon of the item in the Keneric config file.

### Installation:
The keneric-delete-custom-icon.desktop file should be put in a folder in the kde5 path:
```
kf5-config --path services
```
The keneric-delete-custom-icon must be put in the path :
```
echo "$PATH"
```

### Usage:
Just right click on the item (file or folder) then choose "Keneric Actions" and finally "Remove the custom thumbnail link".
