# keneric.conf

## Version Française :
### Fichier keneric.so :
J'ai ajouté la prise en charge d'un fichier de config par keneric.so.

Ce fichier doit être placé dans le dossier de config (généralement ~/.config/keneric.conf).

Il peut contenir differents groupes :
 - icons :
```
[icons]
# Le fichier au hash md5 d06329310e5224bf069270f88cee59ad doit utiliser l'image /home/hizoka/icone.png comme vignette. 
d06329310e5224bf069270f88cee59ad=/home/hizoka/icone.png
```
 - Type de lélément :
```
[x-matroska]
# Le type de fichier x-matroska doit être dans le dossier /home/hizoka/Movies/
# ou le dossier /home/hizoka/OtherMovies/ pour afficher une vignette, sinon le fichier est ignoré.
itemsAuthorized=/home/hizoka/Movies/, /home/hizoka/OtherMovies/

# Le type de fichier x-matroska sera ignoré s'il se trouve dans le dossier /home/hizoka/Movies/HD.
itemsProhibited=/home/hizoka/Movies/HD

# Lorsque les 2 options sont actives, le fichier x-matroska doit les respecter toutes les 2.
# Il doit se trouver dans le dossier /home/hizoka/Movies/ et sa descendence.
# Mais il ne doit pas être dans le dossier /home/hizoka/Movies/HD ou descendence.

# Si l'adresse fini par un /, seuls ses descendants sont concernés.
# Si elle ne finit par par un /, le dossier et ses descendants sont concernés.
```
 - Famille de l'élément :
```
[video]
itemsAuthorized=...
itemsProhibited=...
```
 - all (tous les éléments) :
```
[all]
itemsAuthorized=...
itemsProhibited=...
```

L'ordre ci-dessus est important, car c'est celui utilisé par keneric.so pour décider de son action. L'ordre des éléments dans le fichier conf est sans importance.

La casse doit être respectée !! (icons != IconS)

Les types de fichiers qui seront utilisés sont ceux définis dans les fichiers desktop.

### Script keneric :
Le script keneric accepte 2 variables en lien avec le mode debug.
```
[global]
LogEnabled=1
LogFile=/tmp/keneric.conf
```
 - LogEnabled à 1 active le mode debug. Attention à ne pas le laisser par erreur !
 - LogFile est le fichier log vaut /tmp/keneric.conf par défaut.


## English version:
### keneric.so File:
I have added support for a config file by keneric.so.

This file must be placed in the config folder (usually ~/.config/keneric.conf).

It can contain different groups :
 - icons :
```
[icons]
# The file with hash md5 d06329310e5224bf069270f88cee59ad must use the image /home/hizoka/icone.png as thumbnail. 
d06329310e5224bf069270f88cee59ad=/home/hizoka/icone.png
```
 - Mime type:
```
[x-matroska]
# The x-matroska file type must be in the /home/hizoka/Movies/ folder
# or in the /home/hizoka/OtherMovies/ folder to display a thumbnail, otherwise the file is ignored.
itemsAuthorized=/home/hizoka/Movies/, /home/hizoka/OtherMovies/

# The x-matroska file type will be ignored if it is in the /home/hizoka/Movies/HD folder.
itemsProhibited=/home/hizoka/Movies/HD

# When both options are active, the x-matroska file must respect both of them.
# It must be in the folder /home/hizoka/Movies/ or its descendants.
# But it must not be in the /home/hizoka/Movies/HD folder or its descendants.

# If the address ends with a /, only its descendants are concerned.
# If it does not end with a /, the folder and its descendants are concerned.
```
 - Family of the item:
```
[video]
itemsAuthorized=...
itemsProhibited=...
```
 - all (all items) :
```
[all]
itemsAuthorized=...
itemsProhibited=...
```

The above order is important, as it is the order used by keneric.so to decide its action. The order of the items in the conf file is not important.

The case must be respected! (icons != IconS)

The file types that will be used are those defined in the desktop files.

### keneric Script:
The keneric script accepts 2 debug mode variables.
```
[global]
LogEnabled=1
LogFile=/tmp/keneric.conf
```
 - LogEnabled at 1 activates debug mode. Be careful not to leave it on by mistake!
 - LogFile is /tmp/keneric.conf by default.
