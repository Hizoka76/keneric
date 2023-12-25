# Fichiers desktop

## Version Française :
### Explications :
Ces fichiers font le lien entre le navigateur de fichiers (comme Dolphin ou Konqueror) et keneric.

Le navigateur de fichiers reconnait ces fichiers desktop comme des générateurs de vignettes, ils sont (dés)activables dans Dolphin : Configurer > Configurer Dolphin > Genéral > Aperçu

Lorsque le navigateur verra un élément au mimetype déclaré dans un de ces fichiers desktop, il appelera keneric afin qu'il lui fournisse une vignette.

Les fichiers desktop doivent être placés dans un dossier défini par la commande :
```
kf5-config --path services
```

### Définition d'un fichier desktop :
```
[Desktop Entry]
Type=Service
Name=XXXXX

X-KDE-ServiceTypes=ThumbCreator
MimeType=YYYYY;

X-KDE-Library=keneric
CacheThumbnail=true
```
XXXXX : Nom du générateur qui sera affiché dans le navigateur de fichiers.

YYYYY : Mimetypes concernés par ce fichier desktop, exemples :
 - video/*
 - */x-matroska
 - video/x-matroska
 - video/x-matroska;video/x-matroska-3d;application/x-matroska;application/x-matroska-3d;


## English version:
### Explanations:
These files form the link between the file browser (such as Dolphin or Konqueror) and keneric.

The file browser recognizes these desktop files as thumbnail generators, and they can be (des)activated in Dolphin: Configure > Configure Dolphin > General > Preview.

When the browser sees an element with the declared mimetype in one of these desktop files, it will call keneric to provide a thumbnail.

Desktop files must be placed in a folder defined by the command:
```
kf5-config --path services
```

### Defining a desktop file:
```
[Desktop Entry]
Type=Service
Name=XXXXX

X-KDE-ServiceTypes=ThumbCreator
MimeType=YYYYY;

X-KDE-Library=keneric
CacheThumbnail=true
```
XXXXX : Name of the generator to be displayed in the file browser.

YYYYY: Mimetypes affected by this desktop file, e.g. :
 - video/*
 - */x-matroska
 - video/x-matroska
 - video/x-matroska;video/x-matroska-3d;application/x-matroska;application/x-matroska-3d;
